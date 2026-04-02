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
    fields=(
        FieldMapping(
            cache_attr="authentication.expiry_time",
            api_path="authentication.expiry_time",
        ),
        FieldMapping(
            cache_attr="authentication.generate_passphrase",
            api_path="authentication.generate_passphrase",
            default=False,
        ),
        FieldMapping(
            cache_attr="authentication.in_use",
            api_path="authentication.in_use",
        ),
        FieldMapping(
            cache_attr="authentication.passphrase",
            api_path="authentication.passphrase",
        ),
        FieldMapping(
            cache_attr="authentication.state",
            api_path="authentication.state",
        ),
        FieldMapping(
            cache_attr="encryption.proposed",
            api_path="encryption.proposed",
        ),
        FieldMapping(
            cache_attr="encryption.state",
            api_path="encryption.state",
        ),
        FieldMapping(
            cache_attr="initial_allowed_svms",
            api_path="initial_allowed_svms",
            transform=_transform_initial_allowed_svms,
            default=[],
        ),
        FieldMapping(
            cache_attr="ip_address",
            api_path="ip_address",
        ),
        FieldMapping(
            cache_attr="ipspace.name",
            api_path="ipspace.name",
        ),
        FieldMapping(
            cache_attr="ipspace.uuid",
            api_path="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="local_network.broadcast_domain",
            api_path="local_network.broadcast_domain",
        ),
        FieldMapping(
            cache_attr="local_network.gateway",
            api_path="local_network.gateway",
        ),
        FieldMapping(
            cache_attr="local_network.interfaces",
            api_path="local_network.interfaces",
            default=[],
        ),
        FieldMapping(
            cache_attr="local_network.netmask",
            api_path="local_network.netmask",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="peer_applications",
            api_path="peer_applications",
            default=[],
        ),
        FieldMapping(
            cache_attr="remote.ip_addresses",
            api_path="remote.ip_addresses",
            default=[],
        ),
        FieldMapping(
            cache_attr="remote.name",
            api_path="remote.name",
        ),
        FieldMapping(
            cache_attr="remote.serial_number",
            api_path="remote.serial_number",
        ),
        FieldMapping(
            cache_attr="status.state",
            api_path="status.state",
        ),
        FieldMapping(
            cache_attr="status.update_time",
            api_path="status.update_time",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="version.full",
            api_path="version.full",
        ),
        FieldMapping(
            cache_attr="version.generation",
            api_path="version.generation",
            default=0,
        ),
        FieldMapping(
            cache_attr="version.major",
            api_path="version.major",
            default=0,
        ),
        FieldMapping(
            cache_attr="version.minor",
            api_path="version.minor",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapClusterPeer", ONTAPCLUSTERPEER_MAPPING)
