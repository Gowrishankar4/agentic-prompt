# Changelog

## 1.0.0 — 2026-11-03

First public release.

- `/prompt` skill: classify (technical/general + 11 subtypes) → inspect code → interview (quick / standard / deep) → XML or markdown spec → approval → execute / save / handoff → validate per acceptance criterion.
- Fixed spec format with coverage rules; question bank per subtype.
- Config: depth, format, extra sections, team questions, capabilities mapped to your own skills, rules on six events.
- `scripts/validate_spec.py`: spec structure, ID coverage, TBD tracking, sensitive data, config validation.
- Handoff mode for other skills; works as Agentic Playbook's interview.
