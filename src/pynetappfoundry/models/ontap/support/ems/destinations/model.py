"""OntapEmsDestinationResponse information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapEmsDestinationResponseError(OntapModel):
    """OntapEmsDestinationResponseError sub-model for errors."""

    message_arguments: list[dict[str, Any]] = Field(default_factory=list)
    message_code: str = ""
    message_message: str = ""
    node_name: str = ""
    node_uuid: str = ""


class OntapEmsDestinationResponseFilter(OntapModel):
    """OntapEmsDestinationResponseFilter sub-model for filters."""

    name: str = ""


class OntapEmsDestinationResponse(OntapModel):
    """OntapEmsDestinationResponse information."""

    access_control_role_name: str = ""
    certificate_ca: str = ""
    certificate_name: str = ""
    certificate_serial_number: str = ""
    connectivity_errors: list[OntapEmsDestinationResponseError] = Field(default_factory=list)
    connectivity_state: str = ""
    destination: str = ""
    filters: list[OntapEmsDestinationResponseFilter] = Field(default_factory=list)
    name: str = ""
    syslog_format_hostname_override: str = ""
    syslog_format_message: str = ""
    syslog_format_timestamp_override: str = ""
    syslog_port: int = 0
    syslog_transport: str = ""
    system_defined: bool = False
    type_: str = ""
