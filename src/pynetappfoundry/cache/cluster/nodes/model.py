"""Node information — /cluster/nodes."""

from __future__ import annotations

from pydantic import Field, field_validator

from pynetappfoundry.cache._base import CacheModel


class NodeInfo(CacheModel):
    """Information about a single cluster node."""

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
