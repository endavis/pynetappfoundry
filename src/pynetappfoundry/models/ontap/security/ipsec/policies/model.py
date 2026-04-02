"""OntapIpsecPolicyResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIpsecPolicyResponseCertificate(OntapModel):
    """OntapIpsecPolicyResponseCertificate sub-model for certificate."""

    name: str = ""
    uuid: str = ""


class OntapIpsecPolicyResponseIpspace(OntapModel):
    """OntapIpsecPolicyResponseIpspace sub-model for ipspace."""

    name: str = ""
    uuid: str = ""


class OntapIpsecPolicyResponseLocalEndpoint(OntapModel):
    """OntapIpsecPolicyResponseLocalEndpoint sub-model for local_endpoint."""

    address: str = ""
    family: str = ""
    netmask: str = ""
    port: str = ""


class OntapIpsecPolicyResponseRemoteEndpoint(OntapModel):
    """OntapIpsecPolicyResponseRemoteEndpoint sub-model for remote_endpoint."""

    address: str = ""
    family: str = ""
    netmask: str = ""
    port: str = ""


class OntapIpsecPolicyResponseSvm(OntapModel):
    """OntapIpsecPolicyResponseSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapIpsecPolicyResponse(OntapModel):
    """OntapIpsecPolicyResponse information."""

    action: str = ""
    authentication_method: str = ""
    certificate: OntapIpsecPolicyResponseCertificate = Field(
        default_factory=OntapIpsecPolicyResponseCertificate
    )
    enabled: bool = False
    ipspace: OntapIpsecPolicyResponseIpspace = Field(
        default_factory=OntapIpsecPolicyResponseIpspace
    )
    local_endpoint: OntapIpsecPolicyResponseLocalEndpoint = Field(
        default_factory=OntapIpsecPolicyResponseLocalEndpoint
    )
    local_identity: str = ""
    name: str = ""
    protocol: str = ""
    remote_endpoint: OntapIpsecPolicyResponseRemoteEndpoint = Field(
        default_factory=OntapIpsecPolicyResponseRemoteEndpoint
    )
    remote_identity: str = ""
    scope: str = ""
    secret_key: str = ""
    svm: OntapIpsecPolicyResponseSvm = Field(default_factory=OntapIpsecPolicyResponseSvm)
    uuid: str = ""
