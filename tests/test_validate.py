"""Positive and negative cases for scripts/validate.py.

The two synthetic examples are the positive fixtures. Negative cases are produced by mutating the
examples in memory and writing them to a temp file, so each test states exactly one rule. Review ids
(R01, R21, ...) refer to docs/implementation-plan-review.md.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate  # noqa: E402

ASSETS = ROOT / "skills" / "grill-direction" / "assets"
CONFIRMED = ASSETS / "example-synthetic-city-profile.md"
DRAFT = ASSETS / "example-synthetic-family-us.md"


def load(path: Path) -> tuple[dict, str]:
    return validate.split_frontmatter(path.read_text(encoding="utf-8"))


def write(tmp_path: Path, fm: dict, body: str, name: str = "dir.md") -> Path:
    p = tmp_path / name
    p.write_text("---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False) + "---\n" + body, encoding="utf-8")
    return p


def write_raw(tmp_path: Path, text: str, name: str = "raw.md") -> Path:
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def has(problems: list[str], needle: str) -> bool:
    return any(needle in x for x in problems)


# =============================================================== positive

def test_confirmed_example_is_valid():
    assert validate.validate_direction(CONFIRMED) == []


def test_draft_example_is_valid_in_auto_mode():
    assert validate.validate_direction(DRAFT) == []


def test_draft_example_fails_confirmed_rules_for_the_right_reasons():
    problems = validate.validate_direction(DRAFT, mode="confirmed")
    assert has(problems, "key_fields must have 2-4 entries, got 1")
    assert has(problems, "hard field location.commute_to_family is still pending")


def test_cli_exit_codes(tmp_path):
    assert validate.main(["direction", str(CONFIRMED)]) == 0
    assert validate.main(["direction", str(DRAFT), "--mode", "confirmed"]) == 1
    assert validate.main(["direction", str(tmp_path / "missing.md")]) == 2


# ======================================== direction: confirmed-only rules (§3.5, R02, R12)

def test_confirmed_with_pending_hard_is_rejected(tmp_path):
    fm, body = load(CONFIRMED)
    fm["fields"]["location.workplace_type_after_move"].update({"kind": "hard", "status": "pending", "hard_confirmation_ref": None})
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "still pending")


def test_same_file_passes_as_draft(tmp_path):
    fm, body = load(CONFIRMED)
    fm["fields"]["location.workplace_type_after_move"].update({"kind": "hard", "status": "pending", "hard_confirmation_ref": None})
    fm["status"] = "draft"
    assert validate.validate_direction(write(tmp_path, fm, body)) == []


def test_key_field_count_out_of_range(tmp_path):
    fm, body = load(CONFIRMED)
    fm["key_fields"] = ["location.city_profile"]
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "must have 2-4 entries, got 1")
    fm["key_fields"] = ["location.city_profile", "role.nature", "company.size", "industry", "company.funding_stage"]
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "must have 2-4 entries, got 5")


def test_conflict_field_blocks_confirmation_and_requires_conflicts_with(tmp_path):
    fm, body = load(CONFIRMED)
    fm["fields"]["industry"]["status"] = "conflict"
    problems = validate.validate_direction(write(tmp_path, fm, body))
    assert has(problems, "status=conflict requires conflicts_with")
    assert has(problems, "industry is in conflict")


# ======================================== direction: rules that hold in every mode (R01, R22)

def test_key_field_that_is_soft_is_rejected_even_in_draft(tmp_path):
    fm, body = load(CONFIRMED)
    fm["status"] = "draft"
    fm["key_fields"] = ["location.city_profile", "industry"]
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "key field industry must be kind=hard")


def test_key_field_without_alt_test_is_rejected(tmp_path):
    fm, body = load(CONFIRMED)
    fm["fields"]["role.nature"]["alt_test_ref"] = None
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "role.nature has no alt_test_ref")


def test_confirmed_hard_without_strength_ref_is_rejected_in_confirmed_mode(tmp_path):
    fm, body = load(CONFIRMED)
    fm["fields"]["company.size"]["hard_confirmation_ref"] = None
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "company.size: kind=hard with status=confirmed but no hard_confirmation_ref")


def test_confirmed_hard_without_strength_ref_is_rejected_in_draft_too(tmp_path):
    """R22: a draft may hold pending hard fields, but a field that claims confirmed-hard must prove it,
    because find-openings will filter on it."""
    fm, body = load(CONFIRMED)
    fm["status"] = "draft"
    fm["fields"]["company.size"]["hard_confirmation_ref"] = None
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "company.size: kind=hard with status=confirmed but no hard_confirmation_ref")


def test_draft_keeps_pending_hard_without_strength_ref(tmp_path):
    fm, body = load(CONFIRMED)
    fm["status"] = "draft"
    fm["fields"]["company.size"].update({"status": "pending", "hard_confirmation_ref": None})
    fm["key_fields"] = ["location.city_profile", "role.nature"]
    assert validate.validate_direction(write(tmp_path, fm, body)) == []


# ======================================== direction: reference integrity (R01, R24)

def test_ref_missing_from_chain_is_rejected(tmp_path):
    fm, body = load(CONFIRMED)
    fm["fields"]["role.nature"]["hard_confirmation_ref"] = "I-999"
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "I-999 is not defined in ## 追问链")


def test_ref_only_in_revision_log_does_not_count(tmp_path):
    """R24: an id that appears under ## 修订记录 (or anywhere outside ## 追问链) is not interview evidence."""
    fm, body = load(CONFIRMED)
    fm["fields"]["role.nature"]["hard_confirmation_ref"] = "I-999"
    body = body.rstrip("\n") + "\n\n### I-999\n- 用户原话：伪造的。\n"
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "I-999 is not defined in ## 追问链")


def test_ref_inside_code_fence_does_not_count(tmp_path):
    fm, body = load(CONFIRMED)
    fm["fields"]["role.nature"]["hard_confirmation_ref"] = "I-998"
    body = body.replace("## 修订记录", "```\n### I-998\n```\n\n## 修订记录", 1)
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "I-998 is not defined in ## 追问链")


def test_duplicate_chain_id_is_rejected(tmp_path):
    fm, body = load(CONFIRMED)
    body = body.replace("### I-002\n", "### I-001\n", 1)
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "I-001 defined more than once")


def test_missing_sections_are_rejected(tmp_path):
    fm, body = load(CONFIRMED)
    body = re.sub(r"^## 修订记录\s*$", "## Log", body, flags=re.MULTILINE)
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "missing '## 修订记录'")


def test_key_field_not_a_field_is_rejected(tmp_path):
    fm, body = load(CONFIRMED)
    fm["key_fields"] = ["location.city_profile", "does.not_exist"]
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "does.not_exist is not a field")


# ======================================== direction: kind/status semantics (R12)

def test_skipped_field_cannot_be_hard(tmp_path):
    fm, body = load(DRAFT)
    fm["fields"]["role.nature"]["kind"] = "hard"
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "skipped or does not know cannot be kind=hard")


def test_any_with_unknown_status_is_rejected(tmp_path):
    fm, body = load(DRAFT)
    fm["fields"]["location.city_profile"]["status"] = "unknown"
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "kind=any means the user confirmed no preference")


def test_schema_rejects_old_enum_values(tmp_path):
    fm, body = load(CONFIRMED)
    fm["fields"]["compensation.base"]["kind"] = "unknown"  # r3 vocabulary, no longer allowed
    assert any(x.startswith("schema: fields/compensation.base/kind") for x in validate.validate_direction(write(tmp_path, fm, body)))


def test_dimension_in_both_progress_lists(tmp_path):
    fm, body = load(CONFIRMED)
    fm["interview_progress"]["not_asked"].append("兴趣动力")
    assert has(validate.validate_direction(write(tmp_path, fm, body)), "listed as both asked and not_asked")


# ======================================== YAML duplicate keys (R26)

def test_duplicate_top_level_key_is_a_parse_error(tmp_path):
    text = CONFIRMED.read_text(encoding="utf-8").replace("status: confirmed\n", "status: draft\nstatus: confirmed\n", 1)
    problems = validate.validate_direction(write_raw(tmp_path, text))
    assert len(problems) == 1 and problems[0].startswith("parse: duplicate key 'status'")


def test_duplicate_nested_key_is_a_parse_error(tmp_path):
    text = CONFIRMED.read_text(encoding="utf-8").replace("    value: IC\n", "    value: IC\n    value: manager\n", 1)
    problems = validate.validate_direction(write_raw(tmp_path, text))
    assert len(problems) == 1 and "duplicate key 'value'" in problems[0]


def test_duplicate_key_in_facts_is_a_parse_error(tmp_path):
    p = tmp_path / "facts.yaml"
    p.write_text("facts_revision: 1\nfacts_revision: 2\nupdated_at: x\nitems: []\n", encoding="utf-8")
    problems = validate.validate_facts(p)
    assert len(problems) == 1 and "duplicate key 'facts_revision'" in problems[0]


# ======================================== candidate (R12, R13, R21, R25)

EV = {"id": "E-1", "source_url": "https://example.test/j/123", "claim": "JD says IC role",
      "checked_at": "2026-09-23T00:00:00+00:00", "retrieval_status": "success"}
EV2 = {**EV, "id": "E-2", "claim": "JD says 120 employees"}


def cand(**overrides) -> dict:
    c = {
        "opening_id": "greenhouse:acme:123", "id_source": "provider_native", "company_id": "acme", "provider": "greenhouse",
        "match_status": "eligible_for_comparison", "opening_status": "published_present", "user_decision": "undecided",
        "applicability": [{"field_id": "role.nature", "state": "applicable"}],
        "field_results": [{"field_id": "role.nature", "result": "pass", "evidence_refs": ["E-1"]}],
        "evidence": [EV],
    }
    c.update(overrides)
    return c


def cdoc(candidate: dict, **top) -> dict:
    d = {"direction_id": "dir-001", "direction_revision": 4, "basis": "confirmed",
         "generated_at": "2026-09-23T00:00:00+00:00", "candidates": [candidate]}
    d.update(top)
    return d


def write_fm(tmp_path: Path, fm: dict, name: str) -> Path:
    p = tmp_path / name
    p.write_text("---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False) + "---\n\nbody\n", encoding="utf-8")
    return p


def cval(tmp_path, doc) -> list[str]:
    return validate.validate_frontmatter_only(write_fm(tmp_path, doc, "c.md"), "candidate")


def test_candidate_valid(tmp_path):
    assert cval(tmp_path, cdoc(cand())) == []


def test_candidate_zero_applicable_cannot_be_eligible(tmp_path):
    doc = cdoc(cand(applicability=[{"field_id": "role.nature", "state": "not_confirmed"}], field_results=[]))
    assert has(cval(tmp_path, doc), "imply needs_clarification")


def test_candidate_fail_must_be_rejected(tmp_path):
    doc = cdoc(cand(field_results=[{"field_id": "role.nature", "result": "fail", "evidence_refs": ["E-1"]}]))
    assert has(cval(tmp_path, doc), "imply rejected")


def test_candidate_unknown_cannot_be_eligible(tmp_path):
    doc = cdoc(cand(field_results=[{"field_id": "role.nature", "result": "unknown", "evidence_refs": []}]))
    assert has(cval(tmp_path, doc), "imply needs_verification")


def test_candidate_result_for_inapplicable_field(tmp_path):
    doc = cdoc(cand(applicability=[{"field_id": "role.nature", "state": "not_applicable", "reason": "valid_from 2027"}],
                    match_status="needs_clarification"))
    assert has(cval(tmp_path, doc), "not marked applicable")


def test_r21_applicable_without_result_is_rejected(tmp_path):
    doc = cdoc(cand(field_results=[]))
    problems = cval(tmp_path, doc)
    assert has(problems, "applicable field role.nature has no result")


def test_r21_two_applicable_one_pass_is_not_eligible(tmp_path):
    doc = cdoc(cand(applicability=[{"field_id": "role.nature", "state": "applicable"},
                                   {"field_id": "company.size", "state": "applicable"}]))
    problems = cval(tmp_path, doc)
    assert has(problems, "applicable field company.size has no result")


def test_r21_duplicate_field_result_cannot_override_fail(tmp_path):
    doc = cdoc(cand(field_results=[{"field_id": "role.nature", "result": "fail", "evidence_refs": ["E-1"]},
                                   {"field_id": "role.nature", "result": "pass", "evidence_refs": ["E-1"]}]))
    problems = cval(tmp_path, doc)
    assert has(problems, "field_results lists role.nature more than once")


def test_r21_not_confirmed_field_forces_needs_clarification(tmp_path):
    doc = cdoc(cand(applicability=[{"field_id": "role.nature", "state": "applicable"},
                                   {"field_id": "company.size", "state": "not_confirmed"}]),
               basis="exploratory", pending_fields=["company.size"])
    assert has(cval(tmp_path, doc), "imply needs_clarification")


def test_r21_pass_only_but_rejected_is_inconsistent(tmp_path):
    doc = cdoc(cand(match_status="rejected"))
    assert has(cval(tmp_path, doc), "match_status is rejected but the recorded results imply eligible_for_comparison")


def test_r21_fail_outranks_pending_preferences(tmp_path):
    doc = cdoc(cand(field_results=[{"field_id": "role.nature", "result": "fail", "evidence_refs": ["E-1"]}],
                    match_status="rejected"), basis="exploratory", pending_fields=["industry"])
    assert cval(tmp_path, doc) == []


def test_r25_pass_needs_resolvable_evidence(tmp_path):
    assert has(cval(tmp_path, cdoc(cand(evidence=[]))), "cites evidence E-1 which is not in this candidate's evidence list")
    assert has(cval(tmp_path, cdoc(cand(field_results=[{"field_id": "role.nature", "result": "pass", "evidence_refs": []}]))),
               "is pass without any evidence reference")


def test_r25_evidence_ids_unique(tmp_path):
    assert has(cval(tmp_path, cdoc(cand(evidence=[EV, EV]))), "evidence id E-1 is not unique")


# ======================================== application (R15, R16, R25)

def app(**overrides) -> dict:
    d = {
        "opening_id": "greenhouse:acme:123", "status": "ready_for_review",
        "candidate_refs": [{"direction_id": "dir-001", "direction_revision": 4}], "primary_direction": "dir-001",
        "facts_revision": 1, "created_at": "2026-09-23T00:00:00+00:00", "updated_at": "2026-09-23T00:00:00+00:00",
        "fields": [
            {"label": "Full name", "fill_status": "filled", "review_status": "none", "required_by_form": True,
             "value_readback": "A. Person", "source": {"kind": "fact", "ref": "F-001"}},
            {"label": "Why us", "fill_status": "filled", "review_status": "needs_review", "required_by_form": True,
             "value_readback": "draft text", "source": {"kind": "generated_draft", "ref": "dir-001"}},
            {"label": "I agree to the privacy policy", "fill_status": "pending", "review_status": "none", "required_by_form": True},
        ],
        "blockers": [],
        "review_items": [
            {"kind": "free_text_draft", "detail": "review the Why us answer", "field_label": "Why us"},
            {"kind": "consent_checkbox", "detail": "tick only if you agree", "field_label": "I agree to the privacy policy"},
        ],
    }
    d.update(overrides)
    return d


def aval(tmp_path, doc) -> list[str]:
    return validate.validate_frontmatter_only(write_fm(tmp_path, doc, "a.md"), "application")


def test_application_filled_but_needs_review_can_be_ready(tmp_path):
    assert aval(tmp_path, app()) == []


def test_application_ready_with_blockers_is_rejected(tmp_path):
    assert has(aval(tmp_path, app(blockers=[{"kind": "missing_required_fact", "detail": "phone number"}])), "non-empty blockers")


def test_application_required_unfilled_non_consent_is_rejected(tmp_path):
    doc = app()
    doc["fields"][0]["fill_status"] = "pending"
    del doc["fields"][0]["value_readback"], doc["fields"][0]["source"]
    assert has(aval(tmp_path, doc), "required field 'Full name' is pending")


def test_application_submitted_requires_user_outcome(tmp_path):
    assert has(aval(tmp_path, app(status="submitted_by_user")), "requires user_outcome")


def test_application_primary_direction_must_be_referenced(tmp_path):
    assert has(aval(tmp_path, app(primary_direction="dir-009")), "not among candidate_refs")


def test_r25_filled_field_needs_source_and_readback(tmp_path):
    doc = app()
    del doc["fields"][0]["source"]
    del doc["fields"][0]["value_readback"]
    problems = aval(tmp_path, doc)
    assert has(problems, "'Full name': filled but no value_readback")
    assert has(problems, "'Full name': filled but no source")


def test_r25_fact_source_requires_ref(tmp_path):
    doc = app()
    doc["fields"][0]["source"] = {"kind": "fact"}
    assert has(aval(tmp_path, doc), "source kind fact requires a ref")


# ======================================== facts (R11, R25)

def fval(tmp_path, doc) -> list[str]:
    p = tmp_path / "facts.yaml"
    p.write_text(yaml.safe_dump(doc, allow_unicode=True), encoding="utf-8")
    return validate.validate_facts(p)


def fact(fid="F-001", **kw) -> dict:
    d = {"id": fid, "category": "contact", "value": "x@example.test", "status": "confirmed",
         "confirmed_at": "2026-09-23T00:00:00+00:00", "source": {"kind": "user_statement"}}
    d.update(kw)
    return d


def test_facts_valid(tmp_path):
    assert fval(tmp_path, {"facts_revision": 1, "updated_at": "2026-09-23T00:00:00+00:00", "items": [fact()]}) == []


def test_facts_work_authorization_must_be_user_statement(tmp_path):
    doc = {"facts_revision": 1, "updated_at": "2026-09-23T00:00:00+00:00",
           "items": [fact(category="work_authorization", value="citizen", source={"kind": "resume_parse"})]}
    assert has(fval(tmp_path, doc), "work_authorization must come from the user's own statement")


def test_facts_confirmed_requires_confirmed_at(tmp_path):
    item = fact()
    del item["confirmed_at"]
    doc = {"facts_revision": 1, "updated_at": "2026-09-23T00:00:00+00:00", "items": [item]}
    assert has(fval(tmp_path, doc), "without confirmed_at")


def test_r25_fact_ids_unique(tmp_path):
    doc = {"facts_revision": 1, "updated_at": "2026-09-23T00:00:00+00:00", "items": [fact(), fact(value="y@example.test")]}
    assert has(fval(tmp_path, doc), "fact id F-001 is not unique")


# ======================================== R30: longer and indented fences

def _fake_ref_in_fence(fence_open: str, fence_close: str, indent: str = "") -> str:
    fm_text = CONFIRMED.read_text(encoding="utf-8").replace("    hard_confirmation_ref: I-016\n", "    hard_confirmation_ref: I-999\n", 1)
    block = f"{indent}{fence_open}\n### I-999\n- 用户原话：伪造的。\n{indent}{fence_close}\n\n"
    return fm_text.replace("### I-020\n", block + "### I-020\n", 1)


def test_r30_four_backtick_fence_does_not_count(tmp_path):
    assert has(validate.validate_direction(write_raw(tmp_path, _fake_ref_in_fence("````", "````"))), "I-999 is not defined")


def test_r30_four_tilde_fence_does_not_count(tmp_path):
    assert has(validate.validate_direction(write_raw(tmp_path, _fake_ref_in_fence("~~~~", "~~~~"))), "I-999 is not defined")


def test_r30_indented_fence_does_not_count(tmp_path):
    assert has(validate.validate_direction(write_raw(tmp_path, _fake_ref_in_fence("```", "```", indent="  "))), "I-999 is not defined")


def test_r30_longer_closing_fence_closes_shorter_opening(tmp_path):
    """A ``` block closed by ```` is still one block; the real entries after it must still count."""
    text = _fake_ref_in_fence("```", "`````")
    problems = validate.validate_direction(write_raw(tmp_path, text))
    assert has(problems, "I-999 is not defined")
    assert not has(problems, "I-020 is not defined")


def test_r30_shorter_closing_does_not_close_longer_opening(tmp_path):
    """```` opened, ``` inside does not close it; the fake heading stays inside the fence."""
    text = _fake_ref_in_fence("````", "````").replace("### I-999\n", "```\n### I-999\n", 1)
    assert has(validate.validate_direction(write_raw(tmp_path, text)), "I-999 is not defined")


def test_strip_fences_keeps_real_entries():
    body = CONFIRMED.read_text(encoding="utf-8").split("---\n", 2)[2]
    ids, problems = validate.chain_ids(body)
    assert problems == []
    assert "I-001" in ids and "I-024" in ids
