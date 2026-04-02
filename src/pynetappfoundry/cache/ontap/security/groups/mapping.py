"""OntapSecurityGroup type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.groups.model import OntapSecurityGroup

ONTAPSECURITYGROUP_MAPPING = TypeMapping(
    name="OntapSecurityGroup",
    model_class=OntapSecurityGroup,
    api_endpoint="/security/groups?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="create_time",
            api_path="create_time",
        ),
        FieldMapping(
            cache_attr="id",
            api_path="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="owner.name",
            api_path="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
            api_path="owner.uuid",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSecurityGroup", ONTAPSECURITYGROUP_MAPPING)
