from langgraph.graph import StateGraph
from typing import TypedDict
from src.tools.tools import search_docs, analyze_logs, create_action_plan

class State(TypedDict):
    input: str
    issue: str
    context: list
    analysis: str
    actions: list

def classify(state):
    text = state["input"]
    if "timeout" in text.lower():
        state["issue"] = "timeout"
    else:
        state["issue"] = "unknown"
    return state

def retrieve_context(state):
    state["context"] = search_docs(state["issue"])
    return state

def analyze(state):
    state["analysis"] = analyze_logs(state["input"])
    return state

def plan(state):
    state["actions"] = create_action_plan(state["issue"])
    return state

builder = StateGraph(State)

builder.add_node("classify", classify)
builder.add_node("retrieve", retrieve_context)
builder.add_node("analyze", analyze)
builder.add_node("plan", plan)

builder.set_entry_point("classify")
builder.add_edge("classify", "retrieve")
builder.add_edge("retrieve", "analyze")
builder.add_edge("analyze", "plan")

graph = builder.compile()

def run_agent(input_text):
    return graph.invoke({"input": input_text})
