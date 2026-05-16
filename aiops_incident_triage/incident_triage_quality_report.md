# AgentGrid AIOps Incident Triage Quality Report

## Purpose

This report evaluates AgentGrid-style incident triage for operational incidents using logs, telemetry, and runbook context.

## Evaluation Criteria

| Criterion | Meaning |
|---|---|
| groundedness | Summary uses available logs/runbook evidence |
| unsupported-detail risk | Summary avoids invented or overconfident claims |
| actionability | Summary includes useful next actions |
| runbook/log usage | Summary references provided operational context |
| root-cause framing | Probable cause is framed as a hypothesis |

## Scenarios

- db_timeout_retry_storm
- missing_runbook_context
- latency_breach_after_validation

## Results

See:

```text
aiops_incident_triage/incident_triage_results.json
for:

total scenarios
pass/fail count
average quality score
per-scenario summaries
per-scenario evaluation gates
Why This Matters

AIOps agents should not simply summarize incidents. They should:

ground summaries in logs and runbooks
avoid unsupported root-cause claims
frame probable cause as a hypothesis
generate actionable support steps
identify missing diagnostics
Resume-Safe Summary

Built AI incident-triage scenarios that retrieve logs and runbook context, generate grounded operational summaries and probable-cause hypotheses, and evaluate outputs for unsupported details, missing diagnostics, and actionability.
