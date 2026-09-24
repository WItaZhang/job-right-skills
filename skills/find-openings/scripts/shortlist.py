#!/usr/bin/env python3
"""Shortlist fetched openings for a direction so the agent judges a handful instead of reading hundreds.

Usage:
  shortlist.py --workspace <root> --direction <dir-id or path> [--provider P] [--board B]
               [--limit 12] [--min-score 1] [--extra-keyword T ...] [--extra-deprioritize T ...] [--json]

Boards are usually in English; a direction interviewed in another language may carry keywords in that
language only. Add board-language terms with --extra-keyword; they are recorded in the output so the
user can see exactly which terms shaped discovery.

Reads every evidence/openings/*/posting.json (optionally restricted to one provider/board), scores each
against the direction's search_hints (keywords add, deprioritize subtract) plus the observable_criteria
and examples of hard fields, and prints a compact table: opening_id, title, team, locations,
workplace_type, score, matched terms, url, snapshot path, and a short JD excerpt around the best hit.

This is discovery ranking only. A score is not evidence and never decides pass/fail; the agent still has
to read the snapshot and cite text for every applicable hard field. Deprioritized openings are listed at
the bottom (not dropped) so the user can see what was pushed down.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import validate  # noqa: E402  (shared YAML loader)


def load_direction(workspace: Path, ref: str) -> dict:
    p = Path(ref)
    if not p.exists():
        p = workspace / "directions" / f"{ref}.md"
    fm, _ = validate.split_frontmatter(p.read_text(encoding="utf-8"))
    return fm


def term_list(direction: dict) -> tuple[list[str], list[str]]:
    hints = direction.get("search_hints") or {}
    plus = [t for t in hints.get("keywords") or [] if t]
    for fid, f in direction["fields"].items():
        if f.get("kind") == "hard" and f.get("status") == "confirmed":
            for x in (f.get("examples") or []) + (f.get("observable_criteria") or []):
                if isinstance(x, str) and 2 <= len(x) <= 40:
                    plus.append(x)
    minus = [t for t in hints.get("deprioritize") or [] if t]
    return _dedupe(plus), _dedupe(minus)


def _dedupe(xs):
    out = []
    for x in xs:
        if x not in out:
            out.append(x)
    return out


def _hits(text: str, terms: list[str]) -> list[str]:
    low = text.lower()
    return [t for t in terms if t.lower() in low]


def score_opening(norm: dict, plus: list[str], minus: list[str]) -> dict:
    title = norm.get("title") or ""
    head = " ".join(str(x) for x in [title, norm.get("team") or "", norm.get("department") or ""])
    body = norm.get("jd_text") or ""
    title_hits = _hits(head, plus)
    body_hits = [t for t in _hits(body, plus) if t not in title_hits]
    title_minus = _hits(head, minus)
    body_minus = [t for t in _hits(body, minus) if t not in title_minus]
    # Deprioritize terms push an opening down only when they hit the title/team/department. A JD body that
    # merely mentions "reports to the Head of Infra" is not a management role; body hits just cost a point.
    score = 3 * len(title_hits) + len(body_hits) - 4 * len(title_minus) - 1 * len(body_minus)
    excerpt = None
    for t in title_hits + body_hits:
        m = re.search(re.escape(t), body, re.IGNORECASE)
        if m:
            a, b = max(0, m.start() - 80), min(len(body), m.end() + 80)
            excerpt = ("…" if a else "") + body[a:b].replace("\n", " ") + ("…" if b < len(body) else "")
            break
    return {
        "score": score,
        "matched": title_hits + body_hits,
        "deprioritized_by": title_minus,
        "body_deprioritize_hits": body_minus,
        "excerpt": excerpt,
    }


def shortlist(workspace: Path, direction: dict, provider: str | None, board: str | None, limit: int, min_score: int,
              extra_keywords: list[str] | None = None, extra_deprioritize: list[str] | None = None) -> dict:
    plus, minus = term_list(direction)
    plus = _dedupe(plus + list(extra_keywords or []))
    minus = _dedupe(minus + list(extra_deprioritize or []))
    rows = []
    for p in (workspace / "evidence" / "openings").glob("*/posting.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        n = d["normalized"]
        if provider and n.get("provider") != provider:
            continue
        if board and n.get("board") != board:
            continue
        s = score_opening(n, plus, minus)
        rows.append({
            "opening_id": n["opening_id"], "title": n.get("title"), "team": n.get("team"), "department": n.get("department"),
            "locations": n.get("locations") or [], "workplace_type": n.get("workplace_type"), "job_url": n.get("job_url"),
            "snapshot": str(p.relative_to(workspace)), "checked_at": n.get("checked_at"), **s,
        })
    kept = [r for r in rows if r["score"] >= min_score and not r["deprioritized_by"]]
    pushed_down = [r for r in rows if r["deprioritized_by"]]  # shown regardless of score, for transparency
    kept.sort(key=lambda r: (-r["score"], r["title"] or ""))
    pushed_down.sort(key=lambda r: (-r["score"], r["title"] or ""))
    return {
        "direction_id": direction["id"], "direction_revision": direction["revision"],
        "terms": {"keywords": plus, "deprioritize": minus, "extra_keywords": list(extra_keywords or []),
                  "extra_deprioritize": list(extra_deprioritize or [])},
        "scanned": len(rows), "shortlist": kept[:limit], "pushed_down": pushed_down[:limit],
        "search_bias": minus,
        "note": "Scores rank discovery only. Every pass/fail still needs cited evidence from the snapshot.",
    }


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace", required=True, type=Path)
    ap.add_argument("--direction", required=True)
    ap.add_argument("--provider")
    ap.add_argument("--board")
    ap.add_argument("--limit", type=int, default=12)
    ap.add_argument("--min-score", type=int, default=1)
    ap.add_argument("--extra-keyword", action="append", default=[], help="board-language term to add (e.g. English for a US board); recorded in output")
    ap.add_argument("--extra-deprioritize", action="append", default=[], help="board-language deprioritize term; recorded in search_bias")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    direction = load_direction(a.workspace, a.direction)
    res = shortlist(a.workspace, direction, a.provider, a.board, a.limit, a.min_score, a.extra_keyword, a.extra_deprioritize)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    print(f"direction {res['direction_id']} r{res['direction_revision']}; scanned {res['scanned']} openings; "
          f"keywords={res['terms']['keywords']}; deprioritize={res['terms']['deprioritize']}")
    print("\n== shortlist ==")
    for r in res["shortlist"]:
        print(f"[{r['score']:>3}] {r['opening_id']}  {r['title']}  team={r['team']}  loc={', '.join(r['locations']) or 'null'}  wp={r['workplace_type']}")
        print(f"      matched={r['matched']}  {r['job_url']}")
        if r["excerpt"]:
            print(f"      {r['excerpt']}")
    print("\n== pushed down by deprioritize terms (not judged, shown for transparency) ==")
    for r in res["pushed_down"]:
        print(f"[{r['score']:>3}] {r['opening_id']}  {r['title']}  deprioritized_by={r['deprioritized_by']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
