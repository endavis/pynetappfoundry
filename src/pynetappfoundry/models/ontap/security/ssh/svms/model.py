"""OntapSvmSshServer information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSvmSshServerSvm(OntapModel):
    """OntapSvmSshServerSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSvmSshServer(OntapModel):
    """OntapSvmSshServer information."""

    ciphers: list[str] = Field(default_factory=list)
    host_key_algorithms: list[str] = Field(default_factory=list)
    is_rsa_in_publickey_algorithms_enabled: bool = False
    key_exchange_algorithms: list[str] = Field(default_factory=list)
    mac_algorithms: list[str] = Field(default_factory=list)
    max_authentication_retry_count: int = 0
    svm: OntapSvmSshServerSvm = Field(default_factory=OntapSvmSshServerSvm)
