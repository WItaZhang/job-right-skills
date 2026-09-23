"""Workspace resolution and protection rules (plan §2, review R09/R14). Synthetic data only."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "resolve_workspace.py"
sys.path.insert(0, str(ROOT / "scripts"))
import resolve_workspace as rw  # noqa: E402


def git(*args: str, cwd: Path) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def make_repo(path: Path) -> Path:
    path.mkdir(parents=True)
    git("init", "-q", cwd=path)
    git("-c", "user.name=t", "-c", "user.email=t@example.test", "commit", "-q", "--allow-empty", "-m", "init", cwd=path)
    return path


def run(args: list[str], cwd: Path, env_extra: dict | None = None) -> tuple[int, dict]:
    import os
    env = {k: v for k, v in os.environ.items() if k != "JOB_RIGHT_WORKSPACE"}
    env.update(env_extra or {})
    proc = subprocess.run([sys.executable, str(SCRIPT), "--json", *args], cwd=cwd, env=env, capture_output=True, text=True)
    return proc.returncode, json.loads(proc.stdout)


def test_resolves_to_git_root_workspace_from_subdirectory(tmp_path):
    repo = make_repo(tmp_path / "repoB")
    sub = repo / "a" / "b"
    sub.mkdir(parents=True)
    code, out = run(["--init"], cwd=sub)
    assert code == 0, out
    assert Path(out["workspace_root"]) == (repo / "workspace").resolve()
    assert out["resolved_by"] == "git_root"
    assert out["ignore_verified"] is True


def test_second_repo_private_files_are_ignored(tmp_path):
    """The user's working repository has no job-right rules of its own; the workspace must protect itself."""
    repo = make_repo(tmp_path / "repoB")
    code, out = run(["--init"], cwd=repo)
    assert code == 0, out
    ws = Path(out["workspace_root"])
    (ws / "profile" / "background_facts.yaml").write_text("facts_revision: 1\n", encoding="utf-8")
    (ws / "directions" / "dir-001.md").write_text("---\nid: dir-001\n---\n", encoding="utf-8")
    status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=repo, capture_output=True, text=True).stdout
    listed = {line[3:] for line in status.splitlines()}
    assert "workspace/profile/background_facts.yaml" not in listed
    assert "workspace/directions/dir-001.md" not in listed
    # Only the self-protection files are visible to git
    assert listed <= {"workspace/.gitignore", "workspace/README.md"}


def test_env_var_directory_is_used_and_verified(tmp_path):
    repo = make_repo(tmp_path / "repoC")
    target = repo / "private" / "jr"
    code, out = run(["--init"], cwd=tmp_path, env_extra={"JOB_RIGHT_WORKSPACE": str(target)})
    assert code == 0, out
    assert Path(out["workspace_root"]) == target.resolve()
    assert out["resolved_by"] == "env"
    assert out["ignore_verified"] is True
    (target / "profile" / "x.yaml").write_text("x: 1\n", encoding="utf-8")
    status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=repo, capture_output=True, text=True).stdout
    assert "private/jr/profile/x.yaml" not in status


def test_relative_env_var_is_refused(tmp_path):
    code, out = run([], cwd=tmp_path, env_extra={"JOB_RIGHT_WORKSPACE": "relative/path"})
    assert code == 2
    assert "must be absolute" in out["error"]


def test_outside_git_without_env_cannot_resolve(tmp_path):
    plain = tmp_path / "plain"
    plain.mkdir()
    code, out = run([], cwd=plain)
    assert code == 2
    assert "not inside a git repository" in out["error"]


def test_plugin_cache_path_is_refused(tmp_path):
    cache = tmp_path / "home" / ".claude" / "plugins" / "cache" / "job-right" / "workspace"
    code, out = run([], cwd=tmp_path, env_extra={"JOB_RIGHT_WORKSPACE": str(cache)})
    assert code == 2
    assert "plugin cache" in out["error"]


def test_expect_mismatch_exits_3(tmp_path):
    repo = make_repo(tmp_path / "repoD")
    other = tmp_path / "somewhere-else"
    code, out = run(["--expect", str(other)], cwd=repo)
    assert code == 3
    assert "Resolution changed" in out["error"]


def test_expect_match_exits_0(tmp_path):
    repo = make_repo(tmp_path / "repoE")
    code, out = run(["--expect", str(repo / "workspace")], cwd=repo)
    assert code == 0, out


def test_already_tracked_private_file_is_reported(tmp_path):
    repo = make_repo(tmp_path / "repoF")
    ws = repo / "workspace" / "profile"
    ws.mkdir(parents=True)
    leaked = ws / "background_facts.yaml"
    leaked.write_text("leak\n", encoding="utf-8")
    git("add", str(leaked), cwd=repo)
    git("-c", "user.name=t", "-c", "user.email=t@example.test", "commit", "-q", "-m", "oops", cwd=repo)
    code, out = run(["--init"], cwd=repo)
    assert code == 4
    assert out["ignore_verified"] is False
    assert any("already tracked" in n for n in out["ignore_notes"])


def test_dev_checkout_workspace_allowed_with_warning(tmp_path):
    """Resolving inside the plugin's own dev checkout is allowed, with a warning, when it is not an installed cache."""
    ws, how, warnings = rw.resolve(rw.PLUGIN_ROOT, {})
    assert ws == (rw.PLUGIN_ROOT / "workspace").resolve()
    assert any("dev checkout" in w for w in warnings)


def test_looks_like_plugin_cache():
    assert rw.looks_like_plugin_cache(Path("/home/u/.claude/plugins/cache/x/workspace"))
    assert rw.looks_like_plugin_cache(Path("C:/Users/u/.claude/plugins/marketplaces/x"))
    assert not rw.looks_like_plugin_cache(Path("/home/u/projects/job-right-skills/workspace"))
