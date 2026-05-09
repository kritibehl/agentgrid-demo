from dataclasses import dataclass
from typing import Dict, Set

ROLE_PERMISSIONS: Dict[str, Set[str]] = {
    "admin": {
        "approve_decision",
        "escalate_incident",
        "create_pm_summary",
        "create_bug_report",
        "view_raw_trace",
        "view_metrics",
    },
    "reviewer": {
        "approve_decision",
        "escalate_incident",
        "create_pm_summary",
        "view_raw_trace",
        "view_metrics",
    },
    "engineer": {
        "create_bug_report",
        "view_raw_trace",
        "view_metrics",
    },
    "support_agent": {
        "create_pm_summary",
        "escalate_incident",
        "view_metrics",
    },
}

@dataclass
class UserContext:
    user_id: str
    role: str

def has_permission(role: str, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())

def require_permission(user: UserContext, permission: str) -> dict:
    allowed = has_permission(user.role, permission)

    return {
        "user_id": user.user_id,
        "role": user.role,
        "permission": permission,
        "allowed": allowed,
        "reason": "allowed" if allowed else "permission_denied",
    }
