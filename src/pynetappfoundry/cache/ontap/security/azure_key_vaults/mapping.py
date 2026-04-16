"""OntapAzureKeyVault type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.azure_key_vaults.model import (
    OntapAzureKeyVault,
    OntapAzureKeyVaultEkmipReachability,
)


def _transform_ekmip_reachability(
    record: dict[str, Any],
) -> list[OntapAzureKeyVaultEkmipReachability]:
    """Transform ekmip_reachability into OntapAzureKeyVaultEkmipReachability list."""
    return [
        OntapAzureKeyVaultEkmipReachability(**item) for item in record.get("ekmip_reachability", [])
    ]


ONTAPAZUREKEYVAULT_MAPPING = TypeMapping(
    name="OntapAzureKeyVault",
    model_class=OntapAzureKeyVault,
    api_endpoint="/security/azure-key-vaults?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="authentication_method",
        ),
        FieldMapping(
            cache_attr="azure_reachability.code",
        ),
        FieldMapping(
            cache_attr="azure_reachability.message",
        ),
        FieldMapping(
            cache_attr="azure_reachability.reachable",
            default=False,
        ),
        FieldMapping(
            cache_attr="client_certificate",
        ),
        FieldMapping(
            cache_attr="client_id",
        ),
        FieldMapping(
            cache_attr="client_secret",
        ),
        FieldMapping(
            cache_attr="configuration.name",
        ),
        FieldMapping(
            cache_attr="configuration.uuid",
        ),
        FieldMapping(
            cache_attr="ekmip_reachability",
            transform=_transform_ekmip_reachability,
            default=[],
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="key_id",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="oauth_host",
        ),
        FieldMapping(
            cache_attr="port",
            default=0,
        ),
        FieldMapping(
            cache_attr="proxy_host",
        ),
        FieldMapping(
            cache_attr="proxy_password",
        ),
        FieldMapping(
            cache_attr="proxy_port",
            default=0,
        ),
        FieldMapping(
            cache_attr="proxy_type",
        ),
        FieldMapping(
            cache_attr="proxy_username",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="skip_verification",
            default=False,
        ),
        FieldMapping(
            cache_attr="state.available",
            default=False,
        ),
        FieldMapping(
            cache_attr="state.code",
        ),
        FieldMapping(
            cache_attr="state.message",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="tenant_id",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="vault_host",
        ),
        FieldMapping(
            cache_attr="verify_host",
            default=False,
        ),
        FieldMapping(
            cache_attr="verify_ip",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapAzureKeyVault", ONTAPAZUREKEYVAULT_MAPPING)
