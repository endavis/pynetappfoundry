"""OntapKeyServer type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.key_managers.key_servers.model import (
    OntapKeyServer,
    OntapKeyServerConnectivityNodeState,
    OntapKeyServerRecord,
)

ONTAPKEYSERVER_MAPPING = TypeMapping(
    name="OntapKeyServer",
    model_class=OntapKeyServer,
    api_endpoint="/security/key-managers/{uuid}/key-servers?fields=*",
    api_type="ontap",
    parent_mapping="OntapSecurityKeyManager",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="connectivity.cluster_availability",
            default=False,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="connectivity.node_states",
            item_model=OntapKeyServerConnectivityNodeState,
            default=[],
        ),
        FieldMapping(
            cache_attr="create_remove_timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="password",
        ),
        FieldMapping(
            cache_attr="records",
            item_model=OntapKeyServerRecord,
            default=[],
        ),
        FieldMapping(
            cache_attr="secondary_key_servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="server",
        ),
        FieldMapping(
            cache_attr="timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="username",
        ),
    ),
)

model_registry.register_mapping("OntapKeyServer", ONTAPKEYSERVER_MAPPING)
