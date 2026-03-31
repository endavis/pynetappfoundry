"""OntapIscsiSession information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIscsiSessionConnection(OntapModel):
    """OntapIscsiSessionConnection sub-model for connections."""

    authentication_type: str = ""
    cid: int = 0
    initiator_address_address: str = ""
    initiator_address_port: int = 0
    interface_ip_address: str = ""
    interface_ip_port: int = 0
    interface_name: str = ""
    interface_uuid: str = ""


class OntapIscsiSessionIgroup(OntapModel):
    """OntapIscsiSessionIgroup sub-model for igroups."""

    name: str = ""
    uuid: str = ""


class OntapIscsiSession(OntapModel):
    """OntapIscsiSession information."""

    connections: list[OntapIscsiSessionConnection] = Field(default_factory=list)
    igroups: list[OntapIscsiSessionIgroup] = Field(default_factory=list)
    initiator_alias: str = ""
    initiator_comment: str = ""
    initiator_name: str = ""
    isid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    target_portal_group: str = ""
    target_portal_group_tag: int = 0
    tsih: int = 0
