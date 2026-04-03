"""OntapVvolBinding type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.vvol_bindings.model import OntapVvolBinding

ONTAPVVOLBINDING_MAPPING = TypeMapping(
    name="OntapVvolBinding",
    model_class=OntapVvolBinding,
    api_endpoint="/protocols/san/vvol-bindings?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="count",
            default=0,
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="is_optimal",
            default=False,
        ),
        FieldMapping(
            cache_attr="protocol_endpoint.name",
        ),
        FieldMapping(
            cache_attr="protocol_endpoint.uuid",
        ),
        FieldMapping(
            cache_attr="secondary_id",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="vvol.name",
        ),
        FieldMapping(
            cache_attr="vvol.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapVvolBinding", ONTAPVVOLBINDING_MAPPING)
