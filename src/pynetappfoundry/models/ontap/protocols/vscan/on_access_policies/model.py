"""OntapVscanOnAccess information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapVscanOnAccessScope(OntapModel):
    """OntapVscanOnAccessScope sub-model for scope."""

    exclude_extensions: list[str] = Field(default_factory=list)
    exclude_paths: list[str] = Field(default_factory=list)
    include_extensions: list[str] = Field(default_factory=list)
    max_file_size: int = 0
    only_execute_access: bool = False
    scan_readonly_volumes: bool = False
    scan_without_extension: bool = False


class OntapVscanOnAccessSvm(OntapModel):
    """OntapVscanOnAccessSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapVscanOnAccess(OntapModel):
    """OntapVscanOnAccess information."""

    enabled: bool = False
    mandatory: bool = False
    name: str = ""
    scope: OntapVscanOnAccessScope = Field(default_factory=OntapVscanOnAccessScope)
    svm: OntapVscanOnAccessSvm = Field(default_factory=OntapVscanOnAccessSvm)
