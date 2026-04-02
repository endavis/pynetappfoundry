"""OntapFpolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFpolicyBufferSize(OntapModel):
    """OntapFpolicyBufferSize sub-model for buffer_size."""

    recv_buffer: int = 0
    send_buffer: int = 0


class OntapFpolicyCertificate(OntapModel):
    """OntapFpolicyCertificate sub-model for certificate."""

    ca: str = ""
    name: str = ""
    serial_number: str = ""


class OntapFpolicyResiliency(OntapModel):
    """OntapFpolicyResiliency sub-model for resiliency."""

    directory_path: str = ""
    enabled: bool = False
    retention_duration: str = ""


class OntapFpolicy(OntapModel):
    """OntapFpolicy information."""

    buffer_size: OntapFpolicyBufferSize = Field(default_factory=OntapFpolicyBufferSize)
    certificate: OntapFpolicyCertificate = Field(default_factory=OntapFpolicyCertificate)
    format: str = ""
    keep_alive_interval: str = ""
    max_server_requests: int = 0
    name: str = ""
    port: int = 0
    primary_servers: list[str] = Field(default_factory=list)
    request_abort_timeout: str = ""
    request_cancel_timeout: str = ""
    resiliency: OntapFpolicyResiliency = Field(default_factory=OntapFpolicyResiliency)
    secondary_servers: list[str] = Field(default_factory=list)
    server_progress_timeout: str = ""
    ssl_option: str = ""
    status_request_interval: str = ""
    type_: str = ""
