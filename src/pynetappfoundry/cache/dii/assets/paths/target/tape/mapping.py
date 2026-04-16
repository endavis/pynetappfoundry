"""DiiAssetsPathsTargetTape type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.paths.target.tape.model import DiiAssetsPathsTargetTape

DIIASSETSPATHSTARGETTAPE_MAPPING = TypeMapping(
    name="DiiAssetsPathsTargetTape",
    model_class=DiiAssetsPathsTargetTape,
    api_endpoint="/assets/paths/{id}/target/tape",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="serialNumber",
        ),
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="vendor",
        ),
        FieldMapping(
            cache_attr="ip",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="fcPortCount",
            default=0,
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="isActive",
            default=False,
        ),
    ),
)

model_registry.register_mapping("DiiAssetsPathsTargetTape", DIIASSETSPATHSTARGETTAPE_MAPPING)
