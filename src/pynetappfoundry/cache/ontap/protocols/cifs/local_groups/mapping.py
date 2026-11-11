"""OntapLocalCifsGroup type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.local_groups.model import (
    OntapLocalCifsGroup,
    OntapLocalCifsGroupMember,
)

ONTAPLOCALCIFSGROUP_MAPPING = TypeMapping(
    name="OntapLocalCifsGroup",
    model_class=OntapLocalCifsGroup,
    api_endpoint="/protocols/cifs/local-groups?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="members",
            item_model=OntapLocalCifsGroupMember,
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="sid",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapLocalCifsGroup", ONTAPLOCALCIFSGROUP_MAPPING)
