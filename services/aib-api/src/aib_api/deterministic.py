from __future__ import annotations

import hashlib
import json
from typing import Any, Dict


def canonical_json(obj: Any) -> str:
    """Deterministic JSON encoding: sort keys recursively, no whitespace."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def input_hash(decision_input: Dict[str, Any]) -> str:
    """Computes SHA256 over canonical JSON of decision input."""
    return sha256_hex(canonical_json(decision_input))
