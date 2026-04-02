"""OntapVscanOnDemand information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapVscanOnDemandSchedule(OntapModel):
    """OntapVscanOnDemandSchedule sub-model for schedule."""

    name: str = ""
    uuid: str = ""


class OntapVscanOnDemandScope(OntapModel):
    """OntapVscanOnDemandScope sub-model for scope."""

    exclude_extensions: list[str] = Field(default_factory=list)
    exclude_paths: list[str] = Field(default_factory=list)
    include_extensions: list[str] = Field(default_factory=list)
    max_file_size: int = 0
    scan_without_extension: bool = False


class OntapVscanOnDemandSvm(OntapModel):
    """OntapVscanOnDemandSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapVscanOnDemand(OntapModel):
    """OntapVscanOnDemand information."""

    log_path: str = ""
    name: str = ""
    scan_paths: list[str] = Field(default_factory=list)
    schedule: OntapVscanOnDemandSchedule = Field(default_factory=OntapVscanOnDemandSchedule)
    scope: OntapVscanOnDemandScope = Field(default_factory=OntapVscanOnDemandScope)
    svm: OntapVscanOnDemandSvm = Field(default_factory=OntapVscanOnDemandSvm)
