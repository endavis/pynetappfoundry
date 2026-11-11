"""OntapPortset type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.portsets.model import (
    OntapPortset,
    OntapPortsetIgroup,
    OntapPortsetInterface,
)

ONTAPPORTSET_MAPPING = TypeMapping(
    name="OntapPortset",
    model_class=OntapPortset,
    api_endpoint="/protocols/san/portsets?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="igroups",
            item_model=OntapPortsetIgroup,
            default=[],
        ),
        FieldMapping(
            cache_attr="interfaces",
            item_model=OntapPortsetInterface,
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="protocol",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapPortset", ONTAPPORTSET_MAPPING)
