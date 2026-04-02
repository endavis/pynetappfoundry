"""OntapShadowcopySet information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapShadowcopySetSvm(OntapModel):
    """OntapShadowcopySetSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapShadowcopySet(OntapModel):
    """OntapShadowcopySet information."""

    keep_snapshots: bool = False
    svm: OntapShadowcopySetSvm = Field(default_factory=OntapShadowcopySetSvm)
    uuid: str = ""
