"""OntapClientLock information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapClientLockByteLock(OntapModel):
    """OntapClientLockByteLock sub-model for byte_lock."""

    exclusive: bool = False
    length: int = 0
    mandatory: bool = False
    offset: int = 0
    soft: bool = False
    super: bool = False


class OntapClientLockInterfaceIp(OntapModel):
    """OntapClientLockInterfaceIp sub-model for ip."""

    address: str = ""


class OntapClientLockInterface(OntapModel):
    """OntapClientLockInterface sub-model for interface."""

    ip: OntapClientLockInterfaceIp = Field(default_factory=OntapClientLockInterfaceIp)
    name: str = ""
    uuid: str = ""


class OntapClientLockNode(OntapModel):
    """OntapClientLockNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapClientLockShareLock(OntapModel):
    """OntapClientLockShareLock sub-model for share_lock."""

    mode: str = ""
    soft: bool = False


class OntapClientLockSmb(OntapModel):
    """OntapClientLockSmb sub-model for smb."""

    connect_state: str = ""
    open_group_id: str = ""
    open_type: str = ""


class OntapClientLockSvm(OntapModel):
    """OntapClientLockSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapClientLockVolume(OntapModel):
    """OntapClientLockVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapClientLock(OntapModel):
    """OntapClientLock information."""

    byte_lock: OntapClientLockByteLock = Field(default_factory=OntapClientLockByteLock)
    client_address: str = ""
    constituent: bool = False
    delegation: str = ""
    interface: OntapClientLockInterface = Field(default_factory=OntapClientLockInterface)
    node: OntapClientLockNode = Field(default_factory=OntapClientLockNode)
    oplock_level: str = ""
    owner_id: str = ""
    path: str = ""
    protocol: str = ""
    share_lock: OntapClientLockShareLock = Field(default_factory=OntapClientLockShareLock)
    smb: OntapClientLockSmb = Field(default_factory=OntapClientLockSmb)
    state: str = ""
    svm: OntapClientLockSvm = Field(default_factory=OntapClientLockSvm)
    type_: str = ""
    uuid: str = ""
    volume: OntapClientLockVolume = Field(default_factory=OntapClientLockVolume)
