"""OntapKerberosRealm information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapKerberosRealm(CacheModel):
    """OntapKerberosRealm information."""

    ad_server_address: str = ""
    ad_server_name: str = ""
    admin_server_address: str = ""
    admin_server_port: int = 0
    clock_skew: int = 0
    comment: str = ""
    encryption_types: list[str] = Field(default_factory=list)
    kdc_ip: str = ""
    kdc_port: int = 0
    kdc_vendor: str = ""
    name: str = ""
    password_server_address: str = ""
    password_server_port: int = 0
    svm_name: str = ""
    svm_uuid: str = ""
