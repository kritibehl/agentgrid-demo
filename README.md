# AgentGrid: Production GenAI Support & Deployment System

AgentGrid is a production-style GenAI support system that uses a LangGraph workflow, retrieval over operational documents/logs/runbooks, MCP-style tools, metrics, and an evaluation gate to classify incidents, retrieve evidence, generate action plans, and decide whether to ship, hold, or escalate.

## Why this project exists

Modern support and deployment workflows often fail because operational evidence is scattered across logs, docs, runbooks, and incident notes. AgentGrid turns those inputs into a structured, evidence-backed decision workflow.

## Architecture

```text
Input document/log/runbook
        |
        v
[classify_issue]
        |
        v
[retrieve_context]  ---> local RAG over docs/logs/runbooks
        |
        v
[analyze_logs]      ---> MCP-style tool
        |
        v
[create_action_plan] ---> MCP-style tool
        |
        v
[generate_answer]
        |
        v
[eval_gate]
        |
        v
ship / hold / escalate
What it does
Classifies operational issues from docs, logs, and runbooks
Retrieves supporting evidence with citations
Calls MCP-style tools for document search, log analysis, and action planning
Produces structured JSON outputs
Tracks latency and tool-call success rate
Runs an eval gate for correctness, citation coverage, unsupported answer detection, safety, and final decisioning
Demo

Run one document:

python3 -m src.app --file data/docs/deployment_failure.txt

Run the demo suite:

python3 scripts/run_demo_suite.py

The suite writes metrics to:

reports/demo_metrics.json
Example output
{
  "metrics": {
    "latency_seconds": 0.0028,
    "tool_call_success_rate": 1.0
  },
  "eval_gate": {
    "correctness": true,
    "citation_coverage": true,
    "unsupported_answer": false,
    "safety": true,
    "final_decision": "ship"
  }
}
MCP-style tools

AgentGrid includes three tool-like functions:

search_docs: retrieves evidence from docs, logs, and runbooks
analyze_logs: detects timeout, retry, and latency degradation signals
create_action_plan: generates operational next steps based on the classified issue
Eval gate

The eval gate checks:

correctness
citation coverage
unsupported answer risk
safety
final decision: ship, hold, or escalate
Metrics

AgentGrid tracks:

latency per request
latency p50/p95 across demo suite
tool-call success rate
ship/hold/escalate counts
API

Run locally:

uvicorn src.api.server:app --reload

Health check:

curl http://127.0.0.1:8000/health

Run agent:

curl -X POST "http://127.0.0.1:8000/run?input=DB%20timeout%20failure"
Resume summary

Built a production-style GenAI support and deployment system using LangGraph with RAG over documents, logs, and runbooks, MCP-style tools for retrieval/log analysis/action planning, observability metrics, and an eval gate for correctness, citation coverage, hallucination risk, safety, and ship/hold/escalate decisions.

## Updated Architecture

```text
Query
  |
  v
RAG over docs/logs/runbooks
  |
  v
LangGraph workflow
  |
  v
MCP-style tools
  |
  v
Eval gate
  |
  v
Decision: ship / hold / escalate
  |
  v
AutoOps event emission
API demo

Run the API:

uvicorn src.api.server:app --reload

Request:

curl -s -X POST http://127.0.0.1:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{"input":"Deployment failed because DB timeout caused retry storm and latency spike."}' \
  | python3 -m json.tool

The response includes:

agent_output
metrics
eval_gate
autoops_event
Real Gemini mode

Mock mode is the default.

To run with Gemini:

export USE_REAL_MODEL=true
export GEMINI_API_KEY="your_key_here"
python3 scripts/run_real_gemini_cases.py

Outputs are saved under:

reports/real_model_runs/

