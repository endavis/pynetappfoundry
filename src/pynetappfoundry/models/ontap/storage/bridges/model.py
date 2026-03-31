"""OntapStorageBridge information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapStorageBridgeError(OntapModel):
    """OntapStorageBridgeError sub-model for errors."""

    component_id: int = 0
    component_name: str = ""
    component_unique_id: str = ""
    reason_arguments: list[dict[str, Any]] = Field(default_factory=list)
    reason_code: str = ""
    reason_message: str = ""
    severity: str = ""
    type: str = ""


class OntapStorageBridgeFcPort(OntapModel):
    """OntapStorageBridgeFcPort sub-model for fc_ports."""

    configured_data_rate: float = 0.0
    connection_mode: str = ""
    data_rate_capability: float = 0.0
    enabled: bool = False
    id: int = 0
    negotiated_data_rate: float = 0.0
    peer_wwn: str = ""
    sfp_data_rate_capability: float = 0.0
    sfp_part_number: str = ""
    sfp_serial_number: str = ""
    sfp_vendor: str = ""
    state: str = ""
    wwn: str = ""


class OntapStorageBridgeArgument(OntapModel):
    """OntapStorageBridgeArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapStorageBridgePath(OntapModel):
    """OntapStorageBridgePath sub-model for paths."""

    name: str = ""
    node_name: str = ""
    node_uuid: str = ""
    source_port_id: str = ""
    source_port_name: str = ""
    target_port_id: str = ""
    target_port_name: str = ""
    target_port_wwn: str = ""


class OntapStorageBridgePowerSupplyUnit(OntapModel):
    """OntapStorageBridgePowerSupplyUnit sub-model for power_supply_units."""

    name: str = ""
    state: str = ""


class OntapStorageBridgeSasPort(OntapModel):
    """OntapStorageBridgeSasPort sub-model for sas_ports."""

    cable_part_number: str = ""
    cable_serial_number: str = ""
    cable_technology: str = ""
    cable_vendor: str = ""
    data_rate_capability: float = 0.0
    enabled: bool = False
    id: int = 0
    negotiated_data_rate: float = 0.0
    phy_1_state: str = ""
    phy_2_state: str = ""
    phy_3_state: str = ""
    phy_4_state: str = ""
    state: str = ""
    wwn: str = ""


class OntapStorageBridge(OntapModel):
    """OntapStorageBridge information."""

    chassis_throughput_state: str = ""
    dram_single_bit_error_count: int = 0
    errors: list[OntapStorageBridgeError] = Field(default_factory=list)
    fc_ports: list[OntapStorageBridgeFcPort] = Field(default_factory=list)
    firmware_version: str = ""
    ip_address: str = ""
    last_reboot_reason_arguments: list[OntapStorageBridgeArgument] = Field(default_factory=list)
    last_reboot_reason_code: str = ""
    last_reboot_reason_message: str = ""
    last_reboot_time: str = ""
    managed_by: str = ""
    model_: str = ""
    monitoring_enabled: bool = False
    name: str = ""
    paths: list[OntapStorageBridgePath] = Field(default_factory=list)
    power_supply_units: list[OntapStorageBridgePowerSupplyUnit] = Field(default_factory=list)
    sas_ports: list[OntapStorageBridgeSasPort] = Field(default_factory=list)
    security_enabled: bool = False
    serial_number: str = ""
    state: str = ""
    symbolic_name: str = ""
    temperature_sensor_maximum: int = 0
    temperature_sensor_minimum: int = 0
    temperature_sensor_name: str = ""
    temperature_sensor_reading: int = 0
    temperature_sensor_state: str = ""
    vendor: str = ""
    wwn: str = ""
