"""OntapMetroclusterDiagnostics information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapMetroclusterDiagnosticsDetail(OntapModel):
    """OntapMetroclusterDiagnosticsDetail sub-model for details."""

    aggregate_name: str = ""
    aggregate_uuid: str = ""
    checks: list[dict[str, Any]] = Field(default_factory=list)
    cluster_name: str = ""
    cluster_uuid: OntapUUID = ""
    node_name: str = ""
    node_uuid: str = ""
    timestamp: str = ""
    volume_name: str = ""
    volume_uuid: str = ""


class OntapMetroclusterDiagnosticsDetail2(OntapModel):
    """OntapMetroclusterDiagnosticsDetail2 sub-model for details."""

    aggregate_name: str = ""
    aggregate_uuid: str = ""
    checks: list[dict[str, Any]] = Field(default_factory=list)
    cluster_name: str = ""
    cluster_uuid: OntapUUID = ""
    node_name: str = ""
    node_uuid: str = ""
    timestamp: str = ""
    volume_name: str = ""
    volume_uuid: str = ""


class OntapMetroclusterDiagnosticsDetail3(OntapModel):
    """OntapMetroclusterDiagnosticsDetail3 sub-model for details."""

    cluster_name: str = ""
    cluster_uuid: OntapUUID = ""
    connections: list[dict[str, Any]] = Field(default_factory=list)
    node_name: str = ""
    node_uuid: str = ""


class OntapMetroclusterDiagnosticsDetail4(OntapModel):
    """OntapMetroclusterDiagnosticsDetail4 sub-model for details."""

    aggregate_name: str = ""
    aggregate_uuid: str = ""
    checks: list[dict[str, Any]] = Field(default_factory=list)
    cluster_name: str = ""
    cluster_uuid: OntapUUID = ""
    node_name: str = ""
    node_uuid: str = ""
    timestamp: str = ""
    volume_name: str = ""
    volume_uuid: str = ""


class OntapMetroclusterDiagnosticsDetail5(OntapModel):
    """OntapMetroclusterDiagnosticsDetail5 sub-model for details."""

    aggregate_name: str = ""
    aggregate_uuid: str = ""
    checks: list[dict[str, Any]] = Field(default_factory=list)
    cluster_name: str = ""
    cluster_uuid: OntapUUID = ""
    node_name: str = ""
    node_uuid: str = ""
    timestamp: str = ""
    volume_name: str = ""
    volume_uuid: str = ""


class OntapMetroclusterDiagnostics(OntapModel):
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
