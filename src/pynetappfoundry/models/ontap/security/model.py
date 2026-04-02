# ruff: noqa: E501
"""OntapSecurityConfig information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSecurityConfigFips(OntapModel):
    """OntapSecurityConfigFips sub-model for fips."""

    enabled: bool = False


class OntapSecurityConfigManagementProtocols(OntapModel):
    """OntapSecurityConfigManagementProtocols sub-model for management_protocols."""

    rsh_enabled: bool = False
    telnet_enabled: bool = False


class OntapSecurityConfigOnboardKeyManagerConfigurableStatus(OntapModel):
    """OntapSecurityConfigOnboardKeyManagerConfigurableStatus sub-model for onboard_key_manager_configurable_status."""

    code: int = 0
    message: str = ""
    supported: bool = False


class OntapSecurityConfigSoftwareDataEncryption(OntapModel):
    """OntapSecurityConfigSoftwareDataEncryption sub-model for software_data_encryption."""

    conversion_enabled: bool = False
    disabled_by_default: bool = False
    encryption_state: str = ""
    rekey: bool = False


class OntapSecurityConfigTls(OntapModel):
    """OntapSecurityConfigTls sub-model for tls."""

    cipher_suites: list[str] = Field(default_factory=list)
    protocol_versions: list[str] = Field(default_factory=list)


class OntapSecurityConfig(OntapModel):
    """OntapSecurityConfig information."""

    fips: OntapSecurityConfigFips = Field(default_factory=OntapSecurityConfigFips)
    management_protocols: OntapSecurityConfigManagementProtocols = Field(
        default_factory=OntapSecurityConfigManagementProtocols
    )
    onboard_key_manager_configurable_status: OntapSecurityConfigOnboardKeyManagerConfigurableStatus = Field(
        default_factory=OntapSecurityConfigOnboardKeyManagerConfigurableStatus
    )
    software_data_encryption: OntapSecurityConfigSoftwareDataEncryption = Field(
        default_factory=OntapSecurityConfigSoftwareDataEncryption
    )
    tls: OntapSecurityConfigTls = Field(default_factory=OntapSecurityConfigTls)
