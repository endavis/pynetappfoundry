"""OntapSecurityConfig type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.model import OntapSecurityConfig

ONTAPSECURITYCONFIG_MAPPING = TypeMapping(
    name="OntapSecurityConfig",
    model_class=OntapSecurityConfig,
    api_endpoint="/security?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="fips.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="management_protocols.rsh_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="management_protocols.telnet_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="onboard_key_manager_configurable_status.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="onboard_key_manager_configurable_status.message",
        ),
        FieldMapping(
            cache_attr="onboard_key_manager_configurable_status.supported",
            default=False,
        ),
        FieldMapping(
            cache_attr="software_data_encryption.conversion_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="software_data_encryption.disabled_by_default",
            default=False,
        ),
        FieldMapping(
            cache_attr="software_data_encryption.encryption_state",
        ),
        FieldMapping(
            cache_attr="software_data_encryption.rekey",
            default=False,
        ),
        FieldMapping(
            cache_attr="tls.cipher_suites",
            default=[],
        ),
        FieldMapping(
            cache_attr="tls.protocol_versions",
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapSecurityConfig", ONTAPSECURITYCONFIG_MAPPING)
