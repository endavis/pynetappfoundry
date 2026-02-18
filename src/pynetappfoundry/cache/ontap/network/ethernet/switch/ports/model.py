"""OntapSwitchPort information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapSwitchPort(CacheModel):
    """OntapSwitchPort information."""

    configured: str = ""
    duplex_type: str = ""
    identity_index: int = 0
    identity_name: str = ""
    identity_number: int = 0
    isl: bool = False
    mac_address: str = ""
    mtu: int = 0
    remote_port_device_node_name: str = ""
    remote_port_device_node_uuid: str = ""
    remote_port_device_shelf_module: str = ""
    remote_port_device_shelf_name: str = ""
    remote_port_device_shelf_uid: str = ""
    remote_port_mtu: int = 0
    remote_port_name: str = ""
    speed: int = 0
    state: str = ""
    statistics_receive_raw_discards: int = 0
    statistics_receive_raw_errors: int = 0
    statistics_receive_raw_packets: int = 0
    statistics_transmit_raw_discards: int = 0
    statistics_transmit_raw_errors: int = 0
    statistics_transmit_raw_packets: int = 0
    switch_name: str = ""
    type_: str = ""
    vlan_id: list[int] = Field(default_factory=list)
    vpc_peer_link: bool = False
