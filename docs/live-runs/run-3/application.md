---
opening_id: lever:palantir:6fe5515f-f677-4d98-8ac2-1775a425f5e7
status: blocked
candidate_refs:
  - direction_id: dir-001
    direction_revision: 5
primary_direction: dir-001
facts_revision: 2
resume_version: null
apply_url: https://jobs.lever.co/palantir/6fe5515f-f677-4d98-8ac2-1775a425f5e7/apply
created_at: '2026-09-24T00:30:00+00:00'
updated_at: '2026-09-24T00:45:00+00:00'
fields: []
blockers:
  - kind: other
    detail: No browser tool is available in this session. The Lever apply form at the apply_url above has not been opened, and no field has been filled or file uploaded. Facts F-001..F-009 are now status:confirmed (facts_revision 2) and are available to write into the form once a browser session (Claude in Chrome) opens it.
    raised_at: '2026-09-24T00:30:00+00:00'
review_items:
  - kind: evidence_gap
    detail: 'F-009 confirms work authorization for Singapore only ("Singapore Permanent Resident; does not require sponsorship to work in Singapore"). This opening''s location is New York, NY (hybrid), per c5-workplace evidence in dir-001. If the Lever form asks about US work authorization or visa sponsorship, this fact does not answer that question — it would be a missing_required_fact blocker at fill time, not something to fill from F-009.'
    field_label: Work authorization / visa sponsorship (anticipated form field)
---

## Notes

Pre-check (step 0): `dir-001` candidate entry for this opening shows `opening_status: published_present`, `freshness_status: current`, `user_decision: interested`, last checked 2026-09-24T00:13:55+00:00 — no re-verification needed.

Facts (step 2): imported 8 items (F-001..F-008) from `incoming/synthetic-resume.txt` into `profile/background_facts.yaml`. User confirmed all 8 as-is on 2026-09-24T00:45:00+00:00 and separately stated work authorization, recorded as F-009 (`source.kind: user_statement`) and confirmed in the same message. `facts_revision` is now 2. Resume file registered as document `doc-resume-01` (kind: resume) but not yet uploaded anywhere — no browser tool has touched the site.

Steps 3–5 (fill, read-back, upload) were not attempted: this session has no browser tool, so the form was never opened.
