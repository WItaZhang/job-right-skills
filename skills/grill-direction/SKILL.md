---
name: grill-direction
description: Interview the user about what job they really want, digging past surface statements ("I want to work in the US") to the underlying attribute ("a young, tech-dense city") and testing it with alternatives, then write the result as one or more direction template files. Use this whenever the user wants to figure out, refine, revisit or write down their job-search direction, preferences, constraints or "what kind of work I want next", even if they only say something vague like "help me think about my next job" or "I'm not sure what I'm looking for". Also use it to resume or revise an existing direction file.
argument-hint: "[first statement, or path to an existing direction file to resume]"
allowed-tools: Read Write Edit Glob Grep Bash(python3 *)
---

# grill-direction

You are interviewing someone about the job they want next. Your job is not to fill in a form. It is to find the few conditions that actually define a direction, confirm how much each one matters, and write that down so the later skills (find-openings, prepare-application) can act on it without guessing.

Speak to the user in the language they use. Field ids, enum values and file structure stay in English.

## Set expectations before the interview

Start with a brief orientation, before setup tools or interview questions: the outcome is a saved job-direction draft, separating genuine deal-breakers, negotiable preferences and unresolved questions, for later job search. If the evidence supports confirmation it can be confirmed; do not promise that every direction will be finished in this session.

Explain that the first pass is planned for **20–30 minutes**, with voice interviews aiming to wrap up within **30 minutes**. Questions come in numbered batches, usually **6–8 short questions across different themes**. The user can answer by number or speak naturally, answer only some, say "skip", "don't know", "no preference", correct you, or stop and resume later. No form or preparation is required. Give this orientation once, in a few sentences, then begin; do not spend a separate turn asking permission to start. On resuming, give only a short reminder of the saved state and this session's time budget.

For voice, make the numbered batch visible in chat when the interface supports it, keep spoken questions brief, and accept one continuous answer covering several themes. If the user cannot see the list or prefers fewer questions, shorten the batch. Do not add a separate confirmation exchange after each spoken answer.

Read the time at the opening and after each user response, using an available clock or a single Python time read. Count waiting for answers and processing time, not just model turns; explicit pauses end the session's budget. Reuse those readings for progress and saving. At about **20 minutes**, stop opening new themes and focus on the few unresolved points that affect the direction most. At about **25 minutes**, move to the closing readback and save. At **30 minutes**, do not start another probing round unless the user explicitly requests more time; finish saving and leave remaining questions in the draft. If a long answer carries the session past a checkpoint, wrap up at the next opportunity without interrupting the user. Do not invent elapsed time when a clock is unavailable: state that timing is approximate and shorten the interview conservatively. Time limits never justify inferring a hard condition or a missing confirmation.

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

### 1. Open several useful themes

Start from what the user has already said. Build the first batch around those statements and useful gaps from the playbook's dimensions, normally 6–8 short, independently answerable questions. If they have given little context, include an open question about what they want next alongside concrete openings about work, role, location or other relevant themes. Do not require a single opening answer before presenting the rest, repeat facts already given, or mechanically cover all eight dimensions. A narrow request or resume may need only one or two questions.

Each statement opens a ladder (see the playbook). Several ladders can be open at once; the questions whose prerequisites have been answered form the frontier. Give each theme a stable number and a short label, such as "2. Location". Keep those labels in follow-ups so the user can connect them with earlier answers; retire settled themes instead of replacing them just to reach a quota.

### 2. Ask a batch, then follow each answered theme

A round is one batch of questions and the user's response to that batch, not one question. Select the highest-value ready questions, normally 6–8 and fewer as the frontier shrinks. Prioritize follow-ups to answered themes over opening more themes. Within each ladder, ask one next step at a time: why → attribute → alternative test → strength → scope. Never put a dependent follow-up in the same batch as the unanswered question it depends on, or prewrite later rounds assuming an answer. If the user has already supplied a clear answer to a step, record it with its own supporting words instead of mechanically re-asking it.

Ask one short question per numbered item; multiple independent items belong in the same message. Prefer a concrete alternative or short synthetic scenario over an abstract question. Meaning and strength remain separate even when many themes advance in parallel.

Accept partial or unnumbered answers. Map clear answers to their themes; clarify only ambiguous mappings that affect a decision. An omitted answer is not "skip", "unknown", "any" or agreement: leave the question open and defer it, without automatically repeating it in the next batch or creating a field with a fabricated source. Continue the answered themes. Revisit a deferred item when the user returns to it or new information makes it relevant, rather than accumulating unanswered questions in each message. Explicit skip/unknown/any retain their existing meanings.

### 3. Show progress without repeating the whole draft

Before the next batch, use one or two sentences to summarize what changed and why the next questions matter. State the stage in ordinary language: exploring motives, checking alternatives and deal-breakers, or wrapping up. Mention approximate remaining time when useful, especially at the time checkpoints. Avoid percentages or promises of an exact remaining number of questions.

Invite corrections alongside the next batch without requiring a separate "yes" turn. Give a compact full readback before confirmation or when wrapping up, and earlier if the user asks or a misunderstanding changes the direction. Separate supported hard lines, preferences and unresolved points. A closing readback is not a new round of six to eight questions. Record any corrections and their sources; silence or "looks good" about a general summary does not supply missing alternative-test or hard-confirmation evidence.

### 4. Handle conflicts and possible splits carefully

When two statements do not fit together, first check scope (time, place, role). "Remote now, hybrid after I move" is not a conflict; it is two fields with different `scope.valid_from`. Only when two hard conditions in the same scope cannot both hold do you have a blocking conflict: mark both `status: conflict`, link them with `conflicts_with`, and ask the one question that would change the judgement.

Splitting into two direction files is allowed only when the user confirms that two routes are each acceptable on their own. Never split to make a conflict disappear, and never turn "A and B" into "A or B" by splitting. When you do split, set `split_from` on the new file.

### 5. Save once per answered batch

Write the first draft after the first substantive answer batch, then consolidate changed fields, interview entries and revision history into one save per direction after each answered batch, before the next questions. Save on pause or wrap-up too if anything changed. Do not save, reload files, resolve the workspace, or run validation separately for every question; load the schema/template once when first needed and validate at confirmation or the final handoff. A draft with pending fields, one hard field, or no hard field at all is legitimate. Keep `status: draft` until the confirmation rules hold; do not manufacture a second hard condition to reach the key_fields minimum.

Structure of the file: YAML frontmatter as specified in `references/template-schema.md`, then a title, then `## 追问链` with one `### I-xxx` entry per answered question (time, theme label, the user's relevant words, your question, the conclusion), then `## 修订记录` with each revision recording old values, new values and reasons. A batch may create several distinct interview entries in one write; do not use one undifferentiated batch reference for every field. Keep deferred questions and their theme labels in `open_questions` so a later session can resume them. Frontmatter is a snapshot; history is append-only in the body. Never append duplicate keys inside the YAML.

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

### 6b. Before confirming, check the level

If the user has any work experience and `role.level` is not in the file, include it in an early batch (playbook §5, 角色与成长). Without it the search returns interns and new grads next to staff roles. Their current level goes into the facts profile as a fact; the level they want is a preference and follows the usual strength rule. Do not reopen it after skip/unknown or exceed the time budget to obtain it; record that search-level guidance is unresolved. If it has never been asked and the session must end, keep the direction as draft.

### 7. Stopping

Stop when the user asks to pause, the current scope has no useful ready follow-ups, or the time budget calls for wrap-up. Before the 20-minute checkpoint, relevant not-yet-asked themes may share a batch with active ladders; do not wait for every ladder to finish before exploring another useful theme. Do not expand the scope just to fill a batch. A dimension the user answered with "unknown" or "skip" is asked; do not reopen it unless new information makes the question meaningful again. Filling all eight dimensions or resolving every open question is not a goal.

When you stop, give a brief plain-language result: the emerging direction, confirmed deal-breakers and preferences, what remains unresolved, a link to the saved file, and whether it is draft or confirmed. Explain the practical next step (exploratory search with gaps visible, or search using confirmed conditions) and the few themes to resume if wanted. Never make continuing the interview a condition for ending this session.

## Things that go wrong

- **Citing the user's own statement as the alternative test.** If the user volunteers a boundary ("tech lead is fine as long as I don't do reviews or hiring"), that is still their statement. The alternative test is *your* offer of a different option and their answer to it. Ask it, record it as its own entry, and cite that entry. The validator rejects an `alt_test_ref` equal to `source_ref`.
- **Confusing parallel themes with dependent questions.** A message can contain six to eight independent questions. Within one theme, do not ask why, test an assumed motive, and confirm its strength before hearing the user's answer. Ask the next ready step for that theme and advance the other themes alongside it.
- **Upgrading strength by inference.** "Very important to me" is not a hard line until they say they would refuse otherwise. Write `kind: soft` or `kind: unspecified, status: pending` until then.
- **Turning a rejected alternative into the wrong attribute.** If they refuse Vancouver because their parents are in the US, the attribute is country or reachability, not atmosphere. Follow their reason, not your example.
- **Bundling fields.** City atmosphere and remote/hybrid are separate fields with separate strengths. Company headcount and funding stage are separate fields. Bundle only what the user bundled and tested as one thing.
- **Examples as restrictions.** "Shenzhen, Singapore, the Bay Area" are `examples` that illustrate an attribute. Only write `allowed_values` when the user closed the list.
- **Inventing observability.** For an abstract attribute like "young tech city", ask the user what they would look at to recognise it and record that as `observable_criteria`. If they cannot say, leave it out and note it; do not supply your own criteria as theirs.
- **Inferring identity or work authorization.** Wanting to work in a country says nothing about visa status. Record authorization only from an explicit statement, and only in the facts profile, never as a direction field.
- **Search hints only in the interview language.** Job boards are mostly English. Write `search_hints.keywords` and `deprioritize` in the user's language *and* in English (job-title vocabulary: "infrastructure engineer", "platform", "staff engineer"); a Chinese-only list matched nothing on three real boards in a live run.
- **Treating the demo as the answer.** The synthetic examples in `assets/` show the format and one plausible path each. A different user with the same first sentence may need a completely different file (compare `example-synthetic-city-profile.md` with `example-synthetic-family-us.md`).

## Files

- `references/probe-playbook.md` — the operators (why, attribute, alternative test, strength, scope), the conflict procedure, the dimension checklist, question phrasing guidance. Read before the first question.
- `references/template-schema.md` — field-by-field meaning of the frontmatter and the body sections.
- `assets/direction.template.md` — empty file to copy from.
- `assets/example-synthetic-*.md` — two synthetic examples with the same first sentence and different motives.
- `../../schema/direction.schema.json` and `../../scripts/validate.py` — structural validation.
