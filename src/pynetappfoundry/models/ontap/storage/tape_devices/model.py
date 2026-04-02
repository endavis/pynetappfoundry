"""OntapTapeDevice information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapTapeDeviceAlias(OntapModel):
    """OntapTapeDeviceAlias sub-model for alias."""

    mapping: str = ""
    name: str = ""


class OntapTapeDeviceAlias2(OntapModel):
    """OntapTapeDeviceAlias2 sub-model for aliases."""

    mapping: str = ""
    name: str = ""


class OntapTapeDeviceDeviceName(OntapModel):
    """OntapTapeDeviceDeviceName sub-model for device_names."""

    no_rewind_device: str = ""
    rewind_device: str = ""
    unload_reload_device: str = ""


class OntapTapeDeviceNode(OntapModel):
    """OntapTapeDeviceNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapTapeDevicePosition(OntapModel):
    """OntapTapeDevicePosition sub-model for position."""

    count: int = 0
    operation: str = ""


class OntapTapeDeviceStoragePort(OntapModel):
    """OntapTapeDeviceStoragePort sub-model for storage_port."""

    name: str = ""


class OntapTapeDevice(OntapModel):
    """OntapTapeDevice information."""

    alias: OntapTapeDeviceAlias = Field(default_factory=OntapTapeDeviceAlias)
    aliases: list[OntapTapeDeviceAlias2] = Field(default_factory=list)
    block_number: int = 0
    density: str = ""
    description: str = ""
    device_id: str = ""
    device_names: list[OntapTapeDeviceDeviceName] = Field(default_factory=list)
    device_state: str = ""
    file_number: int = 0
    formats: list[str] = Field(default_factory=list)
    interface: str = ""
    node: OntapTapeDeviceNode = Field(default_factory=OntapTapeDeviceNode)
    online: bool = False
    position: OntapTapeDevicePosition = Field(default_factory=OntapTapeDevicePosition)
    reservation_type: str = ""
    residual_count: int = 0
    serial_number: str = ""
    storage_port: OntapTapeDeviceStoragePort = Field(default_factory=OntapTapeDeviceStoragePort)
    type_: str = ""
    wwnn: str = ""
    wwpn: str = ""
