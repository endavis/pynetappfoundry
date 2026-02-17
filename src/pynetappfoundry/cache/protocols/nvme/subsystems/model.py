"""OntapNvmeSubsystem information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapNvmeSubsystemHost(CacheModel):
    """OntapNvmeSubsystemHost sub-model for hosts."""

    hosts_dh_hmac_chap_controller_secret_key: str = ""
    hosts_dh_hmac_chap_group_size: str = ""
    hosts_dh_hmac_chap_hash_function: str = ""
    hosts_dh_hmac_chap_host_secret_key: str = ""
    hosts_dh_hmac_chap_mode: str = ""
    hosts_nqn: str = ""
    hosts_priority: str = ""
    hosts_tls_configured_psk: str = ""
    hosts_tls_key_type: str = ""


class OntapNvmeSubsystemSubsystemMap(CacheModel):
    """OntapNvmeSubsystemSubsystemMap sub-model for subsystem_maps."""

    subsystem_maps_anagrpid: str = ""
    subsystem_maps_namespace_name: str = ""
    subsystem_maps_namespace_uuid: str = ""
    subsystem_maps_nsid: str = ""


class OntapNvmeSubsystem(CacheModel):
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
