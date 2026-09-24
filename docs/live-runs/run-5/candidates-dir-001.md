---
direction_id: dir-001
direction_revision: 11
facts_revision: null
basis: confirmed
generated_at: 2026-09-24T01:45:00+00:00
search_bias:
  - intern
  - internship
  - new grad
  - junior
  - "实习"
  - "应届"
  - mid-level
  - 2-3 years experience
  - ticket-driven
pending_fields: []
candidates:
  - opening_id: "lever:palantir:d7030550-f80f-422c-965f-3120db433dea"
    id_source: provider_native
    company_id: palantir
    provider: lever
    board: palantir
    title: "Senior Software Engineer - Autonomous Systems"
    job_url: "https://jobs.lever.co/palantir/d7030550-f80f-422c-965f-3120db433dea"
    apply_url: "https://jobs.lever.co/palantir/d7030550-f80f-422c-965f-3120db433dea/apply"
    applicability:
      - field_id: role.system_scale
        state: applicable
      - field_id: role.level
        state: applicable
      - field_id: role.nature
        state: applicable
    field_results:
      - field_id: role.system_scale
        result: unknown
        evidence_refs: [ev-d703-jd]
        note: "JD describes C2/agentic-autonomy software for autonomous systems (sensors, individual and swarm vehicles, real-time kinetic/non-kinetic control). No quantified traffic/data/user-scale text (no PB/亿级用户/high-throughput figures)."
      - field_id: role.level
        result: unknown
        evidence_refs: [ev-d703-jd]
        note: "Title says Senior Software Engineer, but JD text gives no description of independent architecture-decision scope; direction's own alt_test (I-009) requires judging responsibility scope, not title text alone."
      - field_id: role.nature
        result: pass
        evidence_refs: [ev-d703-jd]
        note: "JD frames the role entirely as building/integrating/deploying software ('contribute directly to the development of...'); no management, performance-review or hiring language anywhere in the posting."
    soft_results:
      - field_id: location.city_profile
        result: unknown
        evidence_refs: [ev-d703-jd]
        note: "Palo Alto is not one of the direction's example cities (Singapore/Shenzhen/Hangzhou/Berlin/Seattle); no sourced evidence of local tech-meetup density was collected, so an impression of the city is not used to score it."
      - field_id: location.relocation_ease
        result: tradeoff
        evidence_refs: [ev-d703-jd]
        note: "Not directly tested by the direction. Inferred (medium confidence) from I-006, where the user confirmed a US location (Seattle) as visa-hassle/not-proactively-considered-but-not-excluded; Palo Alto is the same US work-visa regime."
      - field_id: compensation.base
        result: unknown
        evidence_refs: [ev-d703-salary]
        note: "Posting states an estimated USD base salary range of $145,000-$200,000/year. Direction's benchmark is SGD 200,000/year (Singapore) or PPP-equivalent for Shenzhen/Hangzhou; USD/US-location pay is outside that scope, so currency mismatch leaves this unknown rather than compared."
    match_status: needs_verification
    match_reason: "Two of three applicable hard fields (role.system_scale, role.level) have no confirming or disconfirming text in the JD; role.nature passes. No field fails."
    opening_status: published_present
    freshness_status: current
    last_successful_check_at: "2026-09-24T00:54:19+00:00"
    needs_recheck: false
    user_decision: undecided
    evidence:
      - id: ev-board-link
        source_url: "https://www.palantir.com/careers/"
        publisher: palantir.com
        claim: "Palantir's own careers page leads to jobs.lever.co/palantir as the official ATS board (confirmed via company site + board content match on 2026-09-24)."
        checked_at: "2026-09-24T01:10:00+00:00"
        retrieval_status: success
      - id: ev-board-fetch
        source_url: "https://api.lever.co/v0/postings/palantir?mode=json&limit=100&skip=0"
        publisher: jobs.lever.co
        claim: "Full paginated read of the palantir Lever board: 4/4 pages succeeded, 318 postings seen and written."
        snapshot_ref: "evidence/boards/lever/palantir/20260924T005419.605115Z-077199/observation.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success
        coverage: "4 pages requested, 4 pages ok, pagination complete"
      - id: ev-d703-jd
        source_url: "https://jobs.lever.co/palantir/d7030550-f80f-422c-965f-3120db433dea"
        publisher: jobs.lever.co
        claim: "Posting JD text (Palo Alto) for Senior Software Engineer - Autonomous Systems, used for role.system_scale/role.level/role.nature judgement."
        snapshot_ref: "evidence/openings/lever_palantir_d7030550-f80f-422c-965f-3120db433dea/posting.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success
      - id: ev-d703-salary
        source_url: "https://jobs.lever.co/palantir/d7030550-f80f-422c-965f-3120db433dea"
        publisher: jobs.lever.co
        claim: "Posting's additional/benefits text states 'estimated salary range for this position is estimated to be $145,000 - $200,000/year' (USD, base)."
        snapshot_ref: "evidence/openings/lever_palantir_d7030550-f80f-422c-965f-3120db433dea/posting.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success

  - opening_id: "lever:palantir:88f8f593-af1f-4d27-9042-454c24a64d3f"
    id_source: provider_native
    company_id: palantir
    provider: lever
    board: palantir
    title: "Senior Software Engineer - Autonomous Systems"
    job_url: "https://jobs.lever.co/palantir/88f8f593-af1f-4d27-9042-454c24a64d3f"
    apply_url: "https://jobs.lever.co/palantir/88f8f593-af1f-4d27-9042-454c24a64d3f/apply"
    applicability:
      - field_id: role.system_scale
        state: applicable
      - field_id: role.level
        state: applicable
      - field_id: role.nature
        state: applicable
    field_results:
      - field_id: role.system_scale
        result: unknown
        evidence_refs: [ev-88f8-jd]
        note: "Same JD text as the Palo Alto posting of this role (Autonomous Systems). No quantified traffic/data/user-scale text."
      - field_id: role.level
        result: unknown
        evidence_refs: [ev-88f8-jd]
        note: "Title says Senior; JD text gives no explicit description of independent architecture-decision scope."
      - field_id: role.nature
        result: pass
        evidence_refs: [ev-88f8-jd]
        note: "JD frames the role as hands-on building/integrating/deploying software; no management/performance-review/hiring language."
    soft_results:
      - field_id: location.city_profile
        result: meets
        evidence_refs: [ev-88f8-jd]
        note: "Seattle is listed verbatim as an example city in location.city_profile (source_ref I-006)."
      - field_id: location.relocation_ease
        result: tradeoff
        evidence_refs: [ev-88f8-jd]
        note: "Direction's own example (I-006) names Seattle explicitly as visa-hassle/not-proactively-considered but not an absolute exclusion."
      - field_id: compensation.base
        result: unknown
        evidence_refs: [ev-88f8-salary]
        note: "Posting states estimated USD base salary $145,000-$200,000/year. Currency mismatch against the SGD/PPP-anchored benchmark leaves this unknown."
    match_status: needs_verification
    match_reason: "role.system_scale and role.level are unknown; role.nature passes; no field fails."
    opening_status: published_present
    freshness_status: current
    last_successful_check_at: "2026-09-24T00:54:19+00:00"
    needs_recheck: false
    user_decision: undecided
    evidence:
      - id: ev-board-link
        source_url: "https://www.palantir.com/careers/"
        publisher: palantir.com
        claim: "Palantir's own careers page leads to jobs.lever.co/palantir as the official ATS board (confirmed via company site + board content match on 2026-09-24)."
        checked_at: "2026-09-24T01:10:00+00:00"
        retrieval_status: success
      - id: ev-board-fetch
        source_url: "https://api.lever.co/v0/postings/palantir?mode=json&limit=100&skip=0"
        publisher: jobs.lever.co
        claim: "Full paginated read of the palantir Lever board: 4/4 pages succeeded, 318 postings seen and written."
        snapshot_ref: "evidence/boards/lever/palantir/20260924T005419.605115Z-077199/observation.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success
        coverage: "4 pages requested, 4 pages ok, pagination complete"
      - id: ev-88f8-jd
        source_url: "https://jobs.lever.co/palantir/88f8f593-af1f-4d27-9042-454c24a64d3f"
        publisher: jobs.lever.co
        claim: "Posting JD text (Seattle) for Senior Software Engineer - Autonomous Systems, used for role.system_scale/role.level/role.nature judgement."
        snapshot_ref: "evidence/openings/lever_palantir_88f8f593-af1f-4d27-9042-454c24a64d3f/posting.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success
      - id: ev-88f8-salary
        source_url: "https://jobs.lever.co/palantir/88f8f593-af1f-4d27-9042-454c24a64d3f"
        publisher: jobs.lever.co
        claim: "Posting's additional/benefits text states 'estimated salary range for this position is estimated to be $145,000 - $200,000/year' (USD, base)."
        snapshot_ref: "evidence/openings/lever_palantir_88f8f593-af1f-4d27-9042-454c24a64d3f/posting.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success

  - opening_id: "lever:palantir:d40d5d19-8f9e-4e6b-b4d3-b7457c90adec"
    id_source: provider_native
    company_id: palantir
    provider: lever
    board: palantir
    title: "Senior Software Engineer - Autonomous Systems"
    job_url: "https://jobs.lever.co/palantir/d40d5d19-8f9e-4e6b-b4d3-b7457c90adec"
    apply_url: "https://jobs.lever.co/palantir/d40d5d19-8f9e-4e6b-b4d3-b7457c90adec/apply"
    applicability:
      - field_id: role.system_scale
        state: applicable
      - field_id: role.level
        state: applicable
      - field_id: role.nature
        state: applicable
    field_results:
      - field_id: role.system_scale
        result: unknown
        evidence_refs: [ev-d40d-jd]
        note: "Same JD text as the other Autonomous Systems postings. No quantified traffic/data/user-scale text."
      - field_id: role.level
        result: unknown
        evidence_refs: [ev-d40d-jd]
        note: "Title says Senior; JD text gives no explicit description of independent architecture-decision scope."
      - field_id: role.nature
        result: pass
        evidence_refs: [ev-d40d-jd]
        note: "JD frames the role as hands-on building/integrating/deploying software; no management/performance-review/hiring language."
    soft_results:
      - field_id: location.city_profile
        result: unknown
        evidence_refs: [ev-d40d-jd]
        note: "Washington, D.C. is not one of the direction's example cities; no sourced evidence collected on local tech-meetup density."
      - field_id: location.relocation_ease
        result: tradeoff
        evidence_refs: [ev-d40d-jd]
        note: "Not directly tested. Inferred (medium confidence) from I-006's US-visa-hassle finding for Seattle; D.C. is the same US work-visa regime."
      - field_id: compensation.base
        result: unknown
        evidence_refs: [ev-d40d-salary]
        note: "Posting states estimated USD base salary $145,000-$200,000/year. Currency mismatch against SGD/PPP-anchored benchmark leaves this unknown."
    match_status: needs_verification
    match_reason: "role.system_scale and role.level are unknown; role.nature passes; no field fails."
    opening_status: published_present
    freshness_status: current
    last_successful_check_at: "2026-09-24T00:54:19+00:00"
    needs_recheck: false
    user_decision: undecided
    evidence:
      - id: ev-board-link
        source_url: "https://www.palantir.com/careers/"
        publisher: palantir.com
        claim: "Palantir's own careers page leads to jobs.lever.co/palantir as the official ATS board (confirmed via company site + board content match on 2026-09-24)."
        checked_at: "2026-09-24T01:10:00+00:00"
        retrieval_status: success
      - id: ev-board-fetch
        source_url: "https://api.lever.co/v0/postings/palantir?mode=json&limit=100&skip=0"
        publisher: jobs.lever.co
        claim: "Full paginated read of the palantir Lever board: 4/4 pages succeeded, 318 postings seen and written."
        snapshot_ref: "evidence/boards/lever/palantir/20260924T005419.605115Z-077199/observation.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success
        coverage: "4 pages requested, 4 pages ok, pagination complete"
      - id: ev-d40d-jd
        source_url: "https://jobs.lever.co/palantir/d40d5d19-8f9e-4e6b-b4d3-b7457c90adec"
        publisher: jobs.lever.co
        claim: "Posting JD text (Washington, D.C.) for Senior Software Engineer - Autonomous Systems, used for role.system_scale/role.level/role.nature judgement."
        snapshot_ref: "evidence/openings/lever_palantir_d40d5d19-8f9e-4e6b-b4d3-b7457c90adec/posting.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success
      - id: ev-d40d-salary
        source_url: "https://jobs.lever.co/palantir/d40d5d19-8f9e-4e6b-b4d3-b7457c90adec"
        publisher: jobs.lever.co
        claim: "Posting's additional/benefits text states 'estimated salary range for this position is estimated to be $145,000 - $200,000/year' (USD, base)."
        snapshot_ref: "evidence/openings/lever_palantir_d40d5d19-8f9e-4e6b-b4d3-b7457c90adec/posting.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success

  - opening_id: "lever:palantir:bba1ecbc-e56d-48b0-b33a-aefcbffbd655"
    id_source: provider_native
    company_id: palantir
    provider: lever
    board: palantir
    title: "Senior Software Engineer - Autonomous Systems"
    job_url: "https://jobs.lever.co/palantir/bba1ecbc-e56d-48b0-b33a-aefcbffbd655"
    apply_url: "https://jobs.lever.co/palantir/bba1ecbc-e56d-48b0-b33a-aefcbffbd655/apply"
    applicability:
      - field_id: role.system_scale
        state: applicable
      - field_id: role.level
        state: applicable
      - field_id: role.nature
        state: applicable
    field_results:
      - field_id: role.system_scale
        result: unknown
        evidence_refs: [ev-bba1-jd]
        note: "Same JD text as the other Autonomous Systems postings. No quantified traffic/data/user-scale text."
      - field_id: role.level
        result: unknown
        evidence_refs: [ev-bba1-jd]
        note: "Title says Senior; JD text gives no explicit description of independent architecture-decision scope."
      - field_id: role.nature
        result: pass
        evidence_refs: [ev-bba1-jd]
        note: "JD frames the role as hands-on building/integrating/deploying software; no management/performance-review/hiring language."
    soft_results:
      - field_id: location.city_profile
        result: unknown
        evidence_refs: [ev-bba1-jd]
        note: "New York is not one of the direction's example cities; no sourced evidence collected on local tech-meetup density."
      - field_id: location.relocation_ease
        result: tradeoff
        evidence_refs: [ev-bba1-jd]
        note: "Not directly tested. Inferred (medium confidence) from I-006's US-visa-hassle finding for Seattle; New York is the same US work-visa regime."
      - field_id: compensation.base
        result: unknown
        evidence_refs: [ev-bba1-salary]
        note: "Posting states estimated USD base salary $145,000-$200,000/year. Currency mismatch against SGD/PPP-anchored benchmark leaves this unknown."
    match_status: needs_verification
    match_reason: "role.system_scale and role.level are unknown; role.nature passes; no field fails."
    opening_status: published_present
    freshness_status: current
    last_successful_check_at: "2026-09-24T00:54:19+00:00"
    needs_recheck: false
    user_decision: undecided
    evidence:
      - id: ev-board-link
        source_url: "https://www.palantir.com/careers/"
        publisher: palantir.com
        claim: "Palantir's own careers page leads to jobs.lever.co/palantir as the official ATS board (confirmed via company site + board content match on 2026-09-24)."
        checked_at: "2026-09-24T01:10:00+00:00"
        retrieval_status: success
      - id: ev-board-fetch
        source_url: "https://api.lever.co/v0/postings/palantir?mode=json&limit=100&skip=0"
        publisher: jobs.lever.co
        claim: "Full paginated read of the palantir Lever board: 4/4 pages succeeded, 318 postings seen and written."
        snapshot_ref: "evidence/boards/lever/palantir/20260924T005419.605115Z-077199/observation.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success
        coverage: "4 pages requested, 4 pages ok, pagination complete"
      - id: ev-bba1-jd
        source_url: "https://jobs.lever.co/palantir/bba1ecbc-e56d-48b0-b33a-aefcbffbd655"
        publisher: jobs.lever.co
        claim: "Posting JD text (New York) for Senior Software Engineer - Autonomous Systems, used for role.system_scale/role.level/role.nature judgement."
        snapshot_ref: "evidence/openings/lever_palantir_bba1ecbc-e56d-48b0-b33a-aefcbffbd655/posting.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success
      - id: ev-bba1-salary
        source_url: "https://jobs.lever.co/palantir/bba1ecbc-e56d-48b0-b33a-aefcbffbd655"
        publisher: jobs.lever.co
        claim: "Posting's additional/benefits text states 'estimated salary range for this position is estimated to be $145,000 - $200,000/year' (USD, base)."
        snapshot_ref: "evidence/openings/lever_palantir_bba1ecbc-e56d-48b0-b33a-aefcbffbd655/posting.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success

  - opening_id: "lever:palantir:8a95dba1-b814-4243-be14-eba1df340ceb"
    id_source: provider_native
    company_id: palantir
    provider: lever
    board: palantir
    title: "Senior Software Engineer - Observability"
    job_url: "https://jobs.lever.co/palantir/8a95dba1-b814-4243-be14-eba1df340ceb"
    apply_url: "https://jobs.lever.co/palantir/8a95dba1-b814-4243-be14-eba1df340ceb/apply"
    applicability:
      - field_id: role.system_scale
        state: applicable
      - field_id: role.level
        state: applicable
      - field_id: role.nature
        state: applicable
    field_results:
      - field_id: role.system_scale
        result: unknown
        evidence_refs: [ev-8a95-jd]
        note: "JD says the role 'will have a direct impact on Palantir's ability to scale our engineering efforts' but gives no quantified log/metric/trace volume, throughput or user-count figures matching the observable criteria."
      - field_id: role.level
        result: pass
        evidence_refs: [ev-8a95-jd]
        note: "JD states 'you will be directly responsible for Palantir's observability platform' covering ingestion, processing, monitoring and alerting end-to-end -- an explicit statement of individual ownership over a system, not a ticket-driven scope."
      - field_id: role.nature
        result: pass
        evidence_refs: [ev-8a95-jd]
        note: "JD describes hands-on platform ownership and technical execution; no management/performance-review/hiring language."
    soft_results:
      - field_id: location.city_profile
        result: unknown
        evidence_refs: [ev-8a95-jd]
        note: "New York is not one of the direction's example cities; no sourced evidence collected on local tech-meetup density."
      - field_id: location.relocation_ease
        result: tradeoff
        evidence_refs: [ev-8a95-jd]
        note: "Not directly tested. Inferred (medium confidence) from I-006's US-visa-hassle finding for Seattle; New York is the same US work-visa regime."
      - field_id: compensation.base
        result: unknown
        evidence_refs: [ev-8a95-salary]
        note: "Posting states estimated USD base salary $135,000-$200,000/year. Currency mismatch against SGD/PPP-anchored benchmark leaves this unknown."
    match_status: needs_verification
    match_reason: "role.level and role.nature pass; role.system_scale is unknown; no field fails."
    opening_status: published_present
    freshness_status: current
    last_successful_check_at: "2026-09-24T00:54:19+00:00"
    needs_recheck: false
    user_decision: undecided
    evidence:
      - id: ev-board-link
        source_url: "https://www.palantir.com/careers/"
        publisher: palantir.com
        claim: "Palantir's own careers page leads to jobs.lever.co/palantir as the official ATS board (confirmed via company site + board content match on 2026-09-24)."
        checked_at: "2026-09-24T01:10:00+00:00"
        retrieval_status: success
      - id: ev-board-fetch
        source_url: "https://api.lever.co/v0/postings/palantir?mode=json&limit=100&skip=0"
        publisher: jobs.lever.co
        claim: "Full paginated read of the palantir Lever board: 4/4 pages succeeded, 318 postings seen and written."
        snapshot_ref: "evidence/boards/lever/palantir/20260924T005419.605115Z-077199/observation.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success
        coverage: "4 pages requested, 4 pages ok, pagination complete"
      - id: ev-8a95-jd
        source_url: "https://jobs.lever.co/palantir/8a95dba1-b814-4243-be14-eba1df340ceb"
        publisher: jobs.lever.co
        claim: "Posting JD text for Senior Software Engineer - Observability, used for role.system_scale/role.level/role.nature judgement."
        snapshot_ref: "evidence/openings/lever_palantir_8a95dba1-b814-4243-be14-eba1df340ceb/posting.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success
      - id: ev-8a95-salary
        source_url: "https://jobs.lever.co/palantir/8a95dba1-b814-4243-be14-eba1df340ceb"
        publisher: jobs.lever.co
        claim: "Posting's additional/benefits text states 'estimated salary range for this position is estimated to be $135,000 - $200,000/year' (USD, base)."
        snapshot_ref: "evidence/openings/lever_palantir_8a95dba1-b814-4243-be14-eba1df340ceb/posting.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success

  - opening_id: "lever:palantir:39c57909-ae76-4c86-9290-9fb50c689c4f"
    id_source: provider_native
    company_id: palantir
    provider: lever
    board: palantir
    title: "Senior Software Engineer, Network Infrastructure"
    job_url: "https://jobs.lever.co/palantir/39c57909-ae76-4c86-9290-9fb50c689c4f"
    apply_url: "https://jobs.lever.co/palantir/39c57909-ae76-4c86-9290-9fb50c689c4f/apply"
    applicability:
      - field_id: role.system_scale
        state: applicable
      - field_id: role.level
        state: applicable
      - field_id: role.nature
        state: applicable
    field_results:
      - field_id: role.system_scale
        result: pass
        evidence_refs: [ev-39c5-jd]
        note: "JD states the team owns 'north-south and east-west traffic flows across 100s of zero-trust K8s clusters' and 'dynamic control over ephemeral infrastructure (10s of thousands of firewall rules targeting 1000s of short-lived pods)', explicitly framed as 'the intersection of scale, usability and security' -- concrete high-throughput/high-concurrency infrastructure figures matching observable_criteria."
      - field_id: role.level
        result: unknown
        evidence_refs: [ev-39c5-jd]
        note: "Title says Senior; JD text describes team-level ownership ('the Network Infrastructure team owns...') but no individual decision-authority scope for the role itself."
      - field_id: role.nature
        result: pass
        evidence_refs: [ev-39c5-jd]
        note: "JD describes hands-on engineering work on the networking stack; no management/performance-review/hiring language."
    soft_results:
      - field_id: location.city_profile
        result: meets
        evidence_refs: [ev-39c5-jd]
        note: "Seattle is listed verbatim as an example city in location.city_profile (source_ref I-006)."
      - field_id: location.relocation_ease
        result: tradeoff
        evidence_refs: [ev-39c5-jd]
        note: "Direction's own example (I-006) names Seattle explicitly as visa-hassle/not-proactively-considered but not an absolute exclusion."
      - field_id: compensation.base
        result: unknown
        evidence_refs: [ev-39c5-salary]
        note: "Posting states estimated USD base salary $135,000-$200,000/year. Currency mismatch against SGD/PPP-anchored benchmark leaves this unknown."
    match_status: needs_verification
    match_reason: "role.system_scale and role.nature pass; role.level is unknown; no field fails."
    opening_status: published_present
    freshness_status: current
    last_successful_check_at: "2026-09-24T00:54:19+00:00"
    needs_recheck: false
    user_decision: undecided
    evidence:
      - id: ev-board-link
        source_url: "https://www.palantir.com/careers/"
        publisher: palantir.com
        claim: "Palantir's own careers page leads to jobs.lever.co/palantir as the official ATS board (confirmed via company site + board content match on 2026-09-24)."
        checked_at: "2026-09-24T01:10:00+00:00"
        retrieval_status: success
      - id: ev-board-fetch
        source_url: "https://api.lever.co/v0/postings/palantir?mode=json&limit=100&skip=0"
        publisher: jobs.lever.co
        claim: "Full paginated read of the palantir Lever board: 4/4 pages succeeded, 318 postings seen and written."
        snapshot_ref: "evidence/boards/lever/palantir/20260924T005419.605115Z-077199/observation.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success
        coverage: "4 pages requested, 4 pages ok, pagination complete"
      - id: ev-39c5-jd
        source_url: "https://jobs.lever.co/palantir/39c57909-ae76-4c86-9290-9fb50c689c4f"
        publisher: jobs.lever.co
        claim: "Posting JD text (Seattle) for Senior Software Engineer, Network Infrastructure, used for role.system_scale/role.level/role.nature judgement."
        snapshot_ref: "evidence/openings/lever_palantir_39c57909-ae76-4c86-9290-9fb50c689c4f/posting.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success
      - id: ev-39c5-salary
        source_url: "https://jobs.lever.co/palantir/39c57909-ae76-4c86-9290-9fb50c689c4f"
        publisher: jobs.lever.co
        claim: "Posting's additional/benefits text states 'estimated salary range for this position is estimated to be $135,000 - $200,000/year' (USD, base)."
        snapshot_ref: "evidence/openings/lever_palantir_39c57909-ae76-4c86-9290-9fb50c689c4f/posting.json"
        checked_at: "2026-09-24T00:54:19+00:00"
        retrieval_status: success
---

# Palantir (Lever) — dir-001 大规模系统基础设施 · Senior/Staff IC

Board: `jobs.lever.co/palantir`（从 palantir.com/careers 官方链接确认）。全量抓取 318 个在招岗位（4/4 分页成功，check-id `20260924T005419.605115Z-077199`）。按 dir-001 的关键词/排除词打分后，取分数最高的 8 个进入 shortlist（预算上限）；这 8 个并列最高分（score=6，均为 "Senior Software Engineer ..." 标题），按脚本原始排序取前 6 个实际判分（预算：只判分 6 个）。未判分的另外 2 个（Network Infrastructure · Washington D.C. / New York）与其余 310 个岗位仅完成排序扫描，未逐条判定 hard fields。

## needs_verification（6 个，全部）

以下 6 个均因至少一个 applicable hard field 为 unknown 而落入 needs_verification；没有任何 hard field 被判 fail。

- **Senior Software Engineer - Autonomous Systems** · Palo Alto, CA — [posting](https://jobs.lever.co/palantir/d7030550-f80f-422c-965f-3120db433dea)
  role.system_scale=unknown, role.level=unknown, role.nature=pass。JD 讲的是无人系统的指挥控制/传感器融合/实时决策，没有海量流量、PB级数据或数亿用户的量化描述；title 写 Senior 但正文未描述独立架构决策权。base USD $145k–$200k/年（币种不在 SGD/PPP 基准范围内，comp 未知）。

- **Senior Software Engineer - Autonomous Systems** · Seattle, WA — [posting](https://jobs.lever.co/palantir/88f8f593-af1f-4d27-9042-454c24a64d3f)
  同上判定。城市氛围 meets（Seattle 是方向文件 I-006 中明确列出的示例城市），但 relocation_ease=tradeoff（I-006 同样明确指出 Seattle 签证麻烦、不主动考虑但非绝对排除）。

- **Senior Software Engineer - Autonomous Systems** · Washington, D.C. — [posting](https://jobs.lever.co/palantir/d40d5d19-8f9e-4e6b-b4d3-b7457c90adec)
  同上判定；D.C. 不在方向示例城市中，city_profile unknown；relocation_ease 按美国同一签证体系从 Seattle 推断为 tradeoff（中等置信度，已注明推断依据）。

- **Senior Software Engineer - Autonomous Systems** · New York, NY — [posting](https://jobs.lever.co/palantir/bba1ecbc-e56d-48b0-b33a-aefcbffbd655)
  同上判定，同 D.C. 的城市/签证处理方式。

- **Senior Software Engineer - Observability** · New York, NY — [posting](https://jobs.lever.co/palantir/8a95dba1-b814-4243-be14-eba1df340ceb)
  role.level=**pass**（JD 明确写"you will be directly responsible for Palantir's observability platform"，属于对系统的独立负责，满足 role.level 的正面 observable_criteria）；role.nature=pass；role.system_scale=unknown（提到"scale our engineering efforts"但无具体吞吐/数据量数字）。base USD $135k–$200k/年（comp 未知，币种不符）。

- **Senior Software Engineer, Network Infrastructure** · Seattle, WA — [posting](https://jobs.lever.co/palantir/39c57909-ae76-4c86-9290-9fb50c689c4f)
  role.system_scale=**pass**（JD 给出具体量级："100s of zero-trust K8s clusters"、"10s of thousands of firewall rules targeting 1000s of short-lived pods"，并明确框定为"the intersection of scale, usability and security"，满足海量流量/高并发的观测标准）；role.nature=pass；role.level=unknown（JD 只说团队拥有该技术栈，未描述个人决策权范围）。城市氛围 meets（Seattle），relocation_ease=tradeoff（同 I-006）。

## eligible_for_comparison（0 个）

无。6 个候选均至少有一个 hard field 为 unknown，没有一个同时通过全部三项 hard field（role.system_scale、role.level、role.nature）。

## rejected（0 个）

无。本次判分的 6 个岗位没有任何 applicable hard field 被判定为 fail（即没有证据表明其系统规模明显偏中小型，或明确是 mid-level/ticket-driven，或存在正式管理职责）。

## needs_clarification（0 个）

无。role.system_scale、role.level、role.nature 均为 confirmed hard field 且在这些岗位上都 applicable（无 scope 排除、无未确认字段），因此不会仅因"未确认"而卡在这一档；本轮的不确定性全部来自 JD 文本信息不足，体现为 needs_verification 而非 needs_clarification。

## 实习与校招岗位的去向

方向文件的 `search_hints.deprioritize` 明确包含 `intern` / `internship` / `new grad` / `实习` / `应届` 等词。shortlist.py 按此把所有实习/校招岗位（如 "Year at Palantir - Software Engineer, Internship"、"Forward Deployed Software Engineer, New Grad - Commercial/USG/UK Government" 等，score 为负数）排入 `pushed_down`（降权列表），**没有进入 shortlist 前 8，因此本轮完全没有被逐条判分**，也就不会出现在上面任何一组结果里。这不是因为它们的 hard field 判定失败——它们根本没有被判定；deprioritize 只影响发现阶段的排序，不构成拒绝理由（这是 evidence-rules 明确要求的：搜索降权词不能作为字段 fail 的依据）。如果你确实想看实习/校招岗位的判定结果（例如给认识的应届生参考），需要单独跑一次 shortlist 或直接指定这些 opening_id 进行判分。
