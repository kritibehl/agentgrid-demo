from __future__ import annotations

import re
from typing import Dict, List

from .schemas import AgentState

try:
    from langgraph.graph import END, StateGraph  # type: ignore
    LANGGRAPH_AVAILABLE = True
except Exception:  # pragma: no cover
    END = "__end__"
    LANGGRAPH_AVAILABLE = False
    StateGraph = None


def ingest_node(state: AgentState) -> AgentState:
    raw_text = state["raw_text"]
    normalized = re.sub(r"\s+", " ", raw_text.strip().lower())
    return {"normalized_text": normalized}


def classify_node(state: AgentState) -> AgentState:
    text = state["normalized_text"]

    if "rfi" in text or "request for information" in text:
        doc_type = "rfi"
    elif "change order" in text or "cost impact" in text:
        doc_type = "change_order"
    elif "safety" in text or "incident" in text or "osha" in text:
        doc_type = "safety_notice"
    elif "schedule update" in text or "milestone" in text or "lookahead" in text:
        doc_type = "schedule_update"
    else:
        doc_type = "general"

    return {"document_type": doc_type}


def extract_issues_node(state: AgentState) -> AgentState:
    text = state["normalized_text"]
    issues: List[str] = []

    keyword_map = {
        "delay_risk": ["delay", "slip", "behind schedule", "hold", "blocked"],
        "cost_risk": ["cost impact", "price increase", "budget", "overrun"],
        "safety_risk": ["unsafe", "fall hazard", "injury", "incident", "osha"],
        "inspection_dependency": ["inspection", "inspector approval", "sign-off"],
        "permit_dependency": ["permit", "permitting", "approval pending"],
        "material_shortage": ["lead time", "shortage", "backorder", "unavailable"],
        "missing_detail": ["clarify", "missing detail", "not shown", "unclear", "dimension missing"],
        "rework_risk": ["rework", "redo", "remove and replace"],
    }

    for issue, patterns in keyword_map.items():
        if any(pattern in text for pattern in patterns):
            issues.append(issue)

    if not issues:
        issues.append("needs_review")

    return {"issues": sorted(set(issues))}


def score_severity_node(state: AgentState) -> AgentState:
    issues = set(state["issues"])
    doc_type = state["document_type"]

    if "safety_risk" in issues:
        severity = "critical"
    elif {"delay_risk", "inspection_dependency"}.issubset(issues) or "cost_risk" in issues:
        severity = "high"
    elif doc_type in {"rfi", "schedule_update"} or "material_shortage" in issues:
        severity = "medium"
    else:
        severity = "low"

    return {"severity": severity}


def route_owner_node(state: AgentState) -> AgentState:
    issues = set(state["issues"])
    doc_type = state["document_type"]

    if "safety_risk" in issues or doc_type == "safety_notice":
        owner = "safety"
    elif doc_type == "change_order" or "cost_risk" in issues or "material_shortage" in issues:
        owner = "procurement"
    elif doc_type == "rfi" or "missing_detail" in issues or "inspection_dependency" in issues:
        owner = "engineering"
    elif doc_type == "schedule_update" or "delay_risk" in issues:
        owner = "pm"
    else:
        owner = "field_ops"

    return {"owner": owner}


def summarize_node(state: AgentState) -> AgentState:
    severity = state["severity"]
    owner = state["owner"]
    issues = ", ".join(issue.replace("_", " ") for issue in state["issues"])
    doc_type = state["document_type"].replace("_", " ")

    summary = (
        f"Treat as a {severity}-priority {owner} review. "
        f"Document appears to be a {doc_type}. "
        f"Primary concerns: {issues}. "
        f"Confirm owner handoff, next dependency, and mitigation plan in the next coordination cycle."
    )

    if severity in {"high", "critical"}:
        summary += " Escalate today and track closure explicitly."

    return {"action_summary": summary}


class _SequentialCompiledGraph:
    def __init__(self, nodes):
        self.nodes = nodes

    def invoke(self, initial_state: AgentState) -> AgentState:
        state: AgentState = dict(initial_state)
        for node in self.nodes:
            state.update(node(state))
        return state


def build_graph():
    nodes = [
        ingest_node,
        classify_node,
        extract_issues_node,
        score_severity_node,
        route_owner_node,
        summarize_node,
    ]

    if not LANGGRAPH_AVAILABLE:
        return _SequentialCompiledGraph(nodes)

    graph = StateGraph(AgentState)
    graph.add_node("ingest", ingest_node)
    graph.add_node("classify", classify_node)
    graph.add_node("extract_issues", extract_issues_node)
    graph.add_node("score_severity", score_severity_node)
    graph.add_node("route_owner", route_owner_node)
    graph.add_node("summarize", summarize_node)

    graph.set_entry_point("ingest")
    graph.add_edge("ingest", "classify")
    graph.add_edge("classify", "extract_issues")
    graph.add_edge("extract_issues", "score_severity")
    graph.add_edge("score_severity", "route_owner")
    graph.add_edge("route_owner", "summarize")
    graph.add_edge("summarize", END)

    return graph.compile()


def run_document(text: str) -> Dict[str, object]:
    app = build_graph()
    result = app.invoke({"raw_text": text})
    return {
        "document_type": result["document_type"],
        "severity": result["severity"],
        "owner": result["owner"],
        "issues": result["issues"],
        "action_summary": result["action_summary"],
    }
