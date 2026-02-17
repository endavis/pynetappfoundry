"""OntapMetroclusterDiagnostics type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.cluster.metrocluster.diagnostics.model import (
    OntapMetroclusterDiagnostics,
    OntapMetroclusterDiagnosticsDetail,
    OntapMetroclusterDiagnosticsDetail2,
    OntapMetroclusterDiagnosticsDetail3,
    OntapMetroclusterDiagnosticsDetail4,
    OntapMetroclusterDiagnosticsDetail5,
)
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping


def _transform_aggregate_details(
    record: dict[str, Any],
) -> list[OntapMetroclusterDiagnosticsDetail]:
    """Transform aggregate.details into OntapMetroclusterDiagnosticsDetail list."""
    return [
        OntapMetroclusterDiagnosticsDetail(**item) for item in record.get("aggregate.details", [])
    ]


def _transform_cluster_details(record: dict[str, Any]) -> list[OntapMetroclusterDiagnosticsDetail2]:
    """Transform cluster.details into OntapMetroclusterDiagnosticsDetail2 list."""
    return [
        OntapMetroclusterDiagnosticsDetail2(**item) for item in record.get("cluster.details", [])
    ]


def _transform_connection_details(
    record: dict[str, Any],
) -> list[OntapMetroclusterDiagnosticsDetail3]:
    """Transform connection.details into OntapMetroclusterDiagnosticsDetail3 list."""
    return [
        OntapMetroclusterDiagnosticsDetail3(**item) for item in record.get("connection.details", [])
    ]


def _transform_node_details(record: dict[str, Any]) -> list[OntapMetroclusterDiagnosticsDetail4]:
    """Transform node.details into OntapMetroclusterDiagnosticsDetail4 list."""
    return [OntapMetroclusterDiagnosticsDetail4(**item) for item in record.get("node.details", [])]


def _transform_volume_details(record: dict[str, Any]) -> list[OntapMetroclusterDiagnosticsDetail5]:
    """Transform volume.details into OntapMetroclusterDiagnosticsDetail5 list."""
    return [
        OntapMetroclusterDiagnosticsDetail5(**item) for item in record.get("volume.details", [])
    ]


ONTAPMETROCLUSTERDIAGNOSTICS_MAPPING = TypeMapping(
    name="OntapMetroclusterDiagnostics",
    model_class=OntapMetroclusterDiagnostics,
    api_endpoint="/cluster/metrocluster/diagnostics?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="aggregate_details",
            transform=_transform_aggregate_details,
            default=[],
        ),
        FieldMapping(
            cache_attr="aggregate_state",
            api_path="aggregate.state",
        ),
        FieldMapping(
            cache_attr="aggregate_summary_code",
            api_path="aggregate.summary.code",
        ),
        FieldMapping(
            cache_attr="aggregate_summary_message",
            api_path="aggregate.summary.message",
        ),
        FieldMapping(
            cache_attr="aggregate_timestamp",
            api_path="aggregate.timestamp",
        ),
        FieldMapping(
            cache_attr="cluster_details",
            transform=_transform_cluster_details,
            default=[],
        ),
        FieldMapping(
            cache_attr="cluster_state",
            api_path="cluster.state",
        ),
        FieldMapping(
            cache_attr="cluster_summary_code",
            api_path="cluster.summary.code",
        ),
        FieldMapping(
            cache_attr="cluster_summary_message",
            api_path="cluster.summary.message",
        ),
        FieldMapping(
            cache_attr="cluster_timestamp",
            api_path="cluster.timestamp",
        ),
        FieldMapping(
            cache_attr="config_replication_state",
            api_path="config-replication.state",
        ),
        FieldMapping(
            cache_attr="config_replication_summary_code",
            api_path="config-replication.summary.code",
        ),
        FieldMapping(
            cache_attr="config_replication_summary_message",
            api_path="config-replication.summary.message",
        ),
        FieldMapping(
            cache_attr="config_replication_timestamp",
            api_path="config-replication.timestamp",
        ),
        FieldMapping(
            cache_attr="connection_details",
            transform=_transform_connection_details,
            default=[],
        ),
        FieldMapping(
            cache_attr="connection_state",
            api_path="connection.state",
        ),
        FieldMapping(
            cache_attr="connection_summary_code",
            api_path="connection.summary.code",
        ),
        FieldMapping(
            cache_attr="connection_summary_message",
            api_path="connection.summary.message",
        ),
        FieldMapping(
            cache_attr="connection_timestamp",
            api_path="connection.timestamp",
        ),
        FieldMapping(
            cache_attr="interface_state",
            api_path="interface.state",
        ),
        FieldMapping(
            cache_attr="interface_summary_code",
            api_path="interface.summary.code",
        ),
        FieldMapping(
            cache_attr="interface_summary_message",
            api_path="interface.summary.message",
        ),
        FieldMapping(
            cache_attr="interface_timestamp",
            api_path="interface.timestamp",
        ),
        FieldMapping(
            cache_attr="node_details",
            transform=_transform_node_details,
            default=[],
        ),
        FieldMapping(
            cache_attr="node_state",
            api_path="node.state",
        ),
        FieldMapping(
            cache_attr="node_summary_code",
            api_path="node.summary.code",
        ),
        FieldMapping(
            cache_attr="node_summary_message",
            api_path="node.summary.message",
        ),
        FieldMapping(
            cache_attr="node_timestamp",
            api_path="node.timestamp",
        ),
        FieldMapping(
            cache_attr="volume_details",
            transform=_transform_volume_details,
            default=[],
        ),
        FieldMapping(
            cache_attr="volume_state",
            api_path="volume.state",
        ),
        FieldMapping(
            cache_attr="volume_summary_code",
            api_path="volume.summary.code",
        ),
        FieldMapping(
            cache_attr="volume_summary_message",
            api_path="volume.summary.message",
        ),
        FieldMapping(
            cache_attr="volume_timestamp",
            api_path="volume.timestamp",
        ),
    ),
)

model_registry.register_mapping(
    "OntapMetroclusterDiagnostics", ONTAPMETROCLUSTERDIAGNOSTICS_MAPPING
)
