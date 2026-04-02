"""OntapNvmeSubsystem information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNvmeSubsystemHostDhHmacChap(OntapModel):
    """OntapNvmeSubsystemHostDhHmacChap sub-model for dh_hmac_chap."""

    controller_secret_key: str = ""
    group_size: str = ""
    hash_function: str = ""
    host_secret_key: str = ""
    mode: str = ""


class OntapNvmeSubsystemHostTls(OntapModel):
    """OntapNvmeSubsystemHostTls sub-model for tls."""

    configured_psk: str = ""
    key_type: str = ""


class OntapNvmeSubsystemHost(OntapModel):
    """OntapNvmeSubsystemHost sub-model for hosts."""

    dh_hmac_chap: OntapNvmeSubsystemHostDhHmacChap = Field(
        default_factory=OntapNvmeSubsystemHostDhHmacChap
    )
    nqn: str = ""
    priority: str = ""
    tls: OntapNvmeSubsystemHostTls = Field(default_factory=OntapNvmeSubsystemHostTls)


class OntapNvmeSubsystemIoQueueDefault(OntapModel):
    """OntapNvmeSubsystemIoQueueDefault sub-model for default."""

    count: int = 0
    depth: int = 0


class OntapNvmeSubsystemIoQueue(OntapModel):
    """OntapNvmeSubsystemIoQueue sub-model for io_queue."""

    default: OntapNvmeSubsystemIoQueueDefault = Field(
        default_factory=OntapNvmeSubsystemIoQueueDefault
    )


class OntapNvmeSubsystemSubsystemMapNamespace(OntapModel):
    """OntapNvmeSubsystemSubsystemMapNamespace sub-model for namespace."""

    name: str = ""
    uuid: str = ""


class OntapNvmeSubsystemSubsystemMap(OntapModel):
    """OntapNvmeSubsystemSubsystemMap sub-model for subsystem_maps."""

    anagrpid: str = ""
    namespace: OntapNvmeSubsystemSubsystemMapNamespace = Field(
        default_factory=OntapNvmeSubsystemSubsystemMapNamespace
    )
    nsid: str = ""


class OntapNvmeSubsystemSvm(OntapModel):
    """OntapNvmeSubsystemSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNvmeSubsystem(OntapModel):
    """OntapNvmeSubsystem information."""

    comment: str = ""
    delete_on_unmap: bool = False
    hosts: list[OntapNvmeSubsystemHost] = Field(default_factory=list)
    io_queue: OntapNvmeSubsystemIoQueue = Field(default_factory=OntapNvmeSubsystemIoQueue)
    name: str = ""
    os_type: str = ""
    serial_number: str = ""
    subsystem_maps: list[OntapNvmeSubsystemSubsystemMap] = Field(default_factory=list)
    svm: OntapNvmeSubsystemSvm = Field(default_factory=OntapNvmeSubsystemSvm)
    target_nqn: str = ""
    uuid: str = ""
    vendor_uuids: list[str] = Field(default_factory=list)
