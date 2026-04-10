# AgentGrid Demo

A small standalone **LangGraph** project that triages construction / project documents, extracts operational risks, and routes each document to the right owner with a concise action plan.

This repo is intentionally small, interview-friendly, and easy to run locally. It demonstrates a real **agentic workflow** rather than a single LLM call:

- classify the document
- extract structured issues
- score urgency
- route to the right team
- generate an operator-facing summary

## Why this project is useful

This is a good fit for Solutions Engineer / Forward Deployed / SWE I applications because it shows:

- workflow design using a graph instead of one-shot prompting
- structured state passing between nodes
- tool-style deterministic logic mixed with optional LLM summarization
- auditable outputs that are easy to inspect and test

## Project layout

```text
agentgrid-demo/
├── README.md
├── requirements.txt
├── src/
│   ├── app.py
│   ├── graph.py
│   └── schemas.py
├── sample_data/
│   ├── rfi_foundation_delay.txt
│   ├── change_order_steel_cost.txt
│   └── safety_notice_scaffold.txt
└── tests/
    └── test_graph.py
```

## What the workflow does

The graph processes a document through these steps:

1. **Ingest**: load raw text and normalize it.
2. **Classify**: identify whether the file looks like an RFI, change order, safety notice, schedule update, or general correspondence.
3. **Extract issues**: pull out deterministic signals like delay, cost, safety, inspection, permit, rework, or material shortage.
4. **Score urgency**: assign a severity level based on the extracted issues.
5. **Route**: send the item to PM, procurement, field operations, safety, or engineering.
6. **Summarize**: produce a concise operator-facing action note.

## Example

```bash
python -m src.app --file sample_data/rfi_foundation_delay.txt
```

Example output:

```json
{
  "document_type": "rfi",
  "severity": "high",
  "owner": "engineering",
  "issues": [
    "delay_risk",
    "inspection_dependency",
    "missing_detail"
  ],
  "action_summary": "Treat as a high-priority engineering review. Missing details and inspection dependency may block foundation work and create schedule slip. Confirm drawing clarification, inspection timing, and field workaround today."
}
```

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Run locally

```bash
python -m src.app --file sample_data/rfi_foundation_delay.txt
python -m src.app --file sample_data/change_order_steel_cost.txt
python -m src.app --file sample_data/safety_notice_scaffold.txt
```

## Design notes

### LangGraph state

The graph keeps a shared typed state with:

- raw document text
- normalized text
- document type
- extracted issues
- severity
- routed owner
- action summary

### Deterministic-first architecture

The main workflow uses deterministic parsing so it is:

- easy to test
- reproducible in CI
- safe to demo without API keys

You can later swap the `summarize` node with a real LLM-backed summarizer.

## Future extensions

- add OCR/PDF ingestion
- plug in a vector store for similar-doc retrieval
- add human approval step before final routing
- expose the graph behind FastAPI
- store document decisions in PostgreSQL for analytics
