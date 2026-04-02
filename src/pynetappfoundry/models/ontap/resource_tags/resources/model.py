"""OntapResourceTagResource information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapResourceTagResourceSvm(OntapModel):
    """OntapResourceTagResourceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapResourceTagResource(OntapModel):
    """OntapResourceTagResource information."""

    href: str = ""
    label: str = ""
    svm: OntapResourceTagResourceSvm = Field(default_factory=OntapResourceTagResourceSvm)
    value: str = ""
