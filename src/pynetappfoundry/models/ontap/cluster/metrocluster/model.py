"""OntapMetrocluster information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapMetrocluster(OntapModel):
    """OntapMetrocluster information."""

    node_name: str = ""
    node_uuid: str = ""
    partner_name: str = ""
    partner_uuid: str = ""
