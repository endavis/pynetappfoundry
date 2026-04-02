"""OntapShadowcopy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapShadowcopyShadowcopySet(OntapModel):
    """OntapShadowcopyShadowcopySet sub-model for shadowcopy_set."""

    uuid: str = ""


class OntapShadowcopyShare(OntapModel):
    """OntapShadowcopyShare sub-model for share."""

    name: str = ""


class OntapShadowcopySvm(OntapModel):
    """OntapShadowcopySvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapShadowcopyVolume(OntapModel):
    """OntapShadowcopyVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapShadowcopy(OntapModel):
    """OntapShadowcopy information."""

    client_uuid: str = ""
    destination_dir: str = ""
    files: list[str] = Field(default_factory=list)
    shadowcopy_set: OntapShadowcopyShadowcopySet = Field(
        default_factory=OntapShadowcopyShadowcopySet
    )
    share: OntapShadowcopyShare = Field(default_factory=OntapShadowcopyShare)
    source_dir: str = ""
    svm: OntapShadowcopySvm = Field(default_factory=OntapShadowcopySvm)
    uuid: str = ""
    volume: OntapShadowcopyVolume = Field(default_factory=OntapShadowcopyVolume)
    with_content: bool = False
