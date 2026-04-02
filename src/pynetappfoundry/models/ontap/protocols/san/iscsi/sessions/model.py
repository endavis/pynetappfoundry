"""OntapIscsiSession information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIscsiSessionConnectionInitiatorAddress(OntapModel):
    """OntapIscsiSessionConnectionInitiatorAddress sub-model for initiator_address."""

    address: str = ""
    port: int = 0


class OntapIscsiSessionConnectionInterfaceIp(OntapModel):
    """OntapIscsiSessionConnectionInterfaceIp sub-model for ip."""

    address: str = ""
    port: int = 0


class OntapIscsiSessionConnectionInterface(OntapModel):
    """OntapIscsiSessionConnectionInterface sub-model for interface."""

    ip: OntapIscsiSessionConnectionInterfaceIp = Field(
        default_factory=OntapIscsiSessionConnectionInterfaceIp
    )
    name: str = ""
    uuid: str = ""


class OntapIscsiSessionConnection(OntapModel):
    """OntapIscsiSessionConnection sub-model for connections."""

    authentication_type: str = ""
    cid: int = 0
    initiator_address: OntapIscsiSessionConnectionInitiatorAddress = Field(
        default_factory=OntapIscsiSessionConnectionInitiatorAddress
    )
    interface: OntapIscsiSessionConnectionInterface = Field(
        default_factory=OntapIscsiSessionConnectionInterface
    )


class OntapIscsiSessionIgroup(OntapModel):
    """OntapIscsiSessionIgroup sub-model for igroups."""

    name: str = ""
    uuid: str = ""


class OntapIscsiSessionInitiator(OntapModel):
    """OntapIscsiSessionInitiator sub-model for initiator."""

    alias: str = ""
    comment: str = ""
    name: str = ""


class OntapIscsiSessionSvm(OntapModel):
    """OntapIscsiSessionSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapIscsiSession(OntapModel):
    """OntapIscsiSession information."""

    connections: list[OntapIscsiSessionConnection] = Field(default_factory=list)
    igroups: list[OntapIscsiSessionIgroup] = Field(default_factory=list)
    initiator: OntapIscsiSessionInitiator = Field(default_factory=OntapIscsiSessionInitiator)
    isid: str = ""
    svm: OntapIscsiSessionSvm = Field(default_factory=OntapIscsiSessionSvm)
    target_portal_group: str = ""
    target_portal_group_tag: int = 0
    tsih: int = 0
