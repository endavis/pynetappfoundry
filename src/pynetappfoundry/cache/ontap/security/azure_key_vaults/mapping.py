"""OntapAzureKeyVault type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.security.azure_key_vaults.model import (
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
    fields=(
        FieldMapping(
            cache_attr="authentication_method",
            api_path="authentication_method",
        ),
        FieldMapping(
            cache_attr="azure_reachability_code",
            api_path="azure_reachability.code",
        ),
        FieldMapping(
            cache_attr="azure_reachability_message",
            api_path="azure_reachability.message",
        ),
        FieldMapping(
            cache_attr="azure_reachability_reachable",
            api_path="azure_reachability.reachable",
            default=False,
        ),
        FieldMapping(
            cache_attr="client_certificate",
            api_path="client_certificate",
        ),
        FieldMapping(
            cache_attr="client_id",
            api_path="client_id",
        ),
        FieldMapping(
            cache_attr="client_secret",
            api_path="client_secret",
        ),
        FieldMapping(
            cache_attr="configuration_name",
            api_path="configuration.name",
        ),
        FieldMapping(
            cache_attr="configuration_uuid",
            api_path="configuration.uuid",
        ),
        FieldMapping(
            cache_attr="ekmip_reachability",
            api_path="ekmip_reachability",
            transform=_transform_ekmip_reachability,
            default=[],
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="key_id",
            api_path="key_id",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="oauth_host",
            api_path="oauth_host",
        ),
        FieldMapping(
            cache_attr="port",
            api_path="port",
            default=0,
        ),
        FieldMapping(
            cache_attr="proxy_host",
            api_path="proxy_host",
        ),
        FieldMapping(
            cache_attr="proxy_password",
            api_path="proxy_password",
        ),
        FieldMapping(
            cache_attr="proxy_port",
            api_path="proxy_port",
            default=0,
        ),
        FieldMapping(
            cache_attr="proxy_type",
            api_path="proxy_type",
        ),
        FieldMapping(
            cache_attr="proxy_username",
            api_path="proxy_username",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="skip_verification",
            api_path="skip_verification",
            default=False,
        ),
        FieldMapping(
            cache_attr="state_available",
            api_path="state.available",
            default=False,
        ),
        FieldMapping(
            cache_attr="state_code",
            api_path="state.code",
        ),
        FieldMapping(
            cache_attr="state_message",
            api_path="state.message",
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
            cache_attr="tenant_id",
            api_path="tenant_id",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="vault_host",
            api_path="vault_host",
        ),
        FieldMapping(
            cache_attr="verify_host",
            api_path="verify_host",
            default=False,
        ),
        FieldMapping(
            cache_attr="verify_ip",
            api_path="verify_ip",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapAzureKeyVault", ONTAPAZUREKEYVAULT_MAPPING)
