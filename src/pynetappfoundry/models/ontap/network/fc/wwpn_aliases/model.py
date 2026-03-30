"""OntapWwpnAlias information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapWwpnAlias(OntapModel):
    """OntapWwpnAlias information."""

    alias: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    wwpn: str = ""
