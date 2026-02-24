from typing import Dict

# In-memory session store (Phase 1)
ACTIVE_SESSIONS: Dict[str, bool] = {}

def register_session(sid: str):
    ACTIVE_SESSIONS[sid] = True

def revoke_session(sid: str):
    ACTIVE_SESSIONS[sid] = False

def is_session_active(sid: str) -> bool:
    return ACTIVE_SESSIONS.get(sid, False)
