"""OntapEmsDestinationResponse type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.support.ems.destinations.model import (
    OntapEmsDestinationResponse,
    OntapEmsDestinationResponseError,
    OntapEmsDestinationResponseFilter,
)


def _transform_connectivity_errors(
    record: dict[str, Any],
) -> list[OntapEmsDestinationResponseError]:
    """Transform connectivity.errors into OntapEmsDestinationResponseError list."""
    return [
        OntapEmsDestinationResponseError(**item) for item in record.get("connectivity.errors", [])
    ]


def _transform_filters(record: dict[str, Any]) -> list[OntapEmsDestinationResponseFilter]:
    """Transform filters into OntapEmsDestinationResponseFilter list."""
    return [OntapEmsDestinationResponseFilter(**item) for item in record.get("filters", [])]


ONTAPEMSDESTINATIONRESPONSE_MAPPING = TypeMapping(
    name="OntapEmsDestinationResponse",
    model_class=OntapEmsDestinationResponse,
    api_endpoint="/support/ems/destinations?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="access_control_role_name",
            api_path="access_control_role.name",
        ),
        FieldMapping(
            cache_attr="certificate_ca",
            api_path="certificate.ca",
        ),
        FieldMapping(
            cache_attr="certificate_name",
            api_path="certificate.name",
        ),
        FieldMapping(
            cache_attr="certificate_serial_number",
            api_path="certificate.serial_number",
        ),
        FieldMapping(
            cache_attr="connectivity_errors",
            api_path="connectivity.errors",
            transform=_transform_connectivity_errors,
            default=[],
        ),
        FieldMapping(
            cache_attr="connectivity_state",
            api_path="connectivity.state",
        ),
        FieldMapping(
            cache_attr="destination",
            api_path="destination",
        ),
        FieldMapping(
            cache_attr="filters",
            api_path="filters",
            transform=_transform_filters,
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="syslog_format_hostname_override",
            api_path="syslog.format.hostname_override",
        ),
        FieldMapping(
            cache_attr="syslog_format_message",
            api_path="syslog.format.message",
        ),
        FieldMapping(
            cache_attr="syslog_format_timestamp_override",
            api_path="syslog.format.timestamp_override",
        ),
        FieldMapping(
            cache_attr="syslog_port",
            api_path="syslog.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="syslog_transport",
            api_path="syslog.transport",
        ),
        FieldMapping(
            cache_attr="system_defined",
            api_path="system_defined",
            default=False,
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
    ),
)

model_registry.register_mapping("OntapEmsDestinationResponse", ONTAPEMSDESTINATIONRESPONSE_MAPPING)
