from typing import List, Literal, TypedDict

DocumentType = Literal[
    "rfi",
    "change_order",
    "safety_notice",
    "schedule_update",
    "general",
]
Severity = Literal["low", "medium", "high", "critical"]
Owner = Literal["engineering", "procurement", "safety", "pm", "field_ops"]


class AgentState(TypedDict, total=False):
    raw_text: str
    normalized_text: str
    document_type: DocumentType
    issues: List[str]
    severity: Severity
    owner: Owner
    action_summary: str
