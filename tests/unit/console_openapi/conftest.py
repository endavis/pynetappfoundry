"""Shared fixtures for the Console OpenAPI tool tests: the committed spec, built once (#1148).

Parsing the 6 MB committed spec and running ``apply-fragments`` on it (parse, validate, dump) cost
seconds each, and many tests did both. Same idea as ``tests/unit/clients/console/conftest.py``
(#1139): do the work once per session and share it.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, NamedTuple

import pytest
from click.testing import CliRunner, Result

from tools.console_openapi import cli as cli_module
from tools.console_openapi import client_codegen

COMMITTED_SPEC = (
    Path(__file__).resolve().parents[3] / "tools/console_openapi/generated/console_openapi.yaml"
)


@pytest.fixture(scope="session")
def committed_spec_text() -> str:
    """The committed spec file, read once per session."""
    return COMMITTED_SPEC.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def _committed_spec_parsed() -> dict[str, Any]:
    """The committed spec parsed once per session with the production loader. Never hand out."""
    return client_codegen.load_spec(COMMITTED_SPEC)


@pytest.fixture
def committed_spec(_committed_spec_parsed: dict[str, Any]) -> dict[str, Any]:
    """A private deep copy of the parsed committed spec, safe to mutate."""
    return copy.deepcopy(_committed_spec_parsed)


class ApplyFragmentsRuns(NamedTuple):
    """The spec text before, and each pass's CLI result with the file text after it."""

    before: str
    runs: list[tuple[Result, str]]


@pytest.fixture(scope="session")
def apply_fragments_twice(
    tmp_path_factory: pytest.TempPathFactory, committed_spec_text: str
) -> ApplyFragmentsRuns:
    """Run the real, unstubbed ``apply-fragments`` twice on a copy of the committed spec.

    This is the uncached end-to-end run (load, strip, merge, overrides, invariants, validate,
    dump). It is shared only because the two idempotency tests that use it are identical.
    """
    target = tmp_path_factory.mktemp("apply_fragments") / "spec.yaml"
    target.write_text(committed_spec_text, encoding="utf-8")
    runs: list[tuple[Result, str]] = []
    for _ in range(2):
        result = CliRunner().invoke(cli_module.cli, ["apply-fragments", "--spec", str(target)])
        runs.append((result, target.read_text(encoding="utf-8")))
    return ApplyFragmentsRuns(before=committed_spec_text, runs=runs)
