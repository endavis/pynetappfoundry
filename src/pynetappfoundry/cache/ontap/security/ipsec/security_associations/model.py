"""OntapSecurityAssociationResponse information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSecurityAssociationResponse(CacheModel):
    """OntapSecurityAssociationResponse information."""

    cipher_suite: str = ""
    ike_authentication: str = ""
    ike_initiator_security_parameter_index: str = ""
    ike_is_initiator: bool = False
    ike_responder_security_parameter_index: str = ""
    ike_state: str = ""
    ike_version: int = 0
    ipsec_action: str = ""
    ipsec_inbound_bytes: int = 0
    ipsec_inbound_offload_bytes: int = 0
    ipsec_inbound_offload_packets: int = 0
    ipsec_inbound_packets: int = 0
    ipsec_inbound_security_parameter_index: str = ""
    ipsec_outbound_bytes: int = 0
    ipsec_outbound_offload_bytes: int = 0
    ipsec_outbound_offload_packets: int = 0
    ipsec_outbound_packets: int = 0
    ipsec_outbound_security_parameter_index: str = ""
    ipsec_state: str = ""
    lifetime: int = 0
    local_address: str = ""
    node_name: str = ""
    node_uuid: str = ""
    policy_name: str = ""
    remote_address: str = ""
    scope: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    type_: str = ""
    uuid: str = ""
