"""OntapPortset information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPortsetIgroup(OntapModel):
    """OntapPortsetIgroup sub-model for igroups."""

    name: str = ""
    uuid: str = ""


class OntapPortsetInterfaceFc(OntapModel):
    """OntapPortsetInterfaceFc sub-model for fc."""

    name: str = ""
    uuid: str = ""
    wwpn: str = ""


class OntapPortsetInterfaceIpIp(OntapModel):
    """OntapPortsetInterfaceIpIp sub-model for ip."""

    address: str = ""


class OntapPortsetInterfaceIp(OntapModel):
    """OntapPortsetInterfaceIp sub-model for ip."""

    ip: OntapPortsetInterfaceIpIp = Field(default_factory=OntapPortsetInterfaceIpIp)
    name: str = ""
    uuid: str = ""


class OntapPortsetInterface(OntapModel):
    """OntapPortsetInterface sub-model for interfaces."""

    fc: OntapPortsetInterfaceFc = Field(default_factory=OntapPortsetInterfaceFc)
    ip: OntapPortsetInterfaceIp = Field(default_factory=OntapPortsetInterfaceIp)
    uuid: str = ""


class OntapPortsetSvm(OntapModel):
    """OntapPortsetSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapPortset(OntapModel):
    """OntapPortset information."""

    igroups: list[OntapPortsetIgroup] = Field(default_factory=list)
    interfaces: list[OntapPortsetInterface] = Field(default_factory=list)
    name: str = ""
    protocol: str = ""
    svm: OntapPortsetSvm = Field(default_factory=OntapPortsetSvm)
    uuid: str = ""
