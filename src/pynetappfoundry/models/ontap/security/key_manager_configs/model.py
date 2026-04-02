"""OntapKeyManagerConfig information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapKeyManagerConfigHealthMonitorPolicyAkv(OntapModel):
    """OntapKeyManagerConfigHealthMonitorPolicyAkv sub-model for akv."""

    enabled: bool = False
    manage_volume_offline: bool = False


class OntapKeyManagerConfigHealthMonitorPolicyAws(OntapModel):
    """OntapKeyManagerConfigHealthMonitorPolicyAws sub-model for aws."""

    enabled: bool = False
    manage_volume_offline: bool = False


class OntapKeyManagerConfigHealthMonitorPolicyGcp(OntapModel):
    """OntapKeyManagerConfigHealthMonitorPolicyGcp sub-model for gcp."""

    enabled: bool = False
    manage_volume_offline: bool = False


class OntapKeyManagerConfigHealthMonitorPolicyIkp(OntapModel):
    """OntapKeyManagerConfigHealthMonitorPolicyIkp sub-model for ikp."""

    enabled: bool = False
    manage_volume_offline: bool = False


class OntapKeyManagerConfigHealthMonitorPolicyKmip(OntapModel):
    """OntapKeyManagerConfigHealthMonitorPolicyKmip sub-model for kmip."""

    enabled: bool = False
    manage_volume_offline: bool = False


class OntapKeyManagerConfigHealthMonitorPolicyOkm(OntapModel):
    """OntapKeyManagerConfigHealthMonitorPolicyOkm sub-model for okm."""

    enabled: bool = False
    manage_volume_offline: bool = False


class OntapKeyManagerConfigHealthMonitorPolicy(OntapModel):
    """OntapKeyManagerConfigHealthMonitorPolicy sub-model for health_monitor_policy."""

    akv: OntapKeyManagerConfigHealthMonitorPolicyAkv = Field(
        default_factory=OntapKeyManagerConfigHealthMonitorPolicyAkv
    )
    aws: OntapKeyManagerConfigHealthMonitorPolicyAws = Field(
        default_factory=OntapKeyManagerConfigHealthMonitorPolicyAws
    )
    gcp: OntapKeyManagerConfigHealthMonitorPolicyGcp = Field(
        default_factory=OntapKeyManagerConfigHealthMonitorPolicyGcp
    )
    ikp: OntapKeyManagerConfigHealthMonitorPolicyIkp = Field(
        default_factory=OntapKeyManagerConfigHealthMonitorPolicyIkp
    )
    kmip: OntapKeyManagerConfigHealthMonitorPolicyKmip = Field(
        default_factory=OntapKeyManagerConfigHealthMonitorPolicyKmip
    )
    okm: OntapKeyManagerConfigHealthMonitorPolicyOkm = Field(
        default_factory=OntapKeyManagerConfigHealthMonitorPolicyOkm
    )


class OntapKeyManagerConfig(OntapModel):
    """OntapKeyManagerConfig information."""

    cc_mode_enabled: bool = False
    cloud_kms_retry_count: int = 0
    health_monitor_policy: OntapKeyManagerConfigHealthMonitorPolicy = Field(
        default_factory=OntapKeyManagerConfigHealthMonitorPolicy
    )
    health_monitor_polling_interval: int = 0
    passphrase: str = ""
