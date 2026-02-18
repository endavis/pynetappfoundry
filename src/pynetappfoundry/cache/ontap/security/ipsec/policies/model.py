"""OntapIpsecPolicyResponse information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapIpsecPolicyResponse(CacheModel):
    """OntapIpsecPolicyResponse information."""

    action: str = ""
    authentication_method: str = ""
    certificate_name: str = ""
    certificate_uuid: str = ""
    enabled: bool = False
    ipspace_name: str = ""
    ipspace_uuid: str = ""
    local_endpoint_address: str = ""
    local_endpoint_family: str = ""
    local_endpoint_netmask: str = ""
    local_endpoint_port: str = ""
    local_identity: str = ""
    name: str = ""
    protocol: str = ""
    remote_endpoint_address: str = ""
    remote_endpoint_family: str = ""
    remote_endpoint_netmask: str = ""
    remote_endpoint_port: str = ""
    remote_identity: str = ""
    scope: str = ""
    secret_key: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
