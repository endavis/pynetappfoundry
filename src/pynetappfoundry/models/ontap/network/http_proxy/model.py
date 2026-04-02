"""OntapNetworkHttpProxy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNetworkHttpProxyIpspace(OntapModel):
    """OntapNetworkHttpProxyIpspace sub-model for ipspace."""

    name: str = ""
    uuid: str = ""


class OntapNetworkHttpProxySvm(OntapModel):
    """OntapNetworkHttpProxySvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNetworkHttpProxy(OntapModel):
    """OntapNetworkHttpProxy information."""

    authentication_enabled: bool = False
    ipspace: OntapNetworkHttpProxyIpspace = Field(default_factory=OntapNetworkHttpProxyIpspace)
    password: str = ""
    port: int = 0
    scope: str = ""
    server: str = ""
    svm: OntapNetworkHttpProxySvm = Field(default_factory=OntapNetworkHttpProxySvm)
    username: str = ""
    uuid: str = ""
