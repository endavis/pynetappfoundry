"""OntapFcInterface information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapFcInterface(OntapModel):
    """OntapFcInterface information."""

    comment: str = ""
    data_protocol: str = ""
    enabled: bool = False
    location_home_node_name: str = ""
    location_home_node_uuid: str = ""
    location_home_port_name: str = ""
    location_home_port_node_name: str = ""
    location_home_port_uuid: str = ""
    location_is_home: bool = False
    location_node_name: str = ""
    location_node_uuid: str = ""
    location_port_name: str = ""
    location_port_node_name: str = ""
    location_port_uuid: str = ""
    metric_duration: str = ""
    metric_iops_other: int = 0
    metric_iops_read: int = 0
    metric_iops_total: int = 0
    metric_iops_write: int = 0
    metric_latency_other: int = 0
    metric_latency_read: int = 0
    metric_latency_total: int = 0
    metric_latency_write: int = 0
    metric_status: str = ""
    metric_throughput_read: int = 0
    metric_throughput_total: int = 0
    metric_throughput_write: int = 0
    metric_timestamp: str = ""
    name: str = ""
    port_address: str = ""
    state: str = ""
    statistics_iops_raw_other: int = 0
    statistics_iops_raw_read: int = 0
    statistics_iops_raw_total: int = 0
    statistics_iops_raw_write: int = 0
    statistics_latency_raw_other: int = 0
    statistics_latency_raw_read: int = 0
    statistics_latency_raw_total: int = 0
    statistics_latency_raw_write: int = 0
    statistics_status: str = ""
    statistics_throughput_raw_read: int = 0
    statistics_throughput_raw_total: int = 0
    statistics_throughput_raw_write: int = 0
    statistics_timestamp: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
    wwnn: str = ""
    wwpn: str = ""
