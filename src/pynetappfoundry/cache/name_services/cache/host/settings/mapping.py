"""OntapHostsSettings type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.name_services.cache.host.settings.model import OntapHostsSettings

ONTAPHOSTSSETTINGS_MAPPING = TypeMapping(
    name="OntapHostsSettings",
    model_class=OntapHostsSettings,
    api_endpoint="/name-services/cache/host/settings?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="dns_ttl_enabled",
            api_path="dns_ttl_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="negative_cache_enabled",
            api_path="negative_cache_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="negative_ttl",
            api_path="negative_ttl",
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
            cache_attr="ttl",
            api_path="ttl",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapHostsSettings", ONTAPHOSTSSETTINGS_MAPPING)
