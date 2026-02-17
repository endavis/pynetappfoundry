"""OntapNodeResponse type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.cluster.nodes.model import (
    OntapNodeResponse,
    OntapNodeResponseClusterInterface,
    OntapNodeResponseFlashCache,
    OntapNodeResponseFru,
    OntapNodeResponseManagementInterface,
    OntapNodeResponsePartner,
    OntapNodeResponsePort,
    OntapNodeResponsePort2,
    OntapNodeResponseStatus,
)
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping


def _transform_cluster_interfaces(
    record: dict[str, Any],
) -> list[OntapNodeResponseClusterInterface]:
    """Transform cluster_interfaces into OntapNodeResponseClusterInterface list."""
    return [
        OntapNodeResponseClusterInterface(**item) for item in record.get("cluster_interfaces", [])
    ]


def _transform_controller_flash_cache(record: dict[str, Any]) -> list[OntapNodeResponseFlashCache]:
    """Transform controller.flash_cache into OntapNodeResponseFlashCache list."""
    return [
        OntapNodeResponseFlashCache(**item) for item in record.get("controller.flash_cache", [])
    ]


def _transform_controller_frus(record: dict[str, Any]) -> list[OntapNodeResponseFru]:
    """Transform controller.frus into OntapNodeResponseFru list."""
    return [OntapNodeResponseFru(**item) for item in record.get("controller.frus", [])]


def _transform_ha_giveback_status(record: dict[str, Any]) -> list[OntapNodeResponseStatus]:
    """Transform ha.giveback.status into OntapNodeResponseStatus list."""
    return [OntapNodeResponseStatus(**item) for item in record.get("ha.giveback.status", [])]


def _transform_ha_partners(record: dict[str, Any]) -> list[OntapNodeResponsePartner]:
    """Transform ha.partners into OntapNodeResponsePartner list."""
    return [OntapNodeResponsePartner(**item) for item in record.get("ha.partners", [])]


def _transform_ha_ports(record: dict[str, Any]) -> list[OntapNodeResponsePort]:
    """Transform ha.ports into OntapNodeResponsePort list."""
    return [OntapNodeResponsePort(**item) for item in record.get("ha.ports", [])]


def _transform_management_interfaces(
    record: dict[str, Any],
) -> list[OntapNodeResponseManagementInterface]:
    """Transform management_interfaces into OntapNodeResponseManagementInterface list."""
    return [
        OntapNodeResponseManagementInterface(**item)
        for item in record.get("management_interfaces", [])
    ]


def _transform_metrocluster_ports(record: dict[str, Any]) -> list[OntapNodeResponsePort2]:
    """Transform metrocluster.ports into OntapNodeResponsePort2 list."""
    return [OntapNodeResponsePort2(**item) for item in record.get("metrocluster.ports", [])]


ONTAPNODERESPONSE_MAPPING = TypeMapping(
    name="OntapNodeResponse",
    model_class=OntapNodeResponse,
    api_endpoint="/cluster/nodes?fields=*,metric,statistics",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="anti_ransomware_version",
            api_path="anti_ransomware_version",
        ),
        FieldMapping(
            cache_attr="cluster_interface_ip_address",
            api_path="cluster_interface.ip.address",
        ),
        FieldMapping(
            cache_attr="cluster_interfaces",
            transform=_transform_cluster_interfaces,
            default=[],
        ),
        FieldMapping(
            cache_attr="controller_board",
            api_path="controller.board",
        ),
        FieldMapping(
            cache_attr="controller_cpu_count",
            api_path="controller.cpu.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="controller_cpu_firmware_release",
            api_path="controller.cpu.firmware_release",
        ),
        FieldMapping(
            cache_attr="controller_cpu_processor",
            api_path="controller.cpu.processor",
        ),
        FieldMapping(
            cache_attr="controller_failed_fan_count",
            api_path="controller.failed_fan.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="controller_failed_fan_message_code",
            api_path="controller.failed_fan.message.code",
        ),
        FieldMapping(
            cache_attr="controller_failed_fan_message_message",
            api_path="controller.failed_fan.message.message",
        ),
        FieldMapping(
            cache_attr="controller_failed_power_supply_count",
            api_path="controller.failed_power_supply.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="controller_failed_power_supply_message_code",
            api_path="controller.failed_power_supply.message.code",
        ),
        FieldMapping(
            cache_attr="controller_failed_power_supply_message_message",
            api_path="controller.failed_power_supply.message.message",
        ),
        FieldMapping(
            cache_attr="controller_flash_cache",
            transform=_transform_controller_flash_cache,
            default=[],
        ),
        FieldMapping(
            cache_attr="controller_frus",
            transform=_transform_controller_frus,
            default=[],
        ),
        FieldMapping(
            cache_attr="controller_memory_size",
            api_path="controller.memory_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="controller_over_temperature",
            api_path="controller.over_temperature",
        ),
        FieldMapping(
            cache_attr="date",
            api_path="date",
        ),
        FieldMapping(
            cache_attr="external_cache_is_enabled",
            api_path="external_cache.is_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="external_cache_is_hya_enabled",
            api_path="external_cache.is_hya_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="external_cache_is_rewarm_enabled",
            api_path="external_cache.is_rewarm_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="external_cache_pcs_size",
            api_path="external_cache.pcs_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="ha_auto_giveback",
            api_path="ha.auto_giveback",
            default=False,
        ),
        FieldMapping(
            cache_attr="ha_enabled",
            api_path="ha.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="ha_giveback_failure_code",
            api_path="ha.giveback.failure.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="ha_giveback_failure_message",
            api_path="ha.giveback.failure.message",
        ),
        FieldMapping(
            cache_attr="ha_giveback_state",
            api_path="ha.giveback.state",
        ),
        FieldMapping(
            cache_attr="ha_giveback_status",
            transform=_transform_ha_giveback_status,
            default=[],
        ),
        FieldMapping(
            cache_attr="ha_interconnect_adapter",
            api_path="ha.interconnect.adapter",
        ),
        FieldMapping(
            cache_attr="ha_interconnect_state",
            api_path="ha.interconnect.state",
        ),
        FieldMapping(
            cache_attr="ha_partners",
            transform=_transform_ha_partners,
            default=[],
        ),
        FieldMapping(
            cache_attr="ha_ports",
            transform=_transform_ha_ports,
            default=[],
        ),
        FieldMapping(
            cache_attr="ha_takeover_failure_code",
            api_path="ha.takeover.failure.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="ha_takeover_failure_message",
            api_path="ha.takeover.failure.message",
        ),
        FieldMapping(
            cache_attr="ha_takeover_state",
            api_path="ha.takeover.state",
        ),
        FieldMapping(
            cache_attr="ha_takeover_check_reasons",
            api_path="ha.takeover_check.reasons",
            default=[],
        ),
        FieldMapping(
            cache_attr="ha_takeover_check_takeover_possible",
            api_path="ha.takeover_check.takeover_possible",
            default=False,
        ),
        FieldMapping(
            cache_attr="hw_assist_status_enabled",
            api_path="hw_assist.status.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="hw_assist_status_local_ip",
            api_path="hw_assist.status.local.ip",
        ),
        FieldMapping(
            cache_attr="hw_assist_status_local_port",
            api_path="hw_assist.status.local.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="hw_assist_status_local_state",
            api_path="hw_assist.status.local.state",
        ),
        FieldMapping(
            cache_attr="hw_assist_status_partner_ip",
            api_path="hw_assist.status.partner.ip",
        ),
        FieldMapping(
            cache_attr="hw_assist_status_partner_port",
            api_path="hw_assist.status.partner.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="hw_assist_status_partner_state",
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
            cache_attr="management_interface_ip_address",
            api_path="management_interface.ip.address",
        ),
        FieldMapping(
            cache_attr="management_interfaces",
            transform=_transform_management_interfaces,
            default=[],
        ),
        FieldMapping(
            cache_attr="membership",
            api_path="membership",
        ),
        FieldMapping(
            cache_attr="metric_duration",
            api_path="metric.duration",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric_processor_utilization",
            api_path="metric.processor_utilization",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric_status",
            api_path="metric.status",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric_timestamp",
            api_path="metric.timestamp",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric_uuid",
            api_path="metric.uuid",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metrocluster_custom_vlan_capable",
            api_path="metrocluster.custom_vlan_capable",
            default=False,
        ),
        FieldMapping(
            cache_attr="metrocluster_ports",
            transform=_transform_metrocluster_ports,
            default=[],
        ),
        FieldMapping(
            cache_attr="metrocluster_type",
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
            cache_attr="nvram_battery_state",
            api_path="nvram.battery_state",
        ),
        FieldMapping(
            cache_attr="nvram_id",
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
            cache_attr="service_processor_api_service_enabled",
            api_path="service_processor.api_service.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor_api_service_limit_access",
            api_path="service_processor.api_service.limit_access",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor_api_service_port",
            api_path="service_processor.api_service.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="service_processor_auto_config_ipv4_subnet",
            api_path="service_processor.auto_config.ipv4_subnet",
        ),
        FieldMapping(
            cache_attr="service_processor_auto_config_ipv6_subnet",
            api_path="service_processor.auto_config.ipv6_subnet",
        ),
        FieldMapping(
            cache_attr="service_processor_autoupdate_enabled",
            api_path="service_processor.autoupdate_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor_backup_is_current",
            api_path="service_processor.backup.is_current",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor_backup_state",
            api_path="service_processor.backup.state",
        ),
        FieldMapping(
            cache_attr="service_processor_backup_version",
            api_path="service_processor.backup.version",
        ),
        FieldMapping(
            cache_attr="service_processor_dhcp_enabled",
            api_path="service_processor.dhcp_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor_firmware_version",
            api_path="service_processor.firmware_version",
        ),
        FieldMapping(
            cache_attr="service_processor_ipv4_interface_address",
            api_path="service_processor.ipv4_interface.address",
        ),
        FieldMapping(
            cache_attr="service_processor_ipv4_interface_enabled",
            api_path="service_processor.ipv4_interface.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor_ipv4_interface_gateway",
            api_path="service_processor.ipv4_interface.gateway",
        ),
        FieldMapping(
            cache_attr="service_processor_ipv4_interface_netmask",
            api_path="service_processor.ipv4_interface.netmask",
        ),
        FieldMapping(
            cache_attr="service_processor_ipv4_interface_setup_state",
            api_path="service_processor.ipv4_interface.setup_state",
        ),
        FieldMapping(
            cache_attr="service_processor_ipv6_interface_address",
            api_path="service_processor.ipv6_interface.address",
        ),
        FieldMapping(
            cache_attr="service_processor_ipv6_interface_enabled",
            api_path="service_processor.ipv6_interface.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor_ipv6_interface_gateway",
            api_path="service_processor.ipv6_interface.gateway",
        ),
        FieldMapping(
            cache_attr="service_processor_ipv6_interface_is_ipv6_ra_enabled",
            api_path="service_processor.ipv6_interface.is_ipv6_ra_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor_ipv6_interface_link_local_ip",
            api_path="service_processor.ipv6_interface.link_local_ip",
        ),
        FieldMapping(
            cache_attr="service_processor_ipv6_interface_netmask",
            api_path="service_processor.ipv6_interface.netmask",
            default=0,
        ),
        FieldMapping(
            cache_attr="service_processor_ipv6_interface_router_ip",
            api_path="service_processor.ipv6_interface.router_ip",
        ),
        FieldMapping(
            cache_attr="service_processor_ipv6_interface_setup_state",
            api_path="service_processor.ipv6_interface.setup_state",
        ),
        FieldMapping(
            cache_attr="service_processor_is_ip_configured",
            api_path="service_processor.is_ip_configured",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor_last_update_state",
            api_path="service_processor.last_update_state",
        ),
        FieldMapping(
            cache_attr="service_processor_link_status",
            api_path="service_processor.link_status",
        ),
        FieldMapping(
            cache_attr="service_processor_mac_address",
            api_path="service_processor.mac_address",
        ),
        FieldMapping(
            cache_attr="service_processor_primary_is_current",
            api_path="service_processor.primary.is_current",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor_primary_state",
            api_path="service_processor.primary.state",
        ),
        FieldMapping(
            cache_attr="service_processor_primary_version",
            api_path="service_processor.primary.version",
        ),
        FieldMapping(
            cache_attr="service_processor_ssh_info_allowed_addresses",
            api_path="service_processor.ssh_info.allowed_addresses",
            default=[],
        ),
        FieldMapping(
            cache_attr="service_processor_state",
            api_path="service_processor.state",
        ),
        FieldMapping(
            cache_attr="service_processor_type",
            api_path="service_processor.type",
        ),
        FieldMapping(
            cache_attr="service_processor_web_service_enabled",
            api_path="service_processor.web_service.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor_web_service_limit_access",
            api_path="service_processor.web_service.limit_access",
            default=False,
        ),
        FieldMapping(
            cache_attr="snaplock_compliance_clock_time",
            api_path="snaplock.compliance_clock_time",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="statistics_processor_utilization_base",
            api_path="statistics.processor_utilization_base",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics_processor_utilization_raw",
            api_path="statistics.processor_utilization_raw",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics_status",
            api_path="statistics.status",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics_timestamp",
            api_path="statistics.timestamp",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="storage_configuration",
            api_path="storage_configuration",
        ),
        FieldMapping(
            cache_attr="system_aggregate_name",
            api_path="system_aggregate.name",
        ),
        FieldMapping(
            cache_attr="system_aggregate_uuid",
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
            cache_attr="version_full",
            api_path="version.full",
        ),
        FieldMapping(
            cache_attr="version_generation",
            api_path="version.generation",
            default=0,
        ),
        FieldMapping(
            cache_attr="version_major",
            api_path="version.major",
            default=0,
        ),
        FieldMapping(
            cache_attr="version_minor",
            api_path="version.minor",
            default=0,
        ),
        FieldMapping(
            cache_attr="vm_provider_type",
            api_path="vm.provider_type",
        ),
    ),
)

model_registry.register_mapping("OntapNodeResponse", ONTAPNODERESPONSE_MAPPING)
