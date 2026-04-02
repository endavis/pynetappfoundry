"""OntapPort type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.ethernet.ports.model import (
    OntapPort,
    OntapPortDiscoveredDevice,
    OntapPortLagActivePort,
    OntapPortLagMemberPort,
    OntapPortReachableBroadcastDomain,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_discovered_devices(record: dict[str, Any]) -> list[OntapPortDiscoveredDevice]:
    """Transform discovered_devices into OntapPortDiscoveredDevice list."""
    return [OntapPortDiscoveredDevice(**item) for item in record.get("discovered_devices", [])]


def _transform_lag_active_ports(record: dict[str, Any]) -> list[OntapPortLagActivePort]:
    """Transform lag.active_ports into OntapPortLagActivePort list."""
    try:
        items = get_nested_value(record, "lag.active_ports")
    except Exception:
        items = []
    return [OntapPortLagActivePort(**item) for item in items]


def _transform_lag_member_ports(record: dict[str, Any]) -> list[OntapPortLagMemberPort]:
    """Transform lag.member_ports into OntapPortLagMemberPort list."""
    try:
        items = get_nested_value(record, "lag.member_ports")
    except Exception:
        items = []
    return [OntapPortLagMemberPort(**item) for item in items]


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
            cache_attr="broadcast_domain.ipspace.name",
            api_path="broadcast_domain.ipspace.name",
        ),
        FieldMapping(
            cache_attr="broadcast_domain.name",
            api_path="broadcast_domain.name",
        ),
        FieldMapping(
            cache_attr="broadcast_domain.uuid",
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
            cache_attr="lag.active_ports",
            api_path="lag.active_ports",
            transform=_transform_lag_active_ports,
            default=[],
        ),
        FieldMapping(
            cache_attr="lag.distribution_policy",
            api_path="lag.distribution_policy",
        ),
        FieldMapping(
            cache_attr="lag.member_ports",
            api_path="lag.member_ports",
            transform=_transform_lag_member_ports,
            default=[],
        ),
        FieldMapping(
            cache_attr="lag.mode",
            api_path="lag.mode",
        ),
        FieldMapping(
            cache_attr="mac_address",
            api_path="mac_address",
        ),
        FieldMapping(
            cache_attr="metric.duration",
            api_path="metric.duration",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric.status",
            api_path="metric.status",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="metric.throughput.read",
            api_path="metric.throughput.read",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.throughput.total",
            api_path="metric.throughput.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.throughput.write",
            api_path="metric.throughput.write",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="metric.timestamp",
            api_path="metric.timestamp",
            cache_strategy="realtime",
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
            cache_attr="node.name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
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
            cache_attr="statistics.device.link_down_count_raw",
            api_path="statistics.device.link_down_count_raw",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.device.receive_raw.discards",
            api_path="statistics.device.receive_raw.discards",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.device.receive_raw.errors",
            api_path="statistics.device.receive_raw.errors",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.device.receive_raw.packets",
            api_path="statistics.device.receive_raw.packets",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.device.timestamp",
            api_path="statistics.device.timestamp",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics.device.transmit_raw.discards",
            api_path="statistics.device.transmit_raw.discards",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.device.transmit_raw.errors",
            api_path="statistics.device.transmit_raw.errors",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.device.transmit_raw.packets",
            api_path="statistics.device.transmit_raw.packets",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.status",
            api_path="statistics.status",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="statistics.throughput_raw.read",
            api_path="statistics.throughput_raw.read",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.throughput_raw.total",
            api_path="statistics.throughput_raw.total",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.throughput_raw.write",
            api_path="statistics.throughput_raw.write",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="statistics.timestamp",
            api_path="statistics.timestamp",
            cache_strategy="realtime",
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
            cache_attr="vlan.base_port.name",
            api_path="vlan.base_port.name",
        ),
        FieldMapping(
            cache_attr="vlan.base_port.node.name",
            api_path="vlan.base_port.node.name",
        ),
        FieldMapping(
            cache_attr="vlan.base_port.uuid",
            api_path="vlan.base_port.uuid",
        ),
        FieldMapping(
            cache_attr="vlan.tag",
            api_path="vlan.tag",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapPort", ONTAPPORT_MAPPING)
