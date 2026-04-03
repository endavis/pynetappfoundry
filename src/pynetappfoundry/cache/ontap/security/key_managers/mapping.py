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
        ),
        FieldMapping(
            cache_attr="configuration.uuid",
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="external.client_certificate.name",
        ),
        FieldMapping(
            cache_attr="external.client_certificate.uuid",
        ),
        FieldMapping(
            cache_attr="external.server_ca_certificates",
            transform=_transform_external_server_ca_certificates,
            default=[],
        ),
        FieldMapping(
            cache_attr="external.servers",
            transform=_transform_external_servers,
            default=[],
        ),
        FieldMapping(
            cache_attr="is_default_data_at_rest_encryption_disabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="onboard.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="onboard.existing_passphrase",
        ),
        FieldMapping(
            cache_attr="onboard.key_backup",
        ),
        FieldMapping(
            cache_attr="onboard.passphrase",
        ),
        FieldMapping(
            cache_attr="onboard.synchronize",
            default=False,
        ),
        FieldMapping(
            cache_attr="policy",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="status.code",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="status.message",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="volume_encryption.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="volume_encryption.message",
        ),
        FieldMapping(
            cache_attr="volume_encryption.supported",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapSecurityKeyManager", ONTAPSECURITYKEYMANAGER_MAPPING)
