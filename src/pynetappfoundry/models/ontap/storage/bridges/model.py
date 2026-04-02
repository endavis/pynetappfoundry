"""OntapStorageBridge information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapStorageBridgeErrorComponent(OntapModel):
    """OntapStorageBridgeErrorComponent sub-model for component."""

    id: int = 0
    name: str = ""
    unique_id: str = ""


class OntapStorageBridgeErrorReasonArgument(OntapModel):
    """OntapStorageBridgeErrorReasonArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapStorageBridgeErrorReason(OntapModel):
    """OntapStorageBridgeErrorReason sub-model for reason."""

    arguments: list[OntapStorageBridgeErrorReasonArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapStorageBridgeError(OntapModel):
    """OntapStorageBridgeError sub-model for errors."""

    component: OntapStorageBridgeErrorComponent = Field(
        default_factory=OntapStorageBridgeErrorComponent
    )
    reason: OntapStorageBridgeErrorReason = Field(default_factory=OntapStorageBridgeErrorReason)
    severity: str = ""
    type_: str = ""


class OntapStorageBridgeFcPortSfp(OntapModel):
    """OntapStorageBridgeFcPortSfp sub-model for sfp."""

    data_rate_capability: float = 0.0
    part_number: str = ""
    serial_number: str = ""
    vendor: str = ""


class OntapStorageBridgeFcPort(OntapModel):
    """OntapStorageBridgeFcPort sub-model for fc_ports."""

    configured_data_rate: float = 0.0
    connection_mode: str = ""
    data_rate_capability: float = 0.0
    enabled: bool = False
    id: int = 0
    negotiated_data_rate: float = 0.0
    peer_wwn: str = ""
    sfp: OntapStorageBridgeFcPortSfp = Field(default_factory=OntapStorageBridgeFcPortSfp)
    state: str = ""
    wwn: str = ""


class OntapStorageBridgeLastRebootReasonArgument(OntapModel):
    """OntapStorageBridgeLastRebootReasonArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapStorageBridgeLastRebootReason(OntapModel):
    """OntapStorageBridgeLastRebootReason sub-model for reason."""

    arguments: list[OntapStorageBridgeLastRebootReasonArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapStorageBridgeLastReboot(OntapModel):
    """OntapStorageBridgeLastReboot sub-model for last_reboot."""

    reason: OntapStorageBridgeLastRebootReason = Field(
        default_factory=OntapStorageBridgeLastRebootReason
    )
    time: str = ""


class OntapStorageBridgePathNode(OntapModel):
    """OntapStorageBridgePathNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapStorageBridgePathSourcePort(OntapModel):
    """OntapStorageBridgePathSourcePort sub-model for source_port."""

    id: str = ""
    name: str = ""


class OntapStorageBridgePathTargetPort(OntapModel):
    """OntapStorageBridgePathTargetPort sub-model for target_port."""

    id: str = ""
    name: str = ""
    wwn: str = ""


class OntapStorageBridgePath(OntapModel):
    """OntapStorageBridgePath sub-model for paths."""

    name: str = ""
    node: OntapStorageBridgePathNode = Field(default_factory=OntapStorageBridgePathNode)
    source_port: OntapStorageBridgePathSourcePort = Field(
        default_factory=OntapStorageBridgePathSourcePort
    )
    target_port: OntapStorageBridgePathTargetPort = Field(
        default_factory=OntapStorageBridgePathTargetPort
    )


class OntapStorageBridgePowerSupplyUnit(OntapModel):
    """OntapStorageBridgePowerSupplyUnit sub-model for power_supply_units."""

    name: str = ""
    state: str = ""


class OntapStorageBridgeSasPortCable(OntapModel):
    """OntapStorageBridgeSasPortCable sub-model for cable."""

    part_number: str = ""
    serial_number: str = ""
    technology: str = ""
    vendor: str = ""


class OntapStorageBridgeSasPortPhy1(OntapModel):
    """OntapStorageBridgeSasPortPhy1 sub-model for phy_1."""

    state: str = ""


class OntapStorageBridgeSasPortPhy2(OntapModel):
    """OntapStorageBridgeSasPortPhy2 sub-model for phy_2."""

    state: str = ""


class OntapStorageBridgeSasPortPhy3(OntapModel):
    """OntapStorageBridgeSasPortPhy3 sub-model for phy_3."""

    state: str = ""


class OntapStorageBridgeSasPortPhy4(OntapModel):
    """OntapStorageBridgeSasPortPhy4 sub-model for phy_4."""

    state: str = ""


class OntapStorageBridgeSasPort(OntapModel):
    """OntapStorageBridgeSasPort sub-model for sas_ports."""

    cable: OntapStorageBridgeSasPortCable = Field(default_factory=OntapStorageBridgeSasPortCable)
    data_rate_capability: float = 0.0
    enabled: bool = False
    id: int = 0
    negotiated_data_rate: float = 0.0
    phy_1: OntapStorageBridgeSasPortPhy1 = Field(default_factory=OntapStorageBridgeSasPortPhy1)
    phy_2: OntapStorageBridgeSasPortPhy2 = Field(default_factory=OntapStorageBridgeSasPortPhy2)
    phy_3: OntapStorageBridgeSasPortPhy3 = Field(default_factory=OntapStorageBridgeSasPortPhy3)
    phy_4: OntapStorageBridgeSasPortPhy4 = Field(default_factory=OntapStorageBridgeSasPortPhy4)
    state: str = ""
    wwn: str = ""


class OntapStorageBridgeTemperatureSensor(OntapModel):
    """OntapStorageBridgeTemperatureSensor sub-model for temperature_sensor."""

    maximum: int = 0
    minimum: int = 0
    name: str = ""
    reading: int = 0
    state: str = ""


class OntapStorageBridge(OntapModel):
    """OntapStorageBridge information."""

    chassis_throughput_state: str = ""
    dram_single_bit_error_count: int = 0
    errors: list[OntapStorageBridgeError] = Field(default_factory=list)
    fc_ports: list[OntapStorageBridgeFcPort] = Field(default_factory=list)
    firmware_version: str = ""
    ip_address: str = ""
    last_reboot: OntapStorageBridgeLastReboot = Field(default_factory=OntapStorageBridgeLastReboot)
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
    temperature_sensor: OntapStorageBridgeTemperatureSensor = Field(
        default_factory=OntapStorageBridgeTemperatureSensor
    )
    vendor: str = ""
    wwn: str = ""
