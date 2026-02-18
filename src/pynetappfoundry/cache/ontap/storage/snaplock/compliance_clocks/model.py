"""OntapSnaplockComplianceClock information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSnaplockComplianceClock(CacheModel):
    """OntapSnaplockComplianceClock information."""

    node_name: str = ""
    node_uuid: str = ""
    time: str = ""
