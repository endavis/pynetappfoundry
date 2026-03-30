"""OntapNodeResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapNodeResponseClusterInterface(OntapModel):
    """OntapNodeResponseClusterInterface sub-model for cluster_interfaces."""

    cluster_interfaces_ip_address: str = ""
    cluster_interfaces_name: str = ""
    cluster_interfaces_uuid: str = ""


class OntapNodeResponseFlashCache(OntapModel):
    """OntapNodeResponseFlashCache sub-model for flash_cache."""

    controller_flash_cache_capacity: int = 0
    controller_flash_cache_device_id: int = 0
    controller_flash_cache_firmware_file: str = ""
    controller_flash_cache_firmware_version: str = ""
    controller_flash_cache_hardware_revision: str = ""
    controller_flash_cache_model: str = ""
    controller_flash_cache_part_number: str = ""
    controller_flash_cache_serial_number: str = ""
    controller_flash_cache_slot: str = ""
    controller_flash_cache_state: str = ""


class OntapNodeResponseFru(OntapModel):
    """OntapNodeResponseFru sub-model for frus."""

    controller_frus_id: str = ""
    controller_frus_state: str = ""
    controller_frus_type: str = ""


class OntapNodeResponseStatus(OntapModel):
    """OntapNodeResponseStatus sub-model for status."""

    ha_giveback_status_aggregate_name: str = ""
    ha_giveback_status_aggregate_uuid: str = ""
    ha_giveback_status_error_code: str = ""
    ha_giveback_status_error_message: str = ""
    ha_giveback_status_state: str = ""


class OntapNodeResponsePartner(OntapModel):
    """OntapNodeResponsePartner sub-model for partners."""

    ha_partners_name: str = ""
    ha_partners_uuid: str = ""


class OntapNodeResponsePort(OntapModel):
    """OntapNodeResponsePort sub-model for ports."""

    ha_ports_number: int = 0
    ha_ports_state: str = ""


class OntapNodeResponseManagementInterface(OntapModel):
    """OntapNodeResponseManagementInterface sub-model for management_interfaces."""

    management_interfaces_ip_address: str = ""
    management_interfaces_name: str = ""
    management_interfaces_uuid: str = ""


class OntapNodeResponsePort2(OntapModel):
    """OntapNodeResponsePort2 sub-model for ports."""

    metrocluster_ports_name: str = ""


class OntapNodeResponse(OntapModel):
    """OntapNodeResponse information."""

    anti_ransomware_version: str = ""
    cluster_interface_ip_address: str = ""
    cluster_interfaces: list[OntapNodeResponseClusterInterface] = Field(default_factory=list)
    controller_board: str = ""
    controller_cpu_count: int = 0
    controller_cpu_firmware_release: str = ""
    controller_cpu_processor: str = ""
    controller_failed_fan_count: int = 0
    controller_failed_fan_message_code: str = ""
    controller_failed_fan_message_message: str = ""
    controller_failed_power_supply_count: int = 0
    controller_failed_power_supply_message_code: str = ""
    controller_failed_power_supply_message_message: str = ""
    controller_flash_cache: list[OntapNodeResponseFlashCache] = Field(default_factory=list)
    controller_frus: list[OntapNodeResponseFru] = Field(default_factory=list)
    controller_memory_size: int = 0
    controller_over_temperature: str = ""
    date: str = ""
    external_cache_is_enabled: bool = False
    external_cache_is_hya_enabled: bool = False
    external_cache_is_rewarm_enabled: bool = False
    external_cache_pcs_size: int = 0
    ha_auto_giveback: bool = False
    ha_enabled: bool = False
    ha_giveback_failure_code: int = 0
    ha_giveback_failure_message: str = ""
    ha_giveback_state: str = ""
    ha_giveback_status: list[OntapNodeResponseStatus] = Field(default_factory=list)
    ha_interconnect_adapter: str = ""
    ha_interconnect_state: str = ""
    ha_partners: list[OntapNodeResponsePartner] = Field(default_factory=list)
    ha_ports: list[OntapNodeResponsePort] = Field(default_factory=list)
    ha_takeover_failure_code: int = 0
    ha_takeover_failure_message: str = ""
    ha_takeover_state: str = ""
    ha_takeover_check_reasons: list[str] = Field(default_factory=list)
    ha_takeover_check_takeover_possible: bool = False
    hw_assist_status_enabled: bool = False
    hw_assist_status_local_ip: str = ""
    hw_assist_status_local_port: int = 0
    hw_assist_status_local_state: str = ""
    hw_assist_status_partner_ip: str = ""
    hw_assist_status_partner_port: int = 0
    hw_assist_status_partner_state: str = ""
    is_spares_low: bool = False
    location: str = ""
    management_interface_ip_address: str = ""
    management_interfaces: list[OntapNodeResponseManagementInterface] = Field(default_factory=list)
    membership: str = ""
    metric_duration: str = ""
    metric_processor_utilization: int = 0
    metric_status: str = ""
    metric_timestamp: str = ""
    metric_uuid: str = ""
    metrocluster_custom_vlan_capable: bool = False
    metrocluster_ports: list[OntapNodeResponsePort2] = Field(default_factory=list)
    metrocluster_type: str = ""
    model_: str = ""
    name: str = ""
    nvram_battery_state: str = ""
    nvram_id: int = 0
    owner: str = ""
    serial_number: str = ""
    service_processor_api_service_enabled: bool = False
    service_processor_api_service_limit_access: bool = False
    service_processor_api_service_port: int = 0
    service_processor_auto_config_ipv4_subnet: str = ""
    service_processor_auto_config_ipv6_subnet: str = ""
    service_processor_autoupdate_enabled: bool = False
    service_processor_backup_is_current: bool = False
    service_processor_backup_state: str = ""
    service_processor_backup_version: str = ""
    service_processor_dhcp_enabled: bool = False
    service_processor_firmware_version: str = ""
    service_processor_ipv4_interface_address: str = ""
    service_processor_ipv4_interface_enabled: bool = False
    service_processor_ipv4_interface_gateway: str = ""
    service_processor_ipv4_interface_netmask: str = ""
    service_processor_ipv4_interface_setup_state: str = ""
    service_processor_ipv6_interface_address: str = ""
    service_processor_ipv6_interface_enabled: bool = False
    service_processor_ipv6_interface_gateway: str = ""
    service_processor_ipv6_interface_is_ipv6_ra_enabled: bool = False
    service_processor_ipv6_interface_link_local_ip: str = ""
    service_processor_ipv6_interface_netmask: int = 0
    service_processor_ipv6_interface_router_ip: str = ""
    service_processor_ipv6_interface_setup_state: str = ""
    service_processor_is_ip_configured: bool = False
    service_processor_last_update_state: str = ""
    service_processor_link_status: str = ""
    service_processor_mac_address: str = ""
    service_processor_primary_is_current: bool = False
    service_processor_primary_state: str = ""
    service_processor_primary_version: str = ""
    service_processor_ssh_info_allowed_addresses: list[str] = Field(default_factory=list)
    service_processor_state: str = ""
    service_processor_type: str = ""
    service_processor_web_service_enabled: bool = False
    service_processor_web_service_limit_access: bool = False
    snaplock_compliance_clock_time: str = ""
    state: str = ""
    statistics_processor_utilization_base: int = 0
    statistics_processor_utilization_raw: int = 0
    statistics_status: str = ""
    statistics_timestamp: str = ""
    storage_configuration: str = ""
    system_aggregate_name: str = ""
    system_aggregate_uuid: str = ""
    system_id: str = ""
    system_machine_type: str = ""
    uptime: int = 0
    uuid: OntapUUID = ""
    vendor_serial_number: str = ""
    version_full: str = ""
    version_generation: int = 0
    version_major: int = 0
    version_minor: int = 0
    vm_provider_type: str = ""
