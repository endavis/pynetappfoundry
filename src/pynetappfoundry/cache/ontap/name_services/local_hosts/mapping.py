"""OntapLocalHost type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.name_services.local_hosts.model import OntapLocalHost

ONTAPLOCALHOST_MAPPING = TypeMapping(
    name="OntapLocalHost",
    model_class=OntapLocalHost,
    api_endpoint="/name-services/local-hosts?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="address",
            api_path="address",
        ),
        FieldMapping(
            cache_attr="aliases",
            api_path="aliases",
            default=[],
        ),
        FieldMapping(
            cache_attr="hostname",
            api_path="hostname",
        ),
        FieldMapping(
            cache_attr="owner_name",
            api_path="owner.name",
        ),
        FieldMapping(
            cache_attr="owner_uuid",
            api_path="owner.uuid",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
    ),
)

model_registry.register_mapping("OntapLocalHost", ONTAPLOCALHOST_MAPPING)
