# ruff: noqa: E501
"""OntapIgroupInitiator type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.igroups.initiators.model import (
    OntapIgroupInitiator,
    OntapIgroupInitiatorConnectivityTrackingConnection,
    OntapIgroupInitiatorProximityPeerSvm,
    OntapIgroupInitiatorRecord,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_connectivity_tracking_connections(
    record: dict[str, Any],
) -> list[OntapIgroupInitiatorConnectivityTrackingConnection]:
    """Transform connectivity_tracking.connections into OntapIgroupInitiatorConnectivityTrackingConnection list."""
    try:
        items = get_nested_value(record, "connectivity_tracking.connections")
    except Exception:
        items = []
    return [OntapIgroupInitiatorConnectivityTrackingConnection(**item) for item in items]


def _transform_proximity_peer_svms(
    record: dict[str, Any],
) -> list[OntapIgroupInitiatorProximityPeerSvm]:
    """Transform proximity.peer_svms into OntapIgroupInitiatorProximityPeerSvm list."""
    try:
        items = get_nested_value(record, "proximity.peer_svms")
    except Exception:
        items = []
    return [OntapIgroupInitiatorProximityPeerSvm(**item) for item in items]


def _transform_records(record: dict[str, Any]) -> list[OntapIgroupInitiatorRecord]:
    """Transform records into OntapIgroupInitiatorRecord list."""
    return [OntapIgroupInitiatorRecord(**item) for item in record.get("records", [])]


ONTAPIGROUPINITIATOR_MAPPING = TypeMapping(
    name="OntapIgroupInitiator",
    model_class=OntapIgroupInitiator,
    api_endpoint="/protocols/san/igroups/{igroup.uuid}/initiators?fields=*",
    api_type="ontap",
    parent_mapping="OntapIgroup",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="connectivity_tracking.alerts",
            api_path="connectivity_tracking.alerts",
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="connectivity_tracking.connection_state",
            api_path="connectivity_tracking.connection_state",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="connectivity_tracking.connections",
            api_path="connectivity_tracking.connections",
            transform=_transform_connectivity_tracking_connections,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="igroup.name",
            api_path="igroup.name",
        ),
        FieldMapping(
            cache_attr="igroup.uuid",
            api_path="igroup.uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="proximity.local_svm",
            api_path="proximity.local_svm",
            default=False,
        ),
        FieldMapping(
            cache_attr="proximity.peer_svms",
            api_path="proximity.peer_svms",
            transform=_transform_proximity_peer_svms,
            default=[],
        ),
        FieldMapping(
            cache_attr="records",
            api_path="records",
            transform=_transform_records,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapIgroupInitiator", ONTAPIGROUPINITIATOR_MAPPING)
