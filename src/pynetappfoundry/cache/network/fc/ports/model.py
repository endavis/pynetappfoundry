"""OntapFcPort information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapFcPort(CacheModel):
    """OntapFcPort information."""

    description: str = ""
    enabled: bool = False
    fabric_connected: bool = False
    fabric_connected_speed: int = 0
    fabric_name: str = ""
    fabric_port_address: str = ""
    fabric_switch_port: str = ""
    interface_count: int = 0
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
    node_name: str = ""
    node_uuid: str = ""
    physical_protocol: str = ""
    speed_configured: str = ""
    speed_maximum: str = ""
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
    supported_protocols: list[str] = Field(default_factory=list)
    transceiver_capabilities: list[int] = Field(default_factory=list)
    transceiver_form_factor: str = ""
    transceiver_manufacturer: str = ""
    transceiver_part_number: str = ""
    uuid: str = ""
    wwnn: str = ""
    wwpn: str = ""
