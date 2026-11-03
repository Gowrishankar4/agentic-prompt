# Spec format

Same sections, same order, every time. `context`, `task` and `acceptance_criteria` cannot be removed; teams add sections with `sections:` in config (inserted before `<references>`).

```xml
<spec id="<slug>" type="<subtype>" status="DRAFT">
<context>
  Who this is for, the current state (file paths for technical work), why it is needed now.
</context>

<task>
  One or two sentences: the outcome, stated as a deliverable.
</task>

<requirements>
  <requirement id="R1">Testable statement. Default: <value or config key>.</requirement>
  <requirement id="R2">…</requirement>
</requirements>

<constraints>
  Stack and versions, compatibility, performance budgets, deadlines, what must not change.
</constraints>

<acceptance_criteria>
  <criterion id="AC1" covers="R1">Observable check: given / when / then, or a command whose output proves it.</criterion>
  <criterion id="AC2" covers="R2">…</criterion>
</acceptance_criteria>

<out_of_scope>
  What will explicitly not change.
</out_of_scope>

<references>
  Files read, docs, tickets, designs — paths or links. No sensitive values.
</references>

<output_format>
  What is delivered and where: files changed, PR, document, report.
</output_format>

<assumptions>
  Choices made on "you decide" or by default — one per line, or None.
</assumptions>

<open_questions>
  <TBD: what is missing → ask <owner>> — one per line, or None.
</open_questions>
</spec>
```

## Rules

- Every `<requirement>` has a unique `id` (`R1`, `R2` …) and is a single testable statement.
- Every requirement is covered by at least one `<criterion covers="…">`; a criterion may cover several (`covers="R1 R3"`).
- Every `<TBD …>` anywhere in the spec is also listed in `<open_questions>`.
- `status`: `DRAFT` while interviewing → `APPROVED <YYYY-MM-DD> (<who>)` on approval.
- Numbers are quoted from the source, not paraphrased; defaults name their config key when one exists.

## Markdown format

`spec_format: markdown` uses the same section names as `##` headings, requirements and criteria as tables:

```markdown
## Requirements
| ID | Requirement | Default |
|---|---|---|
| R1 | … | … |

## Acceptance criteria
| ID | Covers | Check |
|---|---|---|
| AC1 | R1 | … |
```
