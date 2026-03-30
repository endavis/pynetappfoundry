"""OntapApplicationComponentSnapshot information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapApplicationComponentSnapshot(OntapModel):
    """OntapApplicationComponentSnapshot information."""

    application_name: str = ""
    application_uuid: str = ""
    comment: str = ""
    component_name: str = ""
    component_uuid: str = ""
    consistency_type: str = ""
    create_time: str = ""
    is_partial: bool = False
    name: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
