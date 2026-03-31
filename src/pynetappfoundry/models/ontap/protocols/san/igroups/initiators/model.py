"""OntapIgroupInitiator information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIgroupInitiatorAlert(OntapModel):
    """OntapIgroupInitiatorAlert sub-model for alerts."""

    summary_arguments: list[dict[str, Any]] = Field(default_factory=list)
    summary_code: str = ""
    summary_message: str = ""


class OntapIgroupInitiatorConnection(OntapModel):
    """OntapIgroupInitiatorConnection sub-model for connections."""

    logins: list[dict[str, Any]] = Field(default_factory=list)
    node_name: str = ""
    node_uuid: str = ""


class OntapIgroupInitiatorPeerSvm(OntapModel):
    """OntapIgroupInitiatorPeerSvm sub-model for peer_svms."""

    name: str = ""
    uuid: str = ""


class OntapIgroupInitiatorRecord(OntapModel):
    """OntapIgroupInitiatorRecord sub-model for records."""

    comment: str = ""
    name: str = ""
    proximity_local_svm: bool = False
    proximity_peer_svms: list[dict[str, Any]] = Field(default_factory=list)


class OntapIgroupInitiator(OntapModel):
    """OntapIgroupInitiator information."""

    comment: str = ""
    connectivity_tracking_alerts: list[OntapIgroupInitiatorAlert] = Field(default_factory=list)
    connectivity_tracking_connection_state: str = ""
    connectivity_tracking_connections: list[OntapIgroupInitiatorConnection] = Field(
        default_factory=list
    )
    igroup_name: str = ""
    igroup_uuid: str = ""
    name: str = ""
    proximity_local_svm: bool = False
    proximity_peer_svms: list[OntapIgroupInitiatorPeerSvm] = Field(default_factory=list)
    records: list[OntapIgroupInitiatorRecord] = Field(default_factory=list)
