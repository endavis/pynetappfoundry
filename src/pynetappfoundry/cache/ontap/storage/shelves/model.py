"""OntapShelf information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapShelfAcp(CacheModel):
    """OntapShelfAcp sub-model for acps."""

    acps_address: str = ""
    acps_channel: str = ""
    acps_connection_state: str = ""
    acps_enabled: bool = False
    acps_error_reason_arguments: list[dict[str, Any]] = Field(default_factory=list)
    acps_error_reason_code: str = ""
    acps_error_reason_message: str = ""
    acps_error_severity: str = ""
    acps_error_type: str = ""
    acps_netmask: str = ""
    acps_node_name: str = ""
    acps_node_uuid: str = ""
    acps_port: str = ""
    acps_subnet: str = ""


class OntapShelfBay(CacheModel):
    """OntapShelfBay sub-model for bays."""

    bays_drawer_id: int = 0
    bays_drawer_slot: int = 0
    bays_has_disk: bool = False
    bays_id: int = 0
    bays_state: str = ""
    bays_type: str = ""


class OntapShelfCurrentSensor(CacheModel):
    """OntapShelfCurrentSensor sub-model for current_sensors."""

    current_sensors_current: int = 0
    current_sensors_id: int = 0
    current_sensors_installed: bool = False
    current_sensors_location: str = ""
    current_sensors_state: str = ""


class OntapShelfDrawer(CacheModel):
    """OntapShelfDrawer sub-model for drawers."""

    drawers_closed: bool = False
    drawers_disk_count: int = 0
    drawers_error: str = ""
    drawers_id: int = 0
    drawers_part_number: str = ""
    drawers_serial_number: str = ""
    drawers_state: str = ""


class OntapShelfError(CacheModel):
    """OntapShelfError sub-model for errors."""

    errors_reason_arguments: list[dict[str, Any]] = Field(default_factory=list)
    errors_reason_code: str = ""
    errors_reason_message: str = ""


class OntapShelfFan(CacheModel):
    """OntapShelfFan sub-model for fans."""

    fans_id: int = 0
    fans_installed: bool = False
    fans_location: str = ""
    fans_rpm: int = 0
    fans_state: str = ""


class OntapShelfFru(CacheModel):
    """OntapShelfFru sub-model for frus."""

    frus_firmware_version: str = ""
    frus_id: int = 0
    frus_installed: bool = False
    frus_part_number: str = ""
    frus_psu_crest_factor: int = 0
    frus_psu_model: str = ""
    frus_psu_power_drawn: int = 0
    frus_psu_power_rating: int = 0
    frus_serial_number: str = ""
    frus_state: str = ""
    frus_type: str = ""


class OntapShelfPath(CacheModel):
    """OntapShelfPath sub-model for paths."""

    paths_name: str = ""
    paths_node_name: str = ""
    paths_node_uuid: str = ""


class OntapShelfPort(CacheModel):
    """OntapShelfPort sub-model for ports."""

    ports_cable_identifier: str = ""
    ports_cable_length: str = ""
    ports_cable_part_number: str = ""
    ports_cable_serial_number: str = ""
    ports_designator: str = ""
    ports_id: int = 0
    ports_internal: bool = False
    ports_mac_address: str = ""
    ports_module_id: str = ""
    ports_remote_chassis: str = ""
    ports_remote_device: str = ""
    ports_remote_mac_address: str = ""
    ports_remote_phy: str = ""
    ports_remote_port: str = ""
    ports_remote_wwn: str = ""
    ports_state: str = ""
    ports_wwn: str = ""


class OntapShelfTemperatureSensor(CacheModel):
    """OntapShelfTemperatureSensor sub-model for temperature_sensors."""

    temperature_sensors_ambient: bool = False
    temperature_sensors_id: int = 0
    temperature_sensors_installed: bool = False
    temperature_sensors_location: str = ""
    temperature_sensors_state: str = ""
    temperature_sensors_temperature: int = 0
    temperature_sensors_threshold_high_critical: int = 0
    temperature_sensors_threshold_high_warning: int = 0
    temperature_sensors_threshold_low_critical: int = 0
    temperature_sensors_threshold_low_warning: int = 0


class OntapShelfVoltageSensor(CacheModel):
    """OntapShelfVoltageSensor sub-model for voltage_sensors."""

    voltage_sensors_id: int = 0
    voltage_sensors_installed: bool = False
    voltage_sensors_location: str = ""
    voltage_sensors_state: str = ""
    voltage_sensors_voltage: float = 0.0


class OntapShelf(CacheModel):
    """OntapShelf information."""

    acps: list[OntapShelfAcp] = Field(default_factory=list)
    bays: list[OntapShelfBay] = Field(default_factory=list)
    connection_type: str = ""
    current_sensors: list[OntapShelfCurrentSensor] = Field(default_factory=list)
    disk_count: int = 0
    drawers: list[OntapShelfDrawer] = Field(default_factory=list)
    errors: list[OntapShelfError] = Field(default_factory=list)
    fans: list[OntapShelfFan] = Field(default_factory=list)
    frus: list[OntapShelfFru] = Field(default_factory=list)
    id: str = ""
    internal: bool = False
    local: bool = False
    location_led: str = ""
    manufacturer_name: str = ""
    model_: str = ""
    module_type: str = ""
    name: str = ""
    paths: list[OntapShelfPath] = Field(default_factory=list)
    ports: list[OntapShelfPort] = Field(default_factory=list)
    serial_number: str = ""
    state: str = ""
    temperature_sensors: list[OntapShelfTemperatureSensor] = Field(default_factory=list)
    uid: str = ""
    vendor_manufacturer: str = ""
    vendor_name: str = ""
    vendor_part_number: str = ""
    vendor_product: str = ""
    vendor_serial_number: str = ""
    voltage_sensors: list[OntapShelfVoltageSensor] = Field(default_factory=list)
