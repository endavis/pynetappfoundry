"""OntapAwsKms information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapAwsKmsEkmipReachability(CacheModel):
    """OntapAwsKmsEkmipReachability sub-model for ekmip_reachability."""

    ekmip_reachability_code: str = ""
    ekmip_reachability_message: str = ""
    ekmip_reachability_node_name: str = ""
    ekmip_reachability_node_uuid: str = ""
    ekmip_reachability_reachable: bool = False


class OntapAwsKms(CacheModel):
    """OntapAwsKms information."""

    access_key_id: str = ""
    amazon_reachability_code: str = ""
    amazon_reachability_message: str = ""
    amazon_reachability_reachable: bool = False
    default_domain: str = ""
    ekmip_reachability: list[OntapAwsKmsEkmipReachability] = Field(default_factory=list)
    encryption_context: str = ""
    host: str = ""
    key_id: str = ""
    polling_period: int = 0
    port: int = 0
    proxy_host: str = ""
    proxy_password: str = ""
    proxy_port: int = 0
    proxy_type: str = ""
    proxy_username: str = ""
    region: str = ""
    scope: str = ""
    secret_access_key: str = ""
    service: str = ""
    skip_verify: bool = False
    state_cluster_state: bool = False
    state_code: str = ""
    state_message: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    timeout: int = 0
    uuid: str = ""
    verify: bool = False
    verify_host: bool = False
    verify_ip: bool = False
