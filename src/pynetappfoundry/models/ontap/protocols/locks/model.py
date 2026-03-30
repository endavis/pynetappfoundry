"""OntapClientLock information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapClientLock(OntapModel):
    """OntapClientLock information."""

    byte_lock_exclusive: bool = False
    byte_lock_length: int = 0
    byte_lock_mandatory: bool = False
    byte_lock_offset: int = 0
    byte_lock_soft: bool = False
    byte_lock_super: bool = False
    client_address: str = ""
    constituent: bool = False
    delegation: str = ""
    interface_ip_address: str = ""
    interface_name: str = ""
    interface_uuid: str = ""
    node_name: str = ""
    node_uuid: str = ""
    oplock_level: str = ""
    owner_id: str = ""
    path: str = ""
    protocol: str = ""
    share_lock_mode: str = ""
    share_lock_soft: bool = False
    smb_connect_state: str = ""
    smb_open_group_id: str = ""
    smb_open_type: str = ""
    state: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    type_: str = ""
    uuid: str = ""
    volume_name: str = ""
    volume_uuid: str = ""
