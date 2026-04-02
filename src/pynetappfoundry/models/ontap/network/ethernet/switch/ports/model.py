"""OntapSwitchPort information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSwitchPortIdentity(OntapModel):
    """OntapSwitchPortIdentity sub-model for identity."""

    index: int = 0
    name: str = ""
    number: int = 0


class OntapSwitchPortRemotePortDeviceNode(OntapModel):
    """OntapSwitchPortRemotePortDeviceNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapSwitchPortRemotePortDeviceShelf(OntapModel):
    """OntapSwitchPortRemotePortDeviceShelf sub-model for shelf."""

    module: str = ""
    name: str = ""
    uid: str = ""


class OntapSwitchPortRemotePortDevice(OntapModel):
    """OntapSwitchPortRemotePortDevice sub-model for device."""

    node: OntapSwitchPortRemotePortDeviceNode = Field(
        default_factory=OntapSwitchPortRemotePortDeviceNode
    )
    shelf: OntapSwitchPortRemotePortDeviceShelf = Field(
        default_factory=OntapSwitchPortRemotePortDeviceShelf
    )


class OntapSwitchPortRemotePort(OntapModel):
    """OntapSwitchPortRemotePort sub-model for remote_port."""

    device: OntapSwitchPortRemotePortDevice = Field(default_factory=OntapSwitchPortRemotePortDevice)
    mtu: int = 0
    name: str = ""


class OntapSwitchPortStatisticsReceiveRaw(OntapModel):
    """OntapSwitchPortStatisticsReceiveRaw sub-model for receive_raw."""

    discards: int = 0
    errors: int = 0
    packets: int = 0


class OntapSwitchPortStatisticsTransmitRaw(OntapModel):
    """OntapSwitchPortStatisticsTransmitRaw sub-model for transmit_raw."""

    discards: int = 0
    errors: int = 0
    packets: int = 0


class OntapSwitchPortStatistics(OntapModel):
    """OntapSwitchPortStatistics sub-model for statistics."""

    receive_raw: OntapSwitchPortStatisticsReceiveRaw = Field(
        default_factory=OntapSwitchPortStatisticsReceiveRaw
    )
    transmit_raw: OntapSwitchPortStatisticsTransmitRaw = Field(
        default_factory=OntapSwitchPortStatisticsTransmitRaw
    )


class OntapSwitchPortSwitch(OntapModel):
    """OntapSwitchPortSwitch sub-model for switch."""

    name: str = ""


class OntapSwitchPort(OntapModel):
    """OntapSwitchPort information."""

    configured: str = ""
    duplex_type: str = ""
    identity: OntapSwitchPortIdentity = Field(default_factory=OntapSwitchPortIdentity)
    isl: bool = False
    mac_address: str = ""
    mtu: int = 0
    remote_port: OntapSwitchPortRemotePort = Field(default_factory=OntapSwitchPortRemotePort)
    speed: int = 0
    state: str = ""
    statistics: OntapSwitchPortStatistics = Field(default_factory=OntapSwitchPortStatistics)
    switch: OntapSwitchPortSwitch = Field(default_factory=OntapSwitchPortSwitch)
    type_: str = ""
    vlan_id: list[int] = Field(default_factory=list)
    vpc_peer_link: bool = False
