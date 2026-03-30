"""OntapVscanOnDemand information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapVscanOnDemand(OntapModel):
    """OntapVscanOnDemand information."""

    log_path: str = ""
    name: str = ""
    scan_paths: list[str] = Field(default_factory=list)
    schedule_name: str = ""
    schedule_uuid: str = ""
    scope_exclude_extensions: list[str] = Field(default_factory=list)
    scope_exclude_paths: list[str] = Field(default_factory=list)
    scope_include_extensions: list[str] = Field(default_factory=list)
    scope_max_file_size: int = 0
    scope_scan_without_extension: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
