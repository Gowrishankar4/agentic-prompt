# Walkthrough

Three requests, three modes.

## 1. A feature — execute mode

```text
Dev: /prompt add CSV export to the admin audit log
```
1. **Classify** → technical · feature.
2. **Inspect** → finds `web/src/pages/admin/AuditLog.tsx`, `api/src/audit/query.ts`, the admin policy; states them.
3. **Interview** (standard) → three questions: date range, background job, IP masking. "Ask the privacy lead" becomes an open question with an owner.
4. **Spec** → `R1`–`R4`, `AC1`–`AC4`, one assumption (column order), one open question. `validate_spec.py` passes.
5. **Approve** → the dev says "approved".
6. **Execute** → builds exactly that scope; a request mid-way to also add JSON export is stopped: the spec is updated and re-approved first.
7. **Validate** → AC1–AC3 ✅ with test evidence, AC4 ⚪ waiting on the open question.

Result: [`examples/specs/2026-11-03-audit-log-export.md`](../examples/specs/2026-11-03-audit-log-export.md).

## 2. A bug — quick depth

```text
Dev: /prompt quick — users get logged out after 5 minutes since last release
```
Inspect finds the TTL read from `auth.session_ttl_minutes`; two questions (expected session length, must refresh checks stay strict?). Spec, approve, patch, validate both criteria. Result: [`examples/specs/2026-11-03-login-timeout-bug.md`](../examples/specs/2026-11-03-login-timeout-bug.md).

## 3. A plan for later — save mode

```text
PM: /prompt just spec it — partner API for order status
```
General questions are skipped where the code answers them; the approved spec is written to `docs/specs/2026-11-03-partner-order-status-api.md` and nothing is built.

## Called by another skill — handoff

Agentic Playbook's `/playbook new` calls `/prompt` in handoff mode: same interview and spec, but after approval the spec is returned to the playbook, which saves it into `00-REQUIREMENTS.md`. Nothing is executed until the playbook's plan is approved.
