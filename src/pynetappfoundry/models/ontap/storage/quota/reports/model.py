"""OntapQuotaReport information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapQuotaReportFilesUsed(OntapModel):
    """OntapQuotaReportFilesUsed sub-model for used."""

    hard_limit_percent: int = 0
    soft_limit_percent: int = 0
    total: int = 0


class OntapQuotaReportFiles(OntapModel):
    """OntapQuotaReportFiles sub-model for files."""

    hard_limit: int = 0
    soft_limit: int = 0
    used: OntapQuotaReportFilesUsed = Field(default_factory=OntapQuotaReportFilesUsed)


class OntapQuotaReportGroup(OntapModel):
    """OntapQuotaReportGroup sub-model for group."""

    id: str = ""
    name: str = ""


class OntapQuotaReportQtree(OntapModel):
    """OntapQuotaReportQtree sub-model for qtree."""

    id: int = 0
    name: str = ""


class OntapQuotaReportSpaceUsed(OntapModel):
    """OntapQuotaReportSpaceUsed sub-model for used."""

    hard_limit_percent: int = 0
    soft_limit_percent: int = 0
    total: int = 0


class OntapQuotaReportSpace(OntapModel):
    """OntapQuotaReportSpace sub-model for space."""

    hard_limit: int = 0
    soft_limit: int = 0
    used: OntapQuotaReportSpaceUsed = Field(default_factory=OntapQuotaReportSpaceUsed)


class OntapQuotaReportSvm(OntapModel):
    """OntapQuotaReportSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapQuotaReportUser(OntapModel):
    """OntapQuotaReportUser sub-model for users."""

    id: str = ""
    name: str = ""


class OntapQuotaReportVolume(OntapModel):
    """OntapQuotaReportVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapQuotaReport(OntapModel):
    """OntapQuotaReport information."""

    files: OntapQuotaReportFiles = Field(default_factory=OntapQuotaReportFiles)
    group: OntapQuotaReportGroup = Field(default_factory=OntapQuotaReportGroup)
    index: int = 0
    qtree: OntapQuotaReportQtree = Field(default_factory=OntapQuotaReportQtree)
    space: OntapQuotaReportSpace = Field(default_factory=OntapQuotaReportSpace)
    svm: OntapQuotaReportSvm = Field(default_factory=OntapQuotaReportSvm)
    type_: str = ""
    users: list[OntapQuotaReportUser] = Field(default_factory=list)
    volume: OntapQuotaReportVolume = Field(default_factory=OntapQuotaReportVolume)
