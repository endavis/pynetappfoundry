"""OntapSecurityConfig information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSecurityConfig(OntapModel):
    """OntapSecurityConfig information."""

    fips_enabled: bool = False
    management_protocols_rsh_enabled: bool = False
    management_protocols_telnet_enabled: bool = False
    onboard_key_manager_configurable_status_code: int = 0
    onboard_key_manager_configurable_status_message: str = ""
    onboard_key_manager_configurable_status_supported: bool = False
    software_data_encryption_conversion_enabled: bool = False
    software_data_encryption_disabled_by_default: bool = False
    software_data_encryption_encryption_state: str = ""
    software_data_encryption_rekey: bool = False
    tls_cipher_suites: list[str] = Field(default_factory=list)
    tls_protocol_versions: list[str] = Field(default_factory=list)
