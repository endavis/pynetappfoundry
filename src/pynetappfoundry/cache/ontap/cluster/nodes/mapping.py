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
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="anti_ransomware_version",
        ),
        FieldMapping(
            cache_attr="cluster_interface.ip.address",
        ),
        FieldMapping(
            cache_attr="cluster_interfaces",
            transform=_transform_cluster_interfaces,
            default=[],
        ),
        FieldMapping(
            cache_attr="controller.board",
        ),
        FieldMapping(
            cache_attr="controller.cpu.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="controller.cpu.firmware_release",
        ),
        FieldMapping(
            cache_attr="controller.cpu.processor",
        ),
        FieldMapping(
            cache_attr="controller.failed_fan.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="controller.failed_fan.message.code",
        ),
        FieldMapping(
            cache_attr="controller.failed_fan.message.message",
        ),
        FieldMapping(
            cache_attr="controller.failed_power_supply.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="controller.failed_power_supply.message.code",
        ),
        FieldMapping(
            cache_attr="controller.failed_power_supply.message.message",
        ),
        FieldMapping(
            cache_attr="controller.flash_cache",
            transform=_transform_controller_flash_cache,
            default=[],
        ),
        FieldMapping(
            cache_attr="controller.frus",
            transform=_transform_controller_frus,
            default=[],
        ),
        FieldMapping(
            cache_attr="controller.memory_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="controller.over_temperature",
        ),
        FieldMapping(
            cache_attr="date",
        ),
        FieldMapping(
            cache_attr="external_cache.is_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="external_cache.is_hya_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="external_cache.is_rewarm_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="external_cache.pcs_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="ha.auto_giveback",
            default=False,
        ),
        FieldMapping(
            cache_attr="ha.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="ha.giveback.failure.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="ha.giveback.failure.message",
        ),
        FieldMapping(
            cache_attr="ha.giveback.state",
        ),
        FieldMapping(
            cache_attr="ha.giveback.status",
            transform=_transform_ha_giveback_status,
            default=[],
        ),
        FieldMapping(
            cache_attr="ha.interconnect.adapter",
        ),
        FieldMapping(
            cache_attr="ha.interconnect.state",
        ),
        FieldMapping(
            cache_attr="ha.partners",
            transform=_transform_ha_partners,
            default=[],
        ),
        FieldMapping(
            cache_attr="ha.ports",
            transform=_transform_ha_ports,
            default=[],
        ),
        FieldMapping(
            cache_attr="ha.takeover.failure.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="ha.takeover.failure.message",
        ),
        FieldMapping(
            cache_attr="ha.takeover.state",
        ),
        FieldMapping(
            cache_attr="ha.takeover_check.reasons",
            default=[],
        ),
        FieldMapping(
            cache_attr="ha.takeover_check.takeover_possible",
            default=False,
        ),
        FieldMapping(
            cache_attr="hw_assist.status.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="hw_assist.status.local.ip",
        ),
        FieldMapping(
            cache_attr="hw_assist.status.local.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="hw_assist.status.local.state",
        ),
        FieldMapping(
            cache_attr="hw_assist.status.partner.ip",
        ),
        FieldMapping(
            cache_attr="hw_assist.status.partner.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="hw_assist.status.partner.state",
        ),
        FieldMapping(
            cache_attr="is_spares_low",
            default=False,
        ),
        FieldMapping(
            cache_attr="location",
        ),
        FieldMapping(
            cache_attr="management_interface.ip.address",
        ),
        FieldMapping(
            cache_attr="management_interfaces",
            transform=_transform_management_interfaces,
            default=[],
        ),
        FieldMapping(
            cache_attr="membership",
        ),
        FieldMapping(
            cache_attr="metric.duration",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.processor_utilization",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.status",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.timestamp",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metric.uuid",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="metrocluster.custom_vlan_capable",
            default=False,
        ),
        FieldMapping(
            cache_attr="metrocluster.ports",
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
        ),
        FieldMapping(
            cache_attr="nvram.battery_state",
        ),
        FieldMapping(
            cache_attr="nvram.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="owner",
        ),
        FieldMapping(
            cache_attr="serial_number",
        ),
        FieldMapping(
            cache_attr="service_processor.api_service.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.api_service.limit_access",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.api_service.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="service_processor.auto_config.ipv4_subnet",
        ),
        FieldMapping(
            cache_attr="service_processor.auto_config.ipv6_subnet",
        ),
        FieldMapping(
            cache_attr="service_processor.autoupdate_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.backup.is_current",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.backup.state",
        ),
        FieldMapping(
            cache_attr="service_processor.backup.version",
        ),
        FieldMapping(
            cache_attr="service_processor.dhcp_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.firmware_version",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv4_interface.address",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv4_interface.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.ipv4_interface.gateway",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv4_interface.netmask",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv4_interface.setup_state",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.address",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.gateway",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.is_ipv6_ra_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.link_local_ip",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.netmask",
            default=0,
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.router_ip",
        ),
        FieldMapping(
            cache_attr="service_processor.ipv6_interface.setup_state",
        ),
        FieldMapping(
            cache_attr="service_processor.is_ip_configured",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.last_update_state",
        ),
        FieldMapping(
            cache_attr="service_processor.link_status",
        ),
        FieldMapping(
            cache_attr="service_processor.mac_address",
        ),
        FieldMapping(
            cache_attr="service_processor.primary.is_current",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.primary.state",
        ),
        FieldMapping(
            cache_attr="service_processor.primary.version",
        ),
        FieldMapping(
            cache_attr="service_processor.ssh_info.allowed_addresses",
            default=[],
        ),
        FieldMapping(
            cache_attr="service_processor.state",
        ),
        FieldMapping(
            cache_attr="service_processor.type_",
            api_path="service_processor.type",
        ),
        FieldMapping(
            cache_attr="service_processor.web_service.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="service_processor.web_service.limit_access",
            default=False,
        ),
        FieldMapping(
            cache_attr="snaplock.compliance_clock_time",
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="statistics.processor_utilization_base",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.processor_utilization_raw",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.status",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="statistics.timestamp",
            cache_strategy="realtime",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="storage_configuration",
        ),
        FieldMapping(
            cache_attr="system_aggregate.name",
        ),
        FieldMapping(
            cache_attr="system_aggregate.uuid",
        ),
        FieldMapping(
            cache_attr="system_id",
        ),
        FieldMapping(
            cache_attr="system_machine_type",
        ),
        FieldMapping(
            cache_attr="uptime",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="vendor_serial_number",
        ),
        FieldMapping(
            cache_attr="version.full",
        ),
        FieldMapping(
            cache_attr="version.generation",
            default=0,
        ),
        FieldMapping(
            cache_attr="version.major",
            default=0,
        ),
        FieldMapping(
            cache_attr="version.minor",
            default=0,
        ),
        FieldMapping(
            cache_attr="vm.provider_type",
        ),
    ),
)

model_registry.register_mapping("OntapNodeResponse", ONTAPNODERESPONSE_MAPPING)
