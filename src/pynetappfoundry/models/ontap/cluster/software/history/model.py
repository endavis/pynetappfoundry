"""OntapSoftwareHistory information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSoftwareHistory(OntapModel):
    """OntapSoftwareHistory information."""

    end_time: str = ""
    from_version: str = ""
    node_name: str = ""
    node_uuid: str = ""
    start_time: str = ""
    state: str = ""
    to_version: str = ""
