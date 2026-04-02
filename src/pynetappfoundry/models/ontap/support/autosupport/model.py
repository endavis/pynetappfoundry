"""OntapAutosupport information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapAutosupportCorrectiveAction(OntapModel):
    """OntapAutosupportCorrectiveAction sub-model for corrective_action."""

    code: str = ""
    message: str = ""


class OntapAutosupportIssue(OntapModel):
    """OntapAutosupportIssue sub-model for issue."""

    code: str = ""
    message: str = ""


class OntapAutosupportNode(OntapModel):
    """OntapAutosupportNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapAutosupport(OntapModel):
    """OntapAutosupport information."""

    component: str = ""
    corrective_action: OntapAutosupportCorrectiveAction = Field(
        default_factory=OntapAutosupportCorrectiveAction
    )
    destination: str = ""
    issue: OntapAutosupportIssue = Field(default_factory=OntapAutosupportIssue)
    node: OntapAutosupportNode = Field(default_factory=OntapAutosupportNode)
