"""OntapAntiRansomwareSuspect information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapAntiRansomwareSuspectFile(OntapModel):
    """OntapAntiRansomwareSuspectFile sub-model for file."""

    format: str = ""
    name: str = ""
    path: str = ""
    reason: str = ""
    suspect_time: str = ""


class OntapAntiRansomwareSuspectVolume(OntapModel):
    """OntapAntiRansomwareSuspectVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapAntiRansomwareSuspect(OntapModel):
    """OntapAntiRansomwareSuspect information."""

    file: OntapAntiRansomwareSuspectFile = Field(default_factory=OntapAntiRansomwareSuspectFile)
    volume: OntapAntiRansomwareSuspectVolume = Field(
        default_factory=OntapAntiRansomwareSuspectVolume
    )
