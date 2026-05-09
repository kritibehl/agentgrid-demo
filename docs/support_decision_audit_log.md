# Support Decision Audit Log

AgentGrid records reviewer/admin actions against GenAI support decisions.

## Why this exists

GenAI support workflows need reviewability. A support system should be able to answer:

- who approved a decision?
- who escalated an incident?
- who attempted to view raw traces?
- which action was denied by RBAC?
- which trace/decision did the action affect?

## Audited actions

- approve_decision
- escalate_incident
- create_pm_summary
- create_bug_report
- view_raw_trace
- view_metrics

## Audit fields

| Field | Purpose |
|---|---|
| audit_id | unique audit event ID |
| actor_id | user performing action |
| actor_role | admin/reviewer/engineer/support_agent |
| action | attempted support action |
| decision_id | support decision being acted on |
| trace_id | validation trace |
| outcome | allowed or denied |
| reason | allowed / permission_denied |
| created_at | UTC timestamp |

## API

```bash
GET /audit/events
GET /audit/events?actor_role=reviewer
GET /audit/events?decision_id=decision_123
GET /audit/events?trace_id=trace_123
Scope

This is an in-memory audit-log proof for support-review workflows. It proves auditability and reviewer action tracking, not production-grade immutable audit storage.
