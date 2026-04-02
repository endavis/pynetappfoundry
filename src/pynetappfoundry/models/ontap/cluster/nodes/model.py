"""OntapNodeResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapNodeResponseClusterInterfaceIp(OntapModel):
    """OntapNodeResponseClusterInterfaceIp sub-model for ip."""

    address: str = ""


class OntapNodeResponseClusterInterface(OntapModel):
    """OntapNodeResponseClusterInterface sub-model for cluster_interface."""

    ip: OntapNodeResponseClusterInterfaceIp = Field(
        default_factory=OntapNodeResponseClusterInterfaceIp
    )


class OntapNodeResponseClusterInterface2Ip(OntapModel):
    """OntapNodeResponseClusterInterface2Ip sub-model for ip."""

    address: str = ""


class OntapNodeResponseClusterInterface2(OntapModel):
    """OntapNodeResponseClusterInterface2 sub-model for cluster_interfaces."""

    ip: OntapNodeResponseClusterInterface2Ip = Field(
        default_factory=OntapNodeResponseClusterInterface2Ip
    )
    name: str = ""
    uuid: str = ""


class OntapNodeResponseControllerCpu(OntapModel):
    """OntapNodeResponseControllerCpu sub-model for cpu."""

    count: int = 0
    firmware_release: str = ""
    processor: str = ""


class OntapNodeResponseControllerFailedFanMessage(OntapModel):
    """OntapNodeResponseControllerFailedFanMessage sub-model for message."""

    code: str = ""
    message: str = ""


class OntapNodeResponseControllerFailedFan(OntapModel):
    """OntapNodeResponseControllerFailedFan sub-model for failed_fan."""

    count: int = 0
    message: OntapNodeResponseControllerFailedFanMessage = Field(
        default_factory=OntapNodeResponseControllerFailedFanMessage
    )


class OntapNodeResponseControllerFailedPowerSupplyMessage(OntapModel):
    """OntapNodeResponseControllerFailedPowerSupplyMessage sub-model for message."""

    code: str = ""
    message: str = ""


class OntapNodeResponseControllerFailedPowerSupply(OntapModel):
    """OntapNodeResponseControllerFailedPowerSupply sub-model for failed_power_supply."""

    count: int = 0
    message: OntapNodeResponseControllerFailedPowerSupplyMessage = Field(
        default_factory=OntapNodeResponseControllerFailedPowerSupplyMessage
    )


class OntapNodeResponseControllerFlashCache(OntapModel):
    """OntapNodeResponseControllerFlashCache sub-model for flash_cache."""

    capacity: int = 0
    device_id: int = 0
    firmware_file: str = ""
    firmware_version: str = ""
    hardware_revision: str = ""
    model_: str = ""
    part_number: str = ""
    serial_number: str = ""
    slot: str = ""
    state: str = ""


class OntapNodeResponseControllerFru(OntapModel):
    """OntapNodeResponseControllerFru sub-model for frus."""

    id: str = ""
    state: str = ""
    type_: str = ""


class OntapNodeResponseController(OntapModel):
    """OntapNodeResponseController sub-model for controller."""

    board: str = ""
    cpu: OntapNodeResponseControllerCpu = Field(default_factory=OntapNodeResponseControllerCpu)
    failed_fan: OntapNodeResponseControllerFailedFan = Field(
        default_factory=OntapNodeResponseControllerFailedFan
    )
    failed_power_supply: OntapNodeResponseControllerFailedPowerSupply = Field(
        default_factory=OntapNodeResponseControllerFailedPowerSupply
    )
    flash_cache: list[OntapNodeResponseControllerFlashCache] = Field(default_factory=list)
    frus: list[OntapNodeResponseControllerFru] = Field(default_factory=list)
    memory_size: int = 0
    over_temperature: str = ""


class OntapNodeResponseExternalCache(OntapModel):
    """OntapNodeResponseExternalCache sub-model for external_cache."""

    is_enabled: bool = False
    is_hya_enabled: bool = False
    is_rewarm_enabled: bool = False
    pcs_size: int = 0


class OntapNodeResponseHaGivebackFailure(OntapModel):
    """OntapNodeResponseHaGivebackFailure sub-model for failure."""

    code: int = 0
    message: str = ""


class OntapNodeResponseHaGivebackStatusAggregate(OntapModel):
    """OntapNodeResponseHaGivebackStatusAggregate sub-model for aggregate."""

    name: str = ""
    uuid: str = ""


class OntapNodeResponseHaGivebackStatusError(OntapModel):
    """OntapNodeResponseHaGivebackStatusError sub-model for error."""

    code: str = ""
    message: str = ""


class OntapNodeResponseHaGivebackStatus(OntapModel):
    """OntapNodeResponseHaGivebackStatus sub-model for status."""

    aggregate: OntapNodeResponseHaGivebackStatusAggregate = Field(
        default_factory=OntapNodeResponseHaGivebackStatusAggregate
    )
    error: OntapNodeResponseHaGivebackStatusError = Field(
        default_factory=OntapNodeResponseHaGivebackStatusError
    )
    state: str = ""


class OntapNodeResponseHaGiveback(OntapModel):
    """OntapNodeResponseHaGiveback sub-model for giveback."""

    failure: OntapNodeResponseHaGivebackFailure = Field(
        default_factory=OntapNodeResponseHaGivebackFailure
    )
    state: str = ""
    status: list[OntapNodeResponseHaGivebackStatus] = Field(default_factory=list)


class OntapNodeResponseHaInterconnect(OntapModel):
    """OntapNodeResponseHaInterconnect sub-model for interconnect."""

    adapter: str = ""
    state: str = ""


class OntapNodeResponseHaPartner(OntapModel):
    """OntapNodeResponseHaPartner sub-model for partners."""

    name: str = ""
    uuid: str = ""


class OntapNodeResponseHaPort(OntapModel):
    """OntapNodeResponseHaPort sub-model for ports."""

    number: int = 0
    state: str = ""


class OntapNodeResponseHaTakeoverFailure(OntapModel):
    """OntapNodeResponseHaTakeoverFailure sub-model for failure."""

    code: int = 0
    message: str = ""


class OntapNodeResponseHaTakeover(OntapModel):
    """OntapNodeResponseHaTakeover sub-model for takeover."""

    failure: OntapNodeResponseHaTakeoverFailure = Field(
        default_factory=OntapNodeResponseHaTakeoverFailure
    )
    state: str = ""


class OntapNodeResponseHaTakeoverCheck(OntapModel):
    """OntapNodeResponseHaTakeoverCheck sub-model for takeover_check."""

    reasons: list[str] = Field(default_factory=list)
    takeover_possible: bool = False


class OntapNodeResponseHa(OntapModel):
    """OntapNodeResponseHa sub-model for ha."""

    auto_giveback: bool = False
    enabled: bool = False
    giveback: OntapNodeResponseHaGiveback = Field(default_factory=OntapNodeResponseHaGiveback)
    interconnect: OntapNodeResponseHaInterconnect = Field(
        default_factory=OntapNodeResponseHaInterconnect
    )
    partners: list[OntapNodeResponseHaPartner] = Field(default_factory=list)
    ports: list[OntapNodeResponseHaPort] = Field(default_factory=list)
    takeover: OntapNodeResponseHaTakeover = Field(default_factory=OntapNodeResponseHaTakeover)
    takeover_check: OntapNodeResponseHaTakeoverCheck = Field(
        default_factory=OntapNodeResponseHaTakeoverCheck
    )


class OntapNodeResponseHwAssistStatusLocal(OntapModel):
    """OntapNodeResponseHwAssistStatusLocal sub-model for local."""

    ip: str = ""
    port: int = 0
    state: str = ""


class OntapNodeResponseHwAssistStatusPartner(OntapModel):
    """OntapNodeResponseHwAssistStatusPartner sub-model for partner."""

    ip: str = ""
    port: int = 0
    state: str = ""


class OntapNodeResponseHwAssistStatus(OntapModel):
    """OntapNodeResponseHwAssistStatus sub-model for status."""

    enabled: bool = False
    local: OntapNodeResponseHwAssistStatusLocal = Field(
        default_factory=OntapNodeResponseHwAssistStatusLocal
    )
    partner: OntapNodeResponseHwAssistStatusPartner = Field(
        default_factory=OntapNodeResponseHwAssistStatusPartner
    )


class OntapNodeResponseHwAssist(OntapModel):
    """OntapNodeResponseHwAssist sub-model for hw_assist."""

    status: OntapNodeResponseHwAssistStatus = Field(default_factory=OntapNodeResponseHwAssistStatus)


class OntapNodeResponseManagementInterfaceIp(OntapModel):
    """OntapNodeResponseManagementInterfaceIp sub-model for ip."""

    address: str = ""


class OntapNodeResponseManagementInterface(OntapModel):
    """OntapNodeResponseManagementInterface sub-model for management_interface."""

    ip: OntapNodeResponseManagementInterfaceIp = Field(
        default_factory=OntapNodeResponseManagementInterfaceIp
    )


class OntapNodeResponseManagementInterface2Ip(OntapModel):
    """OntapNodeResponseManagementInterface2Ip sub-model for ip."""

    address: str = ""


class OntapNodeResponseManagementInterface2(OntapModel):
    """OntapNodeResponseManagementInterface2 sub-model for management_interfaces."""

    ip: OntapNodeResponseManagementInterface2Ip = Field(
        default_factory=OntapNodeResponseManagementInterface2Ip
    )
    name: str = ""
    uuid: str = ""


class OntapNodeResponseMetric(OntapModel):
    """OntapNodeResponseMetric sub-model for metric."""

    duration: str = ""
    processor_utilization: int = 0
    status: str = ""
    timestamp: str = ""
    uuid: str = ""


class OntapNodeResponseMetroclusterPort(OntapModel):
    """OntapNodeResponseMetroclusterPort sub-model for ports."""

    name: str = ""


class OntapNodeResponseMetrocluster(OntapModel):
    """OntapNodeResponseMetrocluster sub-model for metrocluster."""

    custom_vlan_capable: bool = False
    ports: list[OntapNodeResponseMetroclusterPort] = Field(default_factory=list)
    type_: str = ""


class OntapNodeResponseNvram(OntapModel):
    """OntapNodeResponseNvram sub-model for nvram."""

    battery_state: str = ""
    id: int = 0


class OntapNodeResponseServiceProcessorApiService(OntapModel):
    """OntapNodeResponseServiceProcessorApiService sub-model for api_service."""

    enabled: bool = False
    limit_access: bool = False
    port: int = 0


class OntapNodeResponseServiceProcessorAutoConfig(OntapModel):
    """OntapNodeResponseServiceProcessorAutoConfig sub-model for auto_config."""

    ipv4_subnet: str = ""
    ipv6_subnet: str = ""


class OntapNodeResponseServiceProcessorBackup(OntapModel):
    """OntapNodeResponseServiceProcessorBackup sub-model for backup."""

    is_current: bool = False
    state: str = ""
    version: str = ""


class OntapNodeResponseServiceProcessorIpv4Interface(OntapModel):
    """OntapNodeResponseServiceProcessorIpv4Interface sub-model for ipv4_interface."""

    address: str = ""
    enabled: bool = False
    gateway: str = ""
    netmask: str = ""
    setup_state: str = ""


class OntapNodeResponseServiceProcessorIpv6Interface(OntapModel):
    """OntapNodeResponseServiceProcessorIpv6Interface sub-model for ipv6_interface."""

    address: str = ""
    enabled: bool = False
    gateway: str = ""
    is_ipv6_ra_enabled: bool = False
    link_local_ip: str = ""
    netmask: int = 0
    router_ip: str = ""
    setup_state: str = ""


class OntapNodeResponseServiceProcessorPrimary(OntapModel):
    """OntapNodeResponseServiceProcessorPrimary sub-model for primary."""

    is_current: bool = False
    state: str = ""
    version: str = ""


class OntapNodeResponseServiceProcessorSshInfo(OntapModel):
    """OntapNodeResponseServiceProcessorSshInfo sub-model for ssh_info."""

    allowed_addresses: list[str] = Field(default_factory=list)


class OntapNodeResponseServiceProcessorWebService(OntapModel):
    """OntapNodeResponseServiceProcessorWebService sub-model for web_service."""

    enabled: bool = False
    limit_access: bool = False


class OntapNodeResponseServiceProcessor(OntapModel):
    """OntapNodeResponseServiceProcessor sub-model for service_processor."""

    api_service: OntapNodeResponseServiceProcessorApiService = Field(
        default_factory=OntapNodeResponseServiceProcessorApiService
    )
    auto_config: OntapNodeResponseServiceProcessorAutoConfig = Field(
        default_factory=OntapNodeResponseServiceProcessorAutoConfig
    )
    autoupdate_enabled: bool = False
    backup: OntapNodeResponseServiceProcessorBackup = Field(
        default_factory=OntapNodeResponseServiceProcessorBackup
    )
    dhcp_enabled: bool = False
    firmware_version: str = ""
    ipv4_interface: OntapNodeResponseServiceProcessorIpv4Interface = Field(
        default_factory=OntapNodeResponseServiceProcessorIpv4Interface
    )
    ipv6_interface: OntapNodeResponseServiceProcessorIpv6Interface = Field(
        default_factory=OntapNodeResponseServiceProcessorIpv6Interface
    )
    is_ip_configured: bool = False
    last_update_state: str = ""
    link_status: str = ""
    mac_address: str = ""
    primary: OntapNodeResponseServiceProcessorPrimary = Field(
        default_factory=OntapNodeResponseServiceProcessorPrimary
    )
    ssh_info: OntapNodeResponseServiceProcessorSshInfo = Field(
        default_factory=OntapNodeResponseServiceProcessorSshInfo
    )
    state: str = ""
    type_: str = ""
    web_service: OntapNodeResponseServiceProcessorWebService = Field(
        default_factory=OntapNodeResponseServiceProcessorWebService
    )


class OntapNodeResponseSnaplock(OntapModel):
    """OntapNodeResponseSnaplock sub-model for snaplock."""

    compliance_clock_time: str = ""


class OntapNodeResponseStatistics(OntapModel):
    """OntapNodeResponseStatistics sub-model for statistics."""

    processor_utilization_base: int = 0
    processor_utilization_raw: int = 0
    status: str = ""
    timestamp: str = ""


class OntapNodeResponseSystemAggregate(OntapModel):
    """OntapNodeResponseSystemAggregate sub-model for system_aggregate."""

    name: str = ""
    uuid: str = ""


class OntapNodeResponseVersion(OntapModel):
    """OntapNodeResponseVersion sub-model for version."""

    full: str = ""
    generation: int = 0
    major: int = 0
    minor: int = 0


class OntapNodeResponseVm(OntapModel):
    """OntapNodeResponseVm sub-model for vm."""

    provider_type: str = ""


class OntapNodeResponse(OntapModel):
    """OntapNodeResponse information."""

    anti_ransomware_version: str = ""
    cluster_interface: OntapNodeResponseClusterInterface = Field(
        default_factory=OntapNodeResponseClusterInterface
    )
    cluster_interfaces: list[OntapNodeResponseClusterInterface2] = Field(default_factory=list)
    controller: OntapNodeResponseController = Field(default_factory=OntapNodeResponseController)
    date: str = ""
    external_cache: OntapNodeResponseExternalCache = Field(
        default_factory=OntapNodeResponseExternalCache
    )
    ha: OntapNodeResponseHa = Field(default_factory=OntapNodeResponseHa)
    hw_assist: OntapNodeResponseHwAssist = Field(default_factory=OntapNodeResponseHwAssist)
    is_spares_low: bool = False
    location: str = ""
    management_interface: OntapNodeResponseManagementInterface = Field(
        default_factory=OntapNodeResponseManagementInterface
    )
    management_interfaces: list[OntapNodeResponseManagementInterface2] = Field(default_factory=list)
    membership: str = ""
    metric: OntapNodeResponseMetric = Field(default_factory=OntapNodeResponseMetric)
    metrocluster: OntapNodeResponseMetrocluster = Field(
        default_factory=OntapNodeResponseMetrocluster
    )
    model_: str = ""
    name: str = ""
    nvram: OntapNodeResponseNvram = Field(default_factory=OntapNodeResponseNvram)
    owner: str = ""
    serial_number: str = ""
    service_processor: OntapNodeResponseServiceProcessor = Field(
        default_factory=OntapNodeResponseServiceProcessor
    )
    snaplock: OntapNodeResponseSnaplock = Field(default_factory=OntapNodeResponseSnaplock)
    state: str = ""
    statistics: OntapNodeResponseStatistics = Field(default_factory=OntapNodeResponseStatistics)
    storage_configuration: str = ""
    system_aggregate: OntapNodeResponseSystemAggregate = Field(
        default_factory=OntapNodeResponseSystemAggregate
    )
    system_id: str = ""
    system_machine_type: str = ""
    uptime: int = 0
    uuid: OntapUUID = ""
    vendor_serial_number: str = ""
    version: OntapNodeResponseVersion = Field(default_factory=OntapNodeResponseVersion)
    vm: OntapNodeResponseVm = Field(default_factory=OntapNodeResponseVm)
