"""OntapActiveDirectory type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.active_directory.model import (
    OntapActiveDirectory,
    OntapActiveDirectoryDiscoveredServer,
    OntapActiveDirectoryPreferredDc,
)

ONTAPACTIVEDIRECTORY_MAPPING = TypeMapping(
    name="OntapActiveDirectory",
    model_class=OntapActiveDirectory,
    api_endpoint="/protocols/active-directory?fields=*",
    api_type="ontap",
    identifier_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="discovered_servers",
            item_model=OntapActiveDirectoryDiscoveredServer,
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
            item_model=OntapActiveDirectoryPreferredDc,
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
