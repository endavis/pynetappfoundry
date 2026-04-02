"""OntapWwpnAlias information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapWwpnAliasSvm(OntapModel):
    """OntapWwpnAliasSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapWwpnAlias(OntapModel):
    """OntapWwpnAlias information."""

    alias: str = ""
    svm: OntapWwpnAliasSvm = Field(default_factory=OntapWwpnAliasSvm)
    wwpn: str = ""
