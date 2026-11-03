# Spec — broken on purpose (CI checks that every problem is caught)

```xml
<spec id="broken" type="feature" status="approved">
<context>Contact the owner at jane.doe@acmecorp.io; staging db postgres://admin:hunter2@db.internal/app</context>
<task>Do the thing.</task>
<requirements>
  <requirement id="R1">First rule.</requirement>
  <requirement id="R1">Duplicate id.</requirement>
  <requirement id="R2">Limit is <TBD: what limit?>.</requirement>
  <requirement id="R3">Nobody tests this.</requirement>
</requirements>
<acceptance_criteria>
  <criterion id="AC1" covers="R1">Works.</criterion>
  <criterion id="AC2" covers="R9">Covers a requirement that does not exist.</criterion>
  <criterion id="AC3">No covers attribute.</criterion>
</acceptance_criteria>
<assumptions></assumptions>
<open_questions>None</open_questions>
</spec>
```
