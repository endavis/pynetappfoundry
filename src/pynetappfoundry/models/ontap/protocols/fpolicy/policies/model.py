"""OntapFpolicyPolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFpolicyPolicyEvent(OntapModel):
    """OntapFpolicyPolicyEvent sub-model for events."""

    events_name: str = ""


class OntapFpolicyPolicy(OntapModel):
    """OntapFpolicyPolicy information."""

    allow_privileged_access: bool = False
    enabled: bool = False
    engine_name: str = ""
    events: list[OntapFpolicyPolicyEvent] = Field(default_factory=list)
    mandatory: bool = False
    name: str = ""
    passthrough_read: bool = False
    persistent_store: str = ""
    priority: int = 0
    privileged_user: str = ""
    scope_check_extensions_on_directories: bool = False
    scope_exclude_export_policies: list[str] = Field(default_factory=list)
    scope_exclude_extension: list[str] = Field(default_factory=list)
    scope_exclude_shares: list[str] = Field(default_factory=list)
    scope_exclude_volumes: list[str] = Field(default_factory=list)
    scope_include_export_policies: list[str] = Field(default_factory=list)
    scope_include_extension: list[str] = Field(default_factory=list)
    scope_include_shares: list[str] = Field(default_factory=list)
    scope_include_volumes: list[str] = Field(default_factory=list)
    scope_object_monitoring_with_no_extension: bool = False
    svm_uuid: str = ""
