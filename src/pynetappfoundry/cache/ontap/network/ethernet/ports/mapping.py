"""OntapPort type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.network.ethernet.ports.model import (
    OntapPort,
    OntapPortActivePort,
    OntapPortDiscoveredDevice,
    OntapPortMemberPort,
    OntapPortReachableBroadcastDomain,
)


def _transform_discovered_devices(record: dict[str, Any]) -> list[OntapPortDiscoveredDevice]:
    """Transform discovered_devices into OntapPortDiscoveredDevice list."""
    return [OntapPortDiscoveredDevice(**item) for item in record.get("discovered_devices", [])]


def _transform_lag_active_ports(record: dict[str, Any]) -> list[OntapPortActivePort]:
    """Transform lag.active_ports into OntapPortActivePort list."""
    return [OntapPortActivePort(**item) for item in record.get("lag.active_ports", [])]


def _transform_lag_member_ports(record: dict[str, Any]) -> list[OntapPortMemberPort]:
    """Transform lag.member_ports into OntapPortMemberPort list."""
    return [OntapPortMemberPort(**item) for item in record.get("lag.member_ports", [])]


def _transform_reachable_broadcast_domains(
    record: dict[str, Any],
) -> list[OntapPortReachableBroadcastDomain]:
    """Transform reachable_broadcast_domains into OntapPortReachableBroadcastDomain list."""
    return [
        OntapPortReachableBroadcastDomain(**item)
        for item in record.get("reachable_broadcast_domains", [])
    ]


ONTAPPORT_MAPPING = TypeMapping(
    name="OntapPort",
    model_class=OntapPort,
    api_endpoint="/network/ethernet/ports?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="broadcast_domain_ipspace_name",
            api_path="broadcast_domain.ipspace.name",
        ),
        FieldMapping(
            cache_attr="broadcast_domain_name",
            api_path="broadcast_domain.name",
        ),
        FieldMapping(
            cache_attr="broadcast_domain_uuid",
            api_path="broadcast_domain.uuid",
        ),
        FieldMapping(
            cache_attr="discovered_devices",
            api_path="discovered_devices",
            transform=_transform_discovered_devices,
            default=[],
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="flowcontrol_admin",
            api_path="flowcontrol_admin",
        ),
        FieldMapping(
            cache_attr="interface_count",
            api_path="interface_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="lag_active_ports",
            api_path="lag.active_ports",
            transform=_transform_lag_active_ports,
            default=[],
        ),
        FieldMapping(
            cache_attr="lag_distribution_policy",
            api_path="lag.distribution_policy",
        ),
        FieldMapping(
            cache_attr="lag_member_ports",
            api_path="lag.member_ports",
            transform=_transform_lag_member_ports,
            default=[],
        ),
        FieldMapping(
            cache_attr="lag_mode",
            api_path="lag.mode",
        ),
        FieldMapping(
            cache_attr="mac_address",
            api_path="mac_address",
        ),
        FieldMapping(
            cache_attr="metric_duration",
            api_path="metric.duration",
        ),
        FieldMapping(
            cache_attr="metric_status",
            api_path="metric.status",
        ),
        FieldMapping(
            cache_attr="metric_throughput_read",
            api_path="metric.throughput.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric_throughput_total",
            api_path="metric.throughput.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric_throughput_write",
            api_path="metric.throughput.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric_timestamp",
            api_path="metric.timestamp",
        ),
        FieldMapping(
            cache_attr="mtu",
            api_path="mtu",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="node_name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node_uuid",
            api_path="node.uuid",
        ),
        FieldMapping(
            cache_attr="pfc_queues_admin",
            api_path="pfc_queues_admin",
            default=[],
        ),
        FieldMapping(
            cache_attr="rdma_protocols",
            api_path="rdma_protocols",
            default=[],
        ),
        FieldMapping(
            cache_attr="reachability",
            api_path="reachability",
        ),
        FieldMapping(
            cache_attr="reachable_broadcast_domains",
            api_path="reachable_broadcast_domains",
            transform=_transform_reachable_broadcast_domains,
            default=[],
        ),
        FieldMapping(
            cache_attr="speed",
            api_path="speed",
            default=0,
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="statistics_device_link_down_count_raw",
            api_path="statistics.device.link_down_count_raw",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_device_receive_raw_discards",
            api_path="statistics.device.receive_raw.discards",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_device_receive_raw_errors",
            api_path="statistics.device.receive_raw.errors",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_device_receive_raw_packets",
            api_path="statistics.device.receive_raw.packets",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_device_timestamp",
            api_path="statistics.device.timestamp",
        ),
        FieldMapping(
            cache_attr="statistics_device_transmit_raw_discards",
            api_path="statistics.device.transmit_raw.discards",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_device_transmit_raw_errors",
            api_path="statistics.device.transmit_raw.errors",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_device_transmit_raw_packets",
            api_path="statistics.device.transmit_raw.packets",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_status",
            api_path="statistics.status",
        ),
        FieldMapping(
            cache_attr="statistics_throughput_raw_read",
            api_path="statistics.throughput_raw.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_throughput_raw_total",
            api_path="statistics.throughput_raw.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_throughput_raw_write",
            api_path="statistics.throughput_raw.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics_timestamp",
            api_path="statistics.timestamp",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="vlan_base_port_name",
            api_path="vlan.base_port.name",
        ),
        FieldMapping(
            cache_attr="vlan_base_port_node_name",
            api_path="vlan.base_port.node.name",
        ),
        FieldMapping(
            cache_attr="vlan_base_port_uuid",
            api_path="vlan.base_port.uuid",
        ),
        FieldMapping(
            cache_attr="vlan_tag",
            api_path="vlan.tag",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapPort", ONTAPPORT_MAPPING)
