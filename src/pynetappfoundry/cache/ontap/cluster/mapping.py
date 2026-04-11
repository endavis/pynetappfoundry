"""Cluster type mapping definition for the declarative field mapping framework.

Defines CLUSTER_MAPPING which maps ONTAP REST API /cluster data to
ClusterInfo cache model attributes.
"""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse

# Known CVO (Cloud Volumes ONTAP) node prefixes.  Verified against real
# CVO clusters in this environment: CDvM200 model with serial numbers in
# the 909201* NetApp cloud range (both HA 9092014* and single-node
# 9092013* variants).  Do NOT add speculative prefixes — see #547 and the
# risks section of the implementation plan.
_CLOUD_MODEL_PREFIXES: tuple[str, ...] = ("CDvM",)
_CLOUD_SERIAL_PREFIXES: tuple[str, ...] = ("909201",)


def _is_cloud_node(node: OntapNodeResponse) -> bool:
    """Return ``True`` if *node* looks like a Cloud Volumes ONTAP node.

    Uses two independent signals OR'd together so detection survives
    future ONTAP releases changing one of them:

    - ``model_`` starts with any of :data:`_CLOUD_MODEL_PREFIXES`.
    - ``serial_number`` starts with any of :data:`_CLOUD_SERIAL_PREFIXES`.

    Fields are read defensively; ONTAP may return empty strings rather
    than populated values on non-cloud clusters.

    Args:
        node: An :class:`OntapNodeResponse` instance.

    Returns:
        ``True`` when the node matches at least one CVO signal.
    """
    model = getattr(node, "model_", "") or ""
    serial = getattr(node, "serial_number", "") or ""
    if model.startswith(_CLOUD_MODEL_PREFIXES):
        return True
    return serial.startswith(_CLOUD_SERIAL_PREFIXES)


def compute_is_ha(cluster: ClusterInfo, results: dict[str, Any]) -> ClusterInfo:
    """Derive ``is_ha`` from the collected node count.

    Args:
        cluster: The ClusterInfo instance to update.
        results: Full collection results dict (needs ``"nodes"`` key).

    Returns:
        Updated ClusterInfo with ``is_ha`` set.
    """
    nodes = results.get("OntapNodeResponse", results.get("nodes", []))
    return cluster.model_copy(update={"is_ha": len(nodes) > 1})


def compute_is_cloud(cluster: ClusterInfo, results: dict[str, Any]) -> ClusterInfo:
    """Derive ``is_cloud`` from the collected nodes.

    A cluster is flagged cloud when any node reports CVO-style model or
    serial number via :func:`_is_cloud_node`.

    Args:
        cluster: The ClusterInfo instance to update.
        results: Full collection results dict (needs ``"nodes"`` key).

    Returns:
        Updated ClusterInfo with ``is_cloud`` set.
    """
    nodes = results.get("OntapNodeResponse", results.get("nodes", []))
    return cluster.model_copy(update={"is_cloud": any(_is_cloud_node(n) for n in nodes)})


CLUSTER_MAPPING = TypeMapping(
    name="Cluster",
    model_class=ClusterInfo,
    api_endpoint="/cluster?fields=*",
    cli_command="",
    id_field="name",
    response_shape="singleton",
    fields=(
        FieldMapping(
            cache_attr="cluster_name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="cluster_uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="ontap_version",
            api_path="version.full",
        ),
        FieldMapping(
            cache_attr="version_generation",
            api_path="version.generation",
        ),
        FieldMapping(
            cache_attr="version_major",
            api_path="version.major",
            default=0,
        ),
        FieldMapping(
            cache_attr="version_minor",
            api_path="version.minor",
            default=0,
        ),
        FieldMapping(
            cache_attr="contact",
        ),
        FieldMapping(
            cache_attr="location",
        ),
        FieldMapping(
            cache_attr="san_optimized",
            default=False,
        ),
        FieldMapping(
            cache_attr="timezone",
            api_path="timezone.name",
        ),
        FieldMapping(
            cache_attr="dns_domains",
            default=[],
        ),
        FieldMapping(
            cache_attr="name_servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="ntp_servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="peering_policy_authentication_required",
            api_path="peering_policy.authentication_required",
            default=False,
        ),
        FieldMapping(
            cache_attr="peering_policy_encryption_required",
            api_path="peering_policy.encryption_required",
            default=False,
        ),
        FieldMapping(
            cache_attr="peering_policy_minimum_passphrase_length",
            api_path="peering_policy.minimum_passphrase_length",
            default=0,
        ),
        FieldMapping(
            cache_attr="management_interface_uuids",
            api_path="management_interfaces[*].uuid",
            default=[],
        ),
        FieldMapping(
            cache_attr="disaggregated",
            default=False,
        ),
        FieldMapping(
            cache_attr="auto_enable_activity_tracking",
            default=False,
        ),
        FieldMapping(
            cache_attr="auto_enable_analytics",
            default=False,
        ),
        FieldMapping(
            cache_attr="is_ha",
            cache_strategy="derived",
            default=False,
            post_collection=compute_is_ha,
            depends_on=(OntapNodeResponse,),
        ),
        FieldMapping(
            cache_attr="is_cloud",
            cache_strategy="derived",
            default=False,
            post_collection=compute_is_cloud,
            depends_on=(OntapNodeResponse,),
        ),
    ),
)

model_registry.register_mapping("Cluster", CLUSTER_MAPPING)
