"""Shared fixtures for the unit tests."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _run_in_tmp_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Run each test from its own temporary directory (#864).

    ``Config`` and ``setup_logger`` write under ``os.getcwd() / "data"``, so a
    test that runs a CLI command from the repository root leaves log files in
    its ``data/``. Under mutmut, that happens once per mutant.
    """
    monkeypatch.chdir(tmp_path)
