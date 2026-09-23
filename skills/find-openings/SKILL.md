---
name: find-openings
description: >-
  Take a direction template written by grill-direction and find current openings for it with
  evidence. Discover companies, confirm their official job board (Greenhouse, Ashby or Lever),
  fetch published postings, judge each against the direction's applicable confirmed hard fields
  as pass/fail/unknown, and write a candidate list the user decides on. Use this whenever the
  user wants to search for jobs, companies or openings that fit a saved direction, or asks
  "what's out there for me", "find companies", "check if this job fits".
argument-hint: "[direction id or path, optional company names]"
allowed-tools: Read Write Edit Glob Grep WebSearch WebFetch Bash(python3 *)
---

# find-openings

**Status: M0 skeleton.** The workflow below is the agreed contract from `docs/implementation-plan.md` §4. `scripts/ats_fetch.py` and the fixtures are not implemented yet; do not claim to have fetched anything until they are.

## What this skill produces

`<workspace_root>/candidates/<direction-id>.md`: frontmatter per `schema/candidate.schema.json`, then a readable list grouped by match status. Every judgement cites a field id, the direction revision, and evidence ids with checked_at. The user's decision (`user_decision`) is theirs alone; you never set it.

## Workflow (contract)

1. **Resolve workspace** with `scripts/resolve_workspace.py --expect <root> --json` (see grill-direction §0 for exit codes). Read the direction. If it is a draft, proceed but set `basis: exploratory` and list `pending_fields`.
2. **Applicability before evidence.** From the direction, select the fields that are `kind: hard`, `status: confirmed` and whose `scope` covers the opening being judged (an opening starting now is not subject to a field with `valid_from` next year). Record every hard field in `applicability` as applicable / not_applicable (with the scope reason) / not_confirmed. Only applicable ones get a `field_results` entry.
3. **Company discovery.** Use `search_hints.keywords` and the key fields for WebSearch, or take company names from the user. `search_hints.deprioritize` only lowers ranking; record the terms in `search_bias`. A company being found is not a company being chosen.
4. **Board confirmation.** From the company's own site, find the link to its job board and record that link as evidence. No official board found: record unknown, do not guess a board slug.
5. **Fetch postings** with `scripts/ats_fetch.py` (to be implemented): list-request observations go to `evidence/boards/<provider>/<board>/<check-id>/`, per-posting snapshots to `evidence/openings/<opening-id>/`. Keep raw fields beside normalized ones. Time fields per provider: Ashby `publishedAt` → `source_published_at`; Greenhouse `updated_at` → `source_updated_at`; Lever has no documented time fields, both null. `team` is null unless the provider supplies it; never fill it from `department`. 404/timeout → `retrieval_status: failed`, `opening_status: unknown`, keep `last_successful_check_at`. Partial pagination → `partial`. A complete empty list is a successful zero result.
6. **Judge.** For each applicable hard field: pass / fail / unknown, each with evidence ids. No JD text evidence → unknown. Never pass a field on your impression of a company or city. Compensation with mismatched basis (currency, period, base vs total) is not compared.
7. **Status.** In this order: any applicable hard field failed → `rejected`; a direction field in conflict or pending, or zero applicable confirmed hard fields → `needs_clarification`; any applicable hard field unknown → `needs_verification`; all pass → `eligible_for_comparison`. Show `opening_status` and `freshness_status` next to it; a match is not an open door.
8. **Write** the candidate file, run `scripts/validate.py candidate <file>`, then present the groups. Ask the user to mark `user_decision` themselves.
9. **Recheck triggers.** Direction revision, facts revision, evidence change, stale check, closed or moved posting: set `needs_recheck: true` with a reason. Keep the old judgement as history.

## Not yet done

- `scripts/ats_fetch.py` for Greenhouse, Ashby, Lever.
- `fixtures/` covering field differences, nulls, multiple locations, JD text, time fields, partial lists, zero results, board-level failure.
- `references/evidence-rules.md` (a working copy of `reference/design/research-evidence.md` rules).
