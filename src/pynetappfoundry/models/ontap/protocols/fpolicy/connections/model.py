"""OntapFpolicyConnection information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFpolicyConnectionDisconnectedReason(OntapModel):
    """OntapFpolicyConnectionDisconnectedReason sub-model for disconnected_reason."""

    code: int = 0
    message: str = ""


class OntapFpolicyConnectionNode(OntapModel):
    """OntapFpolicyConnectionNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapFpolicyConnectionPolicy(OntapModel):
    """OntapFpolicyConnectionPolicy sub-model for policy."""

    name: str = ""


class OntapFpolicyConnectionSvm(OntapModel):
    """OntapFpolicyConnectionSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapFpolicyConnection(OntapModel):
    """OntapFpolicyConnection information."""

    disconnected_reason: OntapFpolicyConnectionDisconnectedReason = Field(
        default_factory=OntapFpolicyConnectionDisconnectedReason
    )
    node: OntapFpolicyConnectionNode = Field(default_factory=OntapFpolicyConnectionNode)
    policy: OntapFpolicyConnectionPolicy = Field(default_factory=OntapFpolicyConnectionPolicy)
    server: str = ""
    session_uuid: str = ""
    state: str = ""
    svm: OntapFpolicyConnectionSvm = Field(default_factory=OntapFpolicyConnectionSvm)
    type_: str = ""
    update_time: str = ""
