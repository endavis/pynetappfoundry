"""OntapMetroclusterDiagnostics type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.metrocluster.diagnostics.model import (
    OntapMetroclusterDiagnostics,
    OntapMetroclusterDiagnosticsAggregateDetail,
    OntapMetroclusterDiagnosticsClusterDetail,
    OntapMetroclusterDiagnosticsConnectionDetail,
    OntapMetroclusterDiagnosticsNodeDetail,
    OntapMetroclusterDiagnosticsVolumeDetail,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_aggregate_details(
    record: dict[str, Any],
) -> list[OntapMetroclusterDiagnosticsAggregateDetail]:
    """Transform aggregate.details into OntapMetroclusterDiagnosticsAggregateDetail list."""
    try:
        items = get_nested_value(record, "aggregate.details")
    except Exception:
        items = []
    return [OntapMetroclusterDiagnosticsAggregateDetail(**item) for item in items]


def _transform_cluster_details(
    record: dict[str, Any],
) -> list[OntapMetroclusterDiagnosticsClusterDetail]:
    """Transform cluster.details into OntapMetroclusterDiagnosticsClusterDetail list."""
    try:
        items = get_nested_value(record, "cluster.details")
    except Exception:
        items = []
    return [OntapMetroclusterDiagnosticsClusterDetail(**item) for item in items]


def _transform_connection_details(
    record: dict[str, Any],
) -> list[OntapMetroclusterDiagnosticsConnectionDetail]:
    """Transform connection.details into OntapMetroclusterDiagnosticsConnectionDetail list."""
    try:
        items = get_nested_value(record, "connection.details")
    except Exception:
        items = []
    return [OntapMetroclusterDiagnosticsConnectionDetail(**item) for item in items]


def _transform_node_details(record: dict[str, Any]) -> list[OntapMetroclusterDiagnosticsNodeDetail]:
    """Transform node.details into OntapMetroclusterDiagnosticsNodeDetail list."""
    try:
        items = get_nested_value(record, "node.details")
    except Exception:
        items = []
    return [OntapMetroclusterDiagnosticsNodeDetail(**item) for item in items]


def _transform_volume_details(
    record: dict[str, Any],
) -> list[OntapMetroclusterDiagnosticsVolumeDetail]:
    """Transform volume.details into OntapMetroclusterDiagnosticsVolumeDetail list."""
    try:
        items = get_nested_value(record, "volume.details")
    except Exception:
        items = []
    return [OntapMetroclusterDiagnosticsVolumeDetail(**item) for item in items]


ONTAPMETROCLUSTERDIAGNOSTICS_MAPPING = TypeMapping(
    name="OntapMetroclusterDiagnostics",
    model_class=OntapMetroclusterDiagnostics,
    api_endpoint="/cluster/metrocluster/diagnostics?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="aggregate.details",
            transform=_transform_aggregate_details,
            default=[],
        ),
        FieldMapping(
            cache_attr="aggregate.state",
        ),
        FieldMapping(
            cache_attr="aggregate.summary.code",
        ),
        FieldMapping(
            cache_attr="aggregate.summary.message",
        ),
        FieldMapping(
            cache_attr="aggregate.timestamp",
        ),
        FieldMapping(
            cache_attr="cluster.details",
            transform=_transform_cluster_details,
            default=[],
        ),
        FieldMapping(
            cache_attr="cluster.state",
        ),
        FieldMapping(
            cache_attr="cluster.summary.code",
        ),
        FieldMapping(
            cache_attr="cluster.summary.message",
        ),
        FieldMapping(
            cache_attr="cluster.timestamp",
        ),
        FieldMapping(
            cache_attr="config_replication.state",
            api_path="config-replication.state",
        ),
        FieldMapping(
            cache_attr="config_replication.summary.code",
            api_path="config-replication.summary.code",
        ),
        FieldMapping(
            cache_attr="config_replication.summary.message",
            api_path="config-replication.summary.message",
        ),
        FieldMapping(
            cache_attr="config_replication.timestamp",
            api_path="config-replication.timestamp",
        ),
        FieldMapping(
            cache_attr="connection.details",
            transform=_transform_connection_details,
            default=[],
        ),
        FieldMapping(
            cache_attr="connection.state",
        ),
        FieldMapping(
            cache_attr="connection.summary.code",
        ),
        FieldMapping(
            cache_attr="connection.summary.message",
        ),
        FieldMapping(
            cache_attr="connection.timestamp",
        ),
        FieldMapping(
            cache_attr="interface.state",
        ),
        FieldMapping(
            cache_attr="interface.summary.code",
        ),
        FieldMapping(
            cache_attr="interface.summary.message",
        ),
        FieldMapping(
            cache_attr="interface.timestamp",
        ),
        FieldMapping(
            cache_attr="node.details",
            transform=_transform_node_details,
            default=[],
        ),
        FieldMapping(
            cache_attr="node.state",
        ),
        FieldMapping(
            cache_attr="node.summary.code",
        ),
        FieldMapping(
            cache_attr="node.summary.message",
        ),
        FieldMapping(
            cache_attr="node.timestamp",
        ),
        FieldMapping(
            cache_attr="volume.details",
            transform=_transform_volume_details,
            default=[],
        ),
        FieldMapping(
            cache_attr="volume.state",
        ),
        FieldMapping(
            cache_attr="volume.summary.code",
        ),
        FieldMapping(
            cache_attr="volume.summary.message",
        ),
        FieldMapping(
            cache_attr="volume.timestamp",
        ),
    ),
)

model_registry.register_mapping(
    "OntapMetroclusterDiagnostics", ONTAPMETROCLUSTERDIAGNOSTICS_MAPPING
)
