"""OntapUnixUserSettings type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.name_services.cache.unix_user.settings.model import (
    OntapUnixUserSettings,
)

ONTAPUNIXUSERSETTINGS_MAPPING = TypeMapping(
    name="OntapUnixUserSettings",
    model_class=OntapUnixUserSettings,
    api_endpoint="/name-services/cache/unix-user/settings?fields=*",
    api_type="ontap",
    fields=(
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
            cache_attr="propagation_enabled",
            default=False,
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
    ),
)

model_registry.register_mapping("OntapUnixUserSettings", ONTAPUNIXUSERSETTINGS_MAPPING)
