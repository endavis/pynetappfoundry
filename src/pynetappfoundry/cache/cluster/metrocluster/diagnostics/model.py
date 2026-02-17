"""OntapMetroclusterDiagnostics information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel, OntapUUID


class OntapMetroclusterDiagnosticsDetail(CacheModel):
    """OntapMetroclusterDiagnosticsDetail sub-model for details."""

    aggregate_details_aggregate_name: str = ""
    aggregate_details_aggregate_uuid: str = ""
    aggregate_details_checks: list[dict[str, Any]] = Field(default_factory=list)
    aggregate_details_cluster_name: str = ""
    aggregate_details_cluster_uuid: OntapUUID = ""
    aggregate_details_node_name: str = ""
    aggregate_details_node_uuid: str = ""
    aggregate_details_timestamp: str = ""
    aggregate_details_volume_name: str = ""
    aggregate_details_volume_uuid: str = ""


class OntapMetroclusterDiagnosticsDetail2(CacheModel):
    """OntapMetroclusterDiagnosticsDetail2 sub-model for details."""

    cluster_details_aggregate_name: str = ""
    cluster_details_aggregate_uuid: str = ""
    cluster_details_checks: list[dict[str, Any]] = Field(default_factory=list)
    cluster_details_cluster_name: str = ""
    cluster_details_cluster_uuid: OntapUUID = ""
    cluster_details_node_name: str = ""
    cluster_details_node_uuid: str = ""
    cluster_details_timestamp: str = ""
    cluster_details_volume_name: str = ""
    cluster_details_volume_uuid: str = ""


class OntapMetroclusterDiagnosticsDetail3(CacheModel):
    """OntapMetroclusterDiagnosticsDetail3 sub-model for details."""

    connection_details_cluster_name: str = ""
    connection_details_cluster_uuid: OntapUUID = ""
    connection_details_connections: list[dict[str, Any]] = Field(default_factory=list)
    connection_details_node_name: str = ""
    connection_details_node_uuid: str = ""


class OntapMetroclusterDiagnosticsDetail4(CacheModel):
    """OntapMetroclusterDiagnosticsDetail4 sub-model for details."""

    node_details_aggregate_name: str = ""
    node_details_aggregate_uuid: str = ""
    node_details_checks: list[dict[str, Any]] = Field(default_factory=list)
    node_details_cluster_name: str = ""
    node_details_cluster_uuid: OntapUUID = ""
    node_details_node_name: str = ""
    node_details_node_uuid: str = ""
    node_details_timestamp: str = ""
    node_details_volume_name: str = ""
    node_details_volume_uuid: str = ""


class OntapMetroclusterDiagnosticsDetail5(CacheModel):
    """OntapMetroclusterDiagnosticsDetail5 sub-model for details."""

    volume_details_aggregate_name: str = ""
    volume_details_aggregate_uuid: str = ""
    volume_details_checks: list[dict[str, Any]] = Field(default_factory=list)
    volume_details_cluster_name: str = ""
    volume_details_cluster_uuid: OntapUUID = ""
    volume_details_node_name: str = ""
    volume_details_node_uuid: str = ""
    volume_details_timestamp: str = ""
    volume_details_volume_name: str = ""
    volume_details_volume_uuid: str = ""


class OntapMetroclusterDiagnostics(CacheModel):
    """OntapMetroclusterDiagnostics information."""

    aggregate_details: list[OntapMetroclusterDiagnosticsDetail] = Field(default_factory=list)
    aggregate_state: str = ""
    aggregate_summary_code: str = ""
    aggregate_summary_message: str = ""
    aggregate_timestamp: str = ""
    cluster_details: list[OntapMetroclusterDiagnosticsDetail2] = Field(default_factory=list)
    cluster_state: str = ""
    cluster_summary_code: str = ""
    cluster_summary_message: str = ""
    cluster_timestamp: str = ""
    config_replication_state: str = ""
    config_replication_summary_code: str = ""
    config_replication_summary_message: str = ""
    config_replication_timestamp: str = ""
    connection_details: list[OntapMetroclusterDiagnosticsDetail3] = Field(default_factory=list)
    connection_state: str = ""
    connection_summary_code: str = ""
    connection_summary_message: str = ""
    connection_timestamp: str = ""
    interface_state: str = ""
    interface_summary_code: str = ""
    interface_summary_message: str = ""
    interface_timestamp: str = ""
    node_details: list[OntapMetroclusterDiagnosticsDetail4] = Field(default_factory=list)
    node_state: str = ""
    node_summary_code: str = ""
    node_summary_message: str = ""
    node_timestamp: str = ""
    volume_details: list[OntapMetroclusterDiagnosticsDetail5] = Field(default_factory=list)
    volume_state: str = ""
    volume_summary_code: str = ""
    volume_summary_message: str = ""
    volume_timestamp: str = ""
