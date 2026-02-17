"""OntapSecurityConfig type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.security.model import OntapSecurityConfig

ONTAPSECURITYCONFIG_MAPPING = TypeMapping(
    name="OntapSecurityConfig",
    model_class=OntapSecurityConfig,
    api_endpoint="/security?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="fips_enabled",
            api_path="fips.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="management_protocols_rsh_enabled",
            api_path="management_protocols.rsh_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="management_protocols_telnet_enabled",
            api_path="management_protocols.telnet_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="onboard_key_manager_configurable_status_code",
            api_path="onboard_key_manager_configurable_status.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="onboard_key_manager_configurable_status_message",
            api_path="onboard_key_manager_configurable_status.message",
        ),
        FieldMapping(
            cache_attr="onboard_key_manager_configurable_status_supported",
            api_path="onboard_key_manager_configurable_status.supported",
            default=False,
        ),
        FieldMapping(
            cache_attr="software_data_encryption_conversion_enabled",
            api_path="software_data_encryption.conversion_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="software_data_encryption_disabled_by_default",
            api_path="software_data_encryption.disabled_by_default",
            default=False,
        ),
        FieldMapping(
            cache_attr="software_data_encryption_encryption_state",
            api_path="software_data_encryption.encryption_state",
        ),
        FieldMapping(
            cache_attr="software_data_encryption_rekey",
            api_path="software_data_encryption.rekey",
            default=False,
        ),
        FieldMapping(
            cache_attr="tls_cipher_suites",
            api_path="tls.cipher_suites",
            default=[],
        ),
        FieldMapping(
            cache_attr="tls_protocol_versions",
            api_path="tls.protocol_versions",
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapSecurityConfig", ONTAPSECURITYCONFIG_MAPPING)
