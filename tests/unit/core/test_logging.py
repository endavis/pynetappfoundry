"""Tests for setup_logger, and that unit tests keep its output out of the repository (#864)."""

from __future__ import annotations

import logging
from collections.abc import Iterator
from pathlib import Path

import pytest

from pynetappfoundry.core.logging import setup_logger

REPO_ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture
def _drop_added_handlers() -> Iterator[None]:
    """Close and remove any handler a test adds to the root logger."""
    root = logging.getLogger()
    before = list(root.handlers)
    level = root.level
    yield
    for handler in [h for h in root.handlers if h not in before]:
        root.removeHandler(handler)
        handler.close()
    root.setLevel(level)


def test_unit_tests_run_in_tmp_path(tmp_path: Path) -> None:
    """tests/unit/conftest.py moves every unit test out of the repository root."""
    assert Path.cwd() == tmp_path
    assert Path.cwd() != REPO_ROOT


@pytest.mark.usefixtures("_drop_added_handlers")
def test_setup_logger_writes_under_the_working_directory(tmp_path: Path) -> None:
    """The log lands in tmp_path/data, and nothing in the repository's data/."""
    _, log_file = setup_logger("isolation-check")

    assert log_file.parent == tmp_path / "data" / "isolation-check" / "logs"
    assert log_file.is_file()
    assert not (REPO_ROOT / "data" / "isolation-check").exists()
