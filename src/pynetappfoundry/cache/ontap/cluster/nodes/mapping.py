"""OntapNodeResponse type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.nodes.model import (
    OntapNodeResponse,
    OntapNodeResponseClusterInterface2,
    OntapNodeResponseControllerFlashCache,
    OntapNodeResponseControllerFru,
    OntapNodeResponseHaGivebackStatus,
    OntapNodeResponseHaPartner,
    OntapNodeResponseHaPort,
    OntapNodeResponseManagementInterface2,
    OntapNodeResponseMetroclusterPort,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_cluster_interfaces(
    record: dict[str, Any],
) -> list[OntapNodeResponseClusterInterface2]:
    """Transform cluster_interfaces into OntapNodeResponseClusterInterface2 list."""
    return [
        OntapNodeResponseClusterInterface2(**item) for item in record.get("cluster_interfaces", [])
    ]


def _transform_controller_flash_cache(
    record: dict[str, Any],
) -> list[OntapNodeResponseControllerFlashCache]:
    """Transform controller.flash_cache into OntapNodeResponseControllerFlashCache list."""
    try:
        items = get_nested_value(record, "controller.flash_cache")
    except Exception:
        items = []
    return [OntapNodeResponseControllerFlashCache(**item) for item in items]


def _transform_controller_frus(record: dict[str, Any]) -> list[OntapNodeResponseControllerFru]:
    """Transform controller.frus into OntapNodeResponseControllerFru list."""
    try:
        items = get_nested_value(record, "controller.frus")
    except Exception:
        items = []
    return [OntapNodeResponseControllerFru(**item) for item in items]


def _transform_ha_giveback_status(
    record: dict[str, Any],
) -> list[OntapNodeResponseHaGivebackStatus]:
    """Transform ha.giveback.status into OntapNodeResponseHaGivebackStatus list."""
    try:
        items = get_nested_value(record, "ha.giveback.status")
    except Exception:
        items = []
    return [OntapNodeResponseHaGivebackStatus(**item) for item in items]


def _transform_ha_partners(record: dict[str, Any]) -> list[OntapNodeResponseHaPartner]:
    """Transform ha.partners into OntapNodeResponseHaPartner list."""
    try:
        items = get_nested_value(record, "ha.partners")
    except Exception:
        items = []
    return [OntapNodeResponseHaPartner(**item) for item in items]


def _transform_ha_ports(record: dict[str, Any]) -> list[OntapNodeResponseHaPort]:
    """Transform ha.ports into OntapNodeResponseHaPort list."""
    try:
        items = get_nested_value(record, "ha.ports")
    except Exception:
        items = []
    return [OntapNodeResponseHaPort(**item) for item in items]


def _transform_management_interfaces(
    record: dict[str, Any],
) -> list[OntapNodeResponseManagementInterface2]:
    """Transform management_interfaces into OntapNodeResponseManagementInterface2 list."""
    return [
        OntapNodeResponseManagementInterface2(**item)
        for item in record.get("management_interfaces", [])
    ]


def _transform_metrocluster_ports(
    record: dict[str, Any],
) -> list[OntapNodeResponseMetroclusterPort]:
    """Transform metrocluster.ports into OntapNodeResponseMetroclusterPort list."""
    try:
        items = get_nested_value(record, "metrocluster.ports")
    except Exception:
        items = []
    return [OntapNodeResponseMetroclusterPort(**item) for item in items]


ONTAPNODERESPONSE_MAPPING = TypeMapping(
    name="OntapNodeResponse",
    model_class=OntapNodeResponse,
    api_endpoint="/cluster/nodes?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="anti_ransomware_version",
            api_path="anti_ransomware_version",
        ),
        FieldMapping(
            cache_attr="cluster_interface.ip.address",
            api_path="cluster_interface.ip.address",
        ),
        FieldMapping(
            cache_attr="cluster_interfaces",
            api_path="cluster_interfaces",
            transform=_transform_cluster_interfaces,
            default=[],
        ),
        FieldMapping(
            cache_attr="controller.board",
            api_path="controller.board",
        ),
        FieldMapping(
            cache_attr="controller.cpu.count",
            api_path="controller.cpu.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="controller.cpu.firmware_release",
            api_path="controller.cpu.firmware_release",
        ),
        FieldMapping(
            cache_attr="controller.cpu.processor",
            api_path="controller.cpu.processor",
        ),
        FieldMapping(
            cache_attr="controller.failed_fan.count",
            api_path="controller.failed_fan.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="controller.failed_fan.message.code",
            api_path="controller.failed_fan.message.code",
        ),
        FieldMapping(
            cache_attr="controller.failed_fan.message.message",
            api_path="controller.failed_fan.message.message",
        ),
        FieldMapping(
            cache_attr="controller.failed_power_supply.count",
            api_path="controller.failed_power_supply.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="controller.failed_power_supply.message.code",
            api_path="controller.failed_power_supply.message.code",
        ),
        FieldMapping(
            cache_attr="controller.failed_power_supply.message.message",
            api_path="controller.failed_power_supply.message.message",
        ),
        FieldMapping(
            cache_attr="controller.flash_cache",
            api_path="controller.flash_cache",
            transform=_transform_controller_flash_cache,
            default=[],
        ),
        FieldMapping(
            cache_attr="controller.frus",
            api_path="controller.frus",
            transform=_transform_controller_frus,
            default=[],
        ),
        FieldMapping(
            cache_attr="controller.memory_size",
            api_path="controller.memory_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="controller.over_temperature",
            api_path="controller.over_temperature",
        ),
        FieldMapping(
            cache_attr="date",
            api_path="date",
        ),
        FieldMapping(
            cache_attr="external_cache.is_enabled",
            api_path="external_cache.is_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="external_cache.is_hya_enabled",
            api_path="external_cache.is_hya_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="external_cache.is_rewarm_enabled",
            api_path="external_cache.is_rewarm_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="external_cache.pcs_size",
            api_path="external_cache.pcs_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="ha.auto_giveback",
            api_path="ha.auto_giveback",
            default=False,
        ),
        FieldMapping(
            cache_attr="ha.enabled",
            api_path="ha.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="ha.giveback.failure.code",
            api_path="ha.giveback.failure.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="ha.giveback.failure.message",
            api_path="ha.giveback.failure.message",
        ),
        FieldMapping(
            cache_attr="ha.giveback.state",
            api_path="ha.giveback.state",
        ),
        FieldMapping(
            cache_attr="ha.giveback.status",
            api_path="ha.giveback.status",
            transform=_transform_ha_giveback_status,
            default=[],
        ),
        FieldMapping(
            cache_attr="ha.interconnect.adapter",
            api_path="ha.interconnect.adapter",
        ),
        FieldMapping(
            cache_attr="ha.interconnect.state",
            api_path="ha.interconnect.state",
        ),
        FieldMapping(
            cache_attr="ha.partners",
            api_path="ha.partners",
            transform=_transform_ha_partners,
            default=[],
        ),
        FieldMapping(
            cache_attr="ha.ports",
            api_path="ha.ports",
            transform=_transform_ha_ports,
            default=[],
        ),
        FieldMapping(
            cache_attr="ha.takeover.failure.code",
            api_path="ha.takeover.failure.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="ha.takeover.failure.message",
            api_path="ha.takeover.failure.message",
        ),
        FieldMapping(
            cache_attr="ha.takeover.state",
            api_path="ha.takeover.state",
        ),
        FieldMapping(
            cache_attr="ha.takeover_check.reasons",
            api_path="ha.takeover_check.reasons",
            default=[],
        ),
        FieldMapping(
            cache_attr="ha.takeover_check.takeover_possible",
            api_path="ha.takeover_check.takeover_possible",
            default=False,
        ),
        FieldMapping(
            cache_attr="hw_assist.status.enabled",
            api_path="hw_assist.status.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="hw_assist.status.local.ip",
            api_path="hw_assist.status.local.ip",
        ),
        FieldMapping(
            cache_attr="hw_assist.status.local.port",
            api_path="hw_assist.status.local.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="hw_assist.status.local.state",
            api_path="hw_assist.status.local.state",
        ),
        FieldMapping(
            cache_attr="hw_assist.status.partner.ip",
            api_path="hw_assist.status.partner.ip",
        ),
        FieldMapping(
            cache_attr="hw_assist.status.partner.port",
            api_path="hw_assist.status.partner.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="hw_assist.status.partner.state",
            api_path="hw_assist.status.partner.state",
        ),
        FieldMapping(
            cache_attr="is_spares_low",
            api_path="is_spares_low",
            default=False,
        ),
        FieldMapping(
            cache_attr="location",
            api_path="location",
        ),
        FieldMapping(
            cache_attr="management_interface.ip.address",
            api_path="management_interface.ip.address",
        ),
        FieldMapping(
            cache_attr="management_interfaces",
            api_path="management_interfaces",
            transform=_transform_management_interfaces,
            default=[],
        ),
        FieldMapping(
            cache_attr="membership",
            api_path="membership",
        ),
        FieldMapping(
            cache_attr="metric.duration",
            api_path="metric.duration",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.processor_utilization",
            api_path="metric.processor_utilization",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.status",
            api_path="metric.status",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.timestamp",
            api_path="metric.timestamp",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.uuid",
            api_path="metric.uuid",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metrocluster.custom_vlan_capable",
            api_path="metrocluster.custom_vlan_capable",
            default=False,
        ),
        FieldMapping(
            cache_attr="metrocluster.ports",
            api_path="metrocluster.ports",
            transform=_transform_metrocluster_ports,
            default=[],
        ),
        FieldMapping(
            cache_attr="metrocluster.type_",
            api_path="metrocluster.type",
        ),
        FieldMapping(
            cache_attr="model_",
            api_path="model",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="nvram.battery_state",
            api_path="nvram.battery_state",
        ),
        FieldMapping(
            cache_attr="nvram.id",
            api_path="nvram.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="owner",
            api_path="owner",
        ),
        FieldMapping(
            cache_attr="serial_number",
            api_path="serial_number",
        ),
        FieldMapping(
            cache_attr="service_processor.api_service.enabled",
            api_path="service_processor.api_service.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.api_service.limit_access",
            api_path="service_processor.api_service.limit_access",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.api_service.port",
            api_path="service_processor.api_service.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="service_processor.auto_config.ipv4_subnet",
            api_path="service_processor.auto_config.ipv4_subnet",
        ),
        FieldMapping(
            cache_attr="service_processor.auto_config.ipv6_subnet",
            api_path="service_processor.auto_config.ipv6_subnet",
        ),
        FieldMapping(
            cache_attr="service_processor.autoupdate_enabled",
            api_path="service_processor.autoupdate_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.backup.is_current",
            api_path="service_processor.backup.is_current",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.backup.state",
            api_path="service_processor.backup.state",
        ),
        FieldMapping(
            cache_attr="service_processor.backup.version",
            api_path="service_processor.backup.version",
        ),
        FieldMapping(
            cache_attr="service_processor.dhcp_enabled",
            api_path="service_processor.dhcp_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.firmware_version",
            api_path="service_processor.firmware_version",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv4_interface.address",
            api_path="service_processor.ipv4_interface.address",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv4_interface.enabled",
            api_path="service_processor.ipv4_interface.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.ipv4_interface.gateway",
            api_path="service_processor.ipv4_interface.gateway",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv4_interface.netmask",
            api_path="service_processor.ipv4_interface.netmask",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv4_interface.setup_state",
            api_path="service_processor.ipv4_interface.setup_state",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.address",
            api_path="service_processor.ipv6_interface.address",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.enabled",
            api_path="service_processor.ipv6_interface.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.gateway",
            api_path="service_processor.ipv6_interface.gateway",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.is_ipv6_ra_enabled",
            api_path="service_processor.ipv6_interface.is_ipv6_ra_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.link_local_ip",
            api_path="service_processor.ipv6_interface.link_local_ip",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.netmask",
            api_path="service_processor.ipv6_interface.netmask",
            default=0,
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.router_ip",
            api_path="service_processor.ipv6_interface.router_ip",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.setup_state",
            api_path="service_processor.ipv6_interface.setup_state",
        ),
        FieldMapping(
            cache_attr="service_processor.is_ip_configured",
            api_path="service_processor.is_ip_configured",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.last_update_state",
            api_path="service_processor.last_update_state",
        ),
        FieldMapping(
            cache_attr="service_processor.link_status",
            api_path="service_processor.link_status",
        ),
        FieldMapping(
            cache_attr="service_processor.mac_address",
            api_path="service_processor.mac_address",
        ),
        FieldMapping(
            cache_attr="service_processor.primary.is_current",
            api_path="service_processor.primary.is_current",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.primary.state",
            api_path="service_processor.primary.state",
        ),
        FieldMapping(
            cache_attr="service_processor.primary.version",
            api_path="service_processor.primary.version",
        ),
        FieldMapping(
            cache_attr="service_processor.ssh_info.allowed_addresses",
            api_path="service_processor.ssh_info.allowed_addresses",
            default=[],
        ),
        FieldMapping(
            cache_attr="service_processor.state",
            api_path="service_processor.state",
        ),
        FieldMapping(
            cache_attr="service_processor.type_",
            api_path="service_processor.type",
        ),
        FieldMapping(
            cache_attr="service_processor.web_service.enabled",
            api_path="service_processor.web_service.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.web_service.limit_access",
            api_path="service_processor.web_service.limit_access",
            default=False,
        ),
        FieldMapping(
            cache_attr="snaplock.compliance_clock_time",
            api_path="snaplock.compliance_clock_time",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="statistics.processor_utilization_base",
            api_path="statistics.processor_utilization_base",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.processor_utilization_raw",
            api_path="statistics.processor_utilization_raw",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.status",
            api_path="statistics.status",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.timestamp",
            api_path="statistics.timestamp",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="storage_configuration",
            api_path="storage_configuration",
        ),
        FieldMapping(
            cache_attr="system_aggregate.name",
            api_path="system_aggregate.name",
        ),
        FieldMapping(
            cache_attr="system_aggregate.uuid",
            api_path="system_aggregate.uuid",
        ),
        FieldMapping(
            cache_attr="system_id",
            api_path="system_id",
        ),
        FieldMapping(
            cache_attr="system_machine_type",
            api_path="system_machine_type",
        ),
        FieldMapping(
            cache_attr="uptime",
            api_path="uptime",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="vendor_serial_number",
            api_path="vendor_serial_number",
        ),
        FieldMapping(
            cache_attr="version.full",
            api_path="version.full",
        ),
        FieldMapping(
            cache_attr="version.generation",
            api_path="version.generation",
            default=0,
        ),
        FieldMapping(
            cache_attr="version.major",
            api_path="version.major",
            default=0,
        ),
        FieldMapping(
            cache_attr="version.minor",
            api_path="version.minor",
            default=0,
        ),
        FieldMapping(
            cache_attr="vm.provider_type",
            api_path="vm.provider_type",
        ),
    ),
)

model_registry.register_mapping("OntapNodeResponse", ONTAPNODERESPONSE_MAPPING)
