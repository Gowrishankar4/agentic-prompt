<p align="center"><img src="assets/logo.png" alt="Agentic Prompt" width="480"></p>

# Agentic Prompt

[![Validate](https://github.com/Gowrishankar4/agentic-prompt/actions/workflows/validate.yml/badge.svg)](https://github.com/Gowrishankar4/agentic-prompt/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Stop agents from building on guesses.** `/prompt` turns a rough request into an approved, implementation-ready spec through a short guided interview — then does exactly that, and proves it.

```
request → classify → read the code → interview → XML spec → APPROVAL → execute | save | hand off → validate
```

- **Reads before it asks.** For technical work it inspects the codebase first and only asks you to confirm.
- **Asks the minimum.** `quick` ≤ 3 questions, `standard` ≤ 8, `deep` probes everything. Skips anything already answered. Related questions come together, each with options and a recommendation — and it recommends the smallest option that fits your request.
- **Plain approval view.** You approve a short plain-language summary; the full spec is one request away. Already-complete requests get a three-line confirmation instead of an interview.
- **One fixed spec shape.** Context, task, requirements, constraints, acceptance criteria, out of scope, references, output, assumptions, open questions.
- **Approval is the gate.** Nothing runs until you approve the written spec.
- **Proves the result.** One line per acceptance criterion: ✅ met · ❌ not met · ⚪ not testable here — with evidence.
- **No secrets in specs.** Placeholders only (`<API_KEY>`, `<USER_EMAIL>`, `<PATIENT_NAME>`).
- **Fits your tools.** Map your own skills to each step, add team questions, hook skills onto events.
- **Works with any agent** — Claude Code, Cursor, Codex, Gemini CLI, Copilot, Windsurf, or chat.

## Install

**Claude Code**
```bash
/plugin marketplace add Gowrishankar4/agentic-prompt
/plugin install prompt@agentic-prompt
```

**Cursor, Codex, Gemini CLI, Windsurf — any agent with a skills folder**
```bash
git clone https://github.com/Gowrishankar4/agentic-prompt && cd agentic-prompt
./install.sh --agent cursor          # or --agent claude, or --dir <skills folder>
```

**Claude.ai / desktop** — zip `plugins/prompt/skills/prompt` and upload it as a skill.

## Use

```text
> /prompt add CSV export to the admin audit log

Classified: technical · feature. I found the audit page in web/src/pages/admin/AuditLog.tsx
and the query in api/src/audit/query.ts (cursor-based).
Topic 1 of 2 — limits and delivery
1. Maximum date range? (a) 30 days ← recommended, matches the page's filter (b) 90 days (c) unlimited
2. Delivery? (a) download in the browser ← recommended (b) background job + emailed link
> 1b 2b, link valid 24h
Topic 2 of 2 — data
3. Are IP addresses shown in full? (a) yes (b) masked ← recommended
> ask the privacy lead

Admins can export up to 90 days of the audit log as CSV, delivered by an emailed link.
  R1 export any range up to 90 days · R2 runs in the background, emails a link valid 24h
  R3 columns follow the on-screen order · R4 respects the current filters
Assumptions: CSV columns follow the on-screen order.
Open questions: unmasked IPs allowed? → Privacy lead
Approve, edit, answer the open question — or "show the spec" for the full XML?
> approved

… builds it …
AC1 ✅ met — export range tests 3/3
AC2 ✅ met — job test + email preview
AC3 ✅ met — permission tests 4/4
AC4 ⚪ not testable yet — waits on the open question
```

Full specs: [`examples/specs/`](examples/specs/). A day-to-day walkthrough: [`docs/WALKTHROUGH.md`](docs/WALKTHROUGH.md).

## Modes

| Mode | After approval |
|---|---|
| `execute` (default) | Builds exactly the spec's scope, then validates |
| `save` | Writes `docs/specs/YYYY-MM-DD-<slug>.md` and stops — "just spec it" |
| `handoff` | Returns the spec to the calling skill and never executes |

## Configure (optional)

`~/.config/prompt/config.yml` (you) or `.prompt.yml` at a repo root (the team):

```yaml
depth: standard
save_on_approval: true
extra_questions:
  - { id: flag, question: "Which feature flag gates this?", when: { subtypes: [feature] } }
capabilities:
  code-analysis: [skill:code-graph, builtin]
  verify:        [command:/verify, script:"npm test"]
rules:
  - id: security-on-auth
    on_event: [after_spec]
    when: { request_matches: "(?i)auth|login|token|payment" }
    use: skill:security-review
    instruction: Add security requirements and criteria before the spec is shown.
```

Events: `before_interview`, `after_classify`, `after_spec`, `after_approval`, `after_execute`, `after_validate`. Every option: [`references/config.md`](plugins/prompt/skills/prompt/references/config.md).

Check a spec or config:
```bash
python3 tools/validate_spec.py docs/specs/2026-11-03-audit-log-export.md
python3 tools/validate_spec.py --validate-config .prompt.yml
```

## Works with Agentic Playbook

[Agentic Playbook](https://github.com/Gowrishankar4/agentic-playbook) uses `/prompt` as its requirement interview. Map it once:

```yaml
# ~/.config/playbook/config.yml
capabilities:
  interview: [skill:prompt, builtin]
```

The playbook calls it in `handoff` mode and saves the approved spec into `00-REQUIREMENTS.md` — the playbook's approval gate then decides when work starts.

## Guarantees no config can switch off

No execution before approval · no sensitive values in specs · handoff never executes · scope changes stop for re-approval · destructive steps are confirmed separately.

## Contributing

Question sets for new subtypes, spec sections for specific domains, and event recipes are the most valuable contributions. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © 2026 Gowrishankar Sivagnanam
