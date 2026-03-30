"""OntapFlexcacheOrigin information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapFlexcacheOrigin(OntapModel):
    """OntapFlexcacheOrigin information."""

    cluster_name: str = ""
    cluster_uuid: OntapUUID = ""
    create_time: str = ""
    ip_address: str = ""
    size: int = 0
    state: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    volume_name: str = ""
    volume_uuid: str = ""
