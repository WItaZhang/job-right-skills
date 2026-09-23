# Direction template: field guide

The machine-checked definition is `schema/direction.schema.json`; the cross-field rules live in `scripts/validate.py`. This page explains what each part means and why it exists.

## File shape

```
---
<YAML frontmatter: snapshot of the current revision>
---
# <title>
<one or two plain sentences: what this direction is>
## 追问链
### I-001 … ### I-nnn   (one entry per exchange)
## 修订记录
- r1 …                 (one line per revision: old value → new value, reason)
```

The frontmatter is a snapshot. It is overwritten on each revision. History is in the body, so old values are never lost and the YAML never accumulates duplicate keys.

## Top level

| Key | Meaning |
|---|---|
| `id` | `dir-001`, stable for the life of the direction |
| `title` | Plain-language name; should read as the key fields in one line |
| `revision` | Increments on every change to a field's value, kind, status or scope |
| `status` | `draft` or `confirmed`. Confirmed has rules (below). Draft is a legitimate resting state |
| `created_at`, `updated_at` | Timestamps with time zone |
| `key_fields` | 2–4 field ids that are the essence of the direction. Must be confirmed hard fields. Used for the title and for search focus. All confirmed hard fields still participate in filtering; key fields are not the only ones checked |
| `fields` | Map of field id → field record |
| `search_hints.keywords` | Discovery terms for find-openings |
| `search_hints.deprioritize` | Terms that lower discovery ranking. Never evidence for rejecting an opening; disclosed to the user as search bias |
| `open_questions` | What you would ask next |
| `interview_progress.asked` / `not_asked` | Dimensions touched vs. untouched. Progress, not field status |
| `split_from` | Set when this direction was split from another after the user confirmed both routes stand alone |

## Field id

Dotted path, one independently confirmable condition per id: `location.city_profile`, `location.workplace_type`, `company.size`, `company.funding_stage`, `role.nature`, `industry`, `compensation.base`. Do not bundle two conditions into one id unless the user stated and tested them as one thing.

## Field record

| Key | Meaning |
|---|---|
| `value` | Whatever shape fits: string, list, range object, or `null` when unknown |
| `kind` | `hard` (would refuse otherwise), `soft` (matters, negotiable), `any` (user confirmed no preference), `unspecified` (strength not yet asked or answered) |
| `status` | `confirmed`, `pending` (stated, strength or meaning not yet confirmed), `conflict` (blocked by another field in the same scope), `skipped` (user chose to skip), `unknown` (user does not know) |
| `scope` | `valid_from`, `valid_until`, `roles`, `locations`, `note`. A field outside its scope does not apply to an opening and is listed as not applicable, not as failed |
| `observable_criteria` | The user's own answer to "how would you recognise this?" for abstract attributes |
| `examples` | Illustrations, not restrictions |
| `allowed_values` | A closed list, only when the user closed it |
| `source_ref` | Interview entry where the user first stated this |
| `alt_test_ref` | Entry where an alternative with the same attribute was offered and answered. Required for key fields |
| `hard_confirmation_ref` | Entry where the user said they would refuse otherwise. Required for every confirmed hard field |
| `rationale`, `note` | Free text, short |
| `conflicts_with` | Field ids in blocking conflict; required when `status: conflict` |

### kind and status combinations

| Situation | kind | status |
|---|---|---|
| Stated, meaning confirmed, would refuse otherwise | hard | confirmed |
| Stated "must", strength not yet asked | hard or unspecified | pending |
| Stated, matters, negotiable | soft | confirmed |
| Stated "no preference" | any | confirmed |
| "I don't know" | unspecified | unknown |
| "Skip that" | unspecified | skipped |
| Two hard fields cannot both hold in the same scope | hard | conflict (both) |

A skipped or unknown field cannot be `kind: hard`: nobody confirmed anything.

## Confirmed-direction rules

`status: confirmed` requires all of:

1. `key_fields` has 2–4 entries.
2. Each key field is `kind: hard`, `status: confirmed`, with both `alt_test_ref` and `hard_confirmation_ref`.
3. No field has `status: conflict`.
4. No `kind: hard` field has `status: pending`.
5. Every `kind: hard, status: confirmed` field has a `hard_confirmation_ref`.

A draft is exempt from 1, 2, 4 and 5 but must still be structurally valid and every reference must exist in `## 追问链`.

## Interview entry (`### I-xxx`)

```
### I-007
- 时间：10:11
- 用户原话：可以啊，深圳我去过，那种感觉挺像的。新加坡也行。
- 访谈者问题：那么深圳、新加坡这类同样年轻、科技公司密集的城市，可以吗？
- 结论：alt_test 通过。属性含义确认为城市氛围，美国不是条件。
```

Ids are unique within the file and never reused. Verbatim words are private and stay in the workspace.

## Revision log line

```
- r4 2026-09-23 11:20：I-024 确认 workplace_type_after_move 为 soft（旧值 kind=hard/status=pending，新值 kind=soft/status=confirmed，原因：用户明确说是希望不是必须）。
```

Always: revision, time, which field, old value, new value, the user's reason, and the entry id that justifies it.
