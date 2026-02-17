"""OntapGlobalCacheSetting type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.name_services.cache.setting.model import OntapGlobalCacheSetting

ONTAPGLOBALCACHESETTING_MAPPING = TypeMapping(
    name="OntapGlobalCacheSetting",
    model_class=OntapGlobalCacheSetting,
    api_endpoint="/name-services/cache/setting?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="eviction_time_interval",
            api_path="eviction_time_interval",
        ),
        FieldMapping(
            cache_attr="remote_fetch_enabled",
            api_path="remote_fetch_enabled",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapGlobalCacheSetting", ONTAPGLOBALCACHESETTING_MAPPING)
