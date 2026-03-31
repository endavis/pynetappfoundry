"""OntapPortsetInterface information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPortsetInterfaceRecord(OntapModel):
    """OntapPortsetInterfaceRecord sub-model for records."""

    fc_name: str = ""
    fc_uuid: str = ""
    fc_wwpn: str = ""
    ip_ip_address: str = ""
    ip_name: str = ""
    ip_uuid: str = ""
    uuid: str = ""


class OntapPortsetInterface(OntapModel):
    """OntapPortsetInterface information."""

    fc_name: str = ""
    fc_uuid: str = ""
    fc_wwpn: str = ""
    ip_ip_address: str = ""
    ip_name: str = ""
    ip_uuid: str = ""
    portset_uuid: str = ""
    records: list[OntapPortsetInterfaceRecord] = Field(default_factory=list)
    uuid: str = ""
