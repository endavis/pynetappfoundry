"""OntapPortset information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPortsetIgroup(OntapModel):
    """OntapPortsetIgroup sub-model for igroups."""

    igroups_name: str = ""
    igroups_uuid: str = ""


class OntapPortsetInterface(OntapModel):
    """OntapPortsetInterface sub-model for interfaces."""

    interfaces_fc_name: str = ""
    interfaces_fc_uuid: str = ""
    interfaces_fc_wwpn: str = ""
    interfaces_ip_ip_address: str = ""
    interfaces_ip_name: str = ""
    interfaces_ip_uuid: str = ""
    interfaces_uuid: str = ""


class OntapPortset(OntapModel):
    """OntapPortset information."""

    igroups: list[OntapPortsetIgroup] = Field(default_factory=list)
    interfaces: list[OntapPortsetInterface] = Field(default_factory=list)
    name: str = ""
    protocol: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
