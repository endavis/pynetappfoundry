"""OntapVscan information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapVscanScope(OntapModel):
    """OntapVscanScope sub-model for scope."""

    exclude_extensions: list[str] = Field(default_factory=list)
    exclude_paths: list[str] = Field(default_factory=list)
    include_extensions: list[str] = Field(default_factory=list)
    max_file_size: int = 0
    only_execute_access: bool = False
    scan_readonly_volumes: bool = False
    scan_without_extension: bool = False


class OntapVscan(OntapModel):
    """OntapVscan information."""

    enabled: bool = False
    mandatory: bool = False
    name: str = ""
    scope: OntapVscanScope = Field(default_factory=OntapVscanScope)
