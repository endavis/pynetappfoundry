"""OntapNvmeInterface information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNvmeInterfaceFcInterfacePortNode(OntapModel):
    """OntapNvmeInterfaceFcInterfacePortNode sub-model for node."""

    name: str = ""


class OntapNvmeInterfaceFcInterfacePort(OntapModel):
    """OntapNvmeInterfaceFcInterfacePort sub-model for port."""

    name: str = ""
    node: OntapNvmeInterfaceFcInterfacePortNode = Field(
        default_factory=OntapNvmeInterfaceFcInterfacePortNode
    )
    uuid: str = ""


class OntapNvmeInterfaceFcInterface(OntapModel):
    """OntapNvmeInterfaceFcInterface sub-model for fc_interface."""

    port: OntapNvmeInterfaceFcInterfacePort = Field(
        default_factory=OntapNvmeInterfaceFcInterfacePort
    )
    wwnn: str = ""
    wwpn: str = ""


class OntapNvmeInterfaceIpInterfaceIp(OntapModel):
    """OntapNvmeInterfaceIpInterfaceIp sub-model for ip."""

    address: str = ""


class OntapNvmeInterfaceIpInterfaceLocationPortNode(OntapModel):
    """OntapNvmeInterfaceIpInterfaceLocationPortNode sub-model for node."""

    name: str = ""


class OntapNvmeInterfaceIpInterfaceLocationPort(OntapModel):
    """OntapNvmeInterfaceIpInterfaceLocationPort sub-model for port."""

    name: str = ""
    node: OntapNvmeInterfaceIpInterfaceLocationPortNode = Field(
        default_factory=OntapNvmeInterfaceIpInterfaceLocationPortNode
    )
    uuid: str = ""


class OntapNvmeInterfaceIpInterfaceLocation(OntapModel):
    """OntapNvmeInterfaceIpInterfaceLocation sub-model for location."""

    port: OntapNvmeInterfaceIpInterfaceLocationPort = Field(
        default_factory=OntapNvmeInterfaceIpInterfaceLocationPort
    )


class OntapNvmeInterfaceIpInterface(OntapModel):
    """OntapNvmeInterfaceIpInterface sub-model for ip_interface."""

    ip: OntapNvmeInterfaceIpInterfaceIp = Field(default_factory=OntapNvmeInterfaceIpInterfaceIp)
    location: OntapNvmeInterfaceIpInterfaceLocation = Field(
        default_factory=OntapNvmeInterfaceIpInterfaceLocation
    )


class OntapNvmeInterfaceNode(OntapModel):
    """OntapNvmeInterfaceNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapNvmeInterfaceSvm(OntapModel):
    """OntapNvmeInterfaceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNvmeInterface(OntapModel):
    """OntapNvmeInterface information."""

    enabled: bool = False
    fc_interface: OntapNvmeInterfaceFcInterface = Field(
        default_factory=OntapNvmeInterfaceFcInterface
    )
    interface_type: str = ""
    ip_interface: OntapNvmeInterfaceIpInterface = Field(
        default_factory=OntapNvmeInterfaceIpInterface
    )
    name: str = ""
    node: OntapNvmeInterfaceNode = Field(default_factory=OntapNvmeInterfaceNode)
    svm: OntapNvmeInterfaceSvm = Field(default_factory=OntapNvmeInterfaceSvm)
    transport_address: str = ""
    transport_protocols: list[str] = Field(default_factory=list)
    uuid: str = ""
