"""OntapStorageSwitch information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapStorageSwitchErrorComponent(OntapModel):
    """OntapStorageSwitchErrorComponent sub-model for component."""

    id: int = 0
    name: str = ""


class OntapStorageSwitchErrorReasonArgument(OntapModel):
    """OntapStorageSwitchErrorReasonArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapStorageSwitchErrorReason(OntapModel):
    """OntapStorageSwitchErrorReason sub-model for reason."""

    arguments: list[OntapStorageSwitchErrorReasonArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapStorageSwitchError(OntapModel):
    """OntapStorageSwitchError sub-model for errors."""

    component: OntapStorageSwitchErrorComponent = Field(
        default_factory=OntapStorageSwitchErrorComponent
    )
    reason: OntapStorageSwitchErrorReason = Field(default_factory=OntapStorageSwitchErrorReason)
    severity: str = ""
    type_: str = ""


class OntapStorageSwitchFan(OntapModel):
    """OntapStorageSwitchFan sub-model for fans."""

    name: str = ""
    speed: int = 0
    state: str = ""


class OntapStorageSwitchPortSfp(OntapModel):
    """OntapStorageSwitchPortSfp sub-model for sfp."""

    serial_number: str = ""
    transmitter_type: str = ""
    type_: str = ""


class OntapStorageSwitchPort(OntapModel):
    """OntapStorageSwitchPort sub-model for ports."""

    enabled: bool = False
    mode: str = ""
    name: str = ""
    sfp: OntapStorageSwitchPortSfp = Field(default_factory=OntapStorageSwitchPortSfp)
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


class OntapStorageSwitchZonePort(OntapModel):
    """OntapStorageSwitchZonePort sub-model for port."""

    id: str = ""
    name: str = ""


class OntapStorageSwitchZone(OntapModel):
    """OntapStorageSwitchZone sub-model for zones."""

    id: int = 0
    name: str = ""
    port: OntapStorageSwitchZonePort = Field(default_factory=OntapStorageSwitchZonePort)
    wwn: str = ""


class OntapStorageSwitch(OntapModel):
    """OntapStorageSwitch information."""

    connections: list[dict[str, Any]] = Field(default_factory=list)
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
    paths: list[dict[str, Any]] = Field(default_factory=list)
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
