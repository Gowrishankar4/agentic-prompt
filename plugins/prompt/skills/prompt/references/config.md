# Configuration

YAML, every key optional. Precedence, highest first: the user's words in the request → settings passed by a calling skill → `.prompt.yml` at the repo root → `$PROMPT_CONFIG` or `~/.config/prompt/config.yml` → `config/default.yml`. Lists (`rules`, `extra_questions`) append; a later entry with the same `id` replaces an earlier one; `enabled: false` switches one off. Annotated example: `../config/config.example.yml`.

## Settings

| Key | Default | Values |
|---|---|---|
| `mode` | `execute` | `execute` · `save` · `handoff` (forced when another skill calls) |
| `depth` | `standard` | `quick` (≤ 3 questions) · `standard` (≤ 8) · `deep` (no cap) |
| `one_question_at_a_time` | `true` | `true` = one topic per message (≤ 4 related questions, each with options); `false` = every remaining question at once |
| `approval_view` | `summary` | `summary` (plain-language view, full spec on request) · `spec` (always show the full spec) |
| `spec_format` | `xml` | `xml` · `markdown` |
| `sections` | standard set | extra section names, inserted before `references` |
| `save_to` | `docs/specs` | folder for `save` mode (and for execute mode if `save_on_approval: true`) |
| `save_on_approval` | `false` | also save the approved spec in execute mode |
| `sensitive_data` | `[secrets, pii]` | add `phi`, `pci`; `secrets` is always on |
| `extra_questions` | `[]` | `{ id, question, when }` — always asked when `when` matches |

## Capabilities — map steps to your tools

| Capability | Used in | Built-in fallback |
|---|---|---|
| `code-analysis` | inspect (step 3) | read and search the repo |
| `implement` | execute (step 7) | implement directly within the spec's scope |
| `verify` | validate (step 8) | run the checks the criteria name |
| *your own* | rules | — |

Entries: `skill:<name>`, `command:/<name>`, `mcp:<server>.<tool>`, `"mcp?<keywords>"` (quote it in YAML), `script:"<shell>"`, `subagent:<type>`, `builtin`, `none` — each optionally `{ use: …, when: … }`. First available and matching entry wins; unmapped means built-in.

## Rules and events

```yaml
rules:
  - id: security-on-auth
    on_event: [after_spec]
    when: { request_matches: "(?i)auth|login|token|permission" }
    mode: required
    use: skill:security-review
    instruction: Add security requirements and criteria to the spec before approval.
```

| Event | Fires |
|---|---|
| `before_interview` | after classify and inspect, before the first question |
| `after_classify` | type and subtype decided |
| `after_spec` | spec drafted, before it is shown |
| `after_approval` | user approved the spec |
| `after_execute` | execute mode finished the work |
| `after_validate` | criteria reported |

Rule fields: `id` · `trigger: always` or `on_event` · `when` · one of `use` (optionally with `instruction`), `ask`, `instruction`, `instruction_file` · `mode: required | advisory` · `enabled`.

Conditions (`when`): `types` (technical / general), `subtypes`, `paths` (files the request or inspection touches), `repos`, `request_matches` (regex), `modes`, `not`.

## Safety rails — config cannot loosen these

No execution before approval (the fast path only skips the wait when the request itself said to go ahead) · no sensitive values in the spec · handoff mode never executes · scope changes stop for re-approval · destructive steps confirmed separately.
