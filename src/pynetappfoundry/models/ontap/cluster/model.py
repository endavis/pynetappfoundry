"""Core cluster identity information — /cluster."""

from __future__ import annotations

from pydantic import Field, field_validator

from pynetappfoundry.models._base import OntapModel


class ClusterInfo(OntapModel):
    """Core cluster identity information.

    Contains cluster name, UUID, and version from ONTAP.
    """

    cluster_name: str = ""
    cluster_uuid: str = ""
    ontap_version: str = ""
    version_generation: str = ""
    version_major: int = 0
    version_minor: int = 0
    contact: str = ""
    location: str = ""
    is_ha: bool = False
    san_optimized: bool = False
    timezone: str = ""
    dns_domains: list[str] = Field(default_factory=list)
    name_servers: list[str] = Field(default_factory=list)
    ntp_servers: list[str] = Field(default_factory=list)
    peering_policy_authentication_required: bool = False
    peering_policy_encryption_required: bool = False
    peering_policy_minimum_passphrase_length: int = 0
    management_interface_uuids: list[str] = Field(default_factory=list)
    disaggregated: bool = False
    auto_enable_activity_tracking: bool = False
    auto_enable_analytics: bool = False

    @field_validator("version_generation", mode="before")
    @classmethod
    def coerce_version_generation_to_str(cls, v: object) -> str:
        """Coerce version_generation to string (API sometimes returns int)."""
        return str(v) if v is not None else ""
