---
name: find-openings
description: >-
  Take a direction template written by grill-direction and find current openings for it with
  evidence. Discover companies, confirm their official job board (Greenhouse, Ashby or Lever),
  fetch published postings with the bundled ats_fetch.py, judge each against the direction's
  applicable confirmed hard fields as pass/fail/unknown, and write a candidate list the user
  decides on. Use this whenever the user wants to search for jobs, companies or openings that fit
  a saved direction, or asks "what's out there for me", "find companies", "check if this job
  fits", "does this posting match my direction".
argument-hint: "[direction id or path, optional company names or board URLs]"
allowed-tools: Read Write Edit Glob Grep WebSearch WebFetch Bash(python3 *)
---

# find-openings

You turn a direction into a list of openings the user can decide on, with the reasoning shown. The hard part is not finding postings; it is not lying about them. Every pass, fail or unknown must point at a field id, a direction revision and evidence with a check time. Read `references/evidence-rules.md` before judging anything.

**Status:** fetcher and fixtures implemented and smoke-tested online against two public boards (M2). Company discovery, judging and the candidate file are agent work following this contract; no end-to-end run has been recorded yet.

## Output

`<workspace_root>/candidates/<direction-id>.md`: frontmatter per `schema/candidate.schema.json`, then a readable list grouped by `match_status`. Run `scripts/validate.py candidate <file>` before showing it; the validator recomputes each status from the recorded results and rejects records where they disagree. `user_decision` is the user's alone; you never set it.

## Workflow

### 0. Workspace and direction

```bash
python3 "${CLAUDE_SKILL_DIR}/../../scripts/resolve_workspace.py" --expect <root> --json
```

Exit 3 means the resolution changed: tell the user. Read the direction file. If `status: draft`, proceed with `basis: exploratory` and copy its pending and conflict field ids into `pending_fields`.

### 1. Applicability before evidence

For each opening you will judge, list every hard field and every pending/conflict field of the direction in `applicability`:

- `applicable`: confirmed hard, `scope` covers this opening (an opening starting now is not subject to a field with `valid_from` next year).
- `not_applicable` with a `reason`: outside scope for this opening. Does not block.
- `not_confirmed`: relevant here but the direction has not confirmed it. Blocks with `needs_clarification`.

Do not leave a pending field out; the validator treats omission as an error, because omission is not proof of irrelevance.

### 2. Company discovery

Use `search_hints.keywords` and the key fields for WebSearch, or take company names and board URLs from the user. `search_hints.deprioritize` only lowers ranking; record the terms used in `search_bias` so the user knows low-ranked openings were not judged. A company being found is not a company being chosen.

### 3. Board confirmation

From the company's own site, find the careers link and follow it to the board. Record that link as evidence. The provider is visible in the board URL: `boards.greenhouse.io/<token>` or `job-boards.greenhouse.io/<token>`, `jobs.ashbyhq.com/<name>`, `jobs.lever.co/<site>`. No official board found: record `unknown`; never guess a slug.

### 4. Fetch

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/ats_fetch.py" --provider greenhouse|ashby|lever --board <token> \
    --workspace <root> --company <company_id>
```

It writes the board-level observation (request, raw pages, `retrieval_status`, coverage) to `evidence/boards/<provider>/<board>/<check-id>/` and one `posting.json` per opening to `evidence/openings/<opening-id>/`, raw beside normalized. Exit code 1 means the read was not complete (`partial` or `failed`); the observation says which pages failed. Read `observation.json` before using any posting from that check.

Provider facts the script encodes and you must not undo: Greenhouse has `updated_at` only and no team; Ashby has `publishedAt` (latest publish, not first) and a real `team` field that may be null; Lever documents no time fields at all, and its `team` is a label. `team` is never filled from `department`.

### 5. Judge

For each applicable field: pass / fail / unknown, each with `evidence_refs` into this candidate's `evidence` list. The evidence entry names the snapshot path and the single claim it supports ("JD text says 'individual contributor', no direct reports"). No relevant text: unknown. Impressions of the company, city or title are not evidence. Compensation with mismatched currency, period or base/total basis is unknown with the mismatch noted. Soft fields get meets / tradeoff / unknown in `soft_results`.

### 6. Status

Recomputed, not chosen: any applicable field fails → `rejected`; any `not_confirmed` entry or zero applicable fields → `needs_clarification`; any unknown → `needs_verification`; otherwise `eligible_for_comparison`. Alongside it, `opening_status` from the latest successful check (`published_present` unless the JD says closed; `unknown` after a failed read) and `freshness_status`. A match is not an open door; show both.

### 7. Write, validate, present

Write the candidate file, run the validator, fix what it reports, then present the four groups with each opening's key evidence. Ask the user to mark `user_decision` themselves. Set `needs_recheck` with a reason when a direction or facts revision changes, evidence changes, a check is stale, or a posting closes or moves. Keep old judgements as history.

## Files

- `scripts/ats_fetch.py` — provider adapters, evidence writing, `--fixture` for offline runs.
- `fixtures/` — synthetic responses for the three providers, an empty list, a 404 and a timeout; used by `tests/test_ats_fetch.py`.
- `references/evidence-rules.md` — the rules above in full, with the status table.
- `../../schema/candidate.schema.json`, `../../scripts/validate.py candidate`.
