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


class FakeParentModel(OntapModel):
    """Synthetic parent model for parent-keyed partial-fetch tests."""

    name: str = ""
    uuid: str = ""


class FakeChildVolume(OntapModel):
    """Nested sub-model providing a parent back-reference via ``uuid``."""

    uuid: str = ""


class FakeChildWithDottedRef(OntapModel):
    """Synthetic child with nested parent ref via ``volume.uuid``."""

    uuid: str = ""
    volume: FakeChildVolume = FakeChildVolume()
    metric: float = 0.0


class FakeOrphanChild(OntapModel):
    """Synthetic child with no parent back-reference (SvmMigrationVolume-like)."""

    volume_uuid: str = ""
    transfer_state: str = ""
