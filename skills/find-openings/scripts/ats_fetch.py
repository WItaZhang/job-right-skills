#!/usr/bin/env python3
"""Fetch published job postings from a company's official ATS board and record them as evidence.

Providers: greenhouse, ashby, lever. Standard library only.

Usage:
  ats_fetch.py --provider greenhouse --board <board-token> --workspace <workspace_root> [--company <id>]
  ats_fetch.py --provider lever --board <site> --workspace <ws> --fixture <file.json> [--fixture <page2.json> ...]
  ats_fetch.py ... --json

What it writes (plan §4.1 step 3, reviews R06/R13/R17):
  <ws>/evidence/boards/<provider>/<board>/<check-id>/request.json     what was asked, when, with which pages
  <ws>/evidence/boards/<provider>/<board>/<check-id>/page-N.raw       raw response bodies (one per page)
  <ws>/evidence/boards/<provider>/<board>/<check-id>/observation.json retrieval_status, coverage, counts, errors
  <ws>/evidence/openings/<opening-id>/posting.json                    raw + normalized record for one posting

A zero-result complete read and a failed board request both land in the boards/ directory; they need no
opening id. retrieval_status: success (all pages read), partial (some pages failed or pagination unfinished),
failed (nothing usable). Openings are only written for pages that were read successfully.

Normalized fields: opening_id, id_source, provider, board, title, department, team, locations[],
workplace_type, job_url, apply_url, jd_text, salary, source_published_at, source_updated_at, checked_at.
Time semantics differ per provider and are mapped explicitly; anything the provider does not document
stays null. team is never derived from department. Raw fields are kept beside the normalized ones.

--fixture replaces the network call with the given file(s); a fixture named *.error.json with
{"http_status": N} or {"timeout": true} simulates a failed page. This is how the tests run offline.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

USER_AGENT = "job-right-skills/0.1 (+https://github.com/WItaZhang/job-right-skills)"
TIMEOUT_S = 30
LEVER_LIMIT = 100
TAG_RE = re.compile(r"<[^>]+>")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def strip_html(markup: str | None) -> str | None:
    """Greenhouse returns entity-escaped HTML (&lt;p&gt;...), Ashby and Lever return real HTML. Unescape
    first, then drop tags, then collapse whitespace. Block-level closes become newlines so list items and
    paragraphs stay separable in the plain text."""
    if not markup:
        return None
    text = html.unescape(markup)
    if "&lt;" in text or "&gt;" in text:  # double-escaped content seen on some boards
        text = html.unescape(text)
    text = re.sub(r"</(p|li|ul|ol|div|h[1-6]|br|tr)\s*>|<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = TAG_RE.sub(" ", text)
    text = re.sub(r"[ \t\xa0]+", " ", text)
    return re.sub(r"\s*\n\s*", "\n", text).strip()


# ---------------------------------------------------------------------------
# Transport
# ---------------------------------------------------------------------------

class PageResult:
    def __init__(self, url: str, status: str, body: str | None, http_status: int | None, error: str | None):
        self.url, self.status, self.body, self.http_status, self.error = url, status, body, http_status, error

    def json(self) -> Any:
        return json.loads(self.body) if self.body else None


def fetch_url(url: str) -> PageResult:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return PageResult(url, "success", body, resp.status, None)
    except urllib.error.HTTPError as exc:
        return PageResult(url, "failed", None, exc.code, f"HTTP {exc.code}")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return PageResult(url, "failed", None, None, f"{type(exc).__name__}: {exc}")


def fixture_page(url: str, path: Path) -> PageResult:
    text = path.read_text(encoding="utf-8")
    if path.name.endswith(".error.json"):
        spec = json.loads(text)
        if spec.get("timeout"):
            return PageResult(url, "failed", None, None, "TimeoutError: simulated")
        code = int(spec.get("http_status", 500))
        return PageResult(url, "failed", None, code, f"HTTP {code}")
    return PageResult(url, "success", text, 200, None)


# ---------------------------------------------------------------------------
# Provider adapters: (list_urls, parse_page, normalize_posting)
# ---------------------------------------------------------------------------

def gh_url(board: str) -> list[str]:
    return [f"https://boards-api.greenhouse.io/v1/boards/{urllib.parse.quote(board)}/jobs?content=true"]


def gh_parse(page: Any) -> list[dict]:
    return list(page.get("jobs", [])) if isinstance(page, dict) else []


def gh_normalize(job: dict, board: str) -> dict:
    offices = [o.get("name") for o in job.get("offices") or [] if o.get("name")]
    loc = (job.get("location") or {}).get("name")
    locations = [x for x in ([loc] if loc else []) + offices if x]
    departments = [d.get("name") for d in job.get("departments") or [] if d.get("name")]
    return {
        "opening_id": f"greenhouse:{board}:{job.get('id')}" if job.get("id") is not None else None,
        "title": job.get("title"),
        "department": departments[0] if departments else None,
        "team": None,  # Greenhouse has no team concept; department is not a team
        "locations": _dedupe(locations),
        "workplace_type": None,  # not a documented field; may appear in metadata, kept raw
        "job_url": job.get("absolute_url"),
        "apply_url": None,  # Greenhouse job board applications go through absolute_url; no separate field
        "jd_text": strip_html(job.get("content")),
        "salary": None,
        "source_published_at": None,  # Greenhouse gives updated_at only
        "source_updated_at": job.get("updated_at"),
        "posting_kind": "prospect" if job.get("internal_job_id") is None else "job",
    }


def ashby_url(board: str) -> list[str]:
    return [f"https://api.ashbyhq.com/posting-api/job-board/{urllib.parse.quote(board)}?includeCompensation=true"]


def ashby_parse(page: Any) -> list[dict]:
    return list(page.get("jobs", [])) if isinstance(page, dict) else []


def ashby_normalize(job: dict, board: str) -> dict:
    locations = []
    if job.get("location"):
        locations.append(job["location"])
    for sec in job.get("secondaryLocations") or []:
        if isinstance(sec, dict) and sec.get("location"):
            locations.append(sec["location"])
    return {
        "opening_id": f"ashby:{board}:{job.get('id')}" if job.get("id") else None,
        "title": job.get("title"),
        "department": job.get("department"),
        "team": job.get("team"),  # Ashby distinguishes team from department; null stays null
        "locations": _dedupe(locations),
        "workplace_type": (job.get("workplaceType") or None),
        "job_url": job.get("jobUrl"),
        "apply_url": job.get("applyUrl"),
        "jd_text": job.get("descriptionPlain") or strip_html(job.get("descriptionHtml")),
        "salary": job.get("compensation"),
        "source_published_at": job.get("publishedAt"),  # most recent publish, not first publish
        "source_updated_at": None,
        "is_listed": job.get("isListed"),
    }


def lever_urls(site: str, pages: int = 50) -> list[str]:
    base = f"https://api.lever.co/v0/postings/{urllib.parse.quote(site)}?mode=json&limit={LEVER_LIMIT}"
    return [f"{base}&skip={i * LEVER_LIMIT}" for i in range(pages)]


def lever_parse(page: Any) -> list[dict]:
    return list(page) if isinstance(page, list) else []


def lever_normalize(job: dict, site: str) -> dict:
    cats = job.get("categories") or {}
    locations = []
    if cats.get("location"):
        locations.append(cats["location"])
    for x in cats.get("allLocations") or []:
        locations.append(x)
    return {
        "opening_id": f"lever:{site}:{job.get('id')}" if job.get("id") else None,
        "title": job.get("text"),
        "department": cats.get("department"),
        "team": cats.get("team"),  # a Lever team tag is one piece of evidence, not proof of reporting line
        "locations": _dedupe(locations),
        "workplace_type": job.get("workplaceType"),
        "job_url": job.get("hostedUrl"),
        "apply_url": job.get("applyUrl"),
        "jd_text": job.get("descriptionPlain") or strip_html(job.get("description")),
        "salary": job.get("salaryRange"),
        # Lever's public Postings API documents no time fields (review R17). Undocumented createdAt stays raw only.
        "source_published_at": None,
        "source_updated_at": None,
        "country": job.get("country"),  # null means unknown, not "no country"
    }


PROVIDERS = {
    "greenhouse": (gh_url, gh_parse, gh_normalize, False),
    "ashby": (ashby_url, ashby_parse, ashby_normalize, False),
    "lever": (lever_urls, lever_parse, lever_normalize, True),  # paginated
}


def _dedupe(xs: list) -> list:
    out = []
    for x in xs:
        if x not in out:
            out.append(x)
    return out


# ---------------------------------------------------------------------------
# Main fetch
# ---------------------------------------------------------------------------

def fetch_board(provider: str, board: str, workspace: Path, company_id: str | None,
                fixtures: list[Path] | None) -> dict:
    urls_fn, parse_fn, norm_fn, paginated = PROVIDERS[provider]
    checked_at = now_iso()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    check_id = stamp + "-" + hashlib.sha1(board.encode()).hexdigest()[:6]
    board_dir = workspace / "evidence" / "boards" / provider / _safe(board) / check_id
    n = 1
    while board_dir.exists():  # never overwrite an earlier check's evidence
        n += 1
        board_dir = board_dir.with_name(f"{check_id}-{n}")
    board_dir.mkdir(parents=True)

    urls = urls_fn(board)
    pages: list[dict] = []
    postings: list[dict] = []
    status = "success"
    for i, url in enumerate(urls):
        if fixtures is not None:
            if i >= len(fixtures):
                break
            page = fixture_page(url, fixtures[i])
        else:
            page = fetch_url(url)
        rec = {"index": i, "url": url, "status": page.status, "http_status": page.http_status, "error": page.error}
        if page.body is not None:
            (board_dir / f"page-{i}.raw").write_text(page.body, encoding="utf-8")
            rec["raw"] = f"page-{i}.raw"
        if page.status != "success":
            pages.append(rec)
            status = "partial" if postings or any(p["status"] == "success" for p in pages) else "failed"
            break
        try:
            items = parse_fn(page.json())
        except (json.JSONDecodeError, TypeError) as exc:
            rec.update({"status": "failed", "error": f"unparseable JSON: {exc}"})
            pages.append(rec)
            status = "partial" if postings else "failed"
            break
        rec["count"] = len(items)
        pages.append(rec)
        postings.extend(items)
        if not paginated or len(items) < LEVER_LIMIT:
            break
    else:
        if paginated:
            status = "partial"  # ran out of page budget before an under-full page

    written = []
    for raw in postings:
        norm = norm_fn(raw, board)
        if not norm.get("opening_id"):
            norm["opening_id"] = f"{provider}:{board}:url:" + hashlib.sha1((norm.get("job_url") or json.dumps(raw, sort_keys=True)).encode()).hexdigest()[:12]
            norm["id_source"] = "derived_from_url"
        else:
            norm["id_source"] = "provider_native"
        norm.update({"provider": provider, "board": board, "company_id": company_id, "checked_at": checked_at,
                     "board_check": f"evidence/boards/{provider}/{_safe(board)}/{check_id}"})
        odir = workspace / "evidence" / "openings" / _safe(norm["opening_id"])
        odir.mkdir(parents=True, exist_ok=True)
        (odir / "posting.json").write_text(json.dumps({"normalized": norm, "raw": raw}, ensure_ascii=False, indent=2), encoding="utf-8")
        written.append(norm)

    observation = {
        "provider": provider, "board": board, "company_id": company_id, "check_id": check_id,
        "checked_at": checked_at, "retrieval_status": status,
        "coverage": {"pages_requested": len(pages), "pages_ok": sum(1 for p in pages if p["status"] == "success"),
                     "paginated": paginated, "complete": status == "success"},
        "postings_seen": len(postings), "openings_written": len(written), "pages": pages,
        "note": ("complete zero-result read: the board published nothing at checked_at; this is not evidence the company never hires"
                 if status == "success" and not postings else None),
    }
    (board_dir / "request.json").write_text(json.dumps({"urls": urls[: len(pages) or 1], "fixtures": [str(f) for f in fixtures] if fixtures else None}, indent=2), encoding="utf-8")
    (board_dir / "observation.json").write_text(json.dumps(observation, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"observation": observation, "openings": written, "board_dir": str(board_dir)}


def _safe(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._:-]+", "_", s).replace(":", "_")


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--provider", required=True, choices=sorted(PROVIDERS))
    ap.add_argument("--board", required=True, help="Greenhouse board token, Ashby job board name, or Lever site")
    ap.add_argument("--workspace", required=True, type=Path)
    ap.add_argument("--company", help="company_id to record on each opening")
    ap.add_argument("--fixture", action="append", type=Path, help="offline response file(s), one per page")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    result = fetch_board(args.provider, args.board, args.workspace, args.company, args.fixture)
    obs = result["observation"]
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{args.provider}/{args.board}: retrieval_status={obs['retrieval_status']} postings={obs['postings_seen']} "
              f"pages_ok={obs['coverage']['pages_ok']}/{obs['coverage']['pages_requested']} -> {result['board_dir']}")
        for o in result["openings"]:
            print(f"  {o['opening_id']}  {o.get('title')}  [{', '.join(o.get('locations') or []) or 'location: null'}]  team={o.get('team')}")
    return 0 if obs["retrieval_status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
