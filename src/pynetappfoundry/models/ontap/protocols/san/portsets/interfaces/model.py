"""OntapPortsetInterface information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


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


class OntapPortsetInterfacePortset(OntapModel):
    """OntapPortsetInterfacePortset sub-model for portset."""

    uuid: str = ""


class OntapPortsetInterfaceRecordFc(OntapModel):
    """OntapPortsetInterfaceRecordFc sub-model for fc."""

    name: str = ""
    uuid: str = ""
    wwpn: str = ""


class OntapPortsetInterfaceRecordIpIp(OntapModel):
    """OntapPortsetInterfaceRecordIpIp sub-model for ip."""

    address: str = ""


class OntapPortsetInterfaceRecordIp(OntapModel):
    """OntapPortsetInterfaceRecordIp sub-model for ip."""

    ip: OntapPortsetInterfaceRecordIpIp = Field(default_factory=OntapPortsetInterfaceRecordIpIp)
    name: str = ""
    uuid: str = ""


class OntapPortsetInterfaceRecord(OntapModel):
    """OntapPortsetInterfaceRecord sub-model for records."""

    fc: OntapPortsetInterfaceRecordFc = Field(default_factory=OntapPortsetInterfaceRecordFc)
    ip: OntapPortsetInterfaceRecordIp = Field(default_factory=OntapPortsetInterfaceRecordIp)
    uuid: str = ""


class OntapPortsetInterface(OntapModel):
    """OntapPortsetInterface information."""

    fc: OntapPortsetInterfaceFc = Field(default_factory=OntapPortsetInterfaceFc)
    ip: OntapPortsetInterfaceIp = Field(default_factory=OntapPortsetInterfaceIp)
    portset: OntapPortsetInterfacePortset = Field(default_factory=OntapPortsetInterfacePortset)
    records: list[OntapPortsetInterfaceRecord] = Field(default_factory=list)
    uuid: str = ""
