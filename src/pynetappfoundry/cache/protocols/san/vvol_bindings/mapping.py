"""OntapVvolBinding type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.protocols.san.vvol_bindings.model import OntapVvolBinding

ONTAPVVOLBINDING_MAPPING = TypeMapping(
    name="OntapVvolBinding",
    model_class=OntapVvolBinding,
    api_endpoint="/protocols/san/vvol-bindings?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="count",
            api_path="count",
            default=0,
        ),
        FieldMapping(
            cache_attr="id",
            api_path="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="is_optimal",
            api_path="is_optimal",
            default=False,
        ),
        FieldMapping(
            cache_attr="protocol_endpoint_name",
            api_path="protocol_endpoint.name",
        ),
        FieldMapping(
            cache_attr="protocol_endpoint_uuid",
            api_path="protocol_endpoint.uuid",
        ),
        FieldMapping(
            cache_attr="secondary_id",
            api_path="secondary_id",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="vvol_name",
            api_path="vvol.name",
        ),
        FieldMapping(
            cache_attr="vvol_uuid",
            api_path="vvol.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapVvolBinding", ONTAPVVOLBINDING_MAPPING)
