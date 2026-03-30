"""OntapKeyManagerConfig information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapKeyManagerConfig(OntapModel):
    """OntapKeyManagerConfig information."""

    cc_mode_enabled: bool = False
    cloud_kms_retry_count: int = 0
    health_monitor_policy_akv_enabled: bool = False
    health_monitor_policy_akv_manage_volume_offline: bool = False
    health_monitor_policy_aws_enabled: bool = False
    health_monitor_policy_aws_manage_volume_offline: bool = False
    health_monitor_policy_gcp_enabled: bool = False
    health_monitor_policy_gcp_manage_volume_offline: bool = False
    health_monitor_policy_ikp_enabled: bool = False
    health_monitor_policy_ikp_manage_volume_offline: bool = False
    health_monitor_policy_kmip_enabled: bool = False
    health_monitor_policy_kmip_manage_volume_offline: bool = False
    health_monitor_policy_okm_enabled: bool = False
    health_monitor_policy_okm_manage_volume_offline: bool = False
    health_monitor_polling_interval: int = 0
    passphrase: str = ""
