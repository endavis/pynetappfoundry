"""OntapKeyServer type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.key_managers.key_servers.model import (
    OntapKeyServer,
    OntapKeyServerConnectivityNodeState,
    OntapKeyServerRecord,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_connectivity_node_states(
    record: dict[str, Any],
) -> list[OntapKeyServerConnectivityNodeState]:
    """Transform connectivity.node_states into OntapKeyServerConnectivityNodeState list."""
    try:
        items = get_nested_value(record, "connectivity.node_states")
    except Exception:
        items = []
    return [OntapKeyServerConnectivityNodeState(**item) for item in items]


def _transform_records(record: dict[str, Any]) -> list[OntapKeyServerRecord]:
    """Transform records into OntapKeyServerRecord list."""
    return [OntapKeyServerRecord(**item) for item in record.get("records", [])]


ONTAPKEYSERVER_MAPPING = TypeMapping(
    name="OntapKeyServer",
    model_class=OntapKeyServer,
    api_endpoint="/security/key-managers/{uuid}/key-servers?fields=*",
    api_type="ontap",
    parent_mapping="OntapSecurityKeyManager",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="connectivity.cluster_availability",
            default=False,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="connectivity.node_states",
            transform=_transform_connectivity_node_states,
            default=[],
        ),
        FieldMapping(
            cache_attr="create_remove_timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="password",
        ),
        FieldMapping(
            cache_attr="records",
            transform=_transform_records,
            default=[],
        ),
        FieldMapping(
            cache_attr="secondary_key_servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="server",
        ),
        FieldMapping(
            cache_attr="timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="username",
        ),
    ),
)

model_registry.register_mapping("OntapKeyServer", ONTAPKEYSERVER_MAPPING)
