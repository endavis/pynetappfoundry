# ruff: noqa: E501
"""OntapMetroclusterDiagnostics information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapMetroclusterDiagnosticsAggregateDetailAggregate(OntapModel):
    """OntapMetroclusterDiagnosticsAggregateDetailAggregate sub-model for aggregate."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterDiagnosticsAggregateDetailCheckAdditionalInfo(OntapModel):
    """OntapMetroclusterDiagnosticsAggregateDetailCheckAdditionalInfo sub-model for additional_info."""

    code: str = ""
    message: str = ""


class OntapMetroclusterDiagnosticsAggregateDetailCheck(OntapModel):
    """OntapMetroclusterDiagnosticsAggregateDetailCheck sub-model for checks."""

    additional_info: OntapMetroclusterDiagnosticsAggregateDetailCheckAdditionalInfo = Field(
        default_factory=OntapMetroclusterDiagnosticsAggregateDetailCheckAdditionalInfo
    )
    name: str = ""
    result: str = ""


class OntapMetroclusterDiagnosticsAggregateDetailCluster(OntapModel):
    """OntapMetroclusterDiagnosticsAggregateDetailCluster sub-model for cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapMetroclusterDiagnosticsAggregateDetailNode(OntapModel):
    """OntapMetroclusterDiagnosticsAggregateDetailNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterDiagnosticsAggregateDetailVolume(OntapModel):
    """OntapMetroclusterDiagnosticsAggregateDetailVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterDiagnosticsAggregateDetail(OntapModel):
    """OntapMetroclusterDiagnosticsAggregateDetail sub-model for details."""

    aggregate: OntapMetroclusterDiagnosticsAggregateDetailAggregate = Field(
        default_factory=OntapMetroclusterDiagnosticsAggregateDetailAggregate
    )
    checks: list[OntapMetroclusterDiagnosticsAggregateDetailCheck] = Field(default_factory=list)
    cluster: OntapMetroclusterDiagnosticsAggregateDetailCluster = Field(
        default_factory=OntapMetroclusterDiagnosticsAggregateDetailCluster
    )
    node: OntapMetroclusterDiagnosticsAggregateDetailNode = Field(
        default_factory=OntapMetroclusterDiagnosticsAggregateDetailNode
    )
    timestamp: str = ""
    volume: OntapMetroclusterDiagnosticsAggregateDetailVolume = Field(
        default_factory=OntapMetroclusterDiagnosticsAggregateDetailVolume
    )


class OntapMetroclusterDiagnosticsAggregateSummary(OntapModel):
    """OntapMetroclusterDiagnosticsAggregateSummary sub-model for summary."""

    code: str = ""
    message: str = ""


class OntapMetroclusterDiagnosticsAggregate(OntapModel):
    """OntapMetroclusterDiagnosticsAggregate sub-model for aggregate."""

    details: list[OntapMetroclusterDiagnosticsAggregateDetail] = Field(default_factory=list)
    state: str = ""
    summary: OntapMetroclusterDiagnosticsAggregateSummary = Field(
        default_factory=OntapMetroclusterDiagnosticsAggregateSummary
    )
    timestamp: str = ""


class OntapMetroclusterDiagnosticsClusterDetailAggregate(OntapModel):
    """OntapMetroclusterDiagnosticsClusterDetailAggregate sub-model for aggregate."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterDiagnosticsClusterDetailCheckAdditionalInfo(OntapModel):
    """OntapMetroclusterDiagnosticsClusterDetailCheckAdditionalInfo sub-model for additional_info."""

    code: str = ""
    message: str = ""


class OntapMetroclusterDiagnosticsClusterDetailCheck(OntapModel):
    """OntapMetroclusterDiagnosticsClusterDetailCheck sub-model for checks."""

    additional_info: OntapMetroclusterDiagnosticsClusterDetailCheckAdditionalInfo = Field(
        default_factory=OntapMetroclusterDiagnosticsClusterDetailCheckAdditionalInfo
    )
    name: str = ""
    result: str = ""


class OntapMetroclusterDiagnosticsClusterDetailCluster(OntapModel):
    """OntapMetroclusterDiagnosticsClusterDetailCluster sub-model for cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapMetroclusterDiagnosticsClusterDetailNode(OntapModel):
    """OntapMetroclusterDiagnosticsClusterDetailNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterDiagnosticsClusterDetailVolume(OntapModel):
    """OntapMetroclusterDiagnosticsClusterDetailVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterDiagnosticsClusterDetail(OntapModel):
    """OntapMetroclusterDiagnosticsClusterDetail sub-model for details."""

    aggregate: OntapMetroclusterDiagnosticsClusterDetailAggregate = Field(
        default_factory=OntapMetroclusterDiagnosticsClusterDetailAggregate
    )
    checks: list[OntapMetroclusterDiagnosticsClusterDetailCheck] = Field(default_factory=list)
    cluster: OntapMetroclusterDiagnosticsClusterDetailCluster = Field(
        default_factory=OntapMetroclusterDiagnosticsClusterDetailCluster
    )
    node: OntapMetroclusterDiagnosticsClusterDetailNode = Field(
        default_factory=OntapMetroclusterDiagnosticsClusterDetailNode
    )
    timestamp: str = ""
    volume: OntapMetroclusterDiagnosticsClusterDetailVolume = Field(
        default_factory=OntapMetroclusterDiagnosticsClusterDetailVolume
    )


class OntapMetroclusterDiagnosticsClusterSummary(OntapModel):
    """OntapMetroclusterDiagnosticsClusterSummary sub-model for summary."""

    code: str = ""
    message: str = ""


class OntapMetroclusterDiagnosticsCluster(OntapModel):
    """OntapMetroclusterDiagnosticsCluster sub-model for cluster."""

    details: list[OntapMetroclusterDiagnosticsClusterDetail] = Field(default_factory=list)
    state: str = ""
    summary: OntapMetroclusterDiagnosticsClusterSummary = Field(
        default_factory=OntapMetroclusterDiagnosticsClusterSummary
    )
    timestamp: str = ""


class OntapMetroclusterDiagnosticsConfigReplicationSummary(OntapModel):
    """OntapMetroclusterDiagnosticsConfigReplicationSummary sub-model for summary."""

    code: str = ""
    message: str = ""


class OntapMetroclusterDiagnosticsConfigReplication(OntapModel):
    """OntapMetroclusterDiagnosticsConfigReplication sub-model for config-replication."""

    state: str = ""
    summary: OntapMetroclusterDiagnosticsConfigReplicationSummary = Field(
        default_factory=OntapMetroclusterDiagnosticsConfigReplicationSummary
    )
    timestamp: str = ""


class OntapMetroclusterDiagnosticsConnectionDetailCluster(OntapModel):
    """OntapMetroclusterDiagnosticsConnectionDetailCluster sub-model for cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapMetroclusterDiagnosticsConnectionDetailConnectionPartnerNode(OntapModel):
    """OntapMetroclusterDiagnosticsConnectionDetailConnectionPartnerNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterDiagnosticsConnectionDetailConnectionPartner(OntapModel):
    """OntapMetroclusterDiagnosticsConnectionDetailConnectionPartner sub-model for partner."""

    node: OntapMetroclusterDiagnosticsConnectionDetailConnectionPartnerNode = Field(
        default_factory=OntapMetroclusterDiagnosticsConnectionDetailConnectionPartnerNode
    )
    type_: str = ""


class OntapMetroclusterDiagnosticsConnectionDetailConnection(OntapModel):
    """OntapMetroclusterDiagnosticsConnectionDetailConnection sub-model for connections."""

    destination_address: str = ""
    partner: OntapMetroclusterDiagnosticsConnectionDetailConnectionPartner = Field(
        default_factory=OntapMetroclusterDiagnosticsConnectionDetailConnectionPartner
    )
    port: str = ""
    result: str = ""
    source_address: str = ""
    state: str = ""


class OntapMetroclusterDiagnosticsConnectionDetailNode(OntapModel):
    """OntapMetroclusterDiagnosticsConnectionDetailNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterDiagnosticsConnectionDetail(OntapModel):
    """OntapMetroclusterDiagnosticsConnectionDetail sub-model for details."""

    cluster: OntapMetroclusterDiagnosticsConnectionDetailCluster = Field(
        default_factory=OntapMetroclusterDiagnosticsConnectionDetailCluster
    )
    connections: list[OntapMetroclusterDiagnosticsConnectionDetailConnection] = Field(
        default_factory=list
    )
    node: OntapMetroclusterDiagnosticsConnectionDetailNode = Field(
        default_factory=OntapMetroclusterDiagnosticsConnectionDetailNode
    )


class OntapMetroclusterDiagnosticsConnectionSummary(OntapModel):
    """OntapMetroclusterDiagnosticsConnectionSummary sub-model for summary."""

    code: str = ""
    message: str = ""


class OntapMetroclusterDiagnosticsConnection(OntapModel):
    """OntapMetroclusterDiagnosticsConnection sub-model for connection."""

    details: list[OntapMetroclusterDiagnosticsConnectionDetail] = Field(default_factory=list)
    state: str = ""
    summary: OntapMetroclusterDiagnosticsConnectionSummary = Field(
        default_factory=OntapMetroclusterDiagnosticsConnectionSummary
    )
    timestamp: str = ""


class OntapMetroclusterDiagnosticsInterfaceSummary(OntapModel):
    """OntapMetroclusterDiagnosticsInterfaceSummary sub-model for summary."""

    code: str = ""
    message: str = ""


class OntapMetroclusterDiagnosticsInterface(OntapModel):
    """OntapMetroclusterDiagnosticsInterface sub-model for interface."""

    state: str = ""
    summary: OntapMetroclusterDiagnosticsInterfaceSummary = Field(
        default_factory=OntapMetroclusterDiagnosticsInterfaceSummary
    )
    timestamp: str = ""


class OntapMetroclusterDiagnosticsNodeDetailAggregate(OntapModel):
    """OntapMetroclusterDiagnosticsNodeDetailAggregate sub-model for aggregate."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterDiagnosticsNodeDetailCheckAdditionalInfo(OntapModel):
    """OntapMetroclusterDiagnosticsNodeDetailCheckAdditionalInfo sub-model for additional_info."""

    code: str = ""
    message: str = ""


class OntapMetroclusterDiagnosticsNodeDetailCheck(OntapModel):
    """OntapMetroclusterDiagnosticsNodeDetailCheck sub-model for checks."""

    additional_info: OntapMetroclusterDiagnosticsNodeDetailCheckAdditionalInfo = Field(
        default_factory=OntapMetroclusterDiagnosticsNodeDetailCheckAdditionalInfo
    )
    name: str = ""
    result: str = ""


class OntapMetroclusterDiagnosticsNodeDetailCluster(OntapModel):
    """OntapMetroclusterDiagnosticsNodeDetailCluster sub-model for cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapMetroclusterDiagnosticsNodeDetailNode(OntapModel):
    """OntapMetroclusterDiagnosticsNodeDetailNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterDiagnosticsNodeDetailVolume(OntapModel):
    """OntapMetroclusterDiagnosticsNodeDetailVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterDiagnosticsNodeDetail(OntapModel):
    """OntapMetroclusterDiagnosticsNodeDetail sub-model for details."""

    aggregate: OntapMetroclusterDiagnosticsNodeDetailAggregate = Field(
        default_factory=OntapMetroclusterDiagnosticsNodeDetailAggregate
    )
    checks: list[OntapMetroclusterDiagnosticsNodeDetailCheck] = Field(default_factory=list)
    cluster: OntapMetroclusterDiagnosticsNodeDetailCluster = Field(
        default_factory=OntapMetroclusterDiagnosticsNodeDetailCluster
    )
    node: OntapMetroclusterDiagnosticsNodeDetailNode = Field(
        default_factory=OntapMetroclusterDiagnosticsNodeDetailNode
    )
    timestamp: str = ""
    volume: OntapMetroclusterDiagnosticsNodeDetailVolume = Field(
        default_factory=OntapMetroclusterDiagnosticsNodeDetailVolume
    )


class OntapMetroclusterDiagnosticsNodeSummary(OntapModel):
    """OntapMetroclusterDiagnosticsNodeSummary sub-model for summary."""

    code: str = ""
    message: str = ""


class OntapMetroclusterDiagnosticsNode(OntapModel):
    """OntapMetroclusterDiagnosticsNode sub-model for node."""

    details: list[OntapMetroclusterDiagnosticsNodeDetail] = Field(default_factory=list)
    state: str = ""
    summary: OntapMetroclusterDiagnosticsNodeSummary = Field(
        default_factory=OntapMetroclusterDiagnosticsNodeSummary
    )
    timestamp: str = ""


class OntapMetroclusterDiagnosticsVolumeDetailAggregate(OntapModel):
    """OntapMetroclusterDiagnosticsVolumeDetailAggregate sub-model for aggregate."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterDiagnosticsVolumeDetailCheckAdditionalInfo(OntapModel):
    """OntapMetroclusterDiagnosticsVolumeDetailCheckAdditionalInfo sub-model for additional_info."""

    code: str = ""
    message: str = ""


class OntapMetroclusterDiagnosticsVolumeDetailCheck(OntapModel):
    """OntapMetroclusterDiagnosticsVolumeDetailCheck sub-model for checks."""

    additional_info: OntapMetroclusterDiagnosticsVolumeDetailCheckAdditionalInfo = Field(
        default_factory=OntapMetroclusterDiagnosticsVolumeDetailCheckAdditionalInfo
    )
    name: str = ""
    result: str = ""


class OntapMetroclusterDiagnosticsVolumeDetailCluster(OntapModel):
    """OntapMetroclusterDiagnosticsVolumeDetailCluster sub-model for cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapMetroclusterDiagnosticsVolumeDetailNode(OntapModel):
    """OntapMetroclusterDiagnosticsVolumeDetailNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterDiagnosticsVolumeDetailVolume(OntapModel):
    """OntapMetroclusterDiagnosticsVolumeDetailVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterDiagnosticsVolumeDetail(OntapModel):
    """OntapMetroclusterDiagnosticsVolumeDetail sub-model for details."""

    aggregate: OntapMetroclusterDiagnosticsVolumeDetailAggregate = Field(
        default_factory=OntapMetroclusterDiagnosticsVolumeDetailAggregate
    )
    checks: list[OntapMetroclusterDiagnosticsVolumeDetailCheck] = Field(default_factory=list)
    cluster: OntapMetroclusterDiagnosticsVolumeDetailCluster = Field(
        default_factory=OntapMetroclusterDiagnosticsVolumeDetailCluster
    )
    node: OntapMetroclusterDiagnosticsVolumeDetailNode = Field(
        default_factory=OntapMetroclusterDiagnosticsVolumeDetailNode
    )
    timestamp: str = ""
    volume: OntapMetroclusterDiagnosticsVolumeDetailVolume = Field(
        default_factory=OntapMetroclusterDiagnosticsVolumeDetailVolume
    )


class OntapMetroclusterDiagnosticsVolumeSummary(OntapModel):
    """OntapMetroclusterDiagnosticsVolumeSummary sub-model for summary."""

    code: str = ""
    message: str = ""


class OntapMetroclusterDiagnosticsVolume(OntapModel):
    """OntapMetroclusterDiagnosticsVolume sub-model for volume."""

    details: list[OntapMetroclusterDiagnosticsVolumeDetail] = Field(default_factory=list)
    state: str = ""
    summary: OntapMetroclusterDiagnosticsVolumeSummary = Field(
        default_factory=OntapMetroclusterDiagnosticsVolumeSummary
    )
    timestamp: str = ""


class OntapMetroclusterDiagnostics(OntapModel):
    """OntapMetroclusterDiagnostics information."""

    aggregate: OntapMetroclusterDiagnosticsAggregate = Field(
        default_factory=OntapMetroclusterDiagnosticsAggregate
    )
    cluster: OntapMetroclusterDiagnosticsCluster = Field(
        default_factory=OntapMetroclusterDiagnosticsCluster
    )
    config_replication: OntapMetroclusterDiagnosticsConfigReplication = Field(
        default_factory=OntapMetroclusterDiagnosticsConfigReplication
    )
    connection: OntapMetroclusterDiagnosticsConnection = Field(
        default_factory=OntapMetroclusterDiagnosticsConnection
    )
    interface: OntapMetroclusterDiagnosticsInterface = Field(
        default_factory=OntapMetroclusterDiagnosticsInterface
    )
    node: OntapMetroclusterDiagnosticsNode = Field(default_factory=OntapMetroclusterDiagnosticsNode)
    volume: OntapMetroclusterDiagnosticsVolume = Field(
        default_factory=OntapMetroclusterDiagnosticsVolume
    )
