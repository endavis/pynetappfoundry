"""Synthetic models for ``pynetappfoundry.data`` tests.

These live in a regular module (not ``conftest.py``) so test files can
import them directly without going through pytest's conftest discovery
machinery.
"""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class FakeVolume(OntapModel):
    """Synthetic single-key model used by data tests."""

    name: str = ""
    uuid: str = ""
    size: int = 0
    iops: float = 0.0
    is_root: bool = False
    files_scanned: int = 0


class FakeComposite(OntapModel):
    """Synthetic composite-key model."""

    svm_name: str = ""
    name: str = ""
