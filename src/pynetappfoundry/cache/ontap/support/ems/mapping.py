"""OntapEmsConfig type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.ems.model import OntapEmsConfig

ONTAPEMSCONFIG_MAPPING = TypeMapping(
    name="OntapEmsConfig",
    model_class=OntapEmsConfig,
    api_endpoint="/support/ems?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="mail_from",
        ),
        FieldMapping(
            cache_attr="mail_server",
        ),
        FieldMapping(
            cache_attr="mail_server_password",
        ),
        FieldMapping(
            cache_attr="mail_server_user",
        ),
        FieldMapping(
            cache_attr="proxy_password",
        ),
        FieldMapping(
            cache_attr="proxy_url",
        ),
        FieldMapping(
            cache_attr="proxy_user",
        ),
        FieldMapping(
            cache_attr="pubsub_enabled",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapEmsConfig", ONTAPEMSCONFIG_MAPPING)
