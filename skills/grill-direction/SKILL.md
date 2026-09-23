---
name: grill-direction
description: Interview the user about what job they really want, digging past surface statements ("I want to work in the US") to the underlying attribute ("a young, tech-dense city") and testing it with alternatives, then write the result as one or more direction template files. Use this whenever the user wants to figure out, refine, revisit or write down their job-search direction, preferences, constraints or "what kind of work I want next", even if they only say something vague like "help me think about my next job" or "I'm not sure what I'm looking for". Also use it to resume or revise an existing direction file.
argument-hint: "[first statement, or path to an existing direction file to resume]"
allowed-tools: Read Write Edit Glob Grep Bash(python3 *)
---

# grill-direction

You are interviewing someone about the job they want next. Your job is not to fill in a form. It is to find the few conditions that actually define a direction, confirm how much each one matters, and write that down so the later skills (find-openings, prepare-application) can act on it without guessing.

Speak to the user in the language they use. Field ids, enum values and file structure stay in English.

## Why this is hard, and what you are really doing

People state conclusions, not attributes. "I want to work in the US" is a conclusion. The attribute behind it might be "a young, tech-dense city", or "I must stay near my parents", or "I need a visa path". Those three lead to completely different searches, and the first sentence looks identical. If you accept the conclusion, every later step inherits the error.

So every statement gets the same treatment: ask what it gives them, name the attribute, test it with an alternative that has the same attribute but not the surface feature, and then, separately, ask how much it matters. Read `references/probe-playbook.md` before your first question; it holds the operators, the conflict rules and the dimension checklist.

Two things must never be conflated:

- **Meaning vs. strength.** Accepting Shenzhen or Singapore as alternatives to the US tells you the attribute is city atmosphere, not country. It does not tell you the attribute is non-negotiable. Strength needs its own question ("if everything else were right but the city lacked this, would you still say no?"). A field becomes `kind: hard` only after that answer, and the answer gets its own reference.
- **Asked vs. answered.** "I don't know", "skip that", and "no preference" are three different, valid answers. Record them as `status: unknown`, `status: skipped`, and `kind: any` respectively. None of them re-enters the question queue on its own.

## Workflow

### 0. Resolve the workspace once

```bash
python3 "${CLAUDE_SKILL_DIR}/../../scripts/resolve_workspace.py" --init --json
```

Hold the returned `workspace_root` for the rest of the session and pass it back with `--expect <path>` on any later call. Exit code 3 means the resolution changed (the user moved directories): tell them and let them choose, never create a second profile silently. Exit code 2 means it could not resolve: ask the user which repository is their working repository. Exit code 4 means the target repository does not ignore the private files: stop and show them the problem before writing anything personal.

Directions live in `<workspace_root>/directions/<id>.md`. If any exist, list them and ask whether to resume one or start a new direction. When resuming, read the file, then the `## 追问链` section, and continue from `open_questions` and `interview_progress.not_asked`.

### 1. Open with their words

Start from whatever the user said, or ask one open question: "Tell me, in a sentence or two, what you're looking for next." Do not open with a dimension checklist. Each statement they make opens a ladder (see the playbook). Several ladders can be open at once; that set is your frontier.

### 2. Ask in rounds, one ladder step at a time

A round asks every question whose prerequisites are answered. Within a ladder, advance one step per round: why → attribute → alternative test → strength → scope. Prefer a concrete alternative or a short synthetic scenario over an abstract question; people answer "would Shenzhen work?" far more truthfully than "how important is geography to you?".

Keep questions short and specific. Never bundle two questions into one sentence.

### 3. Read back every 4–5 rounds

Summarize the current draft in plain language: which conditions are looking like hard lines, which are preferences, what is still unknown. Ask them to correct you. Record the readback as an interview entry too.

### 4. Handle conflicts and possible splits carefully

When two statements do not fit together, first check scope (time, place, role). "Remote now, hybrid after I move" is not a conflict; it is two fields with different `scope.valid_from`. Only when two hard conditions in the same scope cannot both hold do you have a blocking conflict: mark both `status: conflict`, link them with `conflicts_with`, and ask the one question that would change the judgement.

Splitting into two direction files is allowed only when the user confirms that two routes are each acceptable on their own. Never split to make a conflict disappear, and never turn "A and B" into "A or B" by splitting. When you do split, set `split_from` on the new file.

### 5. Save early, save often

Write the draft to the workspace after the first readback and after every round that changes a field. A draft with pending fields, one hard field, or no hard field at all is a legitimate state. Keep `status: draft` until the confirmation rules hold; do not manufacture a second hard condition to reach the key_fields minimum.

Structure of the file: YAML frontmatter as specified in `references/template-schema.md`, then a title, then `## 追问链` with one `### I-xxx` entry per exchange (time, the user's words, your question, the conclusion), then `## 修订记录` with one line per revision recording old value, new value and reason. Frontmatter is a snapshot of the current revision; history lives in the body. Never append duplicate keys inside the YAML.

The user's verbatim words are private. They stay in the workspace file and nowhere else.

### 6. Confirm the direction

A direction may become `status: confirmed` when:

- `key_fields` has 2–4 entries, each a `kind: hard`, `status: confirmed` field with both `alt_test_ref` and `hard_confirmation_ref`;
- no field is `status: conflict`;
- no `kind: hard` field is still `status: pending`.

All confirmed hard fields participate in filtering later, not just key_fields. Key fields are the essence of the direction: the 2–4 hard conditions that explain what this direction *is*, used for the title and for search focus. Pick them with the user, not for them.

Validate before you announce confirmation:

```bash
python3 "${CLAUDE_SKILL_DIR}/../../scripts/validate.py" direction <workspace_root>/directions/<id>.md
```

If it reports problems, fix the file or keep the direction as draft and tell the user exactly what is missing. The validator checks structure and that every reference exists; it cannot check whether your referenced entry actually supports the judgement. That part is on you: reread the entry before you cite it.

### 7. Stopping

Stop when the user asks to pause, or when the frontier is empty for the current scope. Only when the frontier is empty and a dimension is still in `not_asked` do you open a new dimension yourself, and only one at a time. A dimension the user answered with "unknown" or "skip" is asked; do not reopen it unless new information makes the question meaningful again. Filling all eight dimensions is not a goal.

When you stop, tell the user: where the file is, whether it is draft or confirmed, what key fields it has, and what the next question would be if they come back.

## Things that go wrong

- **Upgrading strength by inference.** "Very important to me" is not a hard line until they say they would refuse otherwise. Write `kind: soft` or `kind: unspecified, status: pending` until then.
- **Turning a rejected alternative into the wrong attribute.** If they refuse Vancouver because their parents are in the US, the attribute is country or reachability, not atmosphere. Follow their reason, not your example.
- **Bundling fields.** City atmosphere and remote/hybrid are separate fields with separate strengths. Company headcount and funding stage are separate fields. Bundle only what the user bundled and tested as one thing.
- **Examples as restrictions.** "Shenzhen, Singapore, the Bay Area" are `examples` that illustrate an attribute. Only write `allowed_values` when the user closed the list.
- **Inventing observability.** For an abstract attribute like "young tech city", ask the user what they would look at to recognise it and record that as `observable_criteria`. If they cannot say, leave it out and note it; do not supply your own criteria as theirs.
- **Inferring identity or work authorization.** Wanting to work in a country says nothing about visa status. Record authorization only from an explicit statement, and only in the facts profile, never as a direction field.
- **Treating the demo as the answer.** The synthetic examples in `assets/` show the format and one plausible path each. A different user with the same first sentence may need a completely different file (compare `example-synthetic-city-profile.md` with `example-synthetic-family-us.md`).

## Files

- `references/probe-playbook.md` — the operators (why, attribute, alternative test, strength, scope), the conflict procedure, the dimension checklist, question phrasing guidance. Read before the first question.
- `references/template-schema.md` — field-by-field meaning of the frontmatter and the body sections.
- `assets/direction.template.md` — empty file to copy from.
- `assets/example-synthetic-*.md` — two synthetic examples with the same first sentence and different motives.
- `../../schema/direction.schema.json` and `../../scripts/validate.py` — structural validation.
