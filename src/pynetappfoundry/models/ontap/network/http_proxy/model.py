"""OntapNetworkHttpProxy information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapNetworkHttpProxy(OntapModel):
    """OntapNetworkHttpProxy information."""

    authentication_enabled: bool = False
    ipspace_name: str = ""
    ipspace_uuid: str = ""
    password: str = ""
    port: int = 0
    scope: str = ""
    server: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    username: str = ""
    uuid: str = ""
