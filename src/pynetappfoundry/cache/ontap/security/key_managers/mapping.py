# ruff: noqa: E501
"""OntapSecurityKeyManager type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.key_managers.model import (
    OntapSecurityKeyManager,
    OntapSecurityKeyManagerExternalServer,
    OntapSecurityKeyManagerExternalServerCaCertificate,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_external_server_ca_certificates(
    record: dict[str, Any],
) -> list[OntapSecurityKeyManagerExternalServerCaCertificate]:
    """Transform external.server_ca_certificates into OntapSecurityKeyManagerExternalServerCaCertificate list."""
    try:
        items = get_nested_value(record, "external.server_ca_certificates")
    except Exception:
        items = []
    return [OntapSecurityKeyManagerExternalServerCaCertificate(**item) for item in items]


def _transform_external_servers(
    record: dict[str, Any],
) -> list[OntapSecurityKeyManagerExternalServer]:
    """Transform external.servers into OntapSecurityKeyManagerExternalServer list."""
    try:
        items = get_nested_value(record, "external.servers")
    except Exception:
        items = []
    return [OntapSecurityKeyManagerExternalServer(**item) for item in items]


ONTAPSECURITYKEYMANAGER_MAPPING = TypeMapping(
    name="OntapSecurityKeyManager",
    model_class=OntapSecurityKeyManager,
    api_endpoint="/security/key-managers?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="configuration.name",
            api_path="configuration.name",
        ),
        FieldMapping(
            cache_attr="configuration.uuid",
            api_path="configuration.uuid",
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="external.client_certificate.name",
            api_path="external.client_certificate.name",
        ),
        FieldMapping(
            cache_attr="external.client_certificate.uuid",
            api_path="external.client_certificate.uuid",
        ),
        FieldMapping(
            cache_attr="external.server_ca_certificates",
            api_path="external.server_ca_certificates",
            transform=_transform_external_server_ca_certificates,
            default=[],
        ),
        FieldMapping(
            cache_attr="external.servers",
            api_path="external.servers",
            transform=_transform_external_servers,
            default=[],
        ),
        FieldMapping(
            cache_attr="is_default_data_at_rest_encryption_disabled",
            api_path="is_default_data_at_rest_encryption_disabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="onboard.enabled",
            api_path="onboard.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="onboard.existing_passphrase",
            api_path="onboard.existing_passphrase",
        ),
        FieldMapping(
            cache_attr="onboard.key_backup",
            api_path="onboard.key_backup",
        ),
        FieldMapping(
            cache_attr="onboard.passphrase",
            api_path="onboard.passphrase",
        ),
        FieldMapping(
            cache_attr="onboard.synchronize",
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
            cache_attr="status.code",
            api_path="status.code",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="status.message",
            api_path="status.message",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="volume_encryption.code",
            api_path="volume_encryption.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="volume_encryption.message",
            api_path="volume_encryption.message",
        ),
        FieldMapping(
            cache_attr="volume_encryption.supported",
            api_path="volume_encryption.supported",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapSecurityKeyManager", ONTAPSECURITYKEYMANAGER_MAPPING)
