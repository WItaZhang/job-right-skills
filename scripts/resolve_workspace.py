#!/usr/bin/env python3
"""Resolve, create and verify the private workspace used by the job-right skills.

Resolution order:
  1. JOB_RIGHT_WORKSPACE environment variable (absolute path).
  2. <git repository root of the current directory>/workspace
  3. Error: ask the user to choose.

Rules (implementation-plan.md §2, review R09/R14):
  * plugin_root (the directory containing this scripts/ folder) is for code and assets only.
    Writing into an installed plugin cache is refused. A dev checkout that the user explicitly
    uses as their working repository is allowed, with a warning.
  * The workspace protects itself with its own .gitignore ("*" plus exceptions), so it is safe
    in whichever repository it lands. --init writes it and verifies with `git check-ignore`.
  * --expect <path> lets a skill detect that the resolution changed since the session started
    (for example after a cd). Exit code 3 in that case: the skill must tell the user rather
    than silently create a second profile.

Exit codes: 0 ok, 2 cannot resolve or refused, 3 resolution differs from --expect, 4 ignore
verification failed.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
MARKER = ".job-right.json"
SUBDIRS = ["profile", "directions", "candidates", "applications", "evidence/boards", "evidence/openings"]
WORKSPACE_GITIGNORE = "# Written by job-right resolve_workspace.py. Everything here is private.\n*\n!.gitignore\n!README.md\n"
WORKSPACE_README = (
    "# job-right workspace\n\n"
    "Private runtime data for the job-right skills: background facts, direction templates, candidates,\n"
    "application records and evidence snapshots. The .gitignore next to this file ignores everything\n"
    "except itself and this README. Do not commit the contents.\n"
)


def _run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def git_root(start: Path) -> Path | None:
    proc = _run(["git", "rev-parse", "--show-toplevel"], cwd=start)
    if proc.returncode != 0:
        return None
    return Path(proc.stdout.strip()).resolve()


def looks_like_plugin_cache(path: Path) -> bool:
    parts = [p.lower() for p in path.parts]
    for i, part in enumerate(parts):
        if part == ".claude" and i + 1 < len(parts) and parts[i + 1] == "plugins":
            return True
    return False


def resolve(cwd: Path, env: dict[str, str]) -> tuple[Path, str, list[str]]:
    """Return (workspace_root, how, warnings). Raise ValueError when refused or unresolvable."""
    warnings: list[str] = []
    raw = env.get("JOB_RIGHT_WORKSPACE")
    if raw:
        candidate = Path(raw).expanduser()
        if not candidate.is_absolute():
            raise ValueError(f"JOB_RIGHT_WORKSPACE must be absolute, got {raw!r}")
        candidate = candidate.resolve()
        how = "env"
    else:
        root = git_root(cwd)
        if root is None:
            raise ValueError(
                "Cannot resolve workspace: JOB_RIGHT_WORKSPACE is not set and the current directory is not "
                "inside a git repository. Ask the user where their working repository is."
            )
        candidate = (root / "workspace").resolve()
        how = "git_root"

    if looks_like_plugin_cache(candidate):
        raise ValueError(f"Refusing workspace inside an installed plugin cache: {candidate}")
    if looks_like_plugin_cache(PLUGIN_ROOT) and _is_relative_to(candidate, PLUGIN_ROOT):
        raise ValueError(f"Refusing workspace inside the installed plugin directory: {candidate}")
    if _is_relative_to(candidate, PLUGIN_ROOT):
        warnings.append(
            f"Workspace {candidate} lies inside the plugin dev checkout {PLUGIN_ROOT}. Allowed because this is a "
            "development checkout the user chose as working repository; its own .gitignore protects the contents."
        )
    return candidate, how, warnings


def _is_relative_to(path: Path, other: Path) -> bool:
    try:
        path.relative_to(other)
        return True
    except ValueError:
        return False


def init_workspace(ws: Path) -> list[str]:
    notes: list[str] = []
    ws.mkdir(parents=True, exist_ok=True)
    for sub in SUBDIRS:
        (ws / sub).mkdir(parents=True, exist_ok=True)
    gi = ws / ".gitignore"
    if not gi.exists():
        gi.write_text(WORKSPACE_GITIGNORE, encoding="utf-8")
        notes.append("wrote workspace .gitignore")
    readme = ws / "README.md"
    if not readme.exists():
        readme.write_text(WORKSPACE_README, encoding="utf-8")
    marker = ws / MARKER
    if marker.exists():
        try:
            recorded = json.loads(marker.read_text(encoding="utf-8"))
            if Path(recorded.get("workspace_root", "")).resolve() != ws:
                notes.append(
                    f"marker recorded workspace_root={recorded.get('workspace_root')!r} but the directory now lives at "
                    f"{ws}; it may have been moved. Keeping the old marker content for the user to inspect."
                )
        except (json.JSONDecodeError, OSError):
            notes.append("existing marker unreadable; leaving it in place")
    else:
        marker.write_text(
            json.dumps(
                {
                    "workspace_root": str(ws),
                    "plugin_version": _plugin_version(),
                    "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        notes.append("wrote marker")
    return notes


def _plugin_version() -> str | None:
    manifest = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
    try:
        return json.loads(manifest.read_text(encoding="utf-8")).get("version")
    except (OSError, json.JSONDecodeError):
        return None


def verify_ignore(ws: Path) -> tuple[bool, list[str]]:
    """Check, in the repository that actually contains ws, that private files are ignored and none are tracked."""
    problems: list[str] = []
    root = git_root(ws)
    if root is None:
        return True, ["workspace is not inside a git repository; ignore rules not applicable"]
    probe = ws / "profile" / ".ignore-probe"
    probe.write_text("probe\n", encoding="utf-8")
    try:
        proc = _run(["git", "check-ignore", "-q", str(probe)], cwd=root)
        if proc.returncode != 0:
            problems.append(f"{probe} is NOT ignored by git in {root}")
    finally:
        probe.unlink(missing_ok=True)
    tracked = _run(["git", "ls-files", "--", str(ws)], cwd=root)
    tracked_files = [ln for ln in tracked.stdout.splitlines() if ln.strip()]
    allowed = {"README.md", ".gitignore"}
    offenders = [t for t in tracked_files if Path(t).name not in allowed]
    if offenders:
        problems.append(
            "files under the workspace are already tracked by git and are NOT protected by ignore rules: "
            + ", ".join(offenders)
        )
    return (not problems), problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--init", action="store_true", help="create the directory layout, .gitignore, README and marker")
    parser.add_argument("--verify-ignore", action="store_true", help="verify git ignores private files in the real target repo")
    parser.add_argument("--expect", metavar="PATH", help="previously resolved workspace_root; exit 3 if it differs")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--cwd", metavar="DIR", help="resolve as if run from DIR (tests)")
    args = parser.parse_args(argv)

    cwd = Path(args.cwd).resolve() if args.cwd else Path.cwd()
    out: dict = {"plugin_root": str(PLUGIN_ROOT)}
    try:
        ws, how, warnings = resolve(cwd, dict(os.environ))
    except ValueError as exc:
        out.update({"ok": False, "error": str(exc)})
        _emit(out, args.json)
        return 2

    out.update({"workspace_root": str(ws), "resolved_by": how, "warnings": warnings})

    if args.expect and Path(args.expect).expanduser().resolve() != ws:
        out.update(
            {
                "ok": False,
                "error": (
                    f"Resolution changed: session started with {args.expect} but the current directory now resolves to "
                    f"{ws}. Tell the user and let them choose; do not create a second profile silently."
                ),
            }
        )
        _emit(out, args.json)
        return 3

    if args.init:
        out["init"] = init_workspace(ws)
    if args.init or args.verify_ignore:
        ok, problems = verify_ignore(ws)
        out["ignore_verified"] = ok
        out["ignore_notes"] = problems
        if not ok:
            out["ok"] = False
            _emit(out, args.json)
            return 4
    out["ok"] = True
    out["exists"] = ws.exists()
    _emit(out, args.json)
    return 0


def _emit(out: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    for k, v in out.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    sys.exit(main())
