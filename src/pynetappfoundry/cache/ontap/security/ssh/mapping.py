"""OntapClusterSshServer type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.ssh.model import OntapClusterSshServer

ONTAPCLUSTERSSHSERVER_MAPPING = TypeMapping(
    name="OntapClusterSshServer",
    model_class=OntapClusterSshServer,
    api_endpoint="/security/ssh?fields=*",
    api_type="ontap",
    response_shape="singleton",
    fields=(
        FieldMapping(
            cache_attr="ciphers",
            default=[],
        ),
        FieldMapping(
            cache_attr="connections_per_second",
            default=0,
        ),
        FieldMapping(
            cache_attr="host_key_algorithms",
            default=[],
        ),
        FieldMapping(
            cache_attr="is_rsa_in_publickey_algorithms_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="key_exchange_algorithms",
            default=[],
        ),
        FieldMapping(
            cache_attr="mac_algorithms",
            default=[],
        ),
        FieldMapping(
            cache_attr="max_authentication_retry_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="max_instances",
            default=0,
        ),
        FieldMapping(
            cache_attr="per_source_limit",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapClusterSshServer", ONTAPCLUSTERSSHSERVER_MAPPING)
