"""OntapShelf information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapShelfAcpErrorReasonArgument(OntapModel):
    """OntapShelfAcpErrorReasonArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapShelfAcpErrorReason(OntapModel):
    """OntapShelfAcpErrorReason sub-model for reason."""

    arguments: list[OntapShelfAcpErrorReasonArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapShelfAcpError(OntapModel):
    """OntapShelfAcpError sub-model for error."""

    reason: OntapShelfAcpErrorReason = Field(default_factory=OntapShelfAcpErrorReason)
    severity: str = ""
    type_: str = ""


class OntapShelfAcpNode(OntapModel):
    """OntapShelfAcpNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapShelfAcp(OntapModel):
    """OntapShelfAcp sub-model for acps."""

    address: str = ""
    channel: str = ""
    connection_state: str = ""
    enabled: bool = False
    error: OntapShelfAcpError = Field(default_factory=OntapShelfAcpError)
    netmask: str = ""
    node: OntapShelfAcpNode = Field(default_factory=OntapShelfAcpNode)
    port: str = ""
    subnet: str = ""


class OntapShelfBayDrawer(OntapModel):
    """OntapShelfBayDrawer sub-model for drawer."""

    id: int = 0
    slot: int = 0


class OntapShelfBay(OntapModel):
    """OntapShelfBay sub-model for bays."""

    drawer: OntapShelfBayDrawer = Field(default_factory=OntapShelfBayDrawer)
    has_disk: bool = False
    id: int = 0
    state: str = ""
    type_: str = ""


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


class OntapShelfFan(OntapModel):
    """OntapShelfFan sub-model for fans."""

    id: int = 0
    installed: bool = False
    location: str = ""
    rpm: int = 0
    state: str = ""


class OntapShelfFruPsu(OntapModel):
    """OntapShelfFruPsu sub-model for psu."""

    crest_factor: int = 0
    model_: str = ""
    power_drawn: int = 0
    power_rating: int = 0


class OntapShelfFru(OntapModel):
    """OntapShelfFru sub-model for frus."""

    firmware_version: str = ""
    id: int = 0
    installed: bool = False
    part_number: str = ""
    psu: OntapShelfFruPsu = Field(default_factory=OntapShelfFruPsu)
    serial_number: str = ""
    state: str = ""
    type_: str = ""


class OntapShelfManufacturer(OntapModel):
    """OntapShelfManufacturer sub-model for manufacturer."""

    name: str = ""


class OntapShelfPathNode(OntapModel):
    """OntapShelfPathNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapShelfPath(OntapModel):
    """OntapShelfPath sub-model for paths."""

    name: str = ""
    node: OntapShelfPathNode = Field(default_factory=OntapShelfPathNode)


class OntapShelfPortCable(OntapModel):
    """OntapShelfPortCable sub-model for cable."""

    identifier: str = ""
    length: str = ""
    part_number: str = ""
    serial_number: str = ""


class OntapShelfPortRemote(OntapModel):
    """OntapShelfPortRemote sub-model for remote."""

    chassis: str = ""
    device: str = ""
    mac_address: str = ""
    phy: str = ""
    port: str = ""
    wwn: str = ""


class OntapShelfPort(OntapModel):
    """OntapShelfPort sub-model for ports."""

    cable: OntapShelfPortCable = Field(default_factory=OntapShelfPortCable)
    designator: str = ""
    id: int = 0
    internal: bool = False
    mac_address: str = ""
    module_id: str = ""
    remote: OntapShelfPortRemote = Field(default_factory=OntapShelfPortRemote)
    state: str = ""
    wwn: str = ""


class OntapShelfTemperatureSensorThresholdHigh(OntapModel):
    """OntapShelfTemperatureSensorThresholdHigh sub-model for high."""

    critical: int = 0
    warning: int = 0


class OntapShelfTemperatureSensorThresholdLow(OntapModel):
    """OntapShelfTemperatureSensorThresholdLow sub-model for low."""

    critical: int = 0
    warning: int = 0


class OntapShelfTemperatureSensorThreshold(OntapModel):
    """OntapShelfTemperatureSensorThreshold sub-model for threshold."""

    high: OntapShelfTemperatureSensorThresholdHigh = Field(
        default_factory=OntapShelfTemperatureSensorThresholdHigh
    )
    low: OntapShelfTemperatureSensorThresholdLow = Field(
        default_factory=OntapShelfTemperatureSensorThresholdLow
    )


class OntapShelfTemperatureSensor(OntapModel):
    """OntapShelfTemperatureSensor sub-model for temperature_sensors."""

    ambient: bool = False
    id: int = 0
    installed: bool = False
    location: str = ""
    state: str = ""
    temperature: int = 0
    threshold: OntapShelfTemperatureSensorThreshold = Field(
        default_factory=OntapShelfTemperatureSensorThreshold
    )


class OntapShelfVendor(OntapModel):
    """OntapShelfVendor sub-model for vendor."""

    manufacturer: str = ""
    name: str = ""
    part_number: str = ""
    product: str = ""
    serial_number: str = ""


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
    errors: list[dict[str, Any]] = Field(default_factory=list)
    fans: list[OntapShelfFan] = Field(default_factory=list)
    frus: list[OntapShelfFru] = Field(default_factory=list)
    id: str = ""
    internal: bool = False
    local: bool = False
    location_led: str = ""
    manufacturer: OntapShelfManufacturer = Field(default_factory=OntapShelfManufacturer)
    model_: str = ""
    module_type: str = ""
    name: str = ""
    paths: list[OntapShelfPath] = Field(default_factory=list)
    ports: list[OntapShelfPort] = Field(default_factory=list)
    serial_number: str = ""
    state: str = ""
    temperature_sensors: list[OntapShelfTemperatureSensor] = Field(default_factory=list)
    uid: str = ""
    vendor: OntapShelfVendor = Field(default_factory=OntapShelfVendor)
    voltage_sensors: list[OntapShelfVoltageSensor] = Field(default_factory=list)
