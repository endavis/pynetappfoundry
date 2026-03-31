"""OntapNvmeSubsystemHost information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNvmeSubsystemHostRecord(OntapModel):
    """OntapNvmeSubsystemHostRecord sub-model for records."""

    dh_hmac_chap_controller_secret_key: str = ""
    dh_hmac_chap_group_size: str = ""
    dh_hmac_chap_hash_function: str = ""
    dh_hmac_chap_host_secret_key: str = ""
    dh_hmac_chap_mode: str = ""
    io_queue_count: int = 0
    io_queue_depth: int = 0
    nqn: str = ""
    subsystem_name: str = ""
    subsystem_uuid: str = ""
    tls_configured_psk: str = ""
    tls_key_type: str = ""


class OntapNvmeSubsystemHost(OntapModel):
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
