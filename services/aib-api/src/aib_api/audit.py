from __future__ import annotations

import json
import sys
from typing import Any, Dict


def emit_audit_event(event: Dict[str, Any]) -> None:
    """MVP: write structured JSON to stdout.

    Enterprise: ship to immutable storage / SIEM.
    """
    sys.stdout.write(json.dumps(event, sort_keys=True) + "\n")
    sys.stdout.flush()
