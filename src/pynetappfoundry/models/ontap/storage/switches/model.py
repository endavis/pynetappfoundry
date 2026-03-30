"""OntapStorageSwitch information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapStorageSwitchConnection(OntapModel):
    """OntapStorageSwitchConnection sub-model for connections."""

    connections_peer_port_connection: str = ""
    connections_peer_port_type: str = ""
    connections_peer_port_unique_id: str = ""
    connections_peer_port_wwn: str = ""
    connections_source_port_mode: str = ""
    connections_source_port_name: str = ""
    connections_source_port_wwn: str = ""


class OntapStorageSwitchError(OntapModel):
    """OntapStorageSwitchError sub-model for errors."""

    errors_component_id: int = 0
    errors_component_name: str = ""
    errors_reason_arguments: list[dict[str, Any]] = Field(default_factory=list)
    errors_reason_code: str = ""
    errors_reason_message: str = ""
    errors_severity: str = ""
    errors_type: str = ""


class OntapStorageSwitchFan(OntapModel):
    """OntapStorageSwitchFan sub-model for fans."""

    fans_name: str = ""
    fans_speed: int = 0
    fans_state: str = ""


class OntapStorageSwitchPath(OntapModel):
    """OntapStorageSwitchPath sub-model for paths."""

    paths_adapter_name: str = ""
    paths_adapter_type: str = ""
    paths_adapter_wwn: str = ""
    paths_node_name: str = ""
    paths_node_uuid: str = ""
    paths_port_name: str = ""
    paths_port_speed: int = 0


class OntapStorageSwitchPort(OntapModel):
    """OntapStorageSwitchPort sub-model for ports."""

    ports_enabled: bool = False
    ports_mode: str = ""
    ports_name: str = ""
    ports_sfp_serial_number: str = ""
    ports_sfp_transmitter_type: str = ""
    ports_sfp_type: str = ""
    ports_speed: int = 0
    ports_state: str = ""
    ports_wwn: str = ""


class OntapStorageSwitchPowerSupplyUnit(OntapModel):
    """OntapStorageSwitchPowerSupplyUnit sub-model for power_supply_units."""

    power_supply_units_name: str = ""
    power_supply_units_state: str = ""


class OntapStorageSwitchTemperatureSensor(OntapModel):
    """OntapStorageSwitchTemperatureSensor sub-model for temperature_sensors."""

    temperature_sensors_name: str = ""
    temperature_sensors_reading: int = 0
    temperature_sensors_state: str = ""


class OntapStorageSwitchVsan(OntapModel):
    """OntapStorageSwitchVsan sub-model for vsans."""

    vsans_id: int = 0
    vsans_iod: bool = False
    vsans_load_balancing_types: str = ""
    vsans_name: str = ""
    vsans_state: str = ""


class OntapStorageSwitchZone(OntapModel):
    """OntapStorageSwitchZone sub-model for zones."""

    zones_id: int = 0
    zones_name: str = ""
    zones_port_id: str = ""
    zones_port_name: str = ""
    zones_wwn: str = ""


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
