---
name: prompt
description: Turn a rough request into an approved, implementation-ready specification through a guided requirement interview — classify the request, read the codebase first for technical work, ask only what is missing, write a structured XML spec, get approval, then execute it (or hand it off) and validate the result against its acceptance criteria. Use when the user runs /prompt, says "spec this out", "interview me", "turn this into requirements", "clarify before you build", or gives a vague feature, bug, integration, refactor, design, research, documentation, planning or content request that would otherwise need guessing. Other skills (e.g. Agentic Playbook) call it in handoff mode to gather requirements.
---

# /prompt — requirement interview → approved spec → execution

Do not start building from a vague request. Gather what's missing, write it down in a fixed shape, get it approved, then do exactly that — and prove it with the acceptance criteria.

```
request ─► classify ─► inspect code ─► interview ─► spec ─► APPROVAL ─► execute | save | hand off ─► validate
                       (technical)     (only what's missing)   (gate)
```

## Principles

1. **Never guess.** Unknowns are asked or recorded as `<TBD: what → ask <owner>>`, never filled with a plausible value.
2. **Read before asking.** For technical work, the code answers first; the user confirms only what matters.
3. **Ask the minimum.** Skip what the request, the code or the calling skill already answers. Stop when every required section can be filled.
4. **One fixed shape.** Every spec has the same sections, so specs compare, review and hand off cleanly (`references/spec-format.md`).
5. **Approval is the gate.** Nothing is executed before the user approves the spec.
6. **Prove it.** Every requirement has an acceptance criterion; validation reports each one with evidence.
7. **No sensitive values.** Placeholders only (`<API_KEY>`, `<USER_EMAIL>`, `<PATIENT_NAME>`, `<MRN>`, `<CARD_NUMBER>`).

## Every run — load settings

Read config, highest precedence first: `.prompt.yml` at the repo root → `$PROMPT_CONFIG` or `~/.config/prompt/config.yml` → `config/default.yml`. A calling skill may pass settings (e.g. `mode: handoff`, `depth: quick`); those win for that run. The user's words win over everything ("quick", "deep", "just save it"). All options: `references/config.md`.

## Modes

| Mode | After approval | Used when |
|---|---|---|
| `execute` (default) | Do exactly the spec's scope, then validate | The user wants the work done |
| `save` | Write the spec to `save_to` (`templates/spec.md`), stop | "Just spec it", planning ahead, review by others |
| `handoff` | Return the approved spec to the calling skill, stop — never execute | Called by another skill (Agentic Playbook saves it to `00-REQUIREMENTS.md`) |

A calling skill that asks for a spec is always `handoff`, whatever config says.

## Workflow

### 1. Read the request
Note what it already answers: outcome, users, scope, constraints, examples, files. Extract any IDs, links or pasted material.

### 2. Classify
**Technical** (code, APIs, infra, data, bugs, refactors, architecture) or **general** (docs, research, planning, process, content, analysis). Mixed → technical. Then the subtype — `feature`, `bug`, `integration`, `refactor`, `architecture`, `data`, `research`, `documentation`, `planning`, `content`, `analysis` — which picks the question set. Say both in one line.

### 3. Inspect before asking (technical)
Use the `code-analysis` capability (your mapped skill, a subagent, else read/search): entry points, existing patterns to follow, data model, tests, config, related history. State what you found — with file paths — and turn it into confirmations rather than open questions. No code access (chat-only) → ask for the relevant files or say what you're assuming.

### 4. Interview
Questions from `references/question-bank.md` for the subtype, at the configured depth, plus `extra_questions` whose `when` matches.
- `quick` ≤ 3 questions · `standard` ≤ 8 · `deep` — every section probed, no cap.
- One **topic** per message (default): up to 4 tightly related questions, each with 2–4 lettered options and a marked recommendation, so one reply like `1b 2a` answers them. `one_question_at_a_time: false` = every remaining question in one message.
- **Recommend the smallest option that fits the request as written.** Recommend going further (extra scope, stricter rules, new behaviour) only when the code or the request gives a reason, and say what that reason is.
- "You decide" / "default" → pick the clean standard option and record it under `<assumptions>`.
- Only someone else can answer → don't block: record it under `<open_questions>` with the owner.
- The user pastes secrets or personal data → ask them to redact before continuing.

### 5. Write the spec
Fill `references/spec-format.md` in the configured format (XML default, or markdown). Every requirement has an ID and is covered by at least one acceptance criterion; every TBD appears in `<open_questions>`. Before showing it, check it yourself against `references/spec-format.md`: every requirement ID is covered by an acceptance criterion, every TBD is in `<open_questions>`, no secrets or personal data. If the user has the repository's `tools/validate_spec.py` and scripts can run, run it too.

### 6. Approve
Show the **approval view** (`approval_view`, default `summary`): the outcome in one sentence, the requirements in plain words (one line each, with their IDs), then assumptions and open questions on their own lines — no file paths unless they matter to the reader. The full spec is written either way: show it when the user asks ("show the spec"), when `approval_view: spec`, or in `save` and `handoff` modes, where the spec is the deliverable. Ask: approve, edit, or answer the open questions. Edits → revise and show again. Do nothing else until approved. Fire `after_approval`.

**Fast path — the request was already complete.** If the interview asked nothing (every required section came from the request or the code) and there are no open questions, the approval view is three lines at most: what will be done, the acceptance criteria in one line, any assumption. If the request itself already says to go ahead ("go ahead", "no need to confirm", "just do it"), treat that as approval of this summary and continue to step 7 without waiting; otherwise ask for a one-word yes. Never use the fast path in `handoff` mode, or when an assumption changes behaviour the request didn't mention.

### 7. Execute, save or hand off (by mode)
- **execute** — exactly the spec's scope, using the `implement` capability if mapped. Anything that changes scope → stop and update the spec (and re-approve) before continuing. Destructive or irreversible steps still get their own confirmation.
- **save** — write `save_to/<YYYY-MM-DD>-<slug>.md` from `templates/spec.md`, status `APPROVED <date> (<who>)`.
- **handoff** — return the spec exactly as approved; the caller decides where it lands.

### 8. Validate (execute mode)
Run the `verify` capability or the checks the criteria name. Report one line per criterion: `AC1 ✅ met — <evidence>` · `AC2 ❌ not met — <why>` · `AC3 ⚪ not testable here — <how to check>`. Gaps are reported plainly, never hidden. Fire `after_validate`.

## Extensions

Teams map their own skills to **capabilities** (`code-analysis`, `implement`, `verify`, or any they define) and attach **rules** to **events** — `before_interview`, `after_classify`, `after_spec`, `after_approval`, `after_execute`, `after_validate` — e.g. run a security-review skill after the spec when the request touches auth. Details and examples: `references/config.md`.

## Red flags — stop

| Thought | Reality |
|---|---|
| "The request is clear enough — just build it" | If you'd have to guess anything material, interview. Clear requests get a `quick` interview, not none. |
| "I'll ask about the code structure" | Read the code first; ask only to confirm. |
| "I'll pick a sensible value for that limit" | Unknown → ask, or `<TBD>` in open questions. "You decide" → assumption, recorded. |
| "Ten questions to be thorough" | Ask the minimum; depth sets the ceiling, not the target. |
| "I'll recommend the fuller option — it's better" | Recommend the smallest option that fits the request; go further only with a stated reason from the code or the request. |
| "The user will want the full XML to approve" | Show the plain approval view; the spec is there on request. |
| "They approved the gist — start coding" | Approval is of the written spec. Show it, get a yes. |
| "Small scope change, I'll just include it" | Stop, update the spec, re-approve. |
| "Called by another skill — I'll execute too" | Handoff mode never executes. |
| "Tests mostly pass — call it done" | One line per criterion; ❌ is reported as ❌. |
| "The example needs a real email to be clear" | Placeholders only. |
