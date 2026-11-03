# Contributing

## Most wanted
1. **Question sets** for subtypes or domains (`references/question-bank.md`).
2. **Spec sections** a domain needs (e.g. `compliance`, `rollout`) with guidance.
3. **Event recipes** — tested rules that call a skill on `after_spec` or `after_validate`.
4. **Example specs** in `examples/specs/`, fully fictional.

## Rules
- No company names, internal hosts, people or real data; placeholders only.
- `SKILL.md` stays under 500 lines; detail goes in `references/`.
- Frontmatter keys are only `name` and `description`, at column 0.
- Safety rails cannot be made configurable.

## Before a PR
```bash
python3 scripts/validate.py
claude plugin validate . && claude plugin validate ./plugins/prompt
```
Bump `version` in `plugins/prompt/.claude-plugin/plugin.json` and add a CHANGELOG entry for behaviour changes.
