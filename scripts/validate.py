#!/usr/bin/env python3
"""Validate job-right workspace files against schema/ and the cross-field rules of the plan.

Usage:
  validate.py direction <file.md> [--mode auto|confirmed|draft]
  validate.py candidate <file.md>
  validate.py application <file.md>
  validate.py facts <file.yaml>

Direction files are Markdown with YAML frontmatter; the body must contain a "## 追问链" section whose
entries are headings "### I-xxx". Candidate and application files are Markdown with YAML frontmatter.
Facts files are plain YAML.

What this script proves: structure, enum values, that every interview reference exists, and that the
confirmed-direction rules hold (key_fields are 2-4 confirmed hard fields with alt-test and
hard-confirmation refs; no conflict fields; no pending hard fields). It cannot prove that the referenced
interview entries actually support the recorded judgement. That is what behaviour evals are for.

Exit code 0 when valid, 1 when problems were found, 2 on usage or parse errors.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = PLUGIN_ROOT / "schema"


class _StringTimestampLoader(yaml.SafeLoader):
    """SafeLoader that leaves ISO timestamps as strings so JSON Schema sees the text the author wrote."""


_StringTimestampLoader.yaml_implicit_resolvers = {
    first: [(tag, rx) for tag, rx in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for first, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def yaml_load(text: str):
    return yaml.load(text, Loader=_StringTimestampLoader)
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL)
CHAIN_HEADING_RE = re.compile(r"^###\s+(I-[0-9]{3,})\b", re.MULTILINE)
CHAIN_SECTION_RE = re.compile(r"^##\s+追问链\s*$", re.MULTILINE)
REVISION_SECTION_RE = re.compile(r"^##\s+修订记录\s*$", re.MULTILINE)
KEY_FIELDS_MIN, KEY_FIELDS_MAX = 2, 4


class Problems(list):
    def add(self, msg: str) -> None:
        self.append(msg)


def load_schema(name: str) -> dict:
    return json.loads((SCHEMA_DIR / f"{name}.schema.json").read_text(encoding="utf-8"))


def split_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError("file does not start with a YAML frontmatter block delimited by ---")
    fm = yaml_load(m.group(1))
    if not isinstance(fm, dict):
        raise ValueError("frontmatter is not a mapping")
    return fm, m.group(2)


def schema_problems(instance: dict, schema_name: str) -> list[str]:
    validator = Draft202012Validator(load_schema(schema_name), format_checker=FormatChecker())
    out = []
    for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path)):
        loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
        out.append(f"schema: {loc}: {err.message}")
    return out


def chain_ids(body: str) -> tuple[set[str], list[str]]:
    problems: list[str] = []
    if not CHAIN_SECTION_RE.search(body):
        problems.append("body: missing '## 追问链' section")
    if not REVISION_SECTION_RE.search(body):
        problems.append("body: missing '## 修订记录' section")
    ids = CHAIN_HEADING_RE.findall(body)
    dup = {i for i in ids if ids.count(i) > 1}
    for d in sorted(dup):
        problems.append(f"body: interview ref {d} defined more than once")
    return set(ids), problems


def validate_direction(path: Path, mode: str = "auto") -> list[str]:
    problems = Problems()
    try:
        fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
    except (ValueError, yaml.YAMLError) as exc:
        return [f"parse: {exc}"]

    problems.extend(schema_problems(fm, "direction"))
    if problems:
        # Cross-field checks assume the shape is right; stop here so messages stay meaningful.
        return list(problems)

    refs_defined, chain_problems = chain_ids(body)
    problems.extend(chain_problems)

    fields: dict = fm["fields"]
    for fid, f in fields.items():
        for key in ("source_ref", "alt_test_ref", "hard_confirmation_ref"):
            ref = f.get(key)
            if ref and ref not in refs_defined:
                problems.add(f"{fid}.{key}: {ref} is not defined in ## 追问链")
        if f["kind"] == "any" and f["status"] not in ("confirmed", "pending"):
            problems.add(f"{fid}: kind=any means the user confirmed no preference; status must be confirmed or pending, got {f['status']}")
        if f["status"] in ("skipped", "unknown") and f["kind"] == "hard":
            problems.add(f"{fid}: a field the user skipped or does not know cannot be kind=hard")
        for other in f.get("conflicts_with", []):
            if other not in fields:
                problems.add(f"{fid}.conflicts_with: {other} is not a field")
        if f["status"] == "conflict" and not f.get("conflicts_with"):
            problems.add(f"{fid}: status=conflict requires conflicts_with")

    for fid in fm["key_fields"]:
        if fid not in fields:
            problems.add(f"key_fields: {fid} is not a field")

    for dim in set(fm["interview_progress"]["asked"]) & set(fm["interview_progress"]["not_asked"]):
        problems.add(f"interview_progress: {dim} listed as both asked and not_asked")

    effective_mode = fm["status"] if mode == "auto" else mode
    if effective_mode == "confirmed":
        problems.extend(confirmed_rules(fm))
    return list(problems)


def confirmed_rules(fm: dict) -> list[str]:
    """Rules a direction must satisfy to be status=confirmed (plan §3.5)."""
    problems: list[str] = []
    fields: dict = fm["fields"]
    kf = fm["key_fields"]
    if not (KEY_FIELDS_MIN <= len(kf) <= KEY_FIELDS_MAX):
        problems.append(f"confirmed: key_fields must have {KEY_FIELDS_MIN}-{KEY_FIELDS_MAX} entries, got {len(kf)}")
    for fid in kf:
        f = fields.get(fid)
        if f is None:
            continue
        if f["kind"] != "hard":
            problems.append(f"confirmed: key field {fid} must be kind=hard, got {f['kind']}")
        if f["status"] != "confirmed":
            problems.append(f"confirmed: key field {fid} must be status=confirmed, got {f['status']}")
        if not f.get("alt_test_ref"):
            problems.append(f"confirmed: key field {fid} has no alt_test_ref (alternative test never recorded)")
        if not f.get("hard_confirmation_ref"):
            problems.append(f"confirmed: key field {fid} has no hard_confirmation_ref (strength never confirmed)")
    for fid, f in fields.items():
        if f["status"] == "conflict":
            problems.append(f"confirmed: field {fid} is in conflict; resolve before confirming the direction")
        if f["kind"] == "hard" and f["status"] == "pending":
            problems.append(f"confirmed: hard field {fid} is still pending; confirm its strength or keep the direction as draft")
        if f["kind"] == "hard" and f["status"] == "confirmed" and not f.get("hard_confirmation_ref"):
            problems.append(f"confirmed: hard field {fid} is confirmed without hard_confirmation_ref")
    return problems


def validate_frontmatter_only(path: Path, schema_name: str) -> list[str]:
    try:
        fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    except (ValueError, yaml.YAMLError) as exc:
        return [f"parse: {exc}"]
    problems = schema_problems(fm, schema_name)
    if schema_name == "candidate" and not problems:
        problems.extend(candidate_rules(fm))
    if schema_name == "application" and not problems:
        problems.extend(application_rules(fm))
    return problems


def candidate_rules(fm: dict) -> list[str]:
    problems: list[str] = []
    for c in fm["candidates"]:
        applicable = {a["field_id"] for a in c["applicability"] if a["state"] == "applicable"}
        results = {r["field_id"]: r["result"] for r in c["field_results"]}
        extra = set(results) - applicable
        for fid in sorted(extra):
            problems.append(f"{c['opening_id']}: field_results contains {fid} which is not marked applicable")
        if not applicable and c["match_status"] == "eligible_for_comparison":
            problems.append(f"{c['opening_id']}: eligible_for_comparison with zero applicable confirmed hard fields (empty all() trap)")
        if any(r == "fail" for r in results.values()) and c["match_status"] != "rejected":
            problems.append(f"{c['opening_id']}: a hard field failed but match_status is {c['match_status']}")
        if applicable and all(results.get(f) == "pass" for f in applicable) and c["match_status"] == "needs_verification":
            problems.append(f"{c['opening_id']}: all applicable hard fields pass yet match_status is needs_verification")
        if any(r == "unknown" for r in results.values()) and "fail" not in results.values() \
                and c["match_status"] == "eligible_for_comparison":
            problems.append(f"{c['opening_id']}: a hard field is unknown but match_status is eligible_for_comparison")
    return problems


def application_rules(fm: dict) -> list[str]:
    problems: list[str] = []
    if fm["status"] == "ready_for_review":
        if fm["blockers"]:
            problems.append("ready_for_review with non-empty blockers")
        consent_labels = {ri.get("field_label") for ri in fm["review_items"] if ri["kind"] == "consent_checkbox"}
        for f in fm["fields"]:
            if f.get("required_by_form") and f["fill_status"] != "filled" and f["label"] not in consent_labels:
                problems.append(f"ready_for_review but required field {f['label']!r} is {f['fill_status']} and not a listed consent item")
    for ri in fm["review_items"]:
        if ri["kind"] == "evidence_gap" and "required" in ri["detail"].lower() and "fact" in ri["detail"].lower():
            problems.append("review_items: a missing required fact must be a blocker, not a review item")
    if fm["status"] in ("submitted_by_user", "abandoned_by_user") and not fm.get("user_outcome"):
        problems.append(f"status {fm['status']} requires user_outcome reported by the user")
    primary = fm["primary_direction"]
    if primary not in {c["direction_id"] for c in fm["candidate_refs"]}:
        problems.append(f"primary_direction {primary} is not among candidate_refs")
    return problems


def validate_facts(path: Path) -> list[str]:
    try:
        data = yaml_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return [f"parse: {exc}"]
    if not isinstance(data, dict):
        return ["parse: facts file is not a mapping"]
    problems = schema_problems(data, "background_facts")
    if problems:
        return problems
    for item in data["items"]:
        if item["status"] == "confirmed" and not item.get("confirmed_at"):
            problems.append(f"{item['id']}: confirmed fact without confirmed_at")
        if item["category"] == "work_authorization" and item["source"]["kind"] != "user_statement":
            problems.append(f"{item['id']}: work_authorization must come from the user's own statement")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("kind", choices=["direction", "candidate", "application", "facts"])
    parser.add_argument("file", type=Path)
    parser.add_argument("--mode", choices=["auto", "confirmed", "draft"], default="auto",
                        help="direction only: which rule set to apply; auto follows the file's status")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if not args.file.exists():
        print(f"error: {args.file} does not exist", file=sys.stderr)
        return 2
    if args.kind == "direction":
        problems = validate_direction(args.file, args.mode)
    elif args.kind == "facts":
        problems = validate_facts(args.file)
    else:
        problems = validate_frontmatter_only(args.file, args.kind)

    if args.json:
        print(json.dumps({"file": str(args.file), "ok": not problems, "problems": problems}, ensure_ascii=False, indent=2))
    else:
        if problems:
            print(f"{args.file}: {len(problems)} problem(s)")
            for p in problems:
                print(f"  - {p}")
        else:
            print(f"{args.file}: ok")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
