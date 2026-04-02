"""OntapFpolicyEngine information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFpolicyEngineBufferSize(OntapModel):
    """OntapFpolicyEngineBufferSize sub-model for buffer_size."""

    recv_buffer: int = 0
    send_buffer: int = 0


class OntapFpolicyEngineCertificate(OntapModel):
    """OntapFpolicyEngineCertificate sub-model for certificate."""

    ca: str = ""
    name: str = ""
    serial_number: str = ""


class OntapFpolicyEngineResiliency(OntapModel):
    """OntapFpolicyEngineResiliency sub-model for resiliency."""

    directory_path: str = ""
    enabled: bool = False
    retention_duration: str = ""


class OntapFpolicyEngineSvm(OntapModel):
    """OntapFpolicyEngineSvm sub-model for svm."""

    uuid: str = ""


class OntapFpolicyEngine(OntapModel):
    """OntapFpolicyEngine information."""

    buffer_size: OntapFpolicyEngineBufferSize = Field(default_factory=OntapFpolicyEngineBufferSize)
    certificate: OntapFpolicyEngineCertificate = Field(
        default_factory=OntapFpolicyEngineCertificate
    )
    format: str = ""
    keep_alive_interval: str = ""
    max_server_requests: int = 0
    name: str = ""
    port: int = 0
    primary_servers: list[str] = Field(default_factory=list)
    request_abort_timeout: str = ""
    request_cancel_timeout: str = ""
    resiliency: OntapFpolicyEngineResiliency = Field(default_factory=OntapFpolicyEngineResiliency)
    secondary_servers: list[str] = Field(default_factory=list)
    server_progress_timeout: str = ""
    ssl_option: str = ""
    status_request_interval: str = ""
    svm: OntapFpolicyEngineSvm = Field(default_factory=OntapFpolicyEngineSvm)
    type_: str = ""
