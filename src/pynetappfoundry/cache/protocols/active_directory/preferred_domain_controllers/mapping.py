"""OntapActiveDirectoryPreferredDc type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.protocols.active_directory.preferred_domain_controllers.model import (
    OntapActiveDirectoryPreferredDc,
)

ONTAPACTIVEDIRECTORYPREFERREDDC_MAPPING = TypeMapping(
    name="OntapActiveDirectoryPreferredDc",
    model_class=OntapActiveDirectoryPreferredDc,
    api_endpoint="/protocols/active-directory/{svm.uuid}/preferred-domain-controllers?fields=*",
    api_type="ontap",
    parent_mapping="OntapActiveDirectory",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="fqdn",
            api_path="fqdn",
        ),
        FieldMapping(
            cache_attr="server_ip",
            api_path="server_ip",
        ),
    ),
)

model_registry.register_mapping(
    "OntapActiveDirectoryPreferredDc", ONTAPACTIVEDIRECTORYPREFERREDDC_MAPPING
)
