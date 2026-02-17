"""OntapNfsClientsCache type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.protocols.nfs.connected_client_settings.model import OntapNfsClientsCache

ONTAPNFSCLIENTSCACHE_MAPPING = TypeMapping(
    name="OntapNfsClientsCache",
    model_class=OntapNfsClientsCache,
    api_endpoint="/protocols/nfs/connected-client-settings?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="client_retention_interval",
            api_path="client_retention_interval",
        ),
        FieldMapping(
            cache_attr="enable_nfs_clients_deletion",
            api_path="enable_nfs_clients_deletion",
            default=False,
        ),
        FieldMapping(
            cache_attr="update_interval",
            api_path="update_interval",
        ),
    ),
)

model_registry.register_mapping("OntapNfsClientsCache", ONTAPNFSCLIENTSCACHE_MAPPING)
