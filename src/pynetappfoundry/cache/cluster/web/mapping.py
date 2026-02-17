"""OntapWeb type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.cluster.web.model import OntapWeb
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping

ONTAPWEB_MAPPING = TypeMapping(
    name="OntapWeb",
    model_class=OntapWeb,
    api_endpoint="/cluster/web?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="certificate_name",
            api_path="certificate.name",
        ),
        FieldMapping(
            cache_attr="certificate_uuid",
            api_path="certificate.uuid",
        ),
        FieldMapping(
            cache_attr="client_enabled",
            api_path="client_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="csrf_protection_enabled",
            api_path="csrf.protection_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="csrf_token_concurrent_limit",
            api_path="csrf.token.concurrent_limit",
            default=0,
        ),
        FieldMapping(
            cache_attr="csrf_token_idle_timeout",
            api_path="csrf.token.idle_timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="csrf_token_max_timeout",
            api_path="csrf.token.max_timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="http_enabled",
            api_path="http_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="http_port",
            api_path="http_port",
            default=0,
        ),
        FieldMapping(
            cache_attr="https_port",
            api_path="https_port",
            default=0,
        ),
        FieldMapping(
            cache_attr="ocsp_enabled",
            api_path="ocsp_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="per_address_limit",
            api_path="per_address_limit",
            default=0,
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="wait_queue_capacity",
            api_path="wait_queue_capacity",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapWeb", ONTAPWEB_MAPPING)
