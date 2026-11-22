"""Shared fixtures for the Console client tests: the real spec, parsed once per session (#1139).

Parsing the real Console spec costs seconds, and many tests build a client on it. The session
fixture parses it once; the function fixture routes ``openapi._load_spec`` to that dict for the
real spec path only.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

import pynetappfoundry.clients.openapi as openapi

REAL_SPEC = Path(__file__).parents[4] / "tools/console_openapi/generated/console_openapi.yaml"


@pytest.fixture(scope="session")
def real_console_spec() -> dict[str, Any]:
    """The real Console spec, parsed once per session with the production loader.

    The dict is shared by every test that uses it, so treat it as read-only.
    """
    return openapi._load_spec(REAL_SPEC)


@pytest.fixture
def real_spec_dir(real_console_spec: dict[str, Any], monkeypatch: pytest.MonkeyPatch) -> Path:
    """Directory of the real spec; ``APIWrapper`` construction on it reuses the session parse.

    Any other path still goes to the real loader.
    """
    real_load: Callable[[str | Path], dict[str, Any]] = openapi._load_spec
    real_resolved = REAL_SPEC.resolve()

    def _cached_load(path: str | Path) -> dict[str, Any]:
        if Path(path).resolve() == real_resolved:
            return real_console_spec
        return real_load(path)

    monkeypatch.setattr(openapi, "_load_spec", _cached_load)
    return REAL_SPEC.parent
