"""OntapResourceTagResource information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapResourceTagResource(OntapModel):
    """OntapResourceTagResource information."""

    href: str = ""
    label: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    value: str = ""
