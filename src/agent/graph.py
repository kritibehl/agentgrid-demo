import os
import time
from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from src.tools.tools import search_docs, analyze_logs, create_action_plan

LATENCY_BUDGET_SECONDS = 0.1

class State(TypedDict):
    input: str
    issue: str
    context: List[Dict]
    analysis: List[str]
    actions: List[str]
    answer: str
    tool_errors: List[str]
    retrieval_latency_seconds: float
    trace: List[str]
    model_mode: str

def classify(state: State) -> State:
    text = state["input"].lower()
    state["trace"].append("classify_issue")

    if "simulate_tool_failure" in text:
        state["issue"] = "tool_failure"
    elif "simulate_slow_tool" in text:
        state["issue"] = "latency_breach"
    elif "simulate_unsupported_answer" in text or "delete production data" in text:
        state["issue"] = "unsupported_answer"
    elif "quantum-ledger-cache" in text or "invisible shard leases" in text:
        state["issue"] = "low_retrieval"
    elif "unknown dependency" in text or "no matching runbook" in text:
        state["issue"] = "missing_context"
    elif "doc a" in text and "doc b" in text:
        state["issue"] = "conflicting_docs"
    elif "timeout" in text or "database" in text or "db" in text:
        state["issue"] = "timeout"
    elif "latency" in text:
        state["issue"] = "latency_degradation"
    elif "error" in text or "failed" in text:
        state["issue"] = "deployment_failure"
    else:
        state["issue"] = "unknown"

    return state

def retrieve_context(state: State) -> State:
    state["trace"].append("retrieve_context")
    query = f"{state['issue']} {state['input']}"

    try:
        start = time.time()
        state["context"] = search_docs(query)
        state["retrieval_latency_seconds"] = time.time() - start
    except Exception as exc:
        state["context"] = []
        state["retrieval_latency_seconds"] = 0.0
        state["tool_errors"].append(str(exc))

    return state

def analyze(state: State) -> State:
    state["trace"].append("analyze_logs")
    state["analysis"] = analyze_logs(state["input"])
    return state

def plan(state: State) -> State:
    state["trace"].append("create_action_plan")
    state["actions"] = create_action_plan(state["issue"])
    return state

def generate_mock_answer(state: State) -> str:
    citations = [item["source"] for item in state.get("context", [])]

    if state["issue"] == "unsupported_answer":
        return (
            "I cannot recommend destructive production actions because the retrieved evidence "
            "does not support that remediation. Escalate to a human owner."
        )

    return (
        f"Issue classified as {state['issue']}. "
        f"Findings: {', '.join(state['analysis'])}. "
        f"Recommended actions: {', '.join(state['actions'])}. "
        f"Evidence sources: {', '.join(citations) if citations else 'none'}."
    )

def generate_gemini_answer(state: State) -> str:
    try:
        import google.generativeai as genai

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            state["tool_errors"].append("GEMINI_API_KEY missing")
            return generate_mock_answer(state)

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))

        evidence = "\n\n".join(
            f"[{idx + 1}] source={item.get('source')}\n{item.get('content')}"
            for idx, item in enumerate(state.get("context", []))
        )

        prompt = f"""
You are AgentGrid, a production support and deployment assistant.

Classified issue: {state['issue']}
Findings: {state['analysis']}
Candidate actions: {state['actions']}

Retrieved evidence:
{evidence if evidence else "NO EVIDENCE RETRIEVED"}

User input:
{state['input']}

Return a concise operational answer.
Rules:
- Cite evidence sources by filename.
- Do not recommend unsupported or destructive production actions.
- If evidence is missing or conflicting, say hold or escalate.
"""

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as exc:
        state["tool_errors"].append(f"gemini_error: {exc}")
        return generate_mock_answer(state)

def generate_answer(state: State) -> State:
    state["trace"].append("generate_answer")

    use_real_model = os.getenv("USE_REAL_MODEL", "false").lower() == "true"
    if use_real_model:
        state["model_mode"] = "gemini"
        state["answer"] = generate_gemini_answer(state)
    else:
        state["model_mode"] = "mock"
        state["answer"] = generate_mock_answer(state)

    return state

builder = StateGraph(State)

builder.add_node("classify_issue", classify)
builder.add_node("retrieve_context", retrieve_context)
builder.add_node("analyze_logs", analyze)
builder.add_node("create_action_plan", plan)
builder.add_node("generate_answer", generate_answer)

builder.set_entry_point("classify_issue")
builder.add_edge("classify_issue", "retrieve_context")
builder.add_edge("retrieve_context", "analyze_logs")
builder.add_edge("analyze_logs", "create_action_plan")
builder.add_edge("create_action_plan", "generate_answer")
builder.add_edge("generate_answer", END)

graph = builder.compile()

def run_agent(input_text: str):
    return graph.invoke({
        "input": input_text,
        "issue": "",
        "context": [],
        "analysis": [],
        "actions": [],
        "answer": "",
        "tool_errors": [],
        "retrieval_latency_seconds": 0.0,
        "trace": [],
        "model_mode": "mock",
    })
