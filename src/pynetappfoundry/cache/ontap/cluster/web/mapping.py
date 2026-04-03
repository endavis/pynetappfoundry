"""OntapWeb type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.web.model import OntapWeb

ONTAPWEB_MAPPING = TypeMapping(
    name="OntapWeb",
    model_class=OntapWeb,
    api_endpoint="/cluster/web?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="certificate.name",
        ),
        FieldMapping(
            cache_attr="certificate.uuid",
        ),
        FieldMapping(
            cache_attr="client_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="csrf.protection_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="csrf.token.concurrent_limit",
            default=0,
        ),
        FieldMapping(
            cache_attr="csrf.token.idle_timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="csrf.token.max_timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="http_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="http_port",
            default=0,
        ),
        FieldMapping(
            cache_attr="https_port",
            default=0,
        ),
        FieldMapping(
            cache_attr="ocsp_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="per_address_limit",
            default=0,
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="wait_queue_capacity",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapWeb", ONTAPWEB_MAPPING)
