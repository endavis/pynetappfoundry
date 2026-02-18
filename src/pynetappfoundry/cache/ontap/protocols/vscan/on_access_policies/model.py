"""OntapVscanOnAccess information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapVscanOnAccess(CacheModel):
    """OntapVscanOnAccess information."""

    enabled: bool = False
    mandatory: bool = False
    name: str = ""
    scope_exclude_extensions: list[str] = Field(default_factory=list)
    scope_exclude_paths: list[str] = Field(default_factory=list)
    scope_include_extensions: list[str] = Field(default_factory=list)
    scope_max_file_size: int = 0
    scope_only_execute_access: bool = False
    scope_scan_readonly_volumes: bool = False
    scope_scan_without_extension: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
