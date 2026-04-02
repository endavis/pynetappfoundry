"""OntapKerberosRealm information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapKerberosRealmAdServer(OntapModel):
    """OntapKerberosRealmAdServer sub-model for ad_server."""

    address: str = ""
    name: str = ""


class OntapKerberosRealmAdminServer(OntapModel):
    """OntapKerberosRealmAdminServer sub-model for admin_server."""

    address: str = ""
    port: int = 0


class OntapKerberosRealmKdc(OntapModel):
    """OntapKerberosRealmKdc sub-model for kdc."""

    ip: str = ""
    port: int = 0
    vendor: str = ""


class OntapKerberosRealmPasswordServer(OntapModel):
    """OntapKerberosRealmPasswordServer sub-model for password_server."""

    address: str = ""
    port: int = 0


class OntapKerberosRealmSvm(OntapModel):
    """OntapKerberosRealmSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapKerberosRealm(OntapModel):
    """OntapKerberosRealm information."""

    ad_server: OntapKerberosRealmAdServer = Field(default_factory=OntapKerberosRealmAdServer)
    admin_server: OntapKerberosRealmAdminServer = Field(
        default_factory=OntapKerberosRealmAdminServer
    )
    clock_skew: int = 0
    comment: str = ""
    encryption_types: list[str] = Field(default_factory=list)
    kdc: OntapKerberosRealmKdc = Field(default_factory=OntapKerberosRealmKdc)
    name: str = ""
    password_server: OntapKerberosRealmPasswordServer = Field(
        default_factory=OntapKerberosRealmPasswordServer
    )
    svm: OntapKerberosRealmSvm = Field(default_factory=OntapKerberosRealmSvm)
