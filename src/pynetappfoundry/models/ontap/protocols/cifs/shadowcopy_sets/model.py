"""OntapShadowcopySet information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapShadowcopySet(OntapModel):
    """OntapShadowcopySet information."""

    keep_snapshots: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
