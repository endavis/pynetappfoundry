"""OntapHostsSettings type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.name_services.cache.host.settings.model import OntapHostsSettings

ONTAPHOSTSSETTINGS_MAPPING = TypeMapping(
    name="OntapHostsSettings",
    model_class=OntapHostsSettings,
    api_endpoint="/name-services/cache/host/settings?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="dns_ttl_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="negative_cache_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="negative_ttl",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="ttl",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapHostsSettings", ONTAPHOSTSSETTINGS_MAPPING)
