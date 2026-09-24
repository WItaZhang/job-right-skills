---
direction_id: dir-001
direction_revision: 5
basis: confirmed
generated_at: '2026-09-24T00:18:36+00:00'
search_bias:
- 应用层
- 产品向
- 模型研究/科学家岗位
- 管理岗/People Manager
- product manager
- forward deployed
- sales
- solutions engineer
- manager
- director
- research scientist
candidates:
- opening_id: lever:palantir:b229baac-494b-4a0d-9a13-2e38806e06f3
  id_source: provider_native
  company_id: palantir
  provider: lever
  board: palantir
  title: Software Engineer, Internship - Infrastructure
  job_url: https://jobs.lever.co/palantir/b229baac-494b-4a0d-9a13-2e38806e06f3
  apply_url: https://jobs.lever.co/palantir/b229baac-494b-4a0d-9a13-2e38806e06f3/apply
  applicability:
  - field_id: role.domain
    state: applicable
  - field_id: role.people_management
    state: applicable
  field_results:
  - field_id: role.domain
    result: pass
    evidence_refs:
    - c1-domain
  - field_id: role.people_management
    result: unknown
    evidence_refs:
    - c1-peoplemgmt
    note: No pass/fail without text; a generic IC-sounding title is an impression, not evidence.
  soft_results:
  - field_id: location.city_profile
    result: meets
    note: New York, NY is a well-known dense tech hub with an active meetup/community scene. This is general public knowledge about the city, not derived from the JD text itself — medium confidence, not a JD-cited claim.
  - field_id: role.requirement_stability
    result: unknown
    evidence_refs:
    - c1-reqstab
  - field_id: location.workplace_type
    result: meets
    evidence_refs:
    - c1-workplace
    note: workplace_type is onsite/hybrid, i.e. in-office presence is available, which satisfies the user's stated preference (relocating + office access is the goal; full remote was only stated as acceptable, not required).
  match_status: needs_verification
  match_reason: role.domain passes on the JD's explicit systems/performance/scale description; role.people_management is unknown because the JD never states whether the role carries reports, performance-review, or hiring duties — needs verification (e.g. in a recruiter/hiring-manager call) before this can be treated as a confirmed pure-IC role.
  opening_status: published_present
  freshness_status: current
  last_successful_check_at: '2026-09-24T00:13:55+00:00'
  user_decision: undecided
  evidence:
  - id: c1-board
    source_url: https://www.palantir.com/careers/
    publisher: palantir.com
    claim: Palantir official careers page (palantir.com/careers) links to https://jobs.lever.co/palantir/... confirming the official ATS board is Lever, site token palantir
    snapshot_ref: evidence/companies/palantir/careers-page.html
    checked_at: '2026-09-24T00:13:47+00:00'
    retrieval_status: success
  - id: c1-listing
    source_url: https://jobs.lever.co/palantir/b229baac-494b-4a0d-9a13-2e38806e06f3
    publisher: jobs.lever.co
    claim: Opening lever:palantir:b229baac-494b-4a0d-9a13-2e38806e06f3 was returned by Palantir's Lever Postings API at checked_at (retrieval_status=success, board check under evidence/boards/lever/palantir/); proves the posting was published at that time, not that headcount or hiring-manager budget still exist.
    snapshot_ref: evidence/openings/lever_palantir_b229baac-494b-4a0d-9a13-2e38806e06f3/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c1-domain
    source_url: https://jobs.lever.co/palantir/b229baac-494b-4a0d-9a13-2e38806e06f3
    publisher: jobs.lever.co
    claim: 'JD text says: “Teams within Palantir’s Foundations organization are made up of a small number of engineers, each focused on one of four major categories of our infrastructure: Backend Infrastructure ... Developer Infrastructure ... Frontend Infrastructure ... Storage Infrastructure: Develops Palantir’s database and search systems, which includes supporting storage technologies across cloud, on-premise, and classified or secure environments. This includes evolving our existing technologies to support ever-increasing data scale and latency requirements, and designing the next evolution of our database offering to provide step-change improvements in particular workflows.” — describes systems/performance/scale infrastructure work, not model research or product/application-layer feature work.'
    snapshot_ref: evidence/openings/lever_palantir_b229baac-494b-4a0d-9a13-2e38806e06f3/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c1-peoplemgmt
    source_url: https://jobs.lever.co/palantir/b229baac-494b-4a0d-9a13-2e38806e06f3
    publisher: jobs.lever.co
    claim: Full JD text for this opening was read in its entirety and contains no language about managing a team, having direct reports, conducting performance reviews, or making hiring decisions for this role.
    snapshot_ref: evidence/openings/lever_palantir_b229baac-494b-4a0d-9a13-2e38806e06f3/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c1-workplace
    source_url: https://jobs.lever.co/palantir/b229baac-494b-4a0d-9a13-2e38806e06f3
    publisher: jobs.lever.co
    claim: Lever posting's structured workplaceType field is “onsite” for location New York, NY.
    snapshot_ref: evidence/openings/lever_palantir_b229baac-494b-4a0d-9a13-2e38806e06f3/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c1-reqstab
    source_url: https://jobs.lever.co/palantir/b229baac-494b-4a0d-9a13-2e38806e06f3
    publisher: jobs.lever.co
    claim: 'JD text says: “You''ll collaborate closely with technical and non-technical counterparts to understand our developers'' and customers'' problems and build infrastructure to tackle them.” — mentions both internal “developers’” and “customers’” problems without clarifying whether “customers” means external business stakeholders (would cut against requirement stability) or internal platform users; not specific enough to call meets or tradeoff.'
    snapshot_ref: evidence/openings/lever_palantir_b229baac-494b-4a0d-9a13-2e38806e06f3/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
- opening_id: lever:palantir:f221738b-e97c-4ce3-a12a-17ada2b855e4
  id_source: provider_native
  company_id: palantir
  provider: lever
  board: palantir
  title: Software Engineer, Internship - Infrastructure
  job_url: https://jobs.lever.co/palantir/f221738b-e97c-4ce3-a12a-17ada2b855e4
  apply_url: https://jobs.lever.co/palantir/f221738b-e97c-4ce3-a12a-17ada2b855e4/apply
  applicability:
  - field_id: role.domain
    state: applicable
  - field_id: role.people_management
    state: applicable
  field_results:
  - field_id: role.domain
    result: pass
    evidence_refs:
    - c2-domain
  - field_id: role.people_management
    result: unknown
    evidence_refs:
    - c2-peoplemgmt
    note: No pass/fail without text; a generic IC-sounding title is an impression, not evidence.
  soft_results:
  - field_id: location.city_profile
    result: meets
    note: Palo Alto, CA is a well-known dense tech hub with an active meetup/community scene. This is general public knowledge about the city, not derived from the JD text itself — medium confidence, not a JD-cited claim.
  - field_id: role.requirement_stability
    result: unknown
    evidence_refs:
    - c2-reqstab
  - field_id: location.workplace_type
    result: meets
    evidence_refs:
    - c2-workplace
    note: workplace_type is onsite/hybrid, i.e. in-office presence is available, which satisfies the user's stated preference (relocating + office access is the goal; full remote was only stated as acceptable, not required).
  match_status: needs_verification
  match_reason: role.domain passes on the JD's explicit systems/performance/scale description; role.people_management is unknown because the JD never states whether the role carries reports, performance-review, or hiring duties — needs verification (e.g. in a recruiter/hiring-manager call) before this can be treated as a confirmed pure-IC role.
  opening_status: published_present
  freshness_status: current
  last_successful_check_at: '2026-09-24T00:13:55+00:00'
  user_decision: undecided
  evidence:
  - id: c2-board
    source_url: https://www.palantir.com/careers/
    publisher: palantir.com
    claim: Palantir official careers page (palantir.com/careers) links to https://jobs.lever.co/palantir/... confirming the official ATS board is Lever, site token palantir
    snapshot_ref: evidence/companies/palantir/careers-page.html
    checked_at: '2026-09-24T00:13:47+00:00'
    retrieval_status: success
  - id: c2-listing
    source_url: https://jobs.lever.co/palantir/f221738b-e97c-4ce3-a12a-17ada2b855e4
    publisher: jobs.lever.co
    claim: Opening lever:palantir:f221738b-e97c-4ce3-a12a-17ada2b855e4 was returned by Palantir's Lever Postings API at checked_at (retrieval_status=success, board check under evidence/boards/lever/palantir/); proves the posting was published at that time, not that headcount or hiring-manager budget still exist.
    snapshot_ref: evidence/openings/lever_palantir_f221738b-e97c-4ce3-a12a-17ada2b855e4/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c2-domain
    source_url: https://jobs.lever.co/palantir/f221738b-e97c-4ce3-a12a-17ada2b855e4
    publisher: jobs.lever.co
    claim: 'JD text says: “Teams within Palantir’s Foundations organization are made up of a small number of engineers, each focused on one of four major categories of our infrastructure: Backend Infrastructure ... Developer Infrastructure ... Frontend Infrastructure ... Storage Infrastructure: Develops Palantir’s database and search systems, which includes supporting storage technologies across cloud, on-premise, and classified or secure environments. This includes evolving our existing technologies to support ever-increasing data scale and latency requirements, and designing the next evolution of our database offering to provide step-change improvements in particular workflows.” — describes systems/performance/scale infrastructure work, not model research or product/application-layer feature work.'
    snapshot_ref: evidence/openings/lever_palantir_f221738b-e97c-4ce3-a12a-17ada2b855e4/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c2-peoplemgmt
    source_url: https://jobs.lever.co/palantir/f221738b-e97c-4ce3-a12a-17ada2b855e4
    publisher: jobs.lever.co
    claim: Full JD text for this opening was read in its entirety and contains no language about managing a team, having direct reports, conducting performance reviews, or making hiring decisions for this role.
    snapshot_ref: evidence/openings/lever_palantir_f221738b-e97c-4ce3-a12a-17ada2b855e4/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c2-workplace
    source_url: https://jobs.lever.co/palantir/f221738b-e97c-4ce3-a12a-17ada2b855e4
    publisher: jobs.lever.co
    claim: Lever posting's structured workplaceType field is “onsite” for location Palo Alto, CA.
    snapshot_ref: evidence/openings/lever_palantir_f221738b-e97c-4ce3-a12a-17ada2b855e4/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c2-reqstab
    source_url: https://jobs.lever.co/palantir/f221738b-e97c-4ce3-a12a-17ada2b855e4
    publisher: jobs.lever.co
    claim: 'JD text says: “You''ll collaborate closely with technical and non-technical counterparts to understand our developers'' and customers'' problems and build infrastructure to tackle them.” — mentions both internal “developers’” and “customers’” problems without clarifying whether “customers” means external business stakeholders (would cut against requirement stability) or internal platform users; not specific enough to call meets or tradeoff.'
    snapshot_ref: evidence/openings/lever_palantir_f221738b-e97c-4ce3-a12a-17ada2b855e4/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
- opening_id: lever:palantir:4abf26b4-795c-420a-bf22-1ab98db268b4
  id_source: provider_native
  company_id: palantir
  provider: lever
  board: palantir
  title: Software Engineer, New Grad - Infrastructure
  job_url: https://jobs.lever.co/palantir/4abf26b4-795c-420a-bf22-1ab98db268b4
  apply_url: https://jobs.lever.co/palantir/4abf26b4-795c-420a-bf22-1ab98db268b4/apply
  applicability:
  - field_id: role.domain
    state: applicable
  - field_id: role.people_management
    state: applicable
  field_results:
  - field_id: role.domain
    result: pass
    evidence_refs:
    - c3-domain
  - field_id: role.people_management
    result: unknown
    evidence_refs:
    - c3-peoplemgmt
    note: No pass/fail without text; a generic IC-sounding title is an impression, not evidence.
  soft_results:
  - field_id: location.city_profile
    result: meets
    note: New York, NY is a well-known dense tech hub with an active meetup/community scene. This is general public knowledge about the city, not derived from the JD text itself — medium confidence, not a JD-cited claim.
  - field_id: role.requirement_stability
    result: unknown
    evidence_refs:
    - c3-reqstab
  - field_id: location.workplace_type
    result: meets
    evidence_refs:
    - c3-workplace
    note: workplace_type is onsite/hybrid, i.e. in-office presence is available, which satisfies the user's stated preference (relocating + office access is the goal; full remote was only stated as acceptable, not required).
  match_status: needs_verification
  match_reason: role.domain passes on the JD's explicit systems/performance/scale description; role.people_management is unknown because the JD never states whether the role carries reports, performance-review, or hiring duties — needs verification (e.g. in a recruiter/hiring-manager call) before this can be treated as a confirmed pure-IC role.
  opening_status: published_present
  freshness_status: current
  last_successful_check_at: '2026-09-24T00:13:55+00:00'
  user_decision: undecided
  evidence:
  - id: c3-board
    source_url: https://www.palantir.com/careers/
    publisher: palantir.com
    claim: Palantir official careers page (palantir.com/careers) links to https://jobs.lever.co/palantir/... confirming the official ATS board is Lever, site token palantir
    snapshot_ref: evidence/companies/palantir/careers-page.html
    checked_at: '2026-09-24T00:13:47+00:00'
    retrieval_status: success
  - id: c3-listing
    source_url: https://jobs.lever.co/palantir/4abf26b4-795c-420a-bf22-1ab98db268b4
    publisher: jobs.lever.co
    claim: Opening lever:palantir:4abf26b4-795c-420a-bf22-1ab98db268b4 was returned by Palantir's Lever Postings API at checked_at (retrieval_status=success, board check under evidence/boards/lever/palantir/); proves the posting was published at that time, not that headcount or hiring-manager budget still exist.
    snapshot_ref: evidence/openings/lever_palantir_4abf26b4-795c-420a-bf22-1ab98db268b4/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c3-domain
    source_url: https://jobs.lever.co/palantir/4abf26b4-795c-420a-bf22-1ab98db268b4
    publisher: jobs.lever.co
    claim: 'JD text says: “Teams within Palantir’s Foundations organization are made up of a small number of engineers, each focused on one of four major categories of our infrastructure: Backend Infrastructure ... Developer Infrastructure ... Frontend Infrastructure ... Storage Infrastructure: Develops Palantir’s database and search systems, which includes supporting storage technologies across cloud, on-premise, and classified or secure environments. This includes evolving our existing technologies to support ever-increasing data scale and latency requirements, and designing the next evolution of our database offering to provide step-change improvements in particular workflows.” — describes systems/performance/scale infrastructure work, not model research or product/application-layer feature work.'
    snapshot_ref: evidence/openings/lever_palantir_4abf26b4-795c-420a-bf22-1ab98db268b4/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c3-peoplemgmt
    source_url: https://jobs.lever.co/palantir/4abf26b4-795c-420a-bf22-1ab98db268b4
    publisher: jobs.lever.co
    claim: Full JD text for this opening was read in its entirety and contains no language about managing a team, having direct reports, conducting performance reviews, or making hiring decisions for this role.
    snapshot_ref: evidence/openings/lever_palantir_4abf26b4-795c-420a-bf22-1ab98db268b4/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c3-workplace
    source_url: https://jobs.lever.co/palantir/4abf26b4-795c-420a-bf22-1ab98db268b4
    publisher: jobs.lever.co
    claim: Lever posting's structured workplaceType field is “hybrid” for location New York, NY.
    snapshot_ref: evidence/openings/lever_palantir_4abf26b4-795c-420a-bf22-1ab98db268b4/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c3-reqstab
    source_url: https://jobs.lever.co/palantir/4abf26b4-795c-420a-bf22-1ab98db268b4
    publisher: jobs.lever.co
    claim: 'JD text says: “You''ll collaborate closely with technical and non-technical counterparts to understand our developers'' and customers'' problems and build infrastructure to tackle them.” — mentions both internal “developers’” and “customers’” problems without clarifying whether “customers” means external business stakeholders (would cut against requirement stability) or internal platform users; not specific enough to call meets or tradeoff.'
    snapshot_ref: evidence/openings/lever_palantir_4abf26b4-795c-420a-bf22-1ab98db268b4/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
- opening_id: lever:palantir:7d75bed5-45d8-4876-840a-2d92ea79c98d
  id_source: provider_native
  company_id: palantir
  provider: lever
  board: palantir
  title: Software Engineer, New Grad - Infrastructure
  job_url: https://jobs.lever.co/palantir/7d75bed5-45d8-4876-840a-2d92ea79c98d
  apply_url: https://jobs.lever.co/palantir/7d75bed5-45d8-4876-840a-2d92ea79c98d/apply
  applicability:
  - field_id: role.domain
    state: applicable
  - field_id: role.people_management
    state: applicable
  field_results:
  - field_id: role.domain
    result: pass
    evidence_refs:
    - c4-domain
  - field_id: role.people_management
    result: unknown
    evidence_refs:
    - c4-peoplemgmt
    note: No pass/fail without text; a generic IC-sounding title is an impression, not evidence.
  soft_results:
  - field_id: location.city_profile
    result: meets
    note: Palo Alto, CA is a well-known dense tech hub with an active meetup/community scene. This is general public knowledge about the city, not derived from the JD text itself — medium confidence, not a JD-cited claim.
  - field_id: role.requirement_stability
    result: unknown
    evidence_refs:
    - c4-reqstab
  - field_id: location.workplace_type
    result: meets
    evidence_refs:
    - c4-workplace
    note: workplace_type is onsite/hybrid, i.e. in-office presence is available, which satisfies the user's stated preference (relocating + office access is the goal; full remote was only stated as acceptable, not required).
  match_status: needs_verification
  match_reason: role.domain passes on the JD's explicit systems/performance/scale description; role.people_management is unknown because the JD never states whether the role carries reports, performance-review, or hiring duties — needs verification (e.g. in a recruiter/hiring-manager call) before this can be treated as a confirmed pure-IC role.
  opening_status: published_present
  freshness_status: current
  last_successful_check_at: '2026-09-24T00:13:55+00:00'
  user_decision: undecided
  evidence:
  - id: c4-board
    source_url: https://www.palantir.com/careers/
    publisher: palantir.com
    claim: Palantir official careers page (palantir.com/careers) links to https://jobs.lever.co/palantir/... confirming the official ATS board is Lever, site token palantir
    snapshot_ref: evidence/companies/palantir/careers-page.html
    checked_at: '2026-09-24T00:13:47+00:00'
    retrieval_status: success
  - id: c4-listing
    source_url: https://jobs.lever.co/palantir/7d75bed5-45d8-4876-840a-2d92ea79c98d
    publisher: jobs.lever.co
    claim: Opening lever:palantir:7d75bed5-45d8-4876-840a-2d92ea79c98d was returned by Palantir's Lever Postings API at checked_at (retrieval_status=success, board check under evidence/boards/lever/palantir/); proves the posting was published at that time, not that headcount or hiring-manager budget still exist.
    snapshot_ref: evidence/openings/lever_palantir_7d75bed5-45d8-4876-840a-2d92ea79c98d/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c4-domain
    source_url: https://jobs.lever.co/palantir/7d75bed5-45d8-4876-840a-2d92ea79c98d
    publisher: jobs.lever.co
    claim: 'JD text says: “Teams within Palantir’s Foundations organization are made up of a small number of engineers, each focused on one of four major categories of our infrastructure: Backend Infrastructure ... Developer Infrastructure ... Frontend Infrastructure ... Storage Infrastructure: Develops Palantir’s database and search systems, which includes supporting storage technologies across cloud, on-premise, and classified or secure environments. This includes evolving our existing technologies to support ever-increasing data scale and latency requirements, and designing the next evolution of our database offering to provide step-change improvements in particular workflows.” — describes systems/performance/scale infrastructure work, not model research or product/application-layer feature work.'
    snapshot_ref: evidence/openings/lever_palantir_7d75bed5-45d8-4876-840a-2d92ea79c98d/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c4-peoplemgmt
    source_url: https://jobs.lever.co/palantir/7d75bed5-45d8-4876-840a-2d92ea79c98d
    publisher: jobs.lever.co
    claim: Full JD text for this opening was read in its entirety and contains no language about managing a team, having direct reports, conducting performance reviews, or making hiring decisions for this role.
    snapshot_ref: evidence/openings/lever_palantir_7d75bed5-45d8-4876-840a-2d92ea79c98d/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c4-workplace
    source_url: https://jobs.lever.co/palantir/7d75bed5-45d8-4876-840a-2d92ea79c98d
    publisher: jobs.lever.co
    claim: Lever posting's structured workplaceType field is “hybrid” for location Palo Alto, CA.
    snapshot_ref: evidence/openings/lever_palantir_7d75bed5-45d8-4876-840a-2d92ea79c98d/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c4-reqstab
    source_url: https://jobs.lever.co/palantir/7d75bed5-45d8-4876-840a-2d92ea79c98d
    publisher: jobs.lever.co
    claim: 'JD text says: “You''ll collaborate closely with technical and non-technical counterparts to understand our developers'' and customers'' problems and build infrastructure to tackle them.” — mentions both internal “developers’” and “customers’” problems without clarifying whether “customers” means external business stakeholders (would cut against requirement stability) or internal platform users; not specific enough to call meets or tradeoff.'
    snapshot_ref: evidence/openings/lever_palantir_7d75bed5-45d8-4876-840a-2d92ea79c98d/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
- opening_id: lever:palantir:6fe5515f-f677-4d98-8ac2-1775a425f5e7
  id_source: provider_native
  company_id: palantir
  provider: lever
  board: palantir
  title: Backend Software Engineer - Infrastructure
  job_url: https://jobs.lever.co/palantir/6fe5515f-f677-4d98-8ac2-1775a425f5e7
  apply_url: https://jobs.lever.co/palantir/6fe5515f-f677-4d98-8ac2-1775a425f5e7/apply
  applicability:
  - field_id: role.domain
    state: applicable
  - field_id: role.people_management
    state: applicable
  field_results:
  - field_id: role.domain
    result: pass
    evidence_refs:
    - c5-domain
    note: Core described responsibilities (lowest layers of the stack, database/distributed systems, scalable building blocks) support a pass. The optional Frontline customer-embedding program mentioned in the same JD is flagged separately under role.requirement_stability (soft), not treated as a role.domain fail, since it is presented as an elective opportunity rather than the role's default work.
  - field_id: role.people_management
    result: unknown
    evidence_refs:
    - c5-peoplemgmt
    note: No pass/fail without text; a generic IC-sounding title is an impression, not evidence.
  soft_results:
  - field_id: location.city_profile
    result: meets
    note: New York, NY is a well-known dense tech hub with an active meetup/community scene. This is general public knowledge about the city, not derived from the JD text itself — medium confidence, not a JD-cited claim.
  - field_id: role.requirement_stability
    result: tradeoff
    evidence_refs:
    - c5-frontline
  - field_id: location.workplace_type
    result: meets
    evidence_refs:
    - c5-workplace
    note: workplace_type is onsite/hybrid, i.e. in-office presence is available, which satisfies the user's stated preference (relocating + office access is the goal; full remote was only stated as acceptable, not required).
  match_status: needs_verification
  match_reason: role.domain passes on the JD's explicit systems/performance/scale description; role.people_management is unknown because the JD never states whether the role carries reports, performance-review, or hiring duties — needs verification (e.g. in a recruiter/hiring-manager call) before this can be treated as a confirmed pure-IC role. The JD also describes an optional customer-embedding ‘Frontline’ program; flagged under role.requirement_stability as a tradeoff rather than used to fail role.domain.
  opening_status: published_present
  freshness_status: current
  last_successful_check_at: '2026-09-24T00:13:55+00:00'
  user_decision: undecided
  evidence:
  - id: c5-board
    source_url: https://www.palantir.com/careers/
    publisher: palantir.com
    claim: Palantir official careers page (palantir.com/careers) links to https://jobs.lever.co/palantir/... confirming the official ATS board is Lever, site token palantir
    snapshot_ref: evidence/companies/palantir/careers-page.html
    checked_at: '2026-09-24T00:13:47+00:00'
    retrieval_status: success
  - id: c5-listing
    source_url: https://jobs.lever.co/palantir/6fe5515f-f677-4d98-8ac2-1775a425f5e7
    publisher: jobs.lever.co
    claim: Opening lever:palantir:6fe5515f-f677-4d98-8ac2-1775a425f5e7 was returned by Palantir's Lever Postings API at checked_at (retrieval_status=success, board check under evidence/boards/lever/palantir/); proves the posting was published at that time, not that headcount or hiring-manager budget still exist.
    snapshot_ref: evidence/openings/lever_palantir_6fe5515f-f677-4d98-8ac2-1775a425f5e7/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c5-domain
    source_url: https://jobs.lever.co/palantir/6fe5515f-f677-4d98-8ac2-1775a425f5e7
    publisher: jobs.lever.co
    claim: 'JD text says: “Our infrastructure teams are responsible for the lowest layers of our software stack, often focused on database technologies, distributed systems, large scale data systems, security, and application infrastructure. As a Software Engineer on infrastructure ... you''ll contribute high-quality code to underpin Palantir Foundry and Gotham with performant, secure, and scalable building blocks.” — describes systems/performance/scale infrastructure work, not model research or product/application-layer feature work.'
    snapshot_ref: evidence/openings/lever_palantir_6fe5515f-f677-4d98-8ac2-1775a425f5e7/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c5-peoplemgmt
    source_url: https://jobs.lever.co/palantir/6fe5515f-f677-4d98-8ac2-1775a425f5e7
    publisher: jobs.lever.co
    claim: Full JD text for this opening was read in its entirety and contains no language about managing a team, having direct reports, conducting performance reviews, or making hiring decisions for this role.
    snapshot_ref: evidence/openings/lever_palantir_6fe5515f-f677-4d98-8ac2-1775a425f5e7/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c5-workplace
    source_url: https://jobs.lever.co/palantir/6fe5515f-f677-4d98-8ac2-1775a425f5e7
    publisher: jobs.lever.co
    claim: Lever posting's structured workplaceType field is “hybrid” for location New York, NY.
    snapshot_ref: evidence/openings/lever_palantir_6fe5515f-f677-4d98-8ac2-1775a425f5e7/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c5-frontline
    source_url: https://jobs.lever.co/palantir/6fe5515f-f677-4d98-8ac2-1775a425f5e7
    publisher: jobs.lever.co
    claim: 'JD text says: “Foundry Software Engineers may be offered the opportunity to Frontline, an exclusive program unlike any other. This unique, short-term assignment involves being embedded with customers ... By witnessing how customers engage with Foundry and experiencing these pain points firsthand, you’ll gain unique insights that feed directly back into our development process, helping to refine and enhance our products.” — an optional, short-term customer-embedding program offered to Foundry engineers generally; not described as this role''s default day-to-day work, but does introduce the kind of customer/business-alignment exposure the direction''s role.requirement_stability preference wants to avoid.'
    snapshot_ref: evidence/openings/lever_palantir_6fe5515f-f677-4d98-8ac2-1775a425f5e7/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
- opening_id: lever:palantir:f70cdff7-c62f-4b73-a136-909e5e3d1891
  id_source: provider_native
  company_id: palantir
  provider: lever
  board: palantir
  title: Backend Software Engineer - Infrastructure
  job_url: https://jobs.lever.co/palantir/f70cdff7-c62f-4b73-a136-909e5e3d1891
  apply_url: https://jobs.lever.co/palantir/f70cdff7-c62f-4b73-a136-909e5e3d1891/apply
  applicability:
  - field_id: role.domain
    state: applicable
  - field_id: role.people_management
    state: applicable
  field_results:
  - field_id: role.domain
    result: pass
    evidence_refs:
    - c6-domain
    note: Core described responsibilities (lowest layers of the stack, database/distributed systems, scalable building blocks) support a pass. The optional Frontline customer-embedding program mentioned in the same JD is flagged separately under role.requirement_stability (soft), not treated as a role.domain fail, since it is presented as an elective opportunity rather than the role's default work.
  - field_id: role.people_management
    result: unknown
    evidence_refs:
    - c6-peoplemgmt
    note: No pass/fail without text; a generic IC-sounding title is an impression, not evidence.
  soft_results:
  - field_id: location.city_profile
    result: meets
    note: London, United Kingdom is a well-known dense tech hub with an active meetup/community scene. This is general public knowledge about the city, not derived from the JD text itself — medium confidence, not a JD-cited claim.
  - field_id: role.requirement_stability
    result: tradeoff
    evidence_refs:
    - c6-frontline
  - field_id: location.workplace_type
    result: meets
    evidence_refs:
    - c6-workplace
    note: workplace_type is onsite/hybrid, i.e. in-office presence is available, which satisfies the user's stated preference (relocating + office access is the goal; full remote was only stated as acceptable, not required).
  match_status: needs_verification
  match_reason: role.domain passes on the JD's explicit systems/performance/scale description; role.people_management is unknown because the JD never states whether the role carries reports, performance-review, or hiring duties — needs verification (e.g. in a recruiter/hiring-manager call) before this can be treated as a confirmed pure-IC role. The JD also describes an optional customer-embedding ‘Frontline’ program; flagged under role.requirement_stability as a tradeoff rather than used to fail role.domain.
  opening_status: published_present
  freshness_status: current
  last_successful_check_at: '2026-09-24T00:13:55+00:00'
  user_decision: undecided
  evidence:
  - id: c6-board
    source_url: https://www.palantir.com/careers/
    publisher: palantir.com
    claim: Palantir official careers page (palantir.com/careers) links to https://jobs.lever.co/palantir/... confirming the official ATS board is Lever, site token palantir
    snapshot_ref: evidence/companies/palantir/careers-page.html
    checked_at: '2026-09-24T00:13:47+00:00'
    retrieval_status: success
  - id: c6-listing
    source_url: https://jobs.lever.co/palantir/f70cdff7-c62f-4b73-a136-909e5e3d1891
    publisher: jobs.lever.co
    claim: Opening lever:palantir:f70cdff7-c62f-4b73-a136-909e5e3d1891 was returned by Palantir's Lever Postings API at checked_at (retrieval_status=success, board check under evidence/boards/lever/palantir/); proves the posting was published at that time, not that headcount or hiring-manager budget still exist.
    snapshot_ref: evidence/openings/lever_palantir_f70cdff7-c62f-4b73-a136-909e5e3d1891/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c6-domain
    source_url: https://jobs.lever.co/palantir/f70cdff7-c62f-4b73-a136-909e5e3d1891
    publisher: jobs.lever.co
    claim: 'JD text says: “Our infrastructure teams are responsible for the lowest layers of our software stack, often focused on database technologies, distributed systems, large scale data systems, security, and application infrastructure. As a Software Engineer on infrastructure ... you''ll contribute high-quality code to underpin Palantir Foundry and Gotham with performant, secure, and scalable building blocks.” — describes systems/performance/scale infrastructure work, not model research or product/application-layer feature work.'
    snapshot_ref: evidence/openings/lever_palantir_f70cdff7-c62f-4b73-a136-909e5e3d1891/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c6-peoplemgmt
    source_url: https://jobs.lever.co/palantir/f70cdff7-c62f-4b73-a136-909e5e3d1891
    publisher: jobs.lever.co
    claim: Full JD text for this opening was read in its entirety and contains no language about managing a team, having direct reports, conducting performance reviews, or making hiring decisions for this role.
    snapshot_ref: evidence/openings/lever_palantir_f70cdff7-c62f-4b73-a136-909e5e3d1891/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c6-workplace
    source_url: https://jobs.lever.co/palantir/f70cdff7-c62f-4b73-a136-909e5e3d1891
    publisher: jobs.lever.co
    claim: Lever posting's structured workplaceType field is “hybrid” for location London, United Kingdom.
    snapshot_ref: evidence/openings/lever_palantir_f70cdff7-c62f-4b73-a136-909e5e3d1891/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
  - id: c6-frontline
    source_url: https://jobs.lever.co/palantir/f70cdff7-c62f-4b73-a136-909e5e3d1891
    publisher: jobs.lever.co
    claim: 'JD text says: “Foundry Software Engineers may be offered the opportunity to Frontline, an exclusive program unlike any other. This unique, short-term assignment involves being embedded with customers ... By witnessing how customers engage with Foundry and experiencing these pain points firsthand, you’ll gain unique insights that feed directly back into our development process, helping to refine and enhance our products.” — an optional, short-term customer-embedding program offered to Foundry engineers generally; not described as this role''s default day-to-day work, but does introduce the kind of customer/business-alignment exposure the direction''s role.requirement_stability preference wants to avoid.'
    snapshot_ref: evidence/openings/lever_palantir_f70cdff7-c62f-4b73-a136-909e5e3d1891/posting.json
    checked_at: '2026-09-24T00:13:55+00:00'
    retrieval_status: success
---

# Palantir — Lever 候选列表（dir-001）

本轮仅针对 **Palantir**（官网 palantir.com → 官方 careers 页链到 `jobs.lever.co/palantir`，provider=lever, board=palantir）一家公司。

## 发现与预筛选（scanned vs judged）

- 拉取了 Lever 板上全部 **318** 个已发布职位（`retrieval_status=success`，4/4 页均成功，无分页缺失）。
- 方向的 `search_hints.keywords` 是中文（如"训练系统""数据库内核"等），而 Lever 板是英文，所以用 `shortlist.py --extra-keyword` 补充了英文 board 词：
  `infrastructure, distributed systems, performance, scalability, developer tools, database, storage, training systems, inference, platform, backend, systems engineer`，
  并用 `--extra-deprioritize` 补充了英文降权词：`product manager, forward deployed, sales, solutions engineer, manager, director, research scientist`。
  完整的 `search_bias`（中英文降权词合集）记录在 frontmatter 中。
- 按关键词打分后，取分数最高的 **8** 个进入 shortlist（预算上限），其中分数最高的 **6** 个进行了完整判断（即下面 candidates 列表）。
- 还有 **2** 个在 shortlist 中但未判断（预算用完），仅列在此处供参考，未进入 candidates：
  - `Backend Software Engineer - Infrastructure, Foundations`（New York, NY）— https://jobs.lever.co/palantir/fb2d3222-dbd8-4e03-8d39-47b820e9509c
  - `Backend Software Engineer - Infrastructure, Foundations`（London）— https://jobs.lever.co/palantir/aaee4d20-7f1b-48b1-ad23-d52ffbf42a49
- 另外观察到一类被 `forward deployed` 降权的职位（如 "Forward Deployed Infrastructure Engineer - US/UK Government"）— 标题包含 infrastructure 但实际是面向客户/政府现场交付的应用层工作，与 `role.domain`的排除项匹配，因此被降权未判断（仅供透明展示，不作为拒绝依据）。

## 适用性说明

本方向 `status: confirmed`，无 pending/conflict 字段。两个确认的 hard 字段（`role.domain`, `role.people_management`，也是 key_fields）对所有 6 个候选均适用（applicable）。`company.size`（skipped）与 `compensation.floor`（unknown，且 kind=unspecified）不是 hard 字段，且本轮 Lever 职位也未提供薪资区间（`salary: null`），故未列入 applicability（非确认 hard 字段，不需列举）。

## 结果（按 match_status 分组）

### rejected （0）

无。本轮 6 个候选中没有任何一个在 `role.domain` 或 `role.people_management` 上直接 fail。

### needs_clarification （0）

无。方向已 confirmed，无 not_confirmed 字段，且每个候选都有 ≥ 1 个 applicable 字段。

### needs_verification （6）

全部 6 个候选都在这一组：`role.domain` pass，但 `role.people_management` 均为 **unknown**——这 6 份 JD 全文都没有任何文字提到带团队/绩效/招聘，也没有明确声明"individual contributor"，所以按规则不能凭"标题看起来像 IC"就判 pass，只能记为 unknown，需要面试/HR 确认。

1. **Software Engineer, Internship - Infrastructure**（New York, NY）— https://jobs.lever.co/palantir/b229baac-494b-4a0d-9a13-2e38806e06f3
   Foundations 组，明确描述 Backend/Developer/Frontend/Storage 四类 infra 工作，与 `role.domain` 高度匹配。workplace_type=onsite。注意：这是 **实习**职位。
2. **Software Engineer, Internship - Infrastructure**（Palo Alto, CA）— https://jobs.lever.co/palantir/f221738b-e97c-4ce3-a12a-17ada2b855e4
   同上，地点为 Palo Alto（直接命中方向例子中的"硅谷"）。workplace_type=onsite。同样是实习职位。
3. **Software Engineer, New Grad - Infrastructure**（New York, NY）— https://jobs.lever.co/palantir/4abf26b4-795c-420a-bf22-1ab98db268b4
   Foundations 组，与上同。workplace_type=hybrid。
4. **Software Engineer, New Grad - Infrastructure**（Palo Alto, CA）— https://jobs.lever.co/palantir/7d75bed5-45d8-4876-840a-2d92ea79c98d
   同上，地点 Palo Alto。workplace_type=hybrid。
5. **Backend Software Engineer - Infrastructure**（New York, NY）— https://jobs.lever.co/palantir/6fe5515f-f677-4d98-8ac2-1775a425f5e7
   Product Development 组下的 infra 团队，JD 明言"负责软件栈最底层，专注数据库技术、分布式系统、大规模数据系统"，`role.domain` pass。**但** JD 同时提到可选的 "Frontline" 项目（可能需要驻地客户现场、把客户反馈回馈到产品）——虽然是 "may be offered" 的可选机会而非默认工作内容，但与方向中 "排斥需求多变/业务方拉扯" 的软偏好（`role.requirement_stability`）构成 **tradeoff**，已在 soft_results 中标注。
6. **Backend Software Engineer - Infrastructure**（London, United Kingdom）— https://jobs.lever.co/palantir/f70cdff7-c62f-4b73-a136-909e5e3d1891
   与上一条同文本模板，同样 pass + Frontline tradeoff 提醒。地点为 London，不在方向 examples（硅谷/深圳/新加坡）里，但符合"年轻、科技密集"的属性描述（通用知识判断，非 JD 文本证据）。

### eligible_for_comparison （0）

无。本轮没有一个候选在两个 hard 字段上都确定 pass——原因都是 `role.people_management` 无文本依据。这不意味着这些职位不符合，只是 Lever JD 本身不回答这个问题，需要人工预筛（面试/提问）才能把它从 unknown 推进到 pass 或 fail。

## 补充说明

- 所有 6 个候选的 `salary` 均为 `null`（Lever 公开 API 未提供），与方向 `compensation.floor`（status=unknown）无法比对，未列入字段判断。
- `location.city_profile` 的 meets 判断基于对城市的通用认知（Palo Alto=硅谷原型例子，NY/London 为已知科技密集城市），**不是** JD 文本证据，已在每条 soft_results 的 note 中注明。
- 一次完整、无分页失败的 Lever 拉取（retrieval_status=success）只证明这些职位在 checked_at 时处于已发布状态，不证明编制/预算仍存在。
