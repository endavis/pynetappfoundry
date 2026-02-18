"""OntapStorageBridge information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapStorageBridgeError(CacheModel):
    """OntapStorageBridgeError sub-model for errors."""

    errors_component_id: int = 0
    errors_component_name: str = ""
    errors_component_unique_id: str = ""
    errors_reason_arguments: list[dict[str, Any]] = Field(default_factory=list)
    errors_reason_code: str = ""
    errors_reason_message: str = ""
    errors_severity: str = ""
    errors_type: str = ""


class OntapStorageBridgeFcPort(CacheModel):
    """OntapStorageBridgeFcPort sub-model for fc_ports."""

    fc_ports_configured_data_rate: float = 0.0
    fc_ports_connection_mode: str = ""
    fc_ports_data_rate_capability: float = 0.0
    fc_ports_enabled: bool = False
    fc_ports_id: int = 0
    fc_ports_negotiated_data_rate: float = 0.0
    fc_ports_peer_wwn: str = ""
    fc_ports_sfp_data_rate_capability: float = 0.0
    fc_ports_sfp_part_number: str = ""
    fc_ports_sfp_serial_number: str = ""
    fc_ports_sfp_vendor: str = ""
    fc_ports_state: str = ""
    fc_ports_wwn: str = ""


class OntapStorageBridgeArgument(CacheModel):
    """OntapStorageBridgeArgument sub-model for arguments."""

    last_reboot_reason_arguments_code: str = ""
    last_reboot_reason_arguments_message: str = ""


class OntapStorageBridgePath(CacheModel):
    """OntapStorageBridgePath sub-model for paths."""

    paths_name: str = ""
    paths_node_name: str = ""
    paths_node_uuid: str = ""
    paths_source_port_id: str = ""
    paths_source_port_name: str = ""
    paths_target_port_id: str = ""
    paths_target_port_name: str = ""
    paths_target_port_wwn: str = ""


class OntapStorageBridgePowerSupplyUnit(CacheModel):
    """OntapStorageBridgePowerSupplyUnit sub-model for power_supply_units."""

    power_supply_units_name: str = ""
    power_supply_units_state: str = ""


class OntapStorageBridgeSasPort(CacheModel):
    """OntapStorageBridgeSasPort sub-model for sas_ports."""

    sas_ports_cable_part_number: str = ""
    sas_ports_cable_serial_number: str = ""
    sas_ports_cable_technology: str = ""
    sas_ports_cable_vendor: str = ""
    sas_ports_data_rate_capability: float = 0.0
    sas_ports_enabled: bool = False
    sas_ports_id: int = 0
    sas_ports_negotiated_data_rate: float = 0.0
    sas_ports_phy_1_state: str = ""
    sas_ports_phy_2_state: str = ""
    sas_ports_phy_3_state: str = ""
    sas_ports_phy_4_state: str = ""
    sas_ports_state: str = ""
    sas_ports_wwn: str = ""


class OntapStorageBridge(CacheModel):
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
