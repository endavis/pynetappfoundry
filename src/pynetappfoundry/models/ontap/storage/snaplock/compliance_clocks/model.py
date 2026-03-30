"""OntapSnaplockComplianceClock information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSnaplockComplianceClock(OntapModel):
    """OntapSnaplockComplianceClock information."""

    node_name: str = ""
    node_uuid: str = ""
    time: str = ""
