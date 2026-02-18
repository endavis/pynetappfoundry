"""OntapKeyServer type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.security.key_managers.key_servers.model import (
    OntapKeyServer,
    OntapKeyServerNodeState,
    OntapKeyServerRecord,
)


def _transform_connectivity_node_states(record: dict[str, Any]) -> list[OntapKeyServerNodeState]:
    """Transform connectivity.node_states into OntapKeyServerNodeState list."""
    return [OntapKeyServerNodeState(**item) for item in record.get("connectivity.node_states", [])]


def _transform_records(record: dict[str, Any]) -> list[OntapKeyServerRecord]:
    """Transform records into OntapKeyServerRecord list."""
    return [OntapKeyServerRecord(**item) for item in record.get("records", [])]


ONTAPKEYSERVER_MAPPING = TypeMapping(
    name="OntapKeyServer",
    model_class=OntapKeyServer,
    api_endpoint="/security/key-managers/{uuid}/key-servers?fields=*,connectivity",
    api_type="ontap",
    parent_mapping="OntapSecurityKeyManager",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="connectivity_cluster_availability",
            api_path="connectivity.cluster_availability",
            default=False,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="connectivity_node_states",
            transform=_transform_connectivity_node_states,
            default=[],
        ),
        FieldMapping(
            cache_attr="create_remove_timeout",
            api_path="create_remove_timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="password",
            api_path="password",
        ),
        FieldMapping(
            cache_attr="records",
            transform=_transform_records,
            default=[],
        ),
        FieldMapping(
            cache_attr="secondary_key_servers",
            api_path="secondary_key_servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="server",
            api_path="server",
        ),
        FieldMapping(
            cache_attr="timeout",
            api_path="timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="username",
            api_path="username",
        ),
    ),
)

model_registry.register_mapping("OntapKeyServer", ONTAPKEYSERVER_MAPPING)
