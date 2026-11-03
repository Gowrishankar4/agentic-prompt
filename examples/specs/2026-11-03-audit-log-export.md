# Spec — Audit log CSV export

| | |
|---|---|
| ID | audit-log-export |
| Type | technical · feature |
| Date | 2026-11-03 |
| Status | APPROVED 2026-11-03 (Product lead) |
| Requested by | Product lead |

```xml
<spec id="audit-log-export" type="feature" status="APPROVED 2026-11-03 (Product lead)">
<context>
  Org admins can view their audit log page by page in web/src/pages/admin/AuditLog.tsx; large orgs need a file for quarterly compliance reviews. Logs are read by api/src/audit/query.ts.
</context>
<task>Let org admins download their organisation's audit log for a date range as CSV.</task>
<requirements>
  <requirement id="R1">Admins pick a date range of at most 90 days. Default: audit.export_max_days = 90.</requirement>
  <requirement id="R2">The export runs in the background and the admin is emailed a link valid for 24 hours. Default: audit.export_link_ttl_hours = 24.</requirement>
  <requirement id="R3">Only admins of the organisation can export, and only their own organisation's events.</requirement>
  <requirement id="R4">IP addresses are masked unless <TBD: unmasked export allowed? → ask Privacy lead>.</requirement>
</requirements>
<constraints>Reuse api/src/audit/query.ts with cursor streaming; memory under 256 MB for 1 million rows. No change to the existing pagination endpoint.</constraints>
<acceptance_criteria>
  <criterion id="AC1" covers="R1">A 91-day range returns 422 with a clear message; 90 days is accepted.</criterion>
  <criterion id="AC2" covers="R2">The job writes the CSV and the email contains a link that expires after 24 hours.</criterion>
  <criterion id="AC3" covers="R3">A non-admin and an admin of another organisation both get 403.</criterion>
  <criterion id="AC4" covers="R4">The default export shows IPs as 203.0.x.x.</criterion>
</acceptance_criteria>
<out_of_scope>JSON or Excel formats, scheduled exports, SIEM streaming.</out_of_scope>
<references>web/src/pages/admin/AuditLog.tsx; api/src/audit/query.ts; api/src/policies/audit.ts</references>
<output_format>One PR to api and web with endpoint, job, email template, UI and tests.</output_format>
<assumptions>CSV columns follow the on-screen table order (you decide).</assumptions>
<open_questions><TBD: unmasked export allowed? → ask Privacy lead></open_questions>
</spec>
```

## Validation

| Criterion | Result | Evidence |
|---|---|---|
| AC1 | ✅ met | `api` tests: export range 3/3 |
| AC2 | ✅ met | job test + email preview; link expiry test |
| AC3 | ✅ met | permission tests 4/4 |
| AC4 | ⚪ not testable yet | waits on the open question |
