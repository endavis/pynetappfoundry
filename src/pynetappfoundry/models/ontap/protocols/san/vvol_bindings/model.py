"""OntapVvolBinding information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapVvolBinding(OntapModel):
    """OntapVvolBinding information."""

    count: int = 0
    id: int = 0
    is_optimal: bool = False
    protocol_endpoint_name: str = ""
    protocol_endpoint_uuid: str = ""
    secondary_id: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    vvol_name: str = ""
    vvol_uuid: str = ""
