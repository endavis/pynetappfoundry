"""OntapPortsetInterface information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapPortsetInterfaceRecord(CacheModel):
    """OntapPortsetInterfaceRecord sub-model for records."""

    records_fc_name: str = ""
    records_fc_uuid: str = ""
    records_fc_wwpn: str = ""
    records_ip_ip_address: str = ""
    records_ip_name: str = ""
    records_ip_uuid: str = ""
    records_uuid: str = ""


class OntapPortsetInterface(CacheModel):
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
