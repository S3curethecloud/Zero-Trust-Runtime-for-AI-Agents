from __future__ import annotations

from aib_api.deterministic import canonical_json, input_hash


def test_canonical_json_determinism():
    a = {"b": 1, "a": {"y": 2, "x": 1}}
    b = {"a": {"x": 1, "y": 2}, "b": 1}
    assert canonical_json(a) == canonical_json(b)


def test_input_hash_determinism():
    inp1 = {"b": 1, "a": {"y": 2, "x": 1}}
    inp2 = {"a": {"x": 1, "y": 2}, "b": 1}
    assert input_hash(inp1) == input_hash(inp2)
