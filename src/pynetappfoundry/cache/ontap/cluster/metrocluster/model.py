"""OntapMetrocluster information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapMetrocluster(CacheModel):
    """OntapMetrocluster information."""

    node_name: str = ""
    node_uuid: str = ""
    partner_name: str = ""
    partner_uuid: str = ""
