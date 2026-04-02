"""OntapNvmeSubsystemController information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNvmeSubsystemControllerAdminQueue(OntapModel):
    """OntapNvmeSubsystemControllerAdminQueue sub-model for admin_queue."""

    depth: int = 0


class OntapNvmeSubsystemControllerDhHmacChap(OntapModel):
    """OntapNvmeSubsystemControllerDhHmacChap sub-model for dh_hmac_chap."""

    group_size: str = ""
    hash_function: str = ""
    mode: str = ""


class OntapNvmeSubsystemControllerDigest(OntapModel):
    """OntapNvmeSubsystemControllerDigest sub-model for digest."""

    data: bool = False
    header: bool = False


class OntapNvmeSubsystemControllerHost(OntapModel):
    """OntapNvmeSubsystemControllerHost sub-model for host."""

    id: str = ""
    nqn: str = ""
    transport_address: str = ""


class OntapNvmeSubsystemControllerInterface(OntapModel):
    """OntapNvmeSubsystemControllerInterface sub-model for interface."""

    name: str = ""
    transport_address: str = ""
    uuid: str = ""


class OntapNvmeSubsystemControllerIoQueue(OntapModel):
    """OntapNvmeSubsystemControllerIoQueue sub-model for io_queue."""

    count: int = 0
    depth: list[int] = Field(default_factory=list)


class OntapNvmeSubsystemControllerNode(OntapModel):
    """OntapNvmeSubsystemControllerNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapNvmeSubsystemControllerSubsystem(OntapModel):
    """OntapNvmeSubsystemControllerSubsystem sub-model for subsystem."""

    name: str = ""
    uuid: str = ""


class OntapNvmeSubsystemControllerSvm(OntapModel):
    """OntapNvmeSubsystemControllerSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNvmeSubsystemControllerTls(OntapModel):
    """OntapNvmeSubsystemControllerTls sub-model for tls."""

    cipher: str = ""
    key_type: str = ""
    psk_identity: str = ""


class OntapNvmeSubsystemController(OntapModel):
    """OntapNvmeSubsystemController information."""

    admin_queue: OntapNvmeSubsystemControllerAdminQueue = Field(
        default_factory=OntapNvmeSubsystemControllerAdminQueue
    )
    dh_hmac_chap: OntapNvmeSubsystemControllerDhHmacChap = Field(
        default_factory=OntapNvmeSubsystemControllerDhHmacChap
    )
    digest: OntapNvmeSubsystemControllerDigest = Field(
        default_factory=OntapNvmeSubsystemControllerDigest
    )
    host: OntapNvmeSubsystemControllerHost = Field(default_factory=OntapNvmeSubsystemControllerHost)
    id: str = ""
    interface: OntapNvmeSubsystemControllerInterface = Field(
        default_factory=OntapNvmeSubsystemControllerInterface
    )
    io_queue: OntapNvmeSubsystemControllerIoQueue = Field(
        default_factory=OntapNvmeSubsystemControllerIoQueue
    )
    keep_alive_timeout: int = 0
    node: OntapNvmeSubsystemControllerNode = Field(default_factory=OntapNvmeSubsystemControllerNode)
    subsystem: OntapNvmeSubsystemControllerSubsystem = Field(
        default_factory=OntapNvmeSubsystemControllerSubsystem
    )
    svm: OntapNvmeSubsystemControllerSvm = Field(default_factory=OntapNvmeSubsystemControllerSvm)
    tls: OntapNvmeSubsystemControllerTls = Field(default_factory=OntapNvmeSubsystemControllerTls)
    transport_protocol: str = ""
