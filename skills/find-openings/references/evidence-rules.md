# Evidence rules for find-openings

Working copy of `reference/design/research-evidence.md`, reduced to what this skill has to do. Every judgement you write must be traceable to a direction field, a direction revision, and evidence with a check time. When you cannot trace it, the answer is unknown, not a guess.

## One claim, one piece of evidence

An evidence record supports exactly one assertion with a locator: "JD text at `evidence/openings/<id>/posting.json` says 'individual contributor role'". Not "this company seems IC-friendly". A URL that supports a whole paragraph of conclusions is not evidence, it is an impression.

Source priority: the employer's own site and the ATS board linked from it; then official team pages and dated engineering posts (bounded in time); then aggregators for discovery and cross-check; search snippets only as leads. Higher priority does not mean automatically correct; official pages go stale too.

## Company → board → opening

- Record the link from the company's own site to its board as evidence. Do not guess a board slug from the company name; a wrong board silently attributes another company's jobs.
- A department is not a team. Greenhouse has no team field; Ashby and Lever have one that is a label, not proof of reporting lines. `team: null` stays null.
- An opening being listed proves it was published at `checked_at`. It does not prove headcount, that the hiring manager still has budget, or that the team named in the JD exists as described.

## Statuses never mix

| Dimension | Values | Set by |
|---|---|---|
| retrieval_status | success / partial / failed / not_checked | `ats_fetch.py`, per board check |
| opening_status | published_present / explicitly_closed / unknown | you, from the latest successful check and the JD text |
| claim / field result | pass / fail / unknown | you, per applicable confirmed hard field |
| freshness_status | current / stale / unknown | you, relative to when the user will act |
| match_status | rejected / needs_clarification / needs_verification / eligible_for_comparison | recomputed from results; `validate.py candidate` rejects a mismatch |
| user_decision | undecided / interested / not_interested | the user only |

Rules that follow:

- 404, timeout, redirect to a generic careers page: `retrieval_status: failed`, `opening_status: unknown`. Keep `last_successful_check_at`. Never write `explicitly_closed` from a failed read.
- Partial pagination: `partial`. Absence from a partial list proves nothing.
- A complete read with zero postings: `success`, zero results. Record it in `evidence/boards/...`. It is not evidence the company never hires.
- Text saying "this position has been filled" or "no longer accepting applications": `explicitly_closed`, keep the last open record.
- A past deadline with body text still saying open: conflict; show both, choose neither.
- `isListed: false` (Ashby) means reachable by direct link only. Not closed.

## Applicability before judgement (R12, R29)

For each opening, list every hard field of the direction and every pending or conflict field:

- `applicable`: confirmed hard, scope covers this opening. Gets exactly one result.
- `not_applicable` + reason: outside scope for this opening (for example `valid_from` after the start date). Does not block.
- `not_confirmed`: relevant to this opening, but the direction has not confirmed it. Blocks with `needs_clarification`.

Omitting a pending field is an error; "I did not list it" is not "I showed it is irrelevant". The direction's `pending_fields` list is for display; only `not_confirmed` entries in this opening's applicability change its status.

## Judging a field

- pass / fail only with at least one evidence reference to JD text or a structured field in the snapshot.
- No text about the condition: unknown. Do not pass a field on your impression of the company, the city, or the title.
- Compensation: compare only when currency, period, and base-vs-total match the user's basis. Otherwise unknown with the mismatch noted.
- Search hints (`deprioritize`) rank discovery results. They are never a reason to fail a field.

## Confidence words

high: primary material directly supports this one claim, dated, no contradiction. medium: partial support or an inference step, which you spell out. low: indirect, old or weak; keep as a lead. unknown: no adequate basis or unresolved conflict. Never a percentage, never a hiring probability. Report company facts, team relation and opening status with separate confidence; a trustworthy company page says nothing about a team relation.

## Recheck triggers

Direction revision, facts revision, evidence change, a check older than makes sense for the user's next step, an opening that closed or moved. Set `needs_recheck: true` with the reason. Keep the old judgement as history; do not rewrite it as verified today.
