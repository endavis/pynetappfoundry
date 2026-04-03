"""OntapLocalHost type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.name_services.local_hosts.model import OntapLocalHost

ONTAPLOCALHOST_MAPPING = TypeMapping(
    name="OntapLocalHost",
    model_class=OntapLocalHost,
    api_endpoint="/name-services/local-hosts?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="address",
        ),
        FieldMapping(
            cache_attr="aliases",
            default=[],
        ),
        FieldMapping(
            cache_attr="hostname",
        ),
        FieldMapping(
            cache_attr="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
    ),
)

model_registry.register_mapping("OntapLocalHost", ONTAPLOCALHOST_MAPPING)
