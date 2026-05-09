# AgentGrid RBAC Reviewer Access

AgentGrid includes demo JWT-style access control for support review workflows.

## Roles

| Role | Allowed actions |
|---|---|
| admin | approve decisions, escalate incidents, create PM summaries, create bug reports, view raw traces, view metrics |
| reviewer | approve decisions, escalate incidents, create PM summaries, view raw traces, view metrics |
| engineer | create bug reports, view raw traces, view metrics |
| support_agent | create PM summaries, escalate incidents, view metrics |

## Protected Actions

- approve_decision
- escalate_incident
- create_pm_summary
- create_bug_report
- view_raw_trace
- view_metrics

## Example

```bash
curl http://localhost:8000/auth/demo-token/reviewer
curl -X POST http://localhost:8000/review/action \
  -H "Content-Type: application/json" \
  -d '{"token":"TOKEN","permission":"approve_decision","decision_id":"decision_123"}'
Scope

This is a demo-safe JWT-style implementation for proving reviewer/admin workflow boundaries. It is not a production identity provider integration.
