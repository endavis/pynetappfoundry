"""OntapTapeDevice information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapTapeDeviceAlias(OntapModel):
    """OntapTapeDeviceAlias sub-model for aliases."""

    mapping: str = ""
    name: str = ""


class OntapTapeDeviceDeviceName(OntapModel):
    """OntapTapeDeviceDeviceName sub-model for device_names."""

    no_rewind_device: str = ""
    rewind_device: str = ""
    unload_reload_device: str = ""


class OntapTapeDevice(OntapModel):
    """OntapTapeDevice information."""

    alias_mapping: str = ""
    alias_name: str = ""
    aliases: list[OntapTapeDeviceAlias] = Field(default_factory=list)
    block_number: int = 0
    density: str = ""
    description: str = ""
    device_id: str = ""
    device_names: list[OntapTapeDeviceDeviceName] = Field(default_factory=list)
    device_state: str = ""
    file_number: int = 0
    formats: list[str] = Field(default_factory=list)
    interface: str = ""
    node_name: str = ""
    node_uuid: str = ""
    online: bool = False
    position_count: int = 0
    position_operation: str = ""
    reservation_type: str = ""
    residual_count: int = 0
    serial_number: str = ""
    storage_port_name: str = ""
    type_: str = ""
    wwnn: str = ""
    wwpn: str = ""
