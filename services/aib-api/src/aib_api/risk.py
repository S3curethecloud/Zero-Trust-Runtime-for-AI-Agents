from __future__ import annotations

from typing import Any, Dict


def clamp_int(x: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, x))


def compute_risk_score(context: Dict[str, Any]) -> int:
    """Deterministic placeholder risk scoring.

    Enterprise: replace with explicit risk signals from a risk engine.
    This function MUST remain deterministic.
    """
    # If caller provides a risk score, normalize to [0, 100].
    raw = int(context.get("risk_score", 0))
    return clamp_int(raw, 0, 100)
