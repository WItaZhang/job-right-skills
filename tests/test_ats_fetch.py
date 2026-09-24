"""Offline tests for skills/find-openings/scripts/ats_fetch.py using the bundled fixtures (synthetic company)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "find-openings" / "scripts"
FIX = ROOT / "skills" / "find-openings" / "fixtures"
sys.path.insert(0, str(SCRIPTS))
import ats_fetch  # noqa: E402


def run(provider: str, board: str, ws: Path, *fixtures: str) -> dict:
    return ats_fetch.fetch_board(provider, board, ws, "synthco", [FIX / f for f in fixtures])


def openings(ws: Path) -> dict[str, dict]:
    out = {}
    for p in (ws / "evidence" / "openings").glob("*/posting.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        out[d["normalized"]["opening_id"]] = d
    return out


# ------------------------------------------------------------------ greenhouse

def test_greenhouse_normalization(tmp_path):
    r = run("greenhouse", "synthco", tmp_path, "greenhouse-sample.json")
    assert r["observation"]["retrieval_status"] == "success"
    ops = openings(tmp_path)
    a = ops["greenhouse:synthco:4001"]["normalized"]
    assert a["id_source"] == "provider_native"
    assert a["title"].startswith("Senior Infrastructure Engineer")
    assert a["department"] == "Engineering"
    assert a["team"] is None, "Greenhouse department must not be promoted to team"
    assert a["locations"] == ["Singapore", "Shenzhen"]
    assert a["source_updated_at"] == "2026-09-20T08:15:00-04:00"
    assert a["source_published_at"] is None
    assert "distributed training" in a["jd_text"] and "<" not in a["jd_text"]
    assert a["posting_kind"] == "job"
    b = ops["greenhouse:synthco:4002"]["normalized"]
    assert b["locations"] == [] and b["department"] is None
    assert b["posting_kind"] == "prospect"
    # raw kept beside normalized
    assert ops["greenhouse:synthco:4001"]["raw"]["internal_job_id"] == 9001


def test_greenhouse_zero_result_is_a_successful_read_with_board_evidence(tmp_path):
    r = run("greenhouse", "synthco", tmp_path, "greenhouse-empty.json")
    obs = r["observation"]
    assert obs["retrieval_status"] == "success" and obs["postings_seen"] == 0
    assert "not evidence the company never hires" in obs["note"]
    board_dir = Path(r["board_dir"])
    assert (board_dir / "observation.json").exists() and (board_dir / "page-0.raw").exists()
    assert not (tmp_path / "evidence" / "openings").exists() or not any((tmp_path / "evidence" / "openings").iterdir())


# ------------------------------------------------------------------ ashby

def test_ashby_normalization(tmp_path):
    r = run("ashby", "synthco", tmp_path, "ashby-sample.json")
    assert r["observation"]["retrieval_status"] == "success"
    ops = openings(tmp_path)
    a = ops["ashby:synthco:a1b2c3d4-0000-4000-8000-000000000001"]["normalized"]
    assert a["team"] == "Inference Platform" and a["department"] == "Engineering"
    assert a["locations"] == ["Shenzhen", "Singapore"]
    assert a["workplace_type"] == "Hybrid"
    assert a["source_published_at"] == "2026-09-18T02:00:00.000Z" and a["source_updated_at"] is None
    assert a["apply_url"].endswith("/application") and a["job_url"] != a["apply_url"]
    assert a["salary"]["summaryComponents"][0]["currencyCode"] == "SGD"
    b = ops["ashby:synthco:a1b2c3d4-0000-4000-8000-000000000002"]["normalized"]
    assert b["team"] is None, "null team stays null even though department is set"
    assert b["is_listed"] is False, "isListed=false is visibility, not closure; kept as-is"


# ------------------------------------------------------------------ lever

def test_lever_normalization_has_no_time_fields(tmp_path):
    r = run("lever", "synthco", tmp_path, "lever-sample.json")
    assert r["observation"]["retrieval_status"] == "success"
    ops = openings(tmp_path)
    a = ops["lever:synthco:0f1e2d3c-0000-4000-8000-000000000001"]["normalized"]
    assert a["source_published_at"] is None and a["source_updated_at"] is None, "R17: Lever documents no time fields"
    assert ops["lever:synthco:0f1e2d3c-0000-4000-8000-000000000001"]["raw"]["createdAt"] == 1758500000000, "undocumented field stays raw only"
    assert a["team"] == "Storage" and a["department"] == "Engineering"
    assert a["locations"] == ["Singapore", "Shenzhen"]
    assert a["salary"] == {"currency": "SGD", "interval": "per-year-salary", "min": 180000, "max": 240000}
    assert a["country"] == "SG"
    b = ops["lever:synthco:0f1e2d3c-0000-4000-8000-000000000002"]["normalized"]
    assert b["country"] is None and b["team"] is None


def test_lever_pagination_full_page_then_failure_is_partial(tmp_path):
    full = [{"id": f"p{i:03d}", "text": f"Role {i}", "categories": {}, "hostedUrl": f"https://jobs.lever.co/synthco/p{i:03d}"}
            for i in range(ats_fetch.LEVER_LIMIT)]
    (tmp_path / "page1.json").write_text(json.dumps(full), encoding="utf-8")
    r = ats_fetch.fetch_board("lever", "synthco", tmp_path, "synthco", [tmp_path / "page1.json", FIX / "error-timeout.error.json"])
    obs = r["observation"]
    assert obs["retrieval_status"] == "partial"
    assert obs["coverage"]["pages_ok"] == 1 and obs["coverage"]["pages_requested"] == 2
    assert obs["postings_seen"] == ats_fetch.LEVER_LIMIT
    assert obs["pages"][1]["error"].startswith("TimeoutError")


def test_lever_pagination_stops_on_underfull_page(tmp_path):
    full = [{"id": f"p{i:03d}", "text": f"Role {i}", "categories": {}} for i in range(ats_fetch.LEVER_LIMIT)]
    (tmp_path / "page1.json").write_text(json.dumps(full), encoding="utf-8")
    r = ats_fetch.fetch_board("lever", "synthco", tmp_path, "synthco", [tmp_path / "page1.json", FIX / "lever-sample.json", FIX / "error-404.error.json"])
    obs = r["observation"]
    assert obs["retrieval_status"] == "success"
    assert obs["coverage"]["pages_requested"] == 2, "third fixture never requested"
    assert obs["postings_seen"] == ats_fetch.LEVER_LIMIT + 2


# ------------------------------------------------------------------ failures

def test_404_is_failed_read_not_closed(tmp_path):
    r = run("greenhouse", "synthco", tmp_path, "error-404.error.json")
    obs = r["observation"]
    assert obs["retrieval_status"] == "failed" and obs["postings_seen"] == 0
    assert obs["pages"][0]["http_status"] == 404
    assert (Path(r["board_dir"]) / "observation.json").exists(), "board-level failure lands without any opening id"
    assert "closed" not in json.dumps(obs).lower()


def test_timeout_is_failed(tmp_path):
    r = run("ashby", "synthco", tmp_path, "error-timeout.error.json")
    assert r["observation"]["retrieval_status"] == "failed"


def test_unparseable_body_is_failed(tmp_path):
    (tmp_path / "bad.json").write_text("<html>maintenance</html>", encoding="utf-8")
    r = ats_fetch.fetch_board("lever", "synthco", tmp_path, None, [tmp_path / "bad.json"])
    assert r["observation"]["retrieval_status"] == "failed"
    assert "unparseable" in r["observation"]["pages"][0]["error"]


def test_repeat_checks_keep_history(tmp_path):
    r1 = run("greenhouse", "synthco", tmp_path, "greenhouse-sample.json")
    r2 = run("greenhouse", "synthco", tmp_path, "error-404.error.json")
    assert Path(r1["board_dir"]).exists() and Path(r2["board_dir"]).exists()
    assert r1["board_dir"] != r2["board_dir"]
    # openings from the successful check are still there after the failed one
    assert "greenhouse:synthco:4001" in openings(tmp_path)


def test_cli(tmp_path, capsys):
    code = ats_fetch.main(["--provider", "lever", "--board", "synthco", "--workspace", str(tmp_path), "--fixture", str(FIX / "lever-sample.json")])
    assert code == 0
    out = capsys.readouterr().out
    assert "retrieval_status=success postings=2" in out
    assert "lever:synthco:0f1e2d3c-0000-4000-8000-000000000001" in out
    code = ats_fetch.main(["--provider", "lever", "--board", "synthco", "--workspace", str(tmp_path), "--fixture", str(FIX / "error-404.error.json")])
    assert code == 1


# ------------------------------------------------------------------ shortlist

import shortlist  # noqa: E402

DIRECTION = ROOT / "skills" / "grill-direction" / "assets" / "example-synthetic-city-profile.md"
RUN1_DIRECTION = ROOT / "docs" / "live-runs" / "run-1" / "dir-001.final.md"


def test_shortlist_ranks_and_pushes_down(tmp_path):
    for f in ["greenhouse-sample.json", "ashby-sample.json", "lever-sample.json"]:
        prov = f.split("-")[0]
        ats_fetch.fetch_board(prov, "synthco", tmp_path, "synthco", [FIX / f])
    direction = shortlist.load_direction(tmp_path, str(DIRECTION))
    res = shortlist.shortlist(tmp_path, direction, None, None, 10, 1, extra_keywords=["storage"])
    assert res["scanned"] == 6
    ids = [r["opening_id"] for r in res["shortlist"]]
    # infra / storage / inference roles score; the manager role is pushed down, not dropped
    assert "lever:synthco:0f1e2d3c-0000-4000-8000-000000000001" in ids
    assert "ashby:synthco:a1b2c3d4-0000-4000-8000-000000000001" in ids
    # JD body mentioning "Head of Infra" must not push an IC role down
    assert "greenhouse:synthco:4001" in ids
    pushed = {r["opening_id"]: r for r in res["pushed_down"]}
    assert "ashby:synthco:a1b2c3d4-0000-4000-8000-000000000002" in pushed
    assert any("manager" in t.lower() or "管理" in t for t in pushed["ashby:synthco:a1b2c3d4-0000-4000-8000-000000000002"]["deprioritized_by"])
    assert res["search_bias"] == direction["search_hints"]["deprioritize"]
    for r in res["shortlist"]:
        assert r["snapshot"].startswith("evidence/openings/")


def test_shortlist_cli_filters_by_provider(tmp_path, capsys):
    ats_fetch.fetch_board("lever", "synthco", tmp_path, "synthco", [FIX / "lever-sample.json"])
    ats_fetch.fetch_board("ashby", "synthco", tmp_path, "synthco", [FIX / "ashby-sample.json"])
    code = shortlist.main(["--workspace", str(tmp_path), "--direction", str(DIRECTION), "--provider", "lever", "--json"])
    assert code == 0
    out = json.loads(capsys.readouterr().out)
    assert out["scanned"] == 2 and all(r["opening_id"].startswith("lever:") for r in out["shortlist"])


def test_shortlist_chinese_only_hints_need_extra_keywords(tmp_path):
    """Live run 1 wrote Chinese-only keywords; against English boards nothing matches until the agent adds
    board-language terms, and those terms are recorded."""
    ats_fetch.fetch_board("lever", "synthco", tmp_path, "synthco", [FIX / "lever-sample.json"])
    direction = shortlist.load_direction(tmp_path, str(RUN1_DIRECTION))
    bare = shortlist.shortlist(tmp_path, direction, None, None, 10, 1)
    assert bare["shortlist"] == []
    res = shortlist.shortlist(tmp_path, direction, None, None, 10, 1, extra_keywords=["storage", "distributed"])
    assert [r["opening_id"] for r in res["shortlist"]] == ["lever:synthco:0f1e2d3c-0000-4000-8000-000000000001"]
    assert res["terms"]["extra_keywords"] == ["storage", "distributed"]
