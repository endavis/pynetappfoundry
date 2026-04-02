"""OntapNfsTlsInterface information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNfsTlsInterfaceCertificate(OntapModel):
    """OntapNfsTlsInterfaceCertificate sub-model for certificate."""

    name: str = ""
    uuid: str = ""


class OntapNfsTlsInterfaceInterfaceIp(OntapModel):
    """OntapNfsTlsInterfaceInterfaceIp sub-model for ip."""

    address: str = ""


class OntapNfsTlsInterfaceInterface(OntapModel):
    """OntapNfsTlsInterfaceInterface sub-model for interface."""

    ip: OntapNfsTlsInterfaceInterfaceIp = Field(default_factory=OntapNfsTlsInterfaceInterfaceIp)
    name: str = ""
    uuid: str = ""


class OntapNfsTlsInterfaceSvm(OntapModel):
    """OntapNfsTlsInterfaceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNfsTlsInterface(OntapModel):
    """OntapNfsTlsInterface information."""

    certificate: OntapNfsTlsInterfaceCertificate = Field(
        default_factory=OntapNfsTlsInterfaceCertificate
    )
    enabled: bool = False
    interface: OntapNfsTlsInterfaceInterface = Field(default_factory=OntapNfsTlsInterfaceInterface)
    svm: OntapNfsTlsInterfaceSvm = Field(default_factory=OntapNfsTlsInterfaceSvm)
