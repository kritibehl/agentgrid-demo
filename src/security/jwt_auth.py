import base64
import json
from src.security.rbac import UserContext

def encode_demo_token(user_id: str, role: str) -> str:
    payload = {"user_id": user_id, "role": role}
    raw = json.dumps(payload).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")

def decode_demo_token(token: str) -> UserContext:
    try:
        padded = token + "=" * (-len(token) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))
        return UserContext(
            user_id=payload.get("user_id", "anonymous"),
            role=payload.get("role", "support_agent"),
        )
    except Exception:
        return UserContext(user_id="anonymous", role="support_agent")
