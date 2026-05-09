# AgentGrid API Contracts

## POST /agent/run

Runs GenAI support validation workflow.

### Request

```json
{
  "input": "Why did deployment fail?"
}
Response
{
  "eval_gate": {
    "final_decision": "hold",
    "reason": "missing_context"
  },
  "trace": {
    "trace_id": "trace_xxx",
    "run_id": "run_xxx"
  }
}
GET /metrics

Returns Prometheus-style metrics.

Example
agentgrid_requests_total 25
agentgrid_hold_total 10
agentgrid_escalations_total 6

