<div align="center">

# AgentGrid-Demo

**LangGraph agentic workflow for document triage, risk extraction, and owner routing**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic%20Workflow-1C3A5E?style=flat-square)](https://github.com/langchain-ai/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

</div>

---

> Most LLM applications make a single call and return text.
> **AgentGrid executes a structured multi-step workflow — classify, extract, score, route — with typed state at every transition.**

---

## What it does

AgentGrid takes a construction or project document and runs it through a deterministic four-node graph:

```
Document input
      ↓
Classification node    — what kind of document is this?
      ↓
Issue extraction node  — what schedule, cost, and safety risks does it contain?
      ↓
Urgency scoring node   — how critical is each issue?
      ↓
Routing node           — who owns each issue, and what action is required?
      ↓
Structured output: issue list · risk categories · urgency scores · owner routing
```

Each node has typed input and output state. Transitions are deterministic. The graph is auditable and testable at every step.

---

## Why graph-based over single-call

A single LLM call for document triage has two problems: it cannot be tested in isolation (the whole thing passes or fails), and it conflates distinct concerns (classification, extraction, scoring, routing) into one opaque blob of output.

A graph separates those concerns. Each node can be tested independently, replaced without touching adjacent nodes, and inspected to understand exactly where the workflow is and what state it is holding at any point.

This is the design pattern behind production agentic systems at Anthropic, Google DeepMind, and any serious LLM application team.

---

## Example output

Given a construction project document with schedule delays and a safety concern:

```json
{
  "document_type": "project_status_report",
  "issues": [
    {
      "issue": "Foundation pour delayed 3 weeks",
      "risk_category": "schedule",
      "urgency_score": 8,
      "owner": "project_manager",
      "action": "Escalate to project manager — critical path impact"
    },
    {
      "issue": "Safety harness inspection overdue",
      "risk_category": "safety",
      "urgency_score": 10,
      "owner": "site_safety_officer",
      "action": "Immediate: halt affected operations until inspection complete"
    }
  ],
  "routing_summary": {
    "project_manager": ["foundation delay"],
    "site_safety_officer": ["safety harness inspection"]
  }
}
```

---

## Node design

| Node | Input | Output |
|---|---|---|
| Classification | Raw document text | `document_type`, `domain` |
| Issue extraction | Document + type | List of issues with risk category |
| Urgency scoring | Issues + risk categories | Urgency score per issue (1–10) |
| Routing | Scored issues | Owner + recommended action per issue |

Typed state flows through the graph. No node invents fields the downstream node does not expect.

---

## Structure

```
agentgrid-demo/
├── src/
│   ├── graph.py          # LangGraph workflow definition
│   ├── nodes/
│   │   ├── classify.py   # Document classification node
│   │   ├── extract.py    # Issue extraction node
│   │   ├── score.py      # Urgency scoring node
│   │   └── route.py      # Owner routing node
│   └── state.py          # Typed state schema
├── sample_data/          # Sample construction project documents
├── tests/                # CI-friendly tests per node + integration
└── requirements.txt
```

---

## Running

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run on a sample document
python src/graph.py --input sample_data/project_status.txt

# Run tests
pytest tests/ -v
```

---

## What this demonstrates

**Stateful multi-step agent execution** — not a single LLM call. The graph holds and propagates typed state across four distinct reasoning steps.

**Deterministic node design** — each node has a fixed contract. Classification does not bleed into routing. Scoring does not depend on document type. The graph is composable and extensible.

**Testable agent architecture** — each node can be tested independently with fixed input/output state. CI runs cleanly without mocking the entire graph.

**Real output structure** — the workflow produces structured JSON artifacts, not narrative text. Owner routing is explicit and machine-readable.

---

## Scope

This is a structured demo — intentionally small and clear. It is not a production multi-tenant routing system. The value is in the architecture pattern: graph-based agent design, typed state, deterministic nodes, and testable workflows. These are the same patterns used in production agentic systems at scale.

---

## Stack

Python · LangGraph

---

## Related

- [Faultline](https://github.com/kritibehl/faultline) — distributed correctness under failure
- [AutoOps-Insight](https://github.com/kritibehl/AutoOps-Insight) — structured incident triage for CI failures
- [FairEval](https://github.com/kritibehl/FairEval-Suite) — regression gating for AI system releases
