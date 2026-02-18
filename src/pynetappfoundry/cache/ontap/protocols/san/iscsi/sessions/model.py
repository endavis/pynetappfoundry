"""OntapIscsiSession information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapIscsiSessionConnection(CacheModel):
    """OntapIscsiSessionConnection sub-model for connections."""

    connections_authentication_type: str = ""
    connections_cid: int = 0
    connections_initiator_address_address: str = ""
    connections_initiator_address_port: int = 0
    connections_interface_ip_address: str = ""
    connections_interface_ip_port: int = 0
    connections_interface_name: str = ""
    connections_interface_uuid: str = ""


class OntapIscsiSessionIgroup(CacheModel):
    """OntapIscsiSessionIgroup sub-model for igroups."""

    igroups_name: str = ""
    igroups_uuid: str = ""


class OntapIscsiSession(CacheModel):
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
