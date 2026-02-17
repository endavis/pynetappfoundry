"""OntapFpolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapFpolicy(CacheModel):
    """OntapFpolicy information."""

    buffer_size_recv_buffer: int = 0
    buffer_size_send_buffer: int = 0
    certificate_ca: str = ""
    certificate_name: str = ""
    certificate_serial_number: str = ""
    format: str = ""
    keep_alive_interval: str = ""
    max_server_requests: int = 0
    name: str = ""
    port: int = 0
    primary_servers: list[str] = Field(default_factory=list)
    request_abort_timeout: str = ""
    request_cancel_timeout: str = ""
    resiliency_directory_path: str = ""
    resiliency_enabled: bool = False
    resiliency_retention_duration: str = ""
    secondary_servers: list[str] = Field(default_factory=list)
    server_progress_timeout: str = ""
    ssl_option: str = ""
    status_request_interval: str = ""
    type_: str = ""
