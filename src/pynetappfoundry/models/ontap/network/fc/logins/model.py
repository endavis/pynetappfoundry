"""OntapFcLogin information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFcLoginIgroup(OntapModel):
    """OntapFcLoginIgroup sub-model for igroups."""

    name: str = ""
    uuid: str = ""


class OntapFcLoginInitiator(OntapModel):
    """OntapFcLoginInitiator sub-model for initiator."""

    aliases: list[str] = Field(default_factory=list)
    comment: str = ""
    port_address: str = ""
    wwnn: str = ""
    wwpn: str = ""


class OntapFcLoginInterface(OntapModel):
    """OntapFcLoginInterface sub-model for interface."""

    name: str = ""
    uuid: str = ""
    wwpn: str = ""


class OntapFcLoginSvm(OntapModel):
    """OntapFcLoginSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapFcLogin(OntapModel):
    """OntapFcLogin information."""

    igroups: list[OntapFcLoginIgroup] = Field(default_factory=list)
    initiator: OntapFcLoginInitiator = Field(default_factory=OntapFcLoginInitiator)
    interface: OntapFcLoginInterface = Field(default_factory=OntapFcLoginInterface)
    protocol: str = ""
    svm: OntapFcLoginSvm = Field(default_factory=OntapFcLoginSvm)
