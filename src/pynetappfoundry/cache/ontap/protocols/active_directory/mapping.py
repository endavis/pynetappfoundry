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
    identifier_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="discovered_servers",
            transform=_transform_discovered_servers,
            default=[],
        ),
        FieldMapping(
            cache_attr="force_account_overwrite",
            default=False,
        ),
        FieldMapping(
            cache_attr="fqdn",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="organizational_unit",
        ),
        FieldMapping(
            cache_attr="password",
        ),
        FieldMapping(
            cache_attr="preferred_dcs",
            transform=_transform_preferred_dcs,
            default=[],
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="username",
        ),
    ),
)

model_registry.register_mapping("OntapActiveDirectory", ONTAPACTIVEDIRECTORY_MAPPING)
