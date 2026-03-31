"""OntapStorageSwitch information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapStorageSwitchConnection(OntapModel):
    """OntapStorageSwitchConnection sub-model for connections."""

    peer_port_connection: str = ""
    peer_port_type: str = ""
    peer_port_unique_id: str = ""
    peer_port_wwn: str = ""
    source_port_mode: str = ""
    source_port_name: str = ""
    source_port_wwn: str = ""


class OntapStorageSwitchError(OntapModel):
    """OntapStorageSwitchError sub-model for errors."""

    component_id: int = 0
    component_name: str = ""
    reason_arguments: list[dict[str, Any]] = Field(default_factory=list)
    reason_code: str = ""
    reason_message: str = ""
    severity: str = ""
    type: str = ""


class OntapStorageSwitchFan(OntapModel):
    """OntapStorageSwitchFan sub-model for fans."""

    name: str = ""
    speed: int = 0
    state: str = ""


class OntapStorageSwitchPath(OntapModel):
    """OntapStorageSwitchPath sub-model for paths."""

    adapter_name: str = ""
    adapter_type: str = ""
    adapter_wwn: str = ""
    node_name: str = ""
    node_uuid: str = ""
    port_name: str = ""
    port_speed: int = 0


class OntapStorageSwitchPort(OntapModel):
    """OntapStorageSwitchPort sub-model for ports."""

    enabled: bool = False
    mode: str = ""
    name: str = ""
    sfp_serial_number: str = ""
    sfp_transmitter_type: str = ""
    sfp_type: str = ""
    speed: int = 0
    state: str = ""
    wwn: str = ""


class OntapStorageSwitchPowerSupplyUnit(OntapModel):
    """OntapStorageSwitchPowerSupplyUnit sub-model for power_supply_units."""

    name: str = ""
    state: str = ""


class OntapStorageSwitchTemperatureSensor(OntapModel):
    """OntapStorageSwitchTemperatureSensor sub-model for temperature_sensors."""

    name: str = ""
    reading: int = 0
    state: str = ""


class OntapStorageSwitchVsan(OntapModel):
    """OntapStorageSwitchVsan sub-model for vsans."""

    id: int = 0
    iod: bool = False
    load_balancing_types: str = ""
    name: str = ""
    state: str = ""


class OntapStorageSwitchZone(OntapModel):
    """OntapStorageSwitchZone sub-model for zones."""

    id: int = 0
    name: str = ""
    port_id: str = ""
    port_name: str = ""
    wwn: str = ""


class OntapStorageSwitch(OntapModel):
    """OntapStorageSwitch information."""

    connections: list[OntapStorageSwitchConnection] = Field(default_factory=list)
    director_class: bool = False
    domain_id: int = 0
    errors: list[OntapStorageSwitchError] = Field(default_factory=list)
    fabric_name: str = ""
    fans: list[OntapStorageSwitchFan] = Field(default_factory=list)
    firmware_version: str = ""
    ip_address: str = ""
    local: bool = False
    model_: str = ""
    monitored_blades: list[int] = Field(default_factory=list)
    monitoring_enabled: bool = False
    name: str = ""
    paths: list[OntapStorageSwitchPath] = Field(default_factory=list)
    ports: list[OntapStorageSwitchPort] = Field(default_factory=list)
    power_supply_units: list[OntapStorageSwitchPowerSupplyUnit] = Field(default_factory=list)
    role: str = ""
    state: str = ""
    symbolic_name: str = ""
    temperature_sensors: list[OntapStorageSwitchTemperatureSensor] = Field(default_factory=list)
    vendor: str = ""
    vsans: list[OntapStorageSwitchVsan] = Field(default_factory=list)
    wwn: str = ""
    zones: list[OntapStorageSwitchZone] = Field(default_factory=list)
