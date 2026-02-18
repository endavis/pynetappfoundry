"""OntapKerberosInterface information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapKerberosInterface(CacheModel):
    """OntapKerberosInterface information."""

    enabled: bool = False
    encryption_types: list[str] = Field(default_factory=list)
    force: bool = False
    interface_ip_address: str = ""
    interface_name: str = ""
    interface_uuid: str = ""
    keytab_uri: str = ""
    machine_account: str = ""
    organizational_unit: str = ""
    password: str = ""
    spn: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    user: str = ""
