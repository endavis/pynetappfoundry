"""OntapNetgroupsSettings type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.name_services.cache.netgroup.settings.model import OntapNetgroupsSettings

ONTAPNETGROUPSSETTINGS_MAPPING = TypeMapping(
    name="OntapNetgroupsSettings",
    model_class=OntapNetgroupsSettings,
    api_endpoint="/name-services/cache/netgroup/settings?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="negative_cache_enabled_byhost",
            api_path="negative_cache_enabled_byhost",
            default=False,
        ),
        FieldMapping(
            cache_attr="negative_ttl_byhost",
            api_path="negative_ttl_byhost",
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
            cache_attr="ttl_byhost",
            api_path="ttl_byhost",
        ),
        FieldMapping(
            cache_attr="ttl_for_members",
            api_path="ttl_for_members",
        ),
    ),
)

model_registry.register_mapping("OntapNetgroupsSettings", ONTAPNETGROUPSSETTINGS_MAPPING)
