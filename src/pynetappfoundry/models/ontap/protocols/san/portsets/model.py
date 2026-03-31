"""OntapPortset information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPortsetIgroup(OntapModel):
    """OntapPortsetIgroup sub-model for igroups."""

    name: str = ""
    uuid: str = ""


class OntapPortsetInterface(OntapModel):
    """OntapPortsetInterface sub-model for interfaces."""

    fc_name: str = ""
    fc_uuid: str = ""
    fc_wwpn: str = ""
    ip_ip_address: str = ""
    ip_name: str = ""
    ip_uuid: str = ""
    uuid: str = ""


class OntapPortset(OntapModel):
    """OntapPortset information."""

    igroups: list[OntapPortsetIgroup] = Field(default_factory=list)
    interfaces: list[OntapPortsetInterface] = Field(default_factory=list)
    name: str = ""
    protocol: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
