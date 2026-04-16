"""DiiAssetsHostsDatacenter type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.hosts.dataCenter.model import DiiAssetsHostsDatacenter

DIIASSETSHOSTSDATACENTER_MAPPING = TypeMapping(
    name="DiiAssetsHostsDatacenter",
    model_class=DiiAssetsHostsDatacenter,
    api_endpoint="/assets/hosts/{id}/dataCenter",
    api_type="dii",
    parent_mapping="DiiAssetsHost",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="value",
        ),
    ),
)

model_registry.register_mapping("DiiAssetsHostsDatacenter", DIIASSETSHOSTSDATACENTER_MAPPING)
