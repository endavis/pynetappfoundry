# ruff: noqa: E501
"""OntapSecurityKeyManager type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.security.key_managers.model import (
    OntapSecurityKeyManager,
    OntapSecurityKeyManagerServer,
    OntapSecurityKeyManagerServerCaCertificate,
)


def _transform_external_server_ca_certificates(
    record: dict[str, Any],
) -> list[OntapSecurityKeyManagerServerCaCertificate]:
    """Transform external.server_ca_certificates into OntapSecurityKeyManagerServerCaCertificate list."""
    return [
        OntapSecurityKeyManagerServerCaCertificate(**item)
        for item in record.get("external.server_ca_certificates", [])
    ]


def _transform_external_servers(record: dict[str, Any]) -> list[OntapSecurityKeyManagerServer]:
    """Transform external.servers into OntapSecurityKeyManagerServer list."""
    return [OntapSecurityKeyManagerServer(**item) for item in record.get("external.servers", [])]


ONTAPSECURITYKEYMANAGER_MAPPING = TypeMapping(
    name="OntapSecurityKeyManager",
    model_class=OntapSecurityKeyManager,
    api_endpoint="/security/key-managers?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="configuration_name",
            api_path="configuration.name",
        ),
        FieldMapping(
            cache_attr="configuration_uuid",
            api_path="configuration.uuid",
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="external_client_certificate_name",
            api_path="external.client_certificate.name",
        ),
        FieldMapping(
            cache_attr="external_client_certificate_uuid",
            api_path="external.client_certificate.uuid",
        ),
        FieldMapping(
            cache_attr="external_server_ca_certificates",
            transform=_transform_external_server_ca_certificates,
            default=[],
        ),
        FieldMapping(
            cache_attr="external_servers",
            transform=_transform_external_servers,
            default=[],
        ),
        FieldMapping(
            cache_attr="is_default_data_at_rest_encryption_disabled",
            api_path="is_default_data_at_rest_encryption_disabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="onboard_enabled",
            api_path="onboard.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="onboard_existing_passphrase",
            api_path="onboard.existing_passphrase",
        ),
        FieldMapping(
            cache_attr="onboard_key_backup",
            api_path="onboard.key_backup",
        ),
        FieldMapping(
            cache_attr="onboard_passphrase",
            api_path="onboard.passphrase",
        ),
        FieldMapping(
            cache_attr="onboard_synchronize",
            api_path="onboard.synchronize",
            default=False,
        ),
        FieldMapping(
            cache_attr="policy",
            api_path="policy",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="status_code",
            api_path="status.code",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="status_message",
            api_path="status.message",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="volume_encryption_code",
            api_path="volume_encryption.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="volume_encryption_message",
            api_path="volume_encryption.message",
        ),
        FieldMapping(
            cache_attr="volume_encryption_supported",
            api_path="volume_encryption.supported",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapSecurityKeyManager", ONTAPSECURITYKEYMANAGER_MAPPING)
