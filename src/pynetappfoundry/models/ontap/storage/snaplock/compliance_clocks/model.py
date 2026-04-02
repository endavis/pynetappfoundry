"""OntapSnaplockComplianceClock information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSnaplockComplianceClockNode(OntapModel):
    """OntapSnaplockComplianceClockNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapSnaplockComplianceClock(OntapModel):
    """OntapSnaplockComplianceClock information."""

    node: OntapSnaplockComplianceClockNode = Field(default_factory=OntapSnaplockComplianceClockNode)
    time: str = ""
