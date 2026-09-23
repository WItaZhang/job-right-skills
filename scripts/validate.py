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

What this script proves: structure, enum values, that YAML has no duplicate keys, that every interview
reference resolves to an entry inside the 追问链 section, that every confirmed hard field carries a
strength-confirmation reference (in every mode), and that the confirmed-direction rules hold
(2-4 key fields, no conflict fields, no pending hard fields). For candidates it recomputes the
expected match_status from the recorded results and rejects records whose status does not follow.
It cannot prove that a referenced interview entry actually supports the recorded judgement, or that
an evidence snapshot says what the claim says. That is what behaviour evals are for.

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
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL)
CHAIN_HEADING_RE = re.compile(r"^###\s+(I-[0-9]{3,})\b", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
CHAIN_TITLE = "追问链"
REVISION_TITLE = "修订记录"
KEY_FIELDS_MIN, KEY_FIELDS_MAX = 2, 4


# ---------------------------------------------------------------------------
# YAML loading: timestamps stay strings, duplicate keys are an error (review R26)
# ---------------------------------------------------------------------------

class DuplicateKeyError(yaml.YAMLError):
    pass


class _StrictLoader(yaml.SafeLoader):
    """SafeLoader that leaves ISO timestamps as strings and refuses duplicate mapping keys.

    PyYAML silently keeps the last duplicate. For files an LLM appends to, that hides the original
    contradiction from both the schema and the user, so we fail loudly with the position instead.
    """

    def construct_mapping(self, node, deep=False):
        seen: dict = {}
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=True)
            if key in seen:
                first = seen[key]
                raise DuplicateKeyError(
                    f"duplicate key {key!r} at line {key_node.start_mark.line + 1} "
                    f"(first defined at line {first.start_mark.line + 1})"
                )
            seen[key] = key_node
        return super().construct_mapping(node, deep=deep)


_StrictLoader.yaml_implicit_resolvers = {
    first: [(tag, rx) for tag, rx in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for first, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def yaml_load(text: str):
    return yaml.load(text, Loader=_StrictLoader)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

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


def _duplicates(values) -> list:
    seen, dup = set(), []
    for v in values:
        if v in seen and v not in dup:
            dup.append(v)
        seen.add(v)
    return dup


def strip_fences(body: str) -> str:
    """Remove fenced code blocks (CommonMark rules: same fence character, closing length >= opening,
    up to three spaces of indentation). Content inside a fence is an illustration, never evidence
    (reviews R24, R30). An unterminated fence runs to the end of the body."""
    out: list[str] = []
    fence_char, fence_len = None, 0
    for line in body.splitlines(keepends=True):
        m = FENCE_OPEN_RE.match(line)
        if fence_char is None:
            if m:
                fence_char, fence_len = m.group(1)[0], len(m.group(1))
                continue
            out.append(line)
        else:
            if m and m.group(1)[0] == fence_char and len(m.group(1)) >= fence_len and not line[m.end():].strip():
                fence_char, fence_len = None, 0
            # inside a fence: drop the line
    return "".join(out)


def body_sections(body: str) -> dict[str, str]:
    """Split the Markdown body into {h2 title: section text}, ignoring headings inside code fences."""
    cleaned = strip_fences(body)
    sections: dict[str, str] = {}
    matches = list(H2_RE.finditer(cleaned))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(cleaned)
        sections[m.group(1)] = cleaned[m.end():end]
    return sections


def chain_ids(body: str) -> tuple[set[str], list[str]]:
    """Interview ids defined as ### I-xxx headings inside the 追问链 section only (review R24)."""
    problems: list[str] = []
    sections = body_sections(body)
    if CHAIN_TITLE not in sections:
        problems.append(f"body: missing '## {CHAIN_TITLE}' section")
    if REVISION_TITLE not in sections:
        problems.append(f"body: missing '## {REVISION_TITLE}' section")
    ids = CHAIN_HEADING_RE.findall(sections.get(CHAIN_TITLE, ""))
    for d in _duplicates(ids):
        problems.append(f"body: interview ref {d} defined more than once in ## {CHAIN_TITLE}")
    return set(ids), problems


# ---------------------------------------------------------------------------
# Direction
# ---------------------------------------------------------------------------

def validate_direction(path: Path, mode: str = "auto") -> list[str]:
    try:
        fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
    except (ValueError, yaml.YAMLError) as exc:
        return [f"parse: {exc}"]

    problems = schema_problems(fm, "direction")
    if problems:
        return problems

    refs_defined, chain_problems = chain_ids(body)
    problems.extend(chain_problems)
    problems.extend(field_rules(fm, refs_defined))
    problems.extend(key_field_rules(fm))

    for dim in set(fm["interview_progress"]["asked"]) & set(fm["interview_progress"]["not_asked"]):
        problems.append(f"interview_progress: {dim} listed as both asked and not_asked")

    effective_mode = fm["status"] if mode == "auto" else mode
    if effective_mode == "confirmed":
        problems.extend(confirmed_only_rules(fm))
    return problems


def field_rules(fm: dict, refs_defined: set[str]) -> list[str]:
    """Rules that hold in every mode. A field that claims to be a confirmed hard line must be able to
    prove it, whether or not the direction as a whole is finished (review R22)."""
    problems: list[str] = []
    fields: dict = fm["fields"]
    for fid, f in fields.items():
        for key in ("source_ref", "alt_test_ref", "hard_confirmation_ref"):
            ref = f.get(key)
            if ref and ref not in refs_defined:
                problems.append(f"{fid}.{key}: {ref} is not defined in ## {CHAIN_TITLE}")
        if f.get("alt_test_ref") and f.get("alt_test_ref") == f.get("source_ref"):
            problems.append(
                f"{fid}: alt_test_ref equals source_ref ({f['source_ref']}); an alternative test is a separate exchange "
                "where the interviewer offered a different option, not the user's original statement"
            )
        if f.get("hard_confirmation_ref") and f.get("hard_confirmation_ref") == f.get("source_ref"):
            problems.append(
                f"{fid}: hard_confirmation_ref equals source_ref ({f['source_ref']}); strength must be confirmed in its own exchange"
            )
        if f["kind"] == "hard" and f["status"] == "confirmed" and not f.get("hard_confirmation_ref"):
            problems.append(
                f"{fid}: kind=hard with status=confirmed but no hard_confirmation_ref; "
                "either record the strength confirmation or keep the field pending"
            )
        if f["kind"] == "any" and f["status"] not in ("confirmed", "pending"):
            problems.append(f"{fid}: kind=any means the user confirmed no preference; status must be confirmed or pending, got {f['status']}")
        if f["status"] in ("skipped", "unknown") and f["kind"] == "hard":
            problems.append(f"{fid}: a field the user skipped or does not know cannot be kind=hard")
        for other in f.get("conflicts_with", []):
            if other not in fields:
                problems.append(f"{fid}.conflicts_with: {other} is not a field")
        if f["status"] == "conflict" and not f.get("conflicts_with"):
            problems.append(f"{fid}: status=conflict requires conflicts_with")
    return problems


def key_field_rules(fm: dict) -> list[str]:
    """Each key field must individually qualify, in every mode. Only the count is a confirmed-only rule."""
    problems: list[str] = []
    fields: dict = fm["fields"]
    for fid in fm["key_fields"]:
        f = fields.get(fid)
        if f is None:
            problems.append(f"key_fields: {fid} is not a field")
            continue
        if f["kind"] != "hard":
            problems.append(f"key field {fid} must be kind=hard, got {f['kind']}")
        if f["status"] != "confirmed":
            problems.append(f"key field {fid} must be status=confirmed, got {f['status']}")
        if not f.get("alt_test_ref"):
            problems.append(f"key field {fid} has no alt_test_ref (alternative test never recorded)")
        if not f.get("hard_confirmation_ref"):
            problems.append(f"key field {fid} has no hard_confirmation_ref (strength never confirmed)")
    return problems


def confirmed_only_rules(fm: dict) -> list[str]:
    """What separates a finished direction from a legitimate draft (plan §3.5)."""
    problems: list[str] = []
    kf = fm["key_fields"]
    if not (KEY_FIELDS_MIN <= len(kf) <= KEY_FIELDS_MAX):
        problems.append(f"confirmed: key_fields must have {KEY_FIELDS_MIN}-{KEY_FIELDS_MAX} entries, got {len(kf)}")
    for fid, f in fm["fields"].items():
        if f["status"] == "conflict":
            problems.append(f"confirmed: field {fid} is in conflict; resolve before confirming the direction")
        if f["kind"] == "hard" and f["status"] == "pending":
            problems.append(f"confirmed: hard field {fid} is still pending; confirm its strength or keep the direction as draft")
    return problems


# ---------------------------------------------------------------------------
# Candidate
# ---------------------------------------------------------------------------

def expected_match_status(applicable: set[str], results: dict[str, str], has_unresolved_preference: bool) -> tuple[str, str]:
    """Plan §4.1 step 5. A proven fail on an applicable confirmed hard field outranks everything else."""
    if any(results.get(f) == "fail" for f in applicable):
        return "rejected", "an applicable confirmed hard field failed"
    if has_unresolved_preference or not applicable:
        return "needs_clarification", "unresolved preference or zero applicable confirmed hard fields"
    if any(results.get(f) == "unknown" for f in applicable):
        return "needs_verification", "an applicable hard field is unknown"
    return "eligible_for_comparison", "all applicable hard fields pass"


def candidate_rules(fm: dict) -> list[str]:
    problems: list[str] = []
    pending_fields = set(fm.get("pending_fields") or [])
    for c in fm["candidates"]:
        oid = c["opening_id"]
        app_ids = [a["field_id"] for a in c["applicability"]]
        res_ids = [r["field_id"] for r in c["field_results"]]
        for d in _duplicates(app_ids):
            problems.append(f"{oid}: applicability lists {d} more than once")
        for d in _duplicates(res_ids):
            problems.append(f"{oid}: field_results lists {d} more than once; one result per field, no overriding")
        if _duplicates(app_ids) or _duplicates(res_ids):
            continue  # status computation would be ambiguous

        applicable = {a["field_id"] for a in c["applicability"] if a["state"] == "applicable"}
        not_confirmed = {a["field_id"] for a in c["applicability"] if a["state"] == "not_confirmed"}
        results = {r["field_id"]: r["result"] for r in c["field_results"]}
        for fid in sorted(applicable - set(results)):
            problems.append(f"{oid}: applicable field {fid} has no result; record unknown rather than omitting it")
        for fid in sorted(set(results) - applicable):
            problems.append(f"{oid}: field_results contains {fid} which is not marked applicable")

        ev_ids = [e["id"] for e in c["evidence"]]
        for d in _duplicates(ev_ids):
            problems.append(f"{oid}: evidence id {d} is not unique")
        ev_set = set(ev_ids)
        for r in c["field_results"] + c.get("soft_results", []):
            for ref in r.get("evidence_refs", []):
                if ref not in ev_set:
                    problems.append(f"{oid}: {r['field_id']} cites evidence {ref} which is not in this candidate's evidence list")
            if r["result"] in ("pass", "fail") and not r.get("evidence_refs"):
                problems.append(f"{oid}: {r['field_id']} is {r['result']} without any evidence reference")

        unresolved = bool(not_confirmed or pending_fields)
        expected, why = expected_match_status(applicable, results, unresolved)
        if c["match_status"] != expected:
            problems.append(f"{oid}: match_status is {c['match_status']} but the recorded results imply {expected} ({why})")
    return problems


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

def application_rules(fm: dict) -> list[str]:
    problems: list[str] = []
    consent_labels = {ri.get("field_label") for ri in fm["review_items"] if ri["kind"] == "consent_checkbox"}
    for f in fm["fields"]:
        label = f["label"]
        if f["fill_status"] == "filled":
            if "value_readback" not in f:
                problems.append(f"field {label!r}: filled but no value_readback recorded")
            src = f.get("source")
            if not src:
                problems.append(f"field {label!r}: filled but no source recorded")
            elif src["kind"] in ("fact", "document", "direction_rationale") and not src.get("ref"):
                problems.append(f"field {label!r}: source kind {src['kind']} requires a ref")
    if fm["status"] == "ready_for_review":
        if fm["blockers"]:
            problems.append("ready_for_review with non-empty blockers")
        for f in fm["fields"]:
            if f.get("required_by_form") and f["fill_status"] != "filled" and f["label"] not in consent_labels:
                problems.append(f"ready_for_review but required field {f['label']!r} is {f['fill_status']} and not a listed consent item")
    if fm["status"] in ("submitted_by_user", "abandoned_by_user") and not fm.get("user_outcome"):
        problems.append(f"status {fm['status']} requires user_outcome reported by the user")
    primary = fm["primary_direction"]
    if primary not in {c["direction_id"] for c in fm["candidate_refs"]}:
        problems.append(f"primary_direction {primary} is not among candidate_refs")
    return problems


# ---------------------------------------------------------------------------
# Facts
# ---------------------------------------------------------------------------

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
    for d in _duplicates([i["id"] for i in data["items"]]):
        problems.append(f"fact id {d} is not unique")
    for d in _duplicates([doc["id"] for doc in data.get("documents", [])]):
        problems.append(f"document id {d} is not unique")
    for item in data["items"]:
        if item["status"] == "confirmed" and not item.get("confirmed_at"):
            problems.append(f"{item['id']}: confirmed fact without confirmed_at")
        if item["category"] == "work_authorization" and item["source"]["kind"] != "user_statement":
            problems.append(f"{item['id']}: work_authorization must come from the user's own statement")
    return problems


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def validate_frontmatter_only(path: Path, schema_name: str) -> list[str]:
    try:
        fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    except (ValueError, yaml.YAMLError) as exc:
        return [f"parse: {exc}"]
    problems = schema_problems(fm, schema_name)
    if problems:
        return problems
    if schema_name == "candidate":
        problems.extend(candidate_rules(fm))
    if schema_name == "application":
        problems.extend(application_rules(fm))
    return problems


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
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
