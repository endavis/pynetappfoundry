"""OntapFcLogin information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapFcLoginIgroup(CacheModel):
    """OntapFcLoginIgroup sub-model for igroups."""

    igroups_name: str = ""
    igroups_uuid: str = ""


class OntapFcLogin(CacheModel):
    """OntapFcLogin information."""

    igroups: list[OntapFcLoginIgroup] = Field(default_factory=list)
    initiator_aliases: list[str] = Field(default_factory=list)
    initiator_comment: str = ""
    initiator_port_address: str = ""
    initiator_wwnn: str = ""
    initiator_wwpn: str = ""
    interface_name: str = ""
    interface_uuid: str = ""
    interface_wwpn: str = ""
    protocol: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
