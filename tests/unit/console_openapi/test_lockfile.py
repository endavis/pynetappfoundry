"""Round-trip tests for the build lockfile."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.console_openapi.lockfile import Lockfile


def _sample() -> Lockfile:
    return Lockfile(
        repo="https://github.com/NetAppDocs/console-automation",
        requested_ref="main",
        resolved_sha="6227eade9a7a1cb55e2b7b8adcd1aa7667a289e2",
        tool_version="0.1.0",
        services=("tenancy", "tenancyv4"),
        endpoint_count=222,
    )


def test_to_json_is_stable_and_sorted() -> None:
    lock = _sample()
    text = lock.to_json()
    parsed = json.loads(text)
    assert parsed["repo"].endswith("/console-automation")
    assert parsed["services"] == ["tenancy", "tenancyv4"]
    # sort_keys=True → alphabetical order
    keys = list(parsed.keys())
    assert keys == sorted(keys)
    assert text.endswith("\n")


def test_from_json_round_trip() -> None:
    lock = _sample()
    restored = Lockfile.from_json(lock.to_json())
    assert restored == lock
    assert isinstance(restored.services, tuple)


def test_write_then_read(tmp_path: Path) -> None:
    lock = _sample()
    p = tmp_path / "lock.json"
    lock.write(p)
    assert lock.read(p) == lock


def test_from_json_rejects_missing_field() -> None:
    incomplete = json.dumps(
        {
            "repo": "x",
            "requested_ref": "main",
            "resolved_sha": "abc",
            "tool_version": "0.1",
            "services": [],
            # endpoint_count missing
        }
    )
    with pytest.raises(KeyError):
        Lockfile.from_json(incomplete)
