"""OntapEmsDestinationResponse information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapEmsDestinationResponseAccessControlRole(OntapModel):
    """OntapEmsDestinationResponseAccessControlRole sub-model for access_control_role."""

    name: str = ""


class OntapEmsDestinationResponseCertificate(OntapModel):
    """OntapEmsDestinationResponseCertificate sub-model for certificate."""

    ca: str = ""
    name: str = ""
    serial_number: str = ""


class OntapEmsDestinationResponseConnectivity(OntapModel):
    """OntapEmsDestinationResponseConnectivity sub-model for connectivity."""

    errors: list[dict[str, Any]] = Field(default_factory=list)
    state: str = ""


class OntapEmsDestinationResponseFilter(OntapModel):
    """OntapEmsDestinationResponseFilter sub-model for filters."""

    name: str = ""


class OntapEmsDestinationResponseSyslogFormat(OntapModel):
    """OntapEmsDestinationResponseSyslogFormat sub-model for format."""

    hostname_override: str = ""
    message: str = ""
    timestamp_override: str = ""


class OntapEmsDestinationResponseSyslog(OntapModel):
    """OntapEmsDestinationResponseSyslog sub-model for syslog."""

    format: OntapEmsDestinationResponseSyslogFormat = Field(
        default_factory=OntapEmsDestinationResponseSyslogFormat
    )
    port: int = 0
    transport: str = ""


class OntapEmsDestinationResponse(OntapModel):
    """OntapEmsDestinationResponse information."""

    access_control_role: OntapEmsDestinationResponseAccessControlRole = Field(
        default_factory=OntapEmsDestinationResponseAccessControlRole
    )
    certificate: OntapEmsDestinationResponseCertificate = Field(
        default_factory=OntapEmsDestinationResponseCertificate
    )
    connectivity: OntapEmsDestinationResponseConnectivity = Field(
        default_factory=OntapEmsDestinationResponseConnectivity
    )
    destination: str = ""
    filters: list[OntapEmsDestinationResponseFilter] = Field(default_factory=list)
    name: str = ""
    syslog: OntapEmsDestinationResponseSyslog = Field(
        default_factory=OntapEmsDestinationResponseSyslog
    )
    system_defined: bool = False
    type_: str = ""
