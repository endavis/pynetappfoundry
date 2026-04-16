"""OntapClusterPeer type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.peers.model import (
    OntapClusterPeer,
    OntapClusterPeerInitialAllowedSvm,
)


def _transform_initial_allowed_svms(
    record: dict[str, Any],
) -> list[OntapClusterPeerInitialAllowedSvm]:
    """Transform initial_allowed_svms into OntapClusterPeerInitialAllowedSvm list."""
    return [
        OntapClusterPeerInitialAllowedSvm(**item) for item in record.get("initial_allowed_svms", [])
    ]


ONTAPCLUSTERPEER_MAPPING = TypeMapping(
    name="OntapClusterPeer",
    model_class=OntapClusterPeer,
    api_endpoint="/cluster/peers?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="authentication.expiry_time",
        ),
        FieldMapping(
            cache_attr="authentication.generate_passphrase",
            default=False,
        ),
        FieldMapping(
            cache_attr="authentication.in_use",
        ),
        FieldMapping(
            cache_attr="authentication.passphrase",
        ),
        FieldMapping(
            cache_attr="authentication.state",
        ),
        FieldMapping(
            cache_attr="encryption.proposed",
        ),
        FieldMapping(
            cache_attr="encryption.state",
        ),
        FieldMapping(
            cache_attr="initial_allowed_svms",
            transform=_transform_initial_allowed_svms,
            default=[],
        ),
        FieldMapping(
            cache_attr="ip_address",
        ),
        FieldMapping(
            cache_attr="ipspace.name",
        ),
        FieldMapping(
            cache_attr="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="local_network.broadcast_domain",
        ),
        FieldMapping(
            cache_attr="local_network.gateway",
        ),
        FieldMapping(
            cache_attr="local_network.interfaces",
            default=[],
        ),
        FieldMapping(
            cache_attr="local_network.netmask",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="peer_applications",
            default=[],
        ),
        FieldMapping(
            cache_attr="remote.ip_addresses",
            default=[],
        ),
        FieldMapping(
            cache_attr="remote.name",
        ),
        FieldMapping(
            cache_attr="remote.serial_number",
        ),
        FieldMapping(
            cache_attr="status.state",
        ),
        FieldMapping(
            cache_attr="status.update_time",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="version.full",
        ),
        FieldMapping(
            cache_attr="version.generation",
            default=0,
        ),
        FieldMapping(
            cache_attr="version.major",
            default=0,
        ),
        FieldMapping(
            cache_attr="version.minor",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapClusterPeer", ONTAPCLUSTERPEER_MAPPING)
