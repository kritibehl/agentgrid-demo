from src.security.jwt_auth import encode_demo_token, decode_demo_token
from src.security.rbac import require_permission

def test_reviewer_can_approve_decision():
    token = encode_demo_token("u1", "reviewer")
    user = decode_demo_token(token)
    decision = require_permission(user, "approve_decision")

    assert decision["allowed"] is True
    assert decision["role"] == "reviewer"

def test_support_agent_cannot_view_raw_trace():
    token = encode_demo_token("u2", "support_agent")
    user = decode_demo_token(token)
    decision = require_permission(user, "view_raw_trace")

    assert decision["allowed"] is False
    assert decision["reason"] == "permission_denied"

def test_engineer_can_create_bug_report():
    token = encode_demo_token("u3", "engineer")
    user = decode_demo_token(token)
    decision = require_permission(user, "create_bug_report")

    assert decision["allowed"] is True
