"""OntapWeb information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapWeb(CacheModel):
    """OntapWeb information."""

    certificate_name: str = ""
    certificate_uuid: str = ""
    client_enabled: bool = False
    csrf_protection_enabled: bool = False
    csrf_token_concurrent_limit: int = 0
    csrf_token_idle_timeout: int = 0
    csrf_token_max_timeout: int = 0
    enabled: bool = False
    http_enabled: bool = False
    http_port: int = 0
    https_port: int = 0
    ocsp_enabled: bool = False
    per_address_limit: int = 0
    state: str = ""
    wait_queue_capacity: int = 0
