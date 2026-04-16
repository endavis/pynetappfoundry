"""OntapNtpKey type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.ntp.keys.model import OntapNtpKey

ONTAPNTPKEY_MAPPING = TypeMapping(
    name="OntapNtpKey",
    model_class=OntapNtpKey,
    api_endpoint="/cluster/ntp/keys?fields=*",
    api_type="ontap",
    identifier_field="id",
    fields=(
        FieldMapping(
            cache_attr="digest_type",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="value",
        ),
    ),
)

model_registry.register_mapping("OntapNtpKey", ONTAPNTPKEY_MAPPING)
