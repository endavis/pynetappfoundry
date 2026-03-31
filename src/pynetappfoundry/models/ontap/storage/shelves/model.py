"""OntapShelf information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapShelfAcp(OntapModel):
    """OntapShelfAcp sub-model for acps."""

    address: str = ""
    channel: str = ""
    connection_state: str = ""
    enabled: bool = False
    error_reason_arguments: list[dict[str, Any]] = Field(default_factory=list)
    error_reason_code: str = ""
    error_reason_message: str = ""
    error_severity: str = ""
    error_type: str = ""
    netmask: str = ""
    node_name: str = ""
    node_uuid: str = ""
    port: str = ""
    subnet: str = ""


class OntapShelfBay(OntapModel):
    """OntapShelfBay sub-model for bays."""

    drawer_id: int = 0
    drawer_slot: int = 0
    has_disk: bool = False
    id: int = 0
    state: str = ""
    type: str = ""


class OntapShelfCurrentSensor(OntapModel):
    """OntapShelfCurrentSensor sub-model for current_sensors."""

    current: int = 0
    id: int = 0
    installed: bool = False
    location: str = ""
    state: str = ""


class OntapShelfDrawer(OntapModel):
    """OntapShelfDrawer sub-model for drawers."""

    closed: bool = False
    disk_count: int = 0
    error: str = ""
    id: int = 0
    part_number: str = ""
    serial_number: str = ""
    state: str = ""


class OntapShelfError(OntapModel):
    """OntapShelfError sub-model for errors."""

    reason_arguments: list[dict[str, Any]] = Field(default_factory=list)
    reason_code: str = ""
    reason_message: str = ""


class OntapShelfFan(OntapModel):
    """OntapShelfFan sub-model for fans."""

    id: int = 0
    installed: bool = False
    location: str = ""
    rpm: int = 0
    state: str = ""


class OntapShelfFru(OntapModel):
    """OntapShelfFru sub-model for frus."""

    firmware_version: str = ""
    id: int = 0
    installed: bool = False
    part_number: str = ""
    psu_crest_factor: int = 0
    psu_model: str = ""
    psu_power_drawn: int = 0
    psu_power_rating: int = 0
    serial_number: str = ""
    state: str = ""
    type: str = ""


class OntapShelfPath(OntapModel):
    """OntapShelfPath sub-model for paths."""

    name: str = ""
    node_name: str = ""
    node_uuid: str = ""


class OntapShelfPort(OntapModel):
    """OntapShelfPort sub-model for ports."""

    cable_identifier: str = ""
    cable_length: str = ""
    cable_part_number: str = ""
    cable_serial_number: str = ""
    designator: str = ""
    id: int = 0
    internal: bool = False
    mac_address: str = ""
    module_id: str = ""
    remote_chassis: str = ""
    remote_device: str = ""
    remote_mac_address: str = ""
    remote_phy: str = ""
    remote_port: str = ""
    remote_wwn: str = ""
    state: str = ""
    wwn: str = ""


class OntapShelfTemperatureSensor(OntapModel):
    """OntapShelfTemperatureSensor sub-model for temperature_sensors."""

    ambient: bool = False
    id: int = 0
    installed: bool = False
    location: str = ""
    state: str = ""
    temperature: int = 0
    threshold_high_critical: int = 0
    threshold_high_warning: int = 0
    threshold_low_critical: int = 0
    threshold_low_warning: int = 0


class OntapShelfVoltageSensor(OntapModel):
    """OntapShelfVoltageSensor sub-model for voltage_sensors."""

    id: int = 0
    installed: bool = False
    location: str = ""
    state: str = ""
    voltage: float = 0.0


class OntapShelf(OntapModel):
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
