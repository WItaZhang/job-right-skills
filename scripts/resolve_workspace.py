#!/usr/bin/env python3
"""Resolve, create and verify the private workspace used by the job-right skills.

Resolution order:
  1. JOB_RIGHT_WORKSPACE environment variable (absolute path).
  2. <git repository root of the current directory>/workspace
  3. Error: ask the user to choose.

Rules (implementation-plan.md §2, reviews R09/R14/R19/R20/R23):
  * plugin_root (the directory containing this scripts/ folder) is for code and assets only. Private
    data may never live inside it, with one exception: a *development checkout* (plugin_root is itself
    a git working tree and not an installed copy) may use exactly plugin_root/workspace, with a warning.
    Any other path inside plugin_root, and anything inside an installed plugin location, is refused.
  * The workspace protects itself with its own .gitignore. --init writes or completes it and then
    verifies, in the repository that really contains the workspace, that every private subdirectory
    and every existing private file is ignored and that nothing private is tracked.
  * All subprocess and stdout text is UTF-8 regardless of the system locale, so non-ASCII repository
    paths work on Windows without the user changing global settings.
  * --expect <path> lets a skill detect that the resolution changed since the session started (for
    example after a cd). Exit code 3 in that case: the skill must tell the user rather than silently
    create a second profile.

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
PRIVATE_SUBDIRS = ["profile", "directions", "candidates", "applications", "evidence/boards", "evidence/openings"]
PUBLIC_FILES = {"README.md", ".gitignore"}  # only these, and only directly under the workspace root
IGNORE_BLOCK_START = "# >>> job-right workspace protection >>>"
IGNORE_BLOCK = (
    f"{IGNORE_BLOCK_START}\n"
    "# Written by job-right resolve_workspace.py. Everything here is private.\n"
    "*\n"
    "!.gitignore\n"
    "!README.md\n"
    "# <<< job-right workspace protection <<<\n"
)
WORKSPACE_README = (
    "# job-right workspace\n\n"
    "Private runtime data for the job-right skills: background facts, direction templates, candidates,\n"
    "application records and evidence snapshots. The .gitignore next to this file ignores everything\n"
    "except itself and this README. Do not commit the contents.\n"
)
INSTALLED_MARKERS = (("plugins", "cache"), ("plugins", "marketplaces"), (".claude", "plugins"))


def _run(cmd: list[str], cwd: Path | None = None, input_text: str | None = None) -> subprocess.CompletedProcess:
    # Git prints paths in UTF-8 (core.quotepath aside); decode explicitly so a Chinese repository path
    # does not blow up under a GBK console (review R19).
    return subprocess.run(
        cmd, cwd=cwd, capture_output=True, encoding="utf-8", errors="replace", input=input_text,
        env={**os.environ, "LC_ALL": os.environ.get("LC_ALL", "C.UTF-8")},
    )


def git_root(start: Path) -> Path | None:
    try:
        proc = _run(["git", "-c", "core.quotepath=off", "rev-parse", "--show-toplevel"], cwd=start)
    except (OSError, ValueError):
        return None
    if proc.returncode != 0 or not proc.stdout:
        return None
    return Path(proc.stdout.strip()).resolve()


def looks_like_installed_plugin(path: Path) -> bool:
    """True for paths that look like an installed or cached plugin location rather than a dev checkout."""
    parts = [p.lower() for p in path.parts]
    for i in range(len(parts) - 1):
        if (parts[i], parts[i + 1]) in INSTALLED_MARKERS:
            return True
    return False


def plugin_root_is_dev_checkout(plugin_root: Path = PLUGIN_ROOT) -> bool:
    """A dev checkout is a git working tree whose top level is the plugin root itself."""
    if looks_like_installed_plugin(plugin_root):
        return False
    return git_root(plugin_root) == plugin_root.resolve()


def resolve(cwd: Path, env: dict[str, str], plugin_root: Path = PLUGIN_ROOT) -> tuple[Path, str, list[str]]:
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

    if looks_like_installed_plugin(candidate):
        raise ValueError(f"Refusing workspace inside an installed plugin location: {candidate}")
    plugin_root = plugin_root.resolve()
    if _is_relative_to(candidate, plugin_root):
        dev_ws = (plugin_root / "workspace").resolve()
        if candidate == dev_ws and plugin_root_is_dev_checkout(plugin_root):
            warnings.append(
                f"Workspace {candidate} is the conventional workspace/ of the plugin's own development checkout "
                f"{plugin_root}. Allowed because the checkout is a git working tree the user chose as working "
                "repository; its own .gitignore protects the contents."
            )
        else:
            raise ValueError(
                f"Refusing workspace {candidate}: private data may not live inside the plugin directory "
                f"{plugin_root} (only a development checkout's own workspace/ is allowed)."
            )
    return candidate, how, warnings


def _is_relative_to(path: Path, other: Path) -> bool:
    try:
        path.relative_to(other)
        return True
    except ValueError:
        return False


def ensure_gitignore(ws: Path) -> str | None:
    gi = ws / ".gitignore"
    if not gi.exists():
        gi.write_text(IGNORE_BLOCK, encoding="utf-8")
        return "wrote workspace .gitignore"
    existing = gi.read_text(encoding="utf-8")
    if IGNORE_BLOCK_START in existing:
        return None
    # A pre-existing, weaker .gitignore (review R20): complete it instead of trusting it.
    gi.write_text(existing.rstrip("\n") + "\n\n" + IGNORE_BLOCK, encoding="utf-8")
    return "appended job-right protection block to a pre-existing workspace .gitignore"


def init_workspace(ws: Path) -> list[str]:
    notes: list[str] = []
    ws.mkdir(parents=True, exist_ok=True)
    for sub in PRIVATE_SUBDIRS:
        (ws / sub).mkdir(parents=True, exist_ok=True)
    note = ensure_gitignore(ws)
    if note:
        notes.append(note)
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


def _private_paths(ws: Path) -> list[Path]:
    """Every existing file under the workspace except the two public files at its root."""
    out: list[Path] = []
    for p in ws.rglob("*"):
        if p.is_file() and not (p.parent == ws and p.name in PUBLIC_FILES):
            out.append(p)
    return out


def verify_ignore(ws: Path) -> tuple[bool, list[str]]:
    """Check, in the repository that actually contains ws, that private files are ignored and none are tracked.

    Probes every private subdirectory (not just profile/) and every existing private file, and treats
    any tracked file other than the two root public files as a leak (review R20).
    """
    problems: list[str] = []
    root = git_root(ws)
    if root is None:
        return True, ["workspace is not inside a git repository; ignore rules not applicable"]

    probes: list[Path] = []
    for sub in PRIVATE_SUBDIRS:
        d = ws / sub
        d.mkdir(parents=True, exist_ok=True)
        probes.append(d / ".ignore-probe")
    nested_probe = ws / "profile" / "nested" / "README.md"
    nested_probe.parent.mkdir(parents=True, exist_ok=True)
    probes.append(nested_probe)
    for p in probes:
        p.write_text("probe\n", encoding="utf-8")
    try:
        to_check = probes + _private_paths(ws)
        to_check = [p for p in to_check if p not in probes] + probes  # existing files first, probes last
        not_ignored = _not_ignored(root, to_check)
        for p in not_ignored:
            problems.append(f"{p} is NOT ignored by git in {root}")
    finally:
        for p in probes:
            p.unlink(missing_ok=True)
        try:
            nested_probe.parent.rmdir()
        except OSError:
            pass

    tracked = _run(["git", "-c", "core.quotepath=off", "ls-files", "-z", "--", str(ws)], cwd=root)
    tracked_files = [t for t in tracked.stdout.split("\0") if t]
    offenders = []
    for t in tracked_files:
        full = (root / t).resolve()
        if not (full.parent == ws and full.name in PUBLIC_FILES):
            offenders.append(t)
    if offenders:
        problems.append(
            "files under the workspace are already tracked by git and are NOT protected by ignore rules: "
            + ", ".join(offenders)
        )
    return (not problems), problems


def _not_ignored(root: Path, paths: list[Path]) -> list[Path]:
    if not paths:
        return []
    # -z is only accepted together with --stdin; NUL separation keeps non-ASCII and odd paths intact.
    proc = _run(
        ["git", "-c", "core.quotepath=off", "check-ignore", "--stdin", "-z", "--no-index"],
        cwd=root,
        input_text="\0".join(str(p) for p in paths) + "\0",
    )
    # exit 0: some ignored, 1: none ignored, 128: error
    if proc.returncode == 128:
        return list(paths)
    ignored = {Path(x).resolve() for x in proc.stdout.split("\0") if x}
    return [p for p in paths if p.resolve() not in ignored]


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--init", action="store_true", help="create the directory layout, .gitignore, README and marker")
    parser.add_argument("--verify-ignore", action="store_true", help="verify git ignores private files in the real target repo")
    parser.add_argument("--expect", metavar="PATH", help="previously resolved workspace_root; exit 3 if it differs")
    parser.add_argument("--json", action="store_true", help="machine-readable output (UTF-8)")
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
