"""OntapIgroupInitiator type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.san.igroups.initiators.model import (
    OntapIgroupInitiator,
    OntapIgroupInitiatorAlert,
    OntapIgroupInitiatorConnection,
    OntapIgroupInitiatorPeerSvm,
    OntapIgroupInitiatorRecord,
)


def _transform_connectivity_tracking_alerts(
    record: dict[str, Any],
) -> list[OntapIgroupInitiatorAlert]:
    """Transform connectivity_tracking.alerts into OntapIgroupInitiatorAlert list."""
    return [
        OntapIgroupInitiatorAlert(**item) for item in record.get("connectivity_tracking.alerts", [])
    ]


def _transform_connectivity_tracking_connections(
    record: dict[str, Any],
) -> list[OntapIgroupInitiatorConnection]:
    """Transform connectivity_tracking.connections into OntapIgroupInitiatorConnection list."""
    return [
        OntapIgroupInitiatorConnection(**item)
        for item in record.get("connectivity_tracking.connections", [])
    ]


def _transform_proximity_peer_svms(record: dict[str, Any]) -> list[OntapIgroupInitiatorPeerSvm]:
    """Transform proximity.peer_svms into OntapIgroupInitiatorPeerSvm list."""
    return [OntapIgroupInitiatorPeerSvm(**item) for item in record.get("proximity.peer_svms", [])]


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
            cache_attr="connectivity_tracking_alerts",
            transform=_transform_connectivity_tracking_alerts,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="connectivity_tracking_connection_state",
            api_path="connectivity_tracking.connection_state",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="connectivity_tracking_connections",
            transform=_transform_connectivity_tracking_connections,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="igroup_name",
            api_path="igroup.name",
        ),
        FieldMapping(
            cache_attr="igroup_uuid",
            api_path="igroup.uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="proximity_local_svm",
            api_path="proximity.local_svm",
            default=False,
        ),
        FieldMapping(
            cache_attr="proximity_peer_svms",
            transform=_transform_proximity_peer_svms,
            default=[],
        ),
        FieldMapping(
            cache_attr="records",
            transform=_transform_records,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapIgroupInitiator", ONTAPIGROUPINITIATOR_MAPPING)
