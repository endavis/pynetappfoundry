"""OntapCifsConnection type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.connections.model import (
    OntapCifsConnection,
    OntapCifsConnectionSession,
)


def _transform_sessions(record: dict[str, Any]) -> list[OntapCifsConnectionSession]:
    """Transform sessions into OntapCifsConnectionSession list."""
    return [OntapCifsConnectionSession(**item) for item in record.get("sessions", [])]


ONTAPCIFSCONNECTION_MAPPING = TypeMapping(
    name="OntapCifsConnection",
    model_class=OntapCifsConnection,
    api_endpoint="/protocols/cifs/connections?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="client_ip",
            api_path="client_ip",
        ),
        FieldMapping(
            cache_attr="client_port",
            api_path="client_port",
            default=0,
        ),
        FieldMapping(
            cache_attr="identifier",
            api_path="identifier",
            default=0,
        ),
        FieldMapping(
            cache_attr="network_context_id",
            api_path="network_context_id",
            default=0,
        ),
        FieldMapping(
            cache_attr="node.name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
            api_path="node.uuid",
        ),
        FieldMapping(
            cache_attr="server_ip",
            api_path="server_ip",
        ),
        FieldMapping(
            cache_attr="sessions",
            api_path="sessions",
            cache_strategy="realtime",
            transform=_transform_sessions,
            default=[],
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapCifsConnection", ONTAPCIFSCONNECTION_MAPPING)
