# Probe playbook

How to take one statement from a user and turn it into a field whose meaning, strength and scope they have actually confirmed. Everything here exists because the cheap alternative, writing down what they said and moving on, produces direction files that look complete and search for the wrong thing.

## 1. The ladder

Every statement starts a ladder. Advance one ready step per ladder in a round; a round usually covers 6–8 different themes. Record each answered question as its own `### I-xxx` entry, preserving the theme label; save the batch together. Fields cite the relevant entries, not a catch-all reference to the whole batch. If a user volunteered a clear answer to a later step, reuse that evidence rather than mechanically asking again.

| Step | Purpose | Typical question | What you write |
|---|---|---|---|
| stated | Capture their words | (none, or the opening question) | entry with the verbatim statement; this becomes `source_ref` |
| why | Get past the conclusion | "What does X give you that you would miss without it?" / "If you could only keep one reason for X, which?" | an entry; often you need two why-steps before an attribute appears |
| attribute | Name the property and how they would recognise it | "How would you tell whether a city has that feel? What would you look at?" | field id, `value`, `observable_criteria` (their words), `examples` |
| alt_test | Test the meaning with a different surface, same attribute | "Would Shenzhen or Singapore work, then?" / "A 40-person independent unit inside a large company, with its own systems?" | `alt_test_ref`. Accepted: the attribute is what you named. Refused: follow *their reason* for refusing; it usually reveals another attribute or another field |
| strength | Test how much it matters, separately | "If a role had everything else right but not this, would you still say no?" | `kind` (hard / soft / any) and, for hard, `hard_confirmation_ref` |
| scope | Find when and where it applies | "From when does this apply? Does it change after the move / after the contract ends?" | `scope.valid_from`, `valid_until`, `roles`, `locations` |

Notes on individual steps:

- **why** is where most interviews stop too early. "More opportunities" is still a conclusion. Ask again, differently. A useful second question is "and what would you be doing on an ordinary Tuesday that you can't do now?"
- **alt_test** must change the surface feature while keeping the attribute. Offering "New York instead of San Francisco" tests nothing if the attribute was "in the US". Offering "Shenzhen" tests whether it was really about the US.
- **strength** needs a scenario with a real cost. "Everything else is great" makes the question bite. If the user hedges ("depends"), it is `soft`, not hard. If they name a condition under which they would accept, that condition may be a scope or a new field.
- **scope** applies to any field, but ask it whenever the user mentions a future event: a move, a contract ending, a visa date, a family situation changing.

## 2. Contrast scenarios

When a user cannot answer strength in the abstract, give them two or three short, neutral, clearly synthetic scenarios and ask which they would take and what they would be giving up. Keep them balanced; do not hide a trade-off inside one option. Always include an exit: "neither" and "I don't know yet" are answers.

Example (city atmosphere vs. content):

> A. A company doing exactly the AI infra work you described, fully remote, in a quiet mid-sized city.
> B. A company in a dense, young tech city, doing adjacent but not identical work.
> Which would you pick, and what would you be giving up?

The choice tells you which attribute is stronger. The explanation tells you why, and often names the field.

## 3. Conflict procedure

Trigger: two recorded statements that cannot both be satisfied.

1. **Check scope first.** Different time, place or role is not a conflict. Add or refine `scope` on both fields and move on.
2. **Classify what remains in the same scope.**
   - Two hard conditions that cannot both hold: blocking conflict. Mark both `status: conflict`, fill `conflicts_with` on each, and ask the smallest question that would change the judgement. Do not guess which one wins; do not assume the later statement overrides the earlier one.
   - A hard condition and a soft preference: not a conflict. Record the trade-off in the soft field's `rationale`.
   - Two soft preferences in tension ("I like startups but I value stability"): record both, ask them to describe the range of risk they accept. Do not tell the user they are contradicting themselves.
   - Two routes the user says they would each accept on their own: a candidate for a split (section 4).
3. **Record the resolution** in `## 修订记录` with old value, new value and the user's stated reason.

## 4. Splitting a direction

Split only when the user explicitly confirms that two routes are each acceptable independently. Ask it in those words: "Are these two separate things you'd each be happy with, or do you want both at once?" If they want both at once, it is one direction with two hard fields, even if that makes the search hard. Never split to make a conflict disappear.

When splitting: create the new file with `split_from: <old id>`, copy only the fields that belong to the new route, and note the split in both files' revision logs.

## 5. Dimension checklist

Use this to select useful themes for the opening batch and notice gaps later, not as a compulsory questionnaire. Relevant dimensions in `interview_progress.not_asked` can join a batch while other ladders are active, before the time budget moves to wrap-up. Prioritize follow-ups to answers already given. Move a dimension to `asked` as soon as you have asked one question in it, whatever the answer; an omitted answer stays in `open_questions` without being mislabeled unknown or skipped. No need to cover every dimension.

| Dimension | What you are trying to learn | Opening question that tends to work |
|---|---|---|
| 兴趣动力 | Which problems they keep returning to; what they want less of | "What part of your current work would you protect if you changed everything else?" |
| 人生方向 | What this change is for; time horizon | "What should be different a year after you start the new job?" |
| 压力承受 | Which pressures are fine, which are unsustainable | "Describe a week at work that you'd consider too much. What made it too much?" |
| 风险容忍 | Uncertainty they accept: company stage, comp structure, contract stability | "If a company might not exist in two years but the work is exactly right, how do you feel?" |
| 角色与成长 | IC vs. management, decision scope, mentoring, **target level** | "Do you want to be the person doing it or the person deciding who does it?" then "What level are you aiming for next: same as now, one up, or does it not matter?" |
| 地点与时间 | Remote/hybrid/onsite, regions, time zones, relocation, from when | "Where will you physically be, and when does that change?" |
| 薪酬与身份 | Floors and their basis (currency, period, base vs total); authorization as stated by them | "Is there a number below which you'd stop the conversation? In what currency, per year or month, base or total?" |
| 团队环境 | Collaboration style, meetings, feedback, team size | "Think of the best team you were on. What did an ordinary day look like?" |

Target level (`role.level`): ask it whenever the user has work experience, because boards list interns, new grads, mid, senior and staff roles side by side and a direction without a level pulls in all of them (live run 2 returned only internships and new-grad roles). Their *current* level is a fact for the facts profile; the level they *want* is a preference. Record `value` as the user's words mapped to a coarse band (intern / new_grad / mid / senior / staff_plus / any), with `examples` of titles they consider equivalent. It becomes `kind: hard` only after the strength question like any other field; "senior or above" is often soft ("I'd take a strong mid-level role at the right company"). Also write the level vocabulary into `search_hints`: keywords for the wanted bands, deprioritize for the ones they exclude (e.g. "intern", "internship", "new grad", "university").

Compensation: never compare numbers with different bases. If they give a monthly total and a yearly base, record both with their `basis` and leave the comparison as an open question.

Identity and authorization: record only what they state, in the facts profile, never inferred from where they want to work.

## 6. Phrasing

- One short question per numbered theme; usually 6–8 themes per message. Keep the theme's number and label in later batches. Ask fewer when fewer useful questions are ready or time is short; no padding.
- Concrete beats abstract: name a city, a headcount, a scenario.
- Reflect briefly before the batch, then ask the next ready question for each theme. For example: "It sounds like tech-community density matters more than the country; correct me if that misses it." Do not add a separate confirmation question before every probe.
- Do not recommend answers. You can offer alternatives to test meaning; you do not tell them what they should want.
- Accept "I don't know" and "skip" the first time. Record the status and move on.
- Accept partial, unnumbered or continuous spoken answers. Do not infer agreement from omissions, repeat every unanswered question, or demand a numbered response before continuing.
- When they pause, save and tell them where you are.

## 7. Orientation, progress and closing readback

At the start, briefly explain the outcome, time estimate and controls, in their language. For example:

> We'll turn what you want from your next job into a saved direction draft, showing deal-breakers, preferences and what is still unclear. Plan on 20–30 minutes; in voice we'll aim to wrap up within 30. I'll group short questions by theme. You can answer by number or just talk, answer only some, skip, say you don't know, correct me, or pause and return later.

Do not wait for an acknowledgement before the first batch. Reuse facts from the user's opening rather than asking them again. Between batches, summarize only new understanding and the purpose of the next questions. For example:

> We have a clearer picture of the work and location you want. Next we'll test alternatives so I don't mistake a preference for a deal-breaker.

Use the actual time checks and 20/25/30-minute checkpoints in `SKILL.md`. Report remaining time approximately, not as a guarantee. At wrap-up, provide a compact readback:

> Here is what I have so far.
> Hard lines (would refuse otherwise): …
> Preferences (matter, but negotiable): …
> Target level: …
> No preference: …
> Not yet known / skipped: …
> Still open, saved for another time: …
> Saved draft / confirmed direction: …
> Next step: …

Invite corrections without making an answer compulsory for saving or stopping. Record corrections as interview entries. A broad acknowledgement cannot substitute for an unanswered alternative test or strength question. If time is up, leave those gaps in a draft.

## 8. How parallel follow-ups work (synthetic)

An opening batch can ask about work content, location, role, level, workload, risk and team environment, each with a stable number and label. Suppose the user answers only three themes:

| Theme | User's answer | Next ready question | What stays unresolved |
|---|---|---|---|
| 1. Work | "AI infra; I enjoy building systems others use." | "Would developer tooling outside AI still give you that satisfaction?" | Whether AI itself matters; strength |
| 2. Location | "The US, because I want a dense tech community." | "Would Singapore or Shenzhen work if they offered that community?" | Alternative acceptance; strength |
| 3. Role | "IC; I don't want performance reviews or hiring." | "Would technical leadership without people management work?" | Whether that alternative fits; strength |

The next batch has these three follow-ups, not six to eight invented extras. Keep unanswered level/workload/risk/team questions in `open_questions`; do not repeat them automatically or assign answers. If the user then accepts the location alternative, that establishes meaning, not a hard line. Its strength question belongs in the following batch alongside the next ready questions for work and role. Once a theme is settled, drop it from the active batch.
