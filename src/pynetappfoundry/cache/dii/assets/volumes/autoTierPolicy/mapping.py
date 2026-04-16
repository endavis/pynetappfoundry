"""DiiAssetsVolumesAutotierpolicy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.volumes.autoTierPolicy.model import (
    DiiAssetsVolumesAutotierpolicy,
)

DIIASSETSVOLUMESAUTOTIERPOLICY_MAPPING = TypeMapping(
    name="DiiAssetsVolumesAutotierpolicy",
    model_class=DiiAssetsVolumesAutotierpolicy,
    api_endpoint="/assets/volumes/{id}/autoTierPolicy",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="value",
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsVolumesAutotierpolicy", DIIASSETSVOLUMESAUTOTIERPOLICY_MAPPING
)
