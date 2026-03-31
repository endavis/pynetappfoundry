"""OntapNvmeSubsystem information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNvmeSubsystemHost(OntapModel):
    """OntapNvmeSubsystemHost sub-model for hosts."""

    dh_hmac_chap_controller_secret_key: str = ""
    dh_hmac_chap_group_size: str = ""
    dh_hmac_chap_hash_function: str = ""
    dh_hmac_chap_host_secret_key: str = ""
    dh_hmac_chap_mode: str = ""
    nqn: str = ""
    priority: str = ""
    tls_configured_psk: str = ""
    tls_key_type: str = ""


class OntapNvmeSubsystemSubsystemMap(OntapModel):
    """OntapNvmeSubsystemSubsystemMap sub-model for subsystem_maps."""

    anagrpid: str = ""
    namespace_name: str = ""
    namespace_uuid: str = ""
    nsid: str = ""


class OntapNvmeSubsystem(OntapModel):
    """OntapNvmeSubsystem information."""

    comment: str = ""
    delete_on_unmap: bool = False
    hosts: list[OntapNvmeSubsystemHost] = Field(default_factory=list)
    io_queue_default_count: int = 0
    io_queue_default_depth: int = 0
    name: str = ""
    os_type: str = ""
    serial_number: str = ""
    subsystem_maps: list[OntapNvmeSubsystemSubsystemMap] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
    target_nqn: str = ""
    uuid: str = ""
    vendor_uuids: list[str] = Field(default_factory=list)
