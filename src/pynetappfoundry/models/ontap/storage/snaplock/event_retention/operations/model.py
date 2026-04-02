"""OntapEbrOperation information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapEbrOperationPolicy(OntapModel):
    """OntapEbrOperationPolicy sub-model for policy."""

    name: str = ""
    retention_period: str = ""


class OntapEbrOperationSvm(OntapModel):
    """OntapEbrOperationSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapEbrOperationVolume(OntapModel):
    """OntapEbrOperationVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapEbrOperation(OntapModel):
    """OntapEbrOperation information."""

    id: int = 0
    num_files_failed: int = 0
    num_files_processed: int = 0
    num_files_skipped: int = 0
    num_inodes_ignored: int = 0
    path: str = ""
    policy: OntapEbrOperationPolicy = Field(default_factory=OntapEbrOperationPolicy)
    state: str = ""
    svm: OntapEbrOperationSvm = Field(default_factory=OntapEbrOperationSvm)
    volume: OntapEbrOperationVolume = Field(default_factory=OntapEbrOperationVolume)
