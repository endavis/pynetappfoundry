"""OntapDuogroup type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.authentication.duo.groups.model import OntapDuogroup

ONTAPDUOGROUP_MAPPING = TypeMapping(
    name="OntapDuogroup",
    model_class=OntapDuogroup,
    api_endpoint="/security/authentication/duo/groups?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="excluded_users",
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapDuogroup", ONTAPDUOGROUP_MAPPING)
