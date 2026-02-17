"""OntapSvmSshServer information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapSvmSshServer(CacheModel):
    """OntapSvmSshServer information."""

    ciphers: list[str] = Field(default_factory=list)
    host_key_algorithms: list[str] = Field(default_factory=list)
    is_rsa_in_publickey_algorithms_enabled: bool = False
    key_exchange_algorithms: list[str] = Field(default_factory=list)
    mac_algorithms: list[str] = Field(default_factory=list)
    max_authentication_retry_count: int = 0
    svm_name: str = ""
    svm_uuid: str = ""
