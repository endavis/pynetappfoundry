"""OntapStoragePort information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapStoragePort(CacheModel):
    """OntapStoragePort information."""

    board_name: str = ""
    cable_identifier: str = ""
    cable_length: str = ""
    cable_part_number: str = ""
    cable_serial_number: str = ""
    cable_transceiver: str = ""
    cable_vendor: str = ""
    description: str = ""
    enabled: bool = False
    error_corrective_action: str = ""
    error_message: str = ""
    firmware_version: str = ""
    force: bool = False
    in_use: bool = False
    mac_address: str = ""
    mode: str = ""
    name: str = ""
    node_name: str = ""
    node_uuid: str = ""
    part_number: str = ""
    redundant: bool = False
    serial_number: str = ""
    speed: float = 0.0
    state: str = ""
    type_: str = ""
    wwn: str = ""
    wwpn: str = ""
