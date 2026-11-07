# Changelog

## 1.1.0 — 2026-11-07

From a with/without test on three tasks (vague feature, vague bug, fully specified control): `/prompt` met 20/20 hidden intent checks on the first build against 13/20 without it, at about 1.6× the agent cost. These changes cut the overhead.

- **Grouped questions.** `one_question_at_a_time: true` now means one topic per message — up to 4 related questions, each with lettered options and a marked recommendation (`1b 2a` answers them). The vague-feature test took 4 rounds asking one at a time.
- **Smallest-option recommendations.** The recommended answer is the smallest that fits the request as written; going further needs a stated reason. (In the test, the recommendation added unrequested scope.)
- **Plain approval view** (`approval_view: summary`, default): approve a short plain-language summary; the full spec is shown on request, with `approval_view: spec`, or in `save`/`handoff` modes.
- **Fast path for complete requests.** When nothing needed asking and nothing is open, approval is a three-line summary; if the request already said to go ahead, that counts as approval. Never in `handoff` mode.
- `validate_spec.py --validate-config` accepts `approval_view`.

## 1.0.0 — 2026-11-03

First public release.

- `/prompt` skill: classify (technical/general + 11 subtypes) → inspect code → interview (quick / standard / deep) → XML or markdown spec → approval → execute / save / handoff → validate per acceptance criterion.
- Fixed spec format with coverage rules; question bank per subtype.
- Config: depth, format, extra sections, team questions, capabilities mapped to your own skills, rules on six events.
- `scripts/validate_spec.py`: spec structure, ID coverage, TBD tracking, sensitive data, config validation.
- Handoff mode for other skills; works as Agentic Playbook's interview.
