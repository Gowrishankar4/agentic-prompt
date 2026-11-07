# Agentic Prompt plugin

> **Branch `directory`** — the build listed in the Claude directory, as plugin `agentic-prompt` ("prompt" is too generic a directory name). It is `main` with `validate_spec.py` moved to `tools/` at the repository root (the directory accepts bundled scripts only from Verified organizations), so the skill checks specs itself. Claude Code users installing from this repository's marketplace get `main`, plugin `prompt`, which bundles the script.

One skill, `/prompt`, that stops agents from building on guesses. It classifies a rough request, reads the codebase first for technical work, asks only the questions the request and code don't answer, writes a structured XML spec with requirements and acceptance criteria, and waits for your approval. Then it executes exactly that scope (or saves the spec, or hands it to another skill) and validates the result criterion by criterion.

## Install

```
/plugin marketplace add Gowrishankar4/agentic-prompt
/plugin install prompt@agentic-prompt
```

## Use

- `/prompt:prompt add CSV export to the audit log` — interview, spec, approve, build, validate
- `/prompt:prompt quick …` / `deep …` — fewer or more questions
- `/prompt:prompt just spec it: …` — save the approved spec to `docs/specs/` without building

## Setup

None required. Optional config in `~/.config/prompt/config.yml` or `.prompt.yml` at a repo root: depth, spec format, extra questions, your own skills per step, and rules on events. See the repository README.
