"""OntapSplitStatus information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSplitStatusSvm(OntapModel):
    """OntapSplitStatusSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSplitStatusVolume(OntapModel):
    """OntapSplitStatusVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapSplitStatus(OntapModel):
    """OntapSplitStatus information."""

    pending_splits: int = 0
    svm: OntapSplitStatusSvm = Field(default_factory=OntapSplitStatusSvm)
    unsplit_size: int = 0
    volume: OntapSplitStatusVolume = Field(default_factory=OntapSplitStatusVolume)
