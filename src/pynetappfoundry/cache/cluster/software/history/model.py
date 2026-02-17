"""OntapSoftwareHistory information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSoftwareHistory(CacheModel):
    """OntapSoftwareHistory information."""

    end_time: str = ""
    from_version: str = ""
    node_name: str = ""
    node_uuid: str = ""
    start_time: str = ""
    state: str = ""
    to_version: str = ""
