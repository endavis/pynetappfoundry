"""OntapFlexcacheOrigin information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapFlexcacheOriginCluster(OntapModel):
    """OntapFlexcacheOriginCluster sub-model for cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapFlexcacheOriginSvm(OntapModel):
    """OntapFlexcacheOriginSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapFlexcacheOriginVolume(OntapModel):
    """OntapFlexcacheOriginVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapFlexcacheOrigin(OntapModel):
    """OntapFlexcacheOrigin information."""

    cluster: OntapFlexcacheOriginCluster = Field(default_factory=OntapFlexcacheOriginCluster)
    create_time: str = ""
    ip_address: str = ""
    size: int = 0
    state: str = ""
    svm: OntapFlexcacheOriginSvm = Field(default_factory=OntapFlexcacheOriginSvm)
    volume: OntapFlexcacheOriginVolume = Field(default_factory=OntapFlexcacheOriginVolume)
