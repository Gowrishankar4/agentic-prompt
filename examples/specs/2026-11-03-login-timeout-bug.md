# Spec — Users logged out after 5 minutes

| | |
|---|---|
| ID | login-timeout-bug |
| Type | technical · bug |
| Date | 2026-11-03 |
| Status | APPROVED 2026-11-03 (Tech lead) |
| Requested by | Support |

```xml
<spec id="login-timeout-bug" type="bug" status="APPROVED 2026-11-03 (Tech lead)">
<context>Since the 2026-10-30 release, web users are logged out after about 5 minutes instead of 8 hours. Session refresh lives in web/src/auth/refresh.ts; the token TTL is read from config auth.session_ttl_minutes.</context>
<task>Restore 8-hour sessions without weakening refresh-token checks.</task>
<requirements>
  <requirement id="R1">Sessions stay valid for 8 hours of activity. Default: auth.session_ttl_minutes = 480.</requirement>
  <requirement id="R2">Expired refresh tokens are still rejected.</requirement>
</requirements>
<constraints>No change to the token format; fix must ship as a patch release.</constraints>
<acceptance_criteria>
  <criterion id="AC1" covers="R1">An e2e test with a simulated 7-hour session stays logged in.</criterion>
  <criterion id="AC2" covers="R2">A refresh with a token expired 1 minute ago returns 401.</criterion>
</acceptance_criteria>
<out_of_scope>Remember-me and mobile sessions.</out_of_scope>
<references>web/src/auth/refresh.ts; release notes 2026-10-30</references>
<output_format>Patch PR with the fix and both tests.</output_format>
<assumptions>None</assumptions>
<open_questions>None</open_questions>
</spec>
```
