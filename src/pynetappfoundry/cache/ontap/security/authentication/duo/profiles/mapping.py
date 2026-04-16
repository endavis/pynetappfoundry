"""OntapDuo type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.authentication.duo.profiles.model import OntapDuo

ONTAPDUO_MAPPING = TypeMapping(
    name="OntapDuo",
    model_class=OntapDuo,
    api_endpoint="/security/authentication/duo/profiles?fields=*",
    api_type="ontap",
    identifier_field="owner.uuid",
    fields=(
        FieldMapping(
            cache_attr="api_host",
        ),
        FieldMapping(
            cache_attr="auto_push",
            default=False,
        ),
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="fail_mode",
        ),
        FieldMapping(
            cache_attr="fingerprint",
        ),
        FieldMapping(
            cache_attr="http_proxy",
        ),
        FieldMapping(
            cache_attr="integration_key",
        ),
        FieldMapping(
            cache_attr="is_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="max_prompts",
            default=0,
        ),
        FieldMapping(
            cache_attr="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
        ),
        FieldMapping(
            cache_attr="push_info",
            default=False,
        ),
        FieldMapping(
            cache_attr="secret_key",
        ),
        FieldMapping(
            cache_attr="status",
        ),
    ),
)

model_registry.register_mapping("OntapDuo", ONTAPDUO_MAPPING)
