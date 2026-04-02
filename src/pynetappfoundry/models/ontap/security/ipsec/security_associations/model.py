"""OntapSecurityAssociationResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSecurityAssociationResponseIke(OntapModel):
    """OntapSecurityAssociationResponseIke sub-model for ike."""

    authentication: str = ""
    initiator_security_parameter_index: str = ""
    is_initiator: bool = False
    responder_security_parameter_index: str = ""
    state: str = ""
    version: int = 0


class OntapSecurityAssociationResponseIpsecInbound(OntapModel):
    """OntapSecurityAssociationResponseIpsecInbound sub-model for inbound."""

    bytes: int = 0
    offload_bytes: int = 0
    offload_packets: int = 0
    packets: int = 0
    security_parameter_index: str = ""


class OntapSecurityAssociationResponseIpsecOutbound(OntapModel):
    """OntapSecurityAssociationResponseIpsecOutbound sub-model for outbound."""

    bytes: int = 0
    offload_bytes: int = 0
    offload_packets: int = 0
    packets: int = 0
    security_parameter_index: str = ""


class OntapSecurityAssociationResponseIpsec(OntapModel):
    """OntapSecurityAssociationResponseIpsec sub-model for ipsec."""

    action: str = ""
    inbound: OntapSecurityAssociationResponseIpsecInbound = Field(
        default_factory=OntapSecurityAssociationResponseIpsecInbound
    )
    outbound: OntapSecurityAssociationResponseIpsecOutbound = Field(
        default_factory=OntapSecurityAssociationResponseIpsecOutbound
    )
    state: str = ""


class OntapSecurityAssociationResponseNode(OntapModel):
    """OntapSecurityAssociationResponseNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapSecurityAssociationResponseSvm(OntapModel):
    """OntapSecurityAssociationResponseSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSecurityAssociationResponse(OntapModel):
    """OntapSecurityAssociationResponse information."""

    cipher_suite: str = ""
    ike: OntapSecurityAssociationResponseIke = Field(
        default_factory=OntapSecurityAssociationResponseIke
    )
    ipsec: OntapSecurityAssociationResponseIpsec = Field(
        default_factory=OntapSecurityAssociationResponseIpsec
    )
    lifetime: int = 0
    local_address: str = ""
    node: OntapSecurityAssociationResponseNode = Field(
        default_factory=OntapSecurityAssociationResponseNode
    )
    policy_name: str = ""
    remote_address: str = ""
    scope: str = ""
    svm: OntapSecurityAssociationResponseSvm = Field(
        default_factory=OntapSecurityAssociationResponseSvm
    )
    type_: str = ""
    uuid: str = ""
