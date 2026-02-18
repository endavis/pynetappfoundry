"""OntapNvmeSubsystemHost information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapNvmeSubsystemHostRecord(CacheModel):
    """OntapNvmeSubsystemHostRecord sub-model for records."""

    records_dh_hmac_chap_controller_secret_key: str = ""
    records_dh_hmac_chap_group_size: str = ""
    records_dh_hmac_chap_hash_function: str = ""
    records_dh_hmac_chap_host_secret_key: str = ""
    records_dh_hmac_chap_mode: str = ""
    records_io_queue_count: int = 0
    records_io_queue_depth: int = 0
    records_nqn: str = ""
    records_subsystem_name: str = ""
    records_subsystem_uuid: str = ""
    records_tls_configured_psk: str = ""
    records_tls_key_type: str = ""


class OntapNvmeSubsystemHost(CacheModel):
    """OntapNvmeSubsystemHost information."""

    dh_hmac_chap_controller_secret_key: str = ""
    dh_hmac_chap_group_size: str = ""
    dh_hmac_chap_hash_function: str = ""
    dh_hmac_chap_host_secret_key: str = ""
    dh_hmac_chap_mode: str = ""
    io_queue_count: int = 0
    io_queue_depth: int = 0
    nqn: str = ""
    priority: str = ""
    records: list[OntapNvmeSubsystemHostRecord] = Field(default_factory=list)
    subsystem_name: str = ""
    subsystem_uuid: str = ""
    tls_configured_psk: str = ""
    tls_key_type: str = ""
