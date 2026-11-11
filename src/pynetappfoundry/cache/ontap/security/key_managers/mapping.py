"""OntapSecurityKeyManager type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.key_managers.model import (
    OntapSecurityKeyManager,
    OntapSecurityKeyManagerExternalServer,
    OntapSecurityKeyManagerExternalServerCaCertificate,
)

ONTAPSECURITYKEYMANAGER_MAPPING = TypeMapping(
    name="OntapSecurityKeyManager",
    model_class=OntapSecurityKeyManager,
    api_endpoint="/security/key-managers?fields=*",
    api_type="ontap",
    identifier_field="uuid",
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
            item_model=OntapSecurityKeyManagerExternalServerCaCertificate,
            default=[],
        ),
        FieldMapping(
            cache_attr="external.servers",
            item_model=OntapSecurityKeyManagerExternalServer,
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
