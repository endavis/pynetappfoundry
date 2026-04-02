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
    fields=(
        FieldMapping(
            cache_attr="api_host",
            api_path="api_host",
        ),
        FieldMapping(
            cache_attr="auto_push",
            api_path="auto_push",
            default=False,
        ),
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="fail_mode",
            api_path="fail_mode",
        ),
        FieldMapping(
            cache_attr="fingerprint",
            api_path="fingerprint",
        ),
        FieldMapping(
            cache_attr="http_proxy",
            api_path="http_proxy",
        ),
        FieldMapping(
            cache_attr="integration_key",
            api_path="integration_key",
        ),
        FieldMapping(
            cache_attr="is_enabled",
            api_path="is_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="max_prompts",
            api_path="max_prompts",
            default=0,
        ),
        FieldMapping(
            cache_attr="owner.name",
            api_path="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
            api_path="owner.uuid",
        ),
        FieldMapping(
            cache_attr="push_info",
            api_path="push_info",
            default=False,
        ),
        FieldMapping(
            cache_attr="secret_key",
            api_path="secret_key",
        ),
        FieldMapping(
            cache_attr="status",
            api_path="status",
        ),
    ),
)

model_registry.register_mapping("OntapDuo", ONTAPDUO_MAPPING)
