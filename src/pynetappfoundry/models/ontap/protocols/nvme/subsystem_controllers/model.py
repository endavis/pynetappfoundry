"""OntapNvmeSubsystemController information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNvmeSubsystemController(OntapModel):
    """OntapNvmeSubsystemController information."""

    admin_queue_depth: int = 0
    dh_hmac_chap_group_size: str = ""
    dh_hmac_chap_hash_function: str = ""
    dh_hmac_chap_mode: str = ""
    digest_data: bool = False
    digest_header: bool = False
    host_id: str = ""
    host_nqn: str = ""
    host_transport_address: str = ""
    id: str = ""
    interface_name: str = ""
    interface_transport_address: str = ""
    interface_uuid: str = ""
    io_queue_count: int = 0
    io_queue_depth: list[int] = Field(default_factory=list)
    keep_alive_timeout: int = 0
    node_name: str = ""
    node_uuid: str = ""
    subsystem_name: str = ""
    subsystem_uuid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    tls_cipher: str = ""
    tls_key_type: str = ""
    tls_psk_identity: str = ""
    transport_protocol: str = ""
