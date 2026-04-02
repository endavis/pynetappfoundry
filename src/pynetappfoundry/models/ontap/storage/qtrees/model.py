"""OntapQtree information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapQtreeExportPolicy(OntapModel):
    """OntapQtreeExportPolicy sub-model for export_policy."""

    id: int = 0
    name: str = ""


class OntapQtreeExtPerformanceMonitoring(OntapModel):
    """OntapQtreeExtPerformanceMonitoring sub-model for ext_performance_monitoring."""

    enabled: bool = False


class OntapQtreeGroup(OntapModel):
    """OntapQtreeGroup sub-model for group."""

    id: str = ""
    name: str = ""


class OntapQtreeMetricIops(OntapModel):
    """OntapQtreeMetricIops sub-model for iops."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapQtreeMetricLatency(OntapModel):
    """OntapQtreeMetricLatency sub-model for latency."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapQtreeMetricThroughput(OntapModel):
    """OntapQtreeMetricThroughput sub-model for throughput."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapQtreeMetric(OntapModel):
    """OntapQtreeMetric sub-model for metric."""

    duration: str = ""
    iops: OntapQtreeMetricIops = Field(default_factory=OntapQtreeMetricIops)
    latency: OntapQtreeMetricLatency = Field(default_factory=OntapQtreeMetricLatency)
    status: str = ""
    throughput: OntapQtreeMetricThroughput = Field(default_factory=OntapQtreeMetricThroughput)
    timestamp: str = ""


class OntapQtreeNas(OntapModel):
    """OntapQtreeNas sub-model for nas."""

    path: str = ""


class OntapQtreeQosPolicy(OntapModel):
    """OntapQtreeQosPolicy sub-model for qos_policy."""

    max_throughput_iops: int = 0
    max_throughput_mbps: int = 0
    min_throughput_iops: int = 0
    min_throughput_mbps: int = 0
    name: str = ""
    uuid: str = ""


class OntapQtreeStatisticsIopsRaw(OntapModel):
    """OntapQtreeStatisticsIopsRaw sub-model for iops_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapQtreeStatisticsLatencyRaw(OntapModel):
    """OntapQtreeStatisticsLatencyRaw sub-model for latency_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapQtreeStatisticsThroughputRaw(OntapModel):
    """OntapQtreeStatisticsThroughputRaw sub-model for throughput_raw."""

    other: int = 0
    read: int = 0
    total: int = 0
    write: int = 0


class OntapQtreeStatistics(OntapModel):
    """OntapQtreeStatistics sub-model for statistics."""

    iops_raw: OntapQtreeStatisticsIopsRaw = Field(default_factory=OntapQtreeStatisticsIopsRaw)
    latency_raw: OntapQtreeStatisticsLatencyRaw = Field(
        default_factory=OntapQtreeStatisticsLatencyRaw
    )
    status: str = ""
    throughput_raw: OntapQtreeStatisticsThroughputRaw = Field(
        default_factory=OntapQtreeStatisticsThroughputRaw
    )
    timestamp: str = ""


class OntapQtreeSvm(OntapModel):
    """OntapQtreeSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapQtreeUser(OntapModel):
    """OntapQtreeUser sub-model for user."""

    id: str = ""
    name: str = ""


class OntapQtreeVolume(OntapModel):
    """OntapQtreeVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapQtree(OntapModel):
    """OntapQtree information."""

    export_policy: OntapQtreeExportPolicy = Field(default_factory=OntapQtreeExportPolicy)
    ext_performance_monitoring: OntapQtreeExtPerformanceMonitoring = Field(
        default_factory=OntapQtreeExtPerformanceMonitoring
    )
    group: OntapQtreeGroup = Field(default_factory=OntapQtreeGroup)
    id: int = 0
    metric: OntapQtreeMetric = Field(default_factory=OntapQtreeMetric)
    name: str = ""
    nas: OntapQtreeNas = Field(default_factory=OntapQtreeNas)
    path: str = ""
    qos_policy: OntapQtreeQosPolicy = Field(default_factory=OntapQtreeQosPolicy)
    security_style: str = ""
    statistics: OntapQtreeStatistics = Field(default_factory=OntapQtreeStatistics)
    svm: OntapQtreeSvm = Field(default_factory=OntapQtreeSvm)
    unix_permissions: int = 0
    user: OntapQtreeUser = Field(default_factory=OntapQtreeUser)
    volume: OntapQtreeVolume = Field(default_factory=OntapQtreeVolume)
