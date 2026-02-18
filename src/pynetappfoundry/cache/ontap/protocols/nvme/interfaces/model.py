"""OntapNvmeInterface information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapNvmeInterface(CacheModel):
    """OntapNvmeInterface information."""

    enabled: bool = False
    fc_interface_port_name: str = ""
    fc_interface_port_node_name: str = ""
    fc_interface_port_uuid: str = ""
    fc_interface_wwnn: str = ""
    fc_interface_wwpn: str = ""
    interface_type: str = ""
    ip_interface_ip_address: str = ""
    ip_interface_location_port_name: str = ""
    ip_interface_location_port_node_name: str = ""
    ip_interface_location_port_uuid: str = ""
    name: str = ""
    node_name: str = ""
    node_uuid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    transport_address: str = ""
    transport_protocols: list[str] = Field(default_factory=list)
    uuid: str = ""
