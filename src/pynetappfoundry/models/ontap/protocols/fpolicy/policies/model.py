"""OntapFpolicyPolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFpolicyPolicyEngine(OntapModel):
    """OntapFpolicyPolicyEngine sub-model for engine."""

    name: str = ""


class OntapFpolicyPolicyEvent(OntapModel):
    """OntapFpolicyPolicyEvent sub-model for events."""

    name: str = ""


class OntapFpolicyPolicyScope(OntapModel):
    """OntapFpolicyPolicyScope sub-model for scope."""

    check_extensions_on_directories: bool = False
    exclude_export_policies: list[str] = Field(default_factory=list)
    exclude_extension: list[str] = Field(default_factory=list)
    exclude_shares: list[str] = Field(default_factory=list)
    exclude_volumes: list[str] = Field(default_factory=list)
    include_export_policies: list[str] = Field(default_factory=list)
    include_extension: list[str] = Field(default_factory=list)
    include_shares: list[str] = Field(default_factory=list)
    include_volumes: list[str] = Field(default_factory=list)
    object_monitoring_with_no_extension: bool = False


class OntapFpolicyPolicySvm(OntapModel):
    """OntapFpolicyPolicySvm sub-model for svm."""

    uuid: str = ""


class OntapFpolicyPolicy(OntapModel):
    """OntapFpolicyPolicy information."""

    allow_privileged_access: bool = False
    enabled: bool = False
    engine: OntapFpolicyPolicyEngine = Field(default_factory=OntapFpolicyPolicyEngine)
    events: list[OntapFpolicyPolicyEvent] = Field(default_factory=list)
    mandatory: bool = False
    name: str = ""
    passthrough_read: bool = False
    persistent_store: str = ""
    priority: int = 0
    privileged_user: str = ""
    scope: OntapFpolicyPolicyScope = Field(default_factory=OntapFpolicyPolicyScope)
    svm: OntapFpolicyPolicySvm = Field(default_factory=OntapFpolicyPolicySvm)
