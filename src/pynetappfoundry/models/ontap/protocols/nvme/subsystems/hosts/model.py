"""OntapNvmeSubsystemHost information."""

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


class OntapNvmeSubsystemHostIoQueue(OntapModel):
    """OntapNvmeSubsystemHostIoQueue sub-model for io_queue."""

    count: int = 0
    depth: int = 0


class OntapNvmeSubsystemHostRecordDhHmacChap(OntapModel):
    """OntapNvmeSubsystemHostRecordDhHmacChap sub-model for dh_hmac_chap."""

    controller_secret_key: str = ""
    group_size: str = ""
    hash_function: str = ""
    host_secret_key: str = ""
    mode: str = ""


class OntapNvmeSubsystemHostRecordIoQueue(OntapModel):
    """OntapNvmeSubsystemHostRecordIoQueue sub-model for io_queue."""

    count: int = 0
    depth: int = 0


class OntapNvmeSubsystemHostRecordSubsystem(OntapModel):
    """OntapNvmeSubsystemHostRecordSubsystem sub-model for subsystem."""

    name: str = ""
    uuid: str = ""


class OntapNvmeSubsystemHostRecordTls(OntapModel):
    """OntapNvmeSubsystemHostRecordTls sub-model for tls."""

    configured_psk: str = ""
    key_type: str = ""


class OntapNvmeSubsystemHostRecord(OntapModel):
    """OntapNvmeSubsystemHostRecord sub-model for records."""

    dh_hmac_chap: OntapNvmeSubsystemHostRecordDhHmacChap = Field(
        default_factory=OntapNvmeSubsystemHostRecordDhHmacChap
    )
    io_queue: OntapNvmeSubsystemHostRecordIoQueue = Field(
        default_factory=OntapNvmeSubsystemHostRecordIoQueue
    )
    nqn: str = ""
    subsystem: OntapNvmeSubsystemHostRecordSubsystem = Field(
        default_factory=OntapNvmeSubsystemHostRecordSubsystem
    )
    tls: OntapNvmeSubsystemHostRecordTls = Field(default_factory=OntapNvmeSubsystemHostRecordTls)


class OntapNvmeSubsystemHostSubsystem(OntapModel):
    """OntapNvmeSubsystemHostSubsystem sub-model for subsystem."""

    name: str = ""
    uuid: str = ""


class OntapNvmeSubsystemHostTls(OntapModel):
    """OntapNvmeSubsystemHostTls sub-model for tls."""

    configured_psk: str = ""
    key_type: str = ""


class OntapNvmeSubsystemHost(OntapModel):
    """OntapNvmeSubsystemHost information."""

    dh_hmac_chap: OntapNvmeSubsystemHostDhHmacChap = Field(
        default_factory=OntapNvmeSubsystemHostDhHmacChap
    )
    io_queue: OntapNvmeSubsystemHostIoQueue = Field(default_factory=OntapNvmeSubsystemHostIoQueue)
    nqn: str = ""
    priority: str = ""
    records: list[OntapNvmeSubsystemHostRecord] = Field(default_factory=list)
    subsystem: OntapNvmeSubsystemHostSubsystem = Field(
        default_factory=OntapNvmeSubsystemHostSubsystem
    )
    tls: OntapNvmeSubsystemHostTls = Field(default_factory=OntapNvmeSubsystemHostTls)
