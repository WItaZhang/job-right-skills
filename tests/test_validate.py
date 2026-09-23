"""Positive and negative cases for scripts/validate.py.

The two synthetic examples are the positive fixtures. Negative cases are produced by mutating the
confirmed example in memory and writing it to a temp file, so each test states exactly one rule.
"""
from __future__ import annotations

import copy
import re
import sys
from pathlib import Path

import pytest
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


# ---------- positive ----------

def test_confirmed_example_is_valid():
    assert validate.validate_direction(CONFIRMED) == []


def test_draft_example_is_valid_in_auto_mode():
    assert validate.validate_direction(DRAFT) == []


def test_draft_example_fails_confirmed_rules_for_the_right_reasons():
    problems = validate.validate_direction(DRAFT, mode="confirmed")
    joined = "\n".join(problems)
    assert "key_fields must have 2-4 entries, got 1" in joined
    assert "hard field location.commute_to_family is still pending" in joined


def test_cli_exit_codes(tmp_path):
    assert validate.main(["direction", str(CONFIRMED)]) == 0
    assert validate.main(["direction", str(DRAFT), "--mode", "confirmed"]) == 1
    assert validate.main(["direction", str(tmp_path / "missing.md")]) == 2


# ---------- negative: confirmed-direction rules (plan §3.5) ----------

def test_confirmed_with_pending_hard_is_rejected(tmp_path):
    fm, body = load(CONFIRMED)
    fm["fields"]["location.workplace_type_after_move"].update({"kind": "hard", "status": "pending", "hard_confirmation_ref": None})
    p = write(tmp_path, fm, body)
    problems = validate.validate_direction(p)
    assert any("still pending" in x for x in problems)


def test_same_file_passes_as_draft(tmp_path):
    fm, body = load(CONFIRMED)
    fm["fields"]["location.workplace_type_after_move"].update({"kind": "hard", "status": "pending", "hard_confirmation_ref": None})
    fm["status"] = "draft"
    p = write(tmp_path, fm, body)
    assert validate.validate_direction(p) == []


def test_key_field_that_is_soft_is_rejected(tmp_path):
    fm, body = load(CONFIRMED)
    fm["key_fields"] = ["location.city_profile", "industry"]
    p = write(tmp_path, fm, body)
    problems = validate.validate_direction(p)
    assert any("key field industry must be kind=hard" in x for x in problems)


def test_key_field_count_out_of_range(tmp_path):
    fm, body = load(CONFIRMED)
    fm["key_fields"] = ["location.city_profile"]
    p = write(tmp_path, fm, body)
    assert any("must have 2-4 entries, got 1" in x for x in validate.validate_direction(p))
    fm["key_fields"] = ["location.city_profile", "role.nature", "company.size", "industry", "company.funding_stage"]
    p = write(tmp_path, fm, body)
    assert any("must have 2-4 entries, got 5" in x for x in validate.validate_direction(p))


def test_key_field_without_alt_test_is_rejected(tmp_path):
    fm, body = load(CONFIRMED)
    fm["fields"]["role.nature"]["alt_test_ref"] = None
    p = write(tmp_path, fm, body)
    assert any("role.nature has no alt_test_ref" in x for x in validate.validate_direction(p))


def test_confirmed_hard_without_hard_confirmation_is_rejected(tmp_path):
    fm, body = load(CONFIRMED)
    fm["fields"]["company.size"]["hard_confirmation_ref"] = None
    p = write(tmp_path, fm, body)
    problems = validate.validate_direction(p)
    assert any("company.size has no hard_confirmation_ref" in x for x in problems)


def test_conflict_field_blocks_confirmation_and_requires_conflicts_with(tmp_path):
    fm, body = load(CONFIRMED)
    fm["fields"]["industry"]["status"] = "conflict"
    p = write(tmp_path, fm, body)
    problems = validate.validate_direction(p)
    assert any("status=conflict requires conflicts_with" in x for x in problems)
    assert any("industry is in conflict" in x for x in problems)


# ---------- negative: reference integrity ----------

def test_ref_missing_from_chain_is_rejected(tmp_path):
    fm, body = load(CONFIRMED)
    fm["fields"]["role.nature"]["hard_confirmation_ref"] = "I-999"
    p = write(tmp_path, fm, body)
    assert any("I-999 is not defined in ## 追问链" in x for x in validate.validate_direction(p))


def test_duplicate_chain_id_is_rejected(tmp_path):
    fm, body = load(CONFIRMED)
    body = body.replace("### I-002\n", "### I-001\n", 1)
    p = write(tmp_path, fm, body)
    assert any("I-001 defined more than once" in x for x in validate.validate_direction(p))


def test_missing_sections_are_rejected(tmp_path):
    fm, body = load(CONFIRMED)
    body = re.sub(r"^## 修订记录\s*$", "## Log", body, flags=re.MULTILINE)
    p = write(tmp_path, fm, body)
    assert any("missing '## 修订记录'" in x for x in validate.validate_direction(p))


def test_key_field_not_a_field_is_rejected(tmp_path):
    fm, body = load(CONFIRMED)
    fm["key_fields"] = ["location.city_profile", "does.not_exist"]
    p = write(tmp_path, fm, body)
    assert any("does.not_exist is not a field" in x for x in validate.validate_direction(p))


# ---------- negative: kind/status semantics ----------

def test_skipped_field_cannot_be_hard(tmp_path):
    fm, body = load(DRAFT)
    fm["fields"]["role.nature"]["kind"] = "hard"
    p = write(tmp_path, fm, body)
    assert any("skipped or does not know cannot be kind=hard" in x for x in validate.validate_direction(p))


def test_any_with_unknown_status_is_rejected(tmp_path):
    fm, body = load(DRAFT)
    fm["fields"]["location.city_profile"]["status"] = "unknown"
    p = write(tmp_path, fm, body)
    assert any("kind=any means the user confirmed no preference" in x for x in validate.validate_direction(p))


def test_schema_rejects_old_enum_values(tmp_path):
    fm, body = load(CONFIRMED)
    fm["fields"]["compensation.base"]["kind"] = "unknown"  # r3 vocabulary, no longer allowed
    p = write(tmp_path, fm, body)
    problems = validate.validate_direction(p)
    assert any(x.startswith("schema: fields/compensation.base/kind") for x in problems)


def test_dimension_in_both_progress_lists(tmp_path):
    fm, body = load(CONFIRMED)
    fm["interview_progress"]["not_asked"].append("兴趣动力")
    p = write(tmp_path, fm, body)
    assert any("listed as both asked and not_asked" in x for x in validate.validate_direction(p))


# ---------- candidate rules ----------

def candidate_doc(**overrides) -> dict:
    c = {
        "opening_id": "greenhouse:acme:123",
        "id_source": "provider_native",
        "company_id": "acme",
        "provider": "greenhouse",
        "match_status": "eligible_for_comparison",
        "opening_status": "published_present",
        "user_decision": "undecided",
        "applicability": [{"field_id": "role.nature", "state": "applicable"}],
        "field_results": [{"field_id": "role.nature", "result": "pass", "evidence_refs": ["E-1"]}],
        "evidence": [{"id": "E-1", "source_url": "https://example.test/j/123", "claim": "JD says IC role",
                      "checked_at": "2026-09-23T00:00:00+00:00", "retrieval_status": "success"}],
    }
    c.update(overrides)
    return {"direction_id": "dir-001", "direction_revision": 4, "basis": "confirmed",
            "generated_at": "2026-09-23T00:00:00+00:00", "candidates": [c]}


def write_fm(tmp_path: Path, fm: dict, name: str) -> Path:
    p = tmp_path / name
    p.write_text("---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False) + "---\n\nbody\n", encoding="utf-8")
    return p


def test_candidate_valid(tmp_path):
    assert validate.validate_frontmatter_only(write_fm(tmp_path, candidate_doc(), "c.md"), "candidate") == []


def test_candidate_zero_applicable_cannot_be_eligible(tmp_path):
    doc = candidate_doc(applicability=[{"field_id": "role.nature", "state": "not_confirmed"}], field_results=[])
    problems = validate.validate_frontmatter_only(write_fm(tmp_path, doc, "c.md"), "candidate")
    assert any("empty all() trap" in x for x in problems)


def test_candidate_fail_must_be_rejected(tmp_path):
    doc = candidate_doc(field_results=[{"field_id": "role.nature", "result": "fail", "evidence_refs": ["E-1"]}])
    problems = validate.validate_frontmatter_only(write_fm(tmp_path, doc, "c.md"), "candidate")
    assert any("a hard field failed but match_status" in x for x in problems)


def test_candidate_unknown_cannot_be_eligible(tmp_path):
    doc = candidate_doc(field_results=[{"field_id": "role.nature", "result": "unknown", "evidence_refs": []}])
    problems = validate.validate_frontmatter_only(write_fm(tmp_path, doc, "c.md"), "candidate")
    assert any("unknown but match_status is eligible_for_comparison" in x for x in problems)


def test_candidate_result_for_inapplicable_field(tmp_path):
    doc = candidate_doc(applicability=[{"field_id": "role.nature", "state": "not_applicable", "reason": "valid_from 2027"}],
                        match_status="needs_clarification")
    problems = validate.validate_frontmatter_only(write_fm(tmp_path, doc, "c.md"), "candidate")
    assert any("not marked applicable" in x for x in problems)


# ---------- application rules ----------

def application_doc(**overrides) -> dict:
    d = {
        "opening_id": "greenhouse:acme:123",
        "status": "ready_for_review",
        "candidate_refs": [{"direction_id": "dir-001", "direction_revision": 4}],
        "primary_direction": "dir-001",
        "facts_revision": 1,
        "created_at": "2026-09-23T00:00:00+00:00",
        "updated_at": "2026-09-23T00:00:00+00:00",
        "fields": [
            {"label": "Full name", "fill_status": "filled", "review_status": "none", "required_by_form": True,
             "source": {"kind": "fact", "ref": "F-001"}},
            {"label": "Why us", "fill_status": "filled", "review_status": "needs_review", "required_by_form": True,
             "source": {"kind": "generated_draft", "ref": "dir-001"}},
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


def test_application_filled_but_needs_review_can_be_ready(tmp_path):
    assert validate.validate_frontmatter_only(write_fm(tmp_path, application_doc(), "a.md"), "application") == []


def test_application_ready_with_blockers_is_rejected(tmp_path):
    doc = application_doc(blockers=[{"kind": "missing_required_fact", "detail": "phone number"}])
    problems = validate.validate_frontmatter_only(write_fm(tmp_path, doc, "a.md"), "application")
    assert any("non-empty blockers" in x for x in problems)


def test_application_required_unfilled_non_consent_is_rejected(tmp_path):
    doc = application_doc()
    doc["fields"][0]["fill_status"] = "pending"
    problems = validate.validate_frontmatter_only(write_fm(tmp_path, doc, "a.md"), "application")
    assert any("required field 'Full name' is pending" in x for x in problems)


def test_application_submitted_requires_user_outcome(tmp_path):
    doc = application_doc(status="submitted_by_user")
    problems = validate.validate_frontmatter_only(write_fm(tmp_path, doc, "a.md"), "application")
    assert any("requires user_outcome" in x for x in problems)


def test_application_primary_direction_must_be_referenced(tmp_path):
    doc = application_doc(primary_direction="dir-009")
    problems = validate.validate_frontmatter_only(write_fm(tmp_path, doc, "a.md"), "application")
    assert any("not among candidate_refs" in x for x in problems)


# ---------- facts rules ----------

def test_facts_work_authorization_must_be_user_statement(tmp_path):
    doc = {"facts_revision": 1, "updated_at": "2026-09-23T00:00:00+00:00", "items": [
        {"id": "F-001", "category": "work_authorization", "value": "citizen", "status": "confirmed",
         "confirmed_at": "2026-09-23T00:00:00+00:00", "source": {"kind": "resume_parse"}}]}
    p = tmp_path / "facts.yaml"
    p.write_text(yaml.safe_dump(doc), encoding="utf-8")
    problems = validate.validate_facts(p)
    assert any("work_authorization must come from the user's own statement" in x for x in problems)


def test_facts_confirmed_requires_confirmed_at(tmp_path):
    doc = {"facts_revision": 1, "updated_at": "2026-09-23T00:00:00+00:00", "items": [
        {"id": "F-001", "category": "contact", "value": "x@example.test", "status": "confirmed",
         "source": {"kind": "user_statement"}}]}
    p = tmp_path / "facts.yaml"
    p.write_text(yaml.safe_dump(doc), encoding="utf-8")
    assert any("without confirmed_at" in x for x in validate.validate_facts(p))
