"""OntapActiveDirectory type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.active_directory.model import (
    OntapActiveDirectory,
    OntapActiveDirectoryDiscoveredServer,
    OntapActiveDirectoryPreferredDc,
)


def _transform_discovered_servers(
    record: dict[str, Any],
) -> list[OntapActiveDirectoryDiscoveredServer]:
    """Transform discovered_servers into OntapActiveDirectoryDiscoveredServer list."""
    return [
        OntapActiveDirectoryDiscoveredServer(**item)
        for item in record.get("discovered_servers", [])
    ]


def _transform_preferred_dcs(record: dict[str, Any]) -> list[OntapActiveDirectoryPreferredDc]:
    """Transform preferred_dcs into OntapActiveDirectoryPreferredDc list."""
    return [OntapActiveDirectoryPreferredDc(**item) for item in record.get("preferred_dcs", [])]


ONTAPACTIVEDIRECTORY_MAPPING = TypeMapping(
    name="OntapActiveDirectory",
    model_class=OntapActiveDirectory,
    api_endpoint="/protocols/active-directory?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="discovered_servers",
            api_path="discovered_servers",
            transform=_transform_discovered_servers,
            default=[],
        ),
        FieldMapping(
            cache_attr="force_account_overwrite",
            api_path="force_account_overwrite",
            default=False,
        ),
        FieldMapping(
            cache_attr="fqdn",
            api_path="fqdn",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="organizational_unit",
            api_path="organizational_unit",
        ),
        FieldMapping(
            cache_attr="password",
            api_path="password",
        ),
        FieldMapping(
            cache_attr="preferred_dcs",
            api_path="preferred_dcs",
            transform=_transform_preferred_dcs,
            default=[],
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
            cache_attr="username",
            api_path="username",
        ),
    ),
)

model_registry.register_mapping("OntapActiveDirectory", ONTAPACTIVEDIRECTORY_MAPPING)
