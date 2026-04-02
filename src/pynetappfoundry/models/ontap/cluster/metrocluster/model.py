"""OntapMetrocluster information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapMetroclusterNode(OntapModel):
    """OntapMetroclusterNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterPartner(OntapModel):
    """OntapMetroclusterPartner sub-model for partner."""

    name: str = ""
    uuid: str = ""


class OntapMetrocluster(OntapModel):
    """OntapMetrocluster information."""

    node: OntapMetroclusterNode = Field(default_factory=OntapMetroclusterNode)
    partner: OntapMetroclusterPartner = Field(default_factory=OntapMetroclusterPartner)
