"""OntapKerberosInterface information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapKerberosInterfaceInterfaceIp(OntapModel):
    """OntapKerberosInterfaceInterfaceIp sub-model for ip."""

    address: str = ""


class OntapKerberosInterfaceInterface(OntapModel):
    """OntapKerberosInterfaceInterface sub-model for interface."""

    ip: OntapKerberosInterfaceInterfaceIp = Field(default_factory=OntapKerberosInterfaceInterfaceIp)
    name: str = ""
    uuid: str = ""


class OntapKerberosInterfaceSvm(OntapModel):
    """OntapKerberosInterfaceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapKerberosInterface(OntapModel):
    """OntapKerberosInterface information."""

    enabled: bool = False
    encryption_types: list[str] = Field(default_factory=list)
    force: bool = False
    interface: OntapKerberosInterfaceInterface = Field(
        default_factory=OntapKerberosInterfaceInterface
    )
    keytab_uri: str = ""
    machine_account: str = ""
    organizational_unit: str = ""
    password: str = ""
    spn: str = ""
    svm: OntapKerberosInterfaceSvm = Field(default_factory=OntapKerberosInterfaceSvm)
    user: str = ""
