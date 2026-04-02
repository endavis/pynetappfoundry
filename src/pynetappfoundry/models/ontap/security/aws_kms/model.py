"""OntapAwsKms information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapAwsKmsAmazonReachability(OntapModel):
    """OntapAwsKmsAmazonReachability sub-model for amazon_reachability."""

    code: str = ""
    message: str = ""
    reachable: bool = False


class OntapAwsKmsEkmipReachabilityNode(OntapModel):
    """OntapAwsKmsEkmipReachabilityNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapAwsKmsEkmipReachability(OntapModel):
    """OntapAwsKmsEkmipReachability sub-model for ekmip_reachability."""

    code: str = ""
    message: str = ""
    node: OntapAwsKmsEkmipReachabilityNode = Field(default_factory=OntapAwsKmsEkmipReachabilityNode)
    reachable: bool = False


class OntapAwsKmsState(OntapModel):
    """OntapAwsKmsState sub-model for state."""

    cluster_state: bool = False
    code: str = ""
    message: str = ""


class OntapAwsKmsSvm(OntapModel):
    """OntapAwsKmsSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapAwsKms(OntapModel):
    """OntapAwsKms information."""

    access_key_id: str = ""
    amazon_reachability: OntapAwsKmsAmazonReachability = Field(
        default_factory=OntapAwsKmsAmazonReachability
    )
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
    state: OntapAwsKmsState = Field(default_factory=OntapAwsKmsState)
    svm: OntapAwsKmsSvm = Field(default_factory=OntapAwsKmsSvm)
    timeout: int = 0
    uuid: str = ""
    verify: bool = False
    verify_host: bool = False
    verify_ip: bool = False
