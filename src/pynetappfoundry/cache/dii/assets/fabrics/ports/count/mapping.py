"""DiiAssetsFabricsPortsCount type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.fabrics.ports.count.model import DiiAssetsFabricsPortsCount

DIIASSETSFABRICSPORTSCOUNT_MAPPING = TypeMapping(
    name="DiiAssetsFabricsPortsCount",
    model_class=DiiAssetsFabricsPortsCount,
    api_endpoint="/assets/fabrics/{id}/ports/count",
    api_type="dii",
    parent_mapping="DiiAssetsFabric",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="value",
            default=0,
        ),
    ),
)

model_registry.register_mapping("DiiAssetsFabricsPortsCount", DIIASSETSFABRICSPORTSCOUNT_MAPPING)
