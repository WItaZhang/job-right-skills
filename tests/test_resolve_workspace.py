"""Workspace resolution and protection rules (plan §2, reviews R09/R14/R19/R20/R23). Synthetic data only."""
from __future__ import annotations

import json
import os
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
    env = {k: v for k, v in os.environ.items() if k not in ("JOB_RIGHT_WORKSPACE", "PYTHONUTF8", "PYTHONIOENCODING")}
    env.update(env_extra or {})
    proc = subprocess.run([sys.executable, str(SCRIPT), "--json", *args], cwd=cwd, env=env,
                          capture_output=True, encoding="utf-8")
    assert proc.stdout, proc.stderr
    return proc.returncode, json.loads(proc.stdout)


def porcelain(repo: Path) -> set[str]:
    out = subprocess.run(["git", "-c", "core.quotepath=off", "status", "--porcelain", "--untracked-files=all"],
                         cwd=repo, capture_output=True, encoding="utf-8").stdout
    return {line[3:] for line in out.splitlines()}


# ----------------------------------------------------------------- resolution

def test_resolves_to_git_root_workspace_from_subdirectory(tmp_path):
    repo = make_repo(tmp_path / "repoB")
    sub = repo / "a" / "b"
    sub.mkdir(parents=True)
    code, out = run(["--init"], cwd=sub)
    assert code == 0, out
    assert Path(out["workspace_root"]) == (repo / "workspace").resolve()
    assert out["resolved_by"] == "git_root"
    assert out["ignore_verified"] is True


def test_r19_non_ascii_repository_path(tmp_path):
    """Chinese path components must survive git subprocess decoding and JSON output on any locale."""
    repo = make_repo(tmp_path / "中文仓库 项目")
    sub = repo / "子目录"
    sub.mkdir()
    code, out = run(["--init"], cwd=sub, env_extra={"LANG": "C", "LC_ALL": "C"})
    assert code == 0, out
    assert Path(out["workspace_root"]) == (repo / "workspace").resolve()
    assert "中文仓库" in out["workspace_root"]
    (repo / "workspace" / "directions" / "dir-001.md").write_text("---\nid: dir-001\n---\n", encoding="utf-8")
    assert "workspace/directions/dir-001.md" not in porcelain(repo)


def test_env_var_directory_is_used_and_verified(tmp_path):
    repo = make_repo(tmp_path / "repoC")
    target = repo / "private" / "jr"
    code, out = run(["--init"], cwd=tmp_path, env_extra={"JOB_RIGHT_WORKSPACE": str(target)})
    assert code == 0, out
    assert Path(out["workspace_root"]) == target.resolve()
    assert out["resolved_by"] == "env"
    (target / "profile" / "x.yaml").write_text("x: 1\n", encoding="utf-8")
    assert "private/jr/profile/x.yaml" not in porcelain(repo)


def test_relative_env_var_is_refused(tmp_path):
    code, out = run([], cwd=tmp_path, env_extra={"JOB_RIGHT_WORKSPACE": "relative/path"})
    assert code == 2 and "must be absolute" in out["error"]


def test_outside_git_without_env_cannot_resolve(tmp_path):
    plain = tmp_path / "plain"
    plain.mkdir()
    code, out = run([], cwd=plain)
    assert code == 2 and "not inside a git repository" in out["error"]


def test_expect_mismatch_exits_3(tmp_path):
    repo = make_repo(tmp_path / "repoD")
    code, out = run(["--expect", str(tmp_path / "somewhere-else")], cwd=repo)
    assert code == 3 and "Resolution changed" in out["error"]


def test_expect_match_exits_0(tmp_path):
    repo = make_repo(tmp_path / "repoE")
    code, out = run(["--expect", str(repo / "workspace")], cwd=repo)
    assert code == 0, out


# ----------------------------------------------------------------- protection (R14, R20)

def test_second_repo_private_files_are_ignored(tmp_path):
    repo = make_repo(tmp_path / "repoB")
    code, out = run(["--init"], cwd=repo)
    assert code == 0, out
    ws = Path(out["workspace_root"])
    for rel in ["profile/background_facts.yaml", "directions/dir-001.md", "candidates/dir-001.md",
                "applications/x.md", "evidence/boards/greenhouse/acme/1/list.json", "evidence/openings/x/jd.html"]:
        p = ws / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("private\n", encoding="utf-8")
    listed = porcelain(repo)
    assert not any(l.startswith("workspace/") and l not in {"workspace/.gitignore", "workspace/README.md"} for l in listed), listed


def test_r20_preexisting_weak_gitignore_is_completed(tmp_path):
    """A workspace/.gitignore that only covers profile/ must not be trusted; init completes it and verifies."""
    repo = make_repo(tmp_path / "repoG")
    ws = repo / "workspace"
    ws.mkdir()
    (ws / ".gitignore").write_text("profile/\n", encoding="utf-8")
    code, out = run(["--init"], cwd=repo)
    assert code == 0, out
    assert any("appended job-right protection block" in n for n in out["init"])
    (ws / "directions" / "dir-001.md").write_text("---\nid: dir-001\n---\n", encoding="utf-8")
    assert "workspace/directions/dir-001.md" not in porcelain(repo)


def test_r20_weak_gitignore_that_cannot_be_completed_fails_verification(tmp_path, monkeypatch):
    """If completion is skipped (simulating an external override), the probe of every private dir must catch it."""
    repo = make_repo(tmp_path / "repoH")
    ws = repo / "workspace"
    ws.mkdir()
    (ws / ".gitignore").write_text(rw.IGNORE_BLOCK_START + "\nprofile/\n", encoding="utf-8")  # marker present, rules weak
    code, out = run(["--init"], cwd=repo)
    assert code == 4, out
    assert any("directions" in n and "NOT ignored" in n for n in out["ignore_notes"])


def test_r20_nested_tracked_readme_is_a_leak(tmp_path):
    repo = make_repo(tmp_path / "repoI")
    nested = repo / "workspace" / "profile" / "README.md"
    nested.parent.mkdir(parents=True)
    nested.write_text("private notes\n", encoding="utf-8")
    git("add", "-f", str(nested), cwd=repo)
    git("-c", "user.name=t", "-c", "user.email=t@example.test", "commit", "-q", "-m", "oops", cwd=repo)
    code, out = run(["--init"], cwd=repo)
    assert code == 4
    assert any("already tracked" in n and "profile/README.md" in n for n in out["ignore_notes"])


def test_already_tracked_private_file_is_reported(tmp_path):
    repo = make_repo(tmp_path / "repoF")
    leaked = repo / "workspace" / "profile" / "background_facts.yaml"
    leaked.parent.mkdir(parents=True)
    leaked.write_text("leak\n", encoding="utf-8")
    git("add", str(leaked), cwd=repo)
    git("-c", "user.name=t", "-c", "user.email=t@example.test", "commit", "-q", "-m", "oops", cwd=repo)
    code, out = run(["--init"], cwd=repo)
    assert code == 4 and out["ignore_verified"] is False
    assert any("already tracked" in n for n in out["ignore_notes"])


# ----------------------------------------------------------------- plugin directory boundary (R09, R23)

def test_plugin_cache_path_is_refused(tmp_path):
    cache = tmp_path / "home" / ".claude" / "plugins" / "cache" / "job-right" / "workspace"
    code, out = run([], cwd=tmp_path, env_extra={"JOB_RIGHT_WORKSPACE": str(cache)})
    assert code == 2 and "installed plugin location" in out["error"]


def test_r23_custom_install_root_is_refused_even_without_dot_claude(tmp_path):
    fake_root = tmp_path / "custom-claude-config" / "plugins" / "cache" / "job-right" / "0.1.0"
    fake_root.mkdir(parents=True)
    with pytest.raises(ValueError, match="installed plugin location"):
        rw.resolve(tmp_path, {"JOB_RIGHT_WORKSPACE": str(fake_root / "workspace")}, plugin_root=fake_root)


def test_r23_non_git_plugin_copy_is_not_a_dev_checkout(tmp_path):
    fake_root = tmp_path / "somewhere" / "job-right"
    (fake_root / "scripts").mkdir(parents=True)
    with pytest.raises(ValueError, match="only a development checkout"):
        rw.resolve(tmp_path, {"JOB_RIGHT_WORKSPACE": str(fake_root / "workspace")}, plugin_root=fake_root)


def test_r23_assets_path_inside_real_plugin_is_refused():
    target = rw.PLUGIN_ROOT / "skills" / "grill-direction" / "assets" / "private-runtime"
    with pytest.raises(ValueError, match="only a development checkout"):
        rw.resolve(rw.PLUGIN_ROOT, {"JOB_RIGHT_WORKSPACE": str(target)})


def test_dev_checkout_workspace_allowed_with_warning():
    """The real repo is a git checkout: exactly PLUGIN_ROOT/workspace is allowed, with a warning."""
    ws, how, warnings = rw.resolve(rw.PLUGIN_ROOT, {})
    assert ws == (rw.PLUGIN_ROOT / "workspace").resolve()
    assert any("development checkout" in w for w in warnings)


def test_looks_like_installed_plugin():
    assert rw.looks_like_installed_plugin(Path("/home/u/.claude/plugins/cache/x/workspace"))
    assert rw.looks_like_installed_plugin(Path("C:/Users/u/.claude/plugins/marketplaces/x"))
    assert rw.looks_like_installed_plugin(Path("/opt/custom/plugins/cache/job-right/0.1.0"))
    assert not rw.looks_like_installed_plugin(Path("/home/u/projects/job-right-skills/workspace"))


# ----------------------------------------------------------------- R28: verification never touches files

def _snapshot(ws: Path) -> dict[str, bytes]:
    return {str(p.relative_to(ws)): p.read_bytes() for p in ws.rglob("*") if p.is_file()}


def _seed_collisions(ws: Path) -> dict[str, bytes]:
    files = {
        "profile/.ignore-probe": b"user file that happens to share the probe name\n",
        "profile/nested/README.md": b"# private notes\nkeep me\n",
        "directions/.ignore-probe": b"another collision\n",
        "directions/dir-001.md": b"---\nid: dir-001\n---\n",
    }
    for rel, content in files.items():
        p = ws / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content)
    return files


def test_r28_success_path_leaves_existing_files_untouched(tmp_path):
    repo = make_repo(tmp_path / "repoJ")
    code, out = run(["--init"], cwd=repo)
    assert code == 0, out
    ws = repo / "workspace"
    seeded = _seed_collisions(ws)
    before = _snapshot(ws)
    ok, notes = rw.verify_ignore(ws)
    assert ok, notes
    after = _snapshot(ws)
    assert after == before
    for rel, content in seeded.items():
        assert (ws / rel).read_bytes() == content


def test_r28_failure_path_leaves_existing_files_untouched(tmp_path):
    repo = make_repo(tmp_path / "repoK")
    ws = repo / "workspace"
    ws.mkdir()
    (ws / ".gitignore").write_text(rw.IGNORE_BLOCK_START + "\nprofile/\n", encoding="utf-8")  # weak, marker present
    seeded = _seed_collisions(ws)
    before = _snapshot(ws)
    ok, notes = rw.verify_ignore(ws)
    assert not ok
    assert any("directions" in n and "NOT ignored" in n for n in notes)
    assert _snapshot(ws) == before
    for rel, content in seeded.items():
        assert (ws / rel).read_bytes() == content


def test_r28_git_error_is_reported_not_passed_and_touches_nothing(tmp_path, monkeypatch):
    repo = make_repo(tmp_path / "repoL")
    code, out = run(["--init"], cwd=repo)
    assert code == 0, out
    ws = repo / "workspace"
    _seed_collisions(ws)
    before = _snapshot(ws)
    real_run = rw._run

    def failing_run(cmd, cwd=None, input_text=None):
        if "check-ignore" in cmd:
            proc = real_run(["git", "--no-such-flag"], cwd=cwd)  # a real failing git call
            return proc
        return real_run(cmd, cwd=cwd, input_text=input_text)

    monkeypatch.setattr(rw, "_run", failing_run)
    ok, notes = rw.verify_ignore(ws)
    assert not ok
    assert any("could not verify ignore rules" in n for n in notes)
    assert _snapshot(ws) == before


def test_r28_verify_creates_no_directories(tmp_path):
    repo = make_repo(tmp_path / "repoM")
    ws = repo / "workspace"
    ws.mkdir()
    (ws / ".gitignore").write_text(rw.IGNORE_BLOCK, encoding="utf-8")
    listing_before = sorted(p.relative_to(ws) for p in ws.rglob("*"))
    ok, notes = rw.verify_ignore(ws)
    assert ok, notes
    assert sorted(p.relative_to(ws) for p in ws.rglob("*")) == listing_before
