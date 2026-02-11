"""Cluster identity and node models (/cluster API path)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ClusterInfo(BaseModel):
    """Core cluster identity information.

    Contains cluster name, UUID, and version from ONTAP.
    """

    model_config = ConfigDict(extra="allow")

    cluster_name: str = ""
    cluster_uuid: str = ""
    ontap_version: str = ""
    model: str = ""
    contact: str = ""
    location: str = ""

    @field_validator("model", mode="before")
    @classmethod
    def coerce_model_to_str(cls, v: object) -> str:
        """Coerce model field to string (API sometimes returns int)."""
        return str(v) if v is not None else ""


class NodeInfo(BaseModel):
    """Information about a single cluster node."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    serial_number: str = ""
    system_id: str = ""
    model: str = ""
    location: str = ""

    @field_validator("system_id", "model", mode="before")
    @classmethod
    def coerce_to_str(cls, v: object) -> str:
        """Coerce system_id and model to string (API sometimes returns int)."""
        return str(v) if v is not None else ""

    membership: str = ""
    version_full: str = ""
    storage_configuration: str = ""
    system_machine_type: str = ""
    controller_board: str = ""
    controller_memory_size: int = 0
    controller_cpu_count: int = 0
    vm_provider_type: str = ""
    ha_enabled: bool = False
    ha_auto_giveback: bool = False
    ha_partner_uuids: list[str] = Field(default_factory=list)
    system_aggregate_uuid: str = ""
    cluster_interface_uuids: list[str] = Field(default_factory=list)
    management_interface_uuids: list[str] = Field(default_factory=list)


class HAInfo(BaseModel):
    """High Availability configuration information.

    For CVO HA configurations.
    """

    model_config = ConfigDict(extra="allow")

    is_ha: bool = False
    partner_node: str = ""
    ha_state: str = ""
    mediator_address: str = ""


class LicenseFeature(BaseModel):
    """License feature information."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    state: str = ""  # compliant, noncompliant
    scope: str = ""  # cluster, node


class CapacityLicense(BaseModel):
    """Capacity-based license information."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    licensed_capacity: int = 0  # bytes
    used_capacity: int = 0  # bytes


class LicenseInfo(BaseModel):
    """Licensing information.

    Contains feature and capacity licenses.
    """

    model_config = ConfigDict(extra="allow")

    feature_licenses: list[LicenseFeature] = Field(default_factory=list)
    capacity_licenses: list[CapacityLicense] = Field(default_factory=list)


class ScheduleInfo(BaseModel):
    """Job schedule information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    type: str = ""  # cron, interval
    scope: str = ""  # cluster, svm
    svm: str = ""
    cron: dict[str, list[int]] = Field(default_factory=dict)
    interval: str = ""
