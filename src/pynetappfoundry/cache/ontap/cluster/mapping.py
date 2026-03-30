"""Cluster type mapping definition for the declarative field mapping framework.

Defines CLUSTER_MAPPING which maps ONTAP REST API /cluster data to
ClusterInfo cache model attributes.
"""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo


def compute_is_ha(cluster: ClusterInfo, results: dict[str, Any]) -> ClusterInfo:
    """Derive ``is_ha`` from the collected node count.

    Args:
        cluster: The ClusterInfo instance to update.
        results: Full collection results dict (needs ``"nodes"`` key).

    Returns:
        Updated ClusterInfo with ``is_ha`` set.
    """
    nodes = results.get("nodes", [])
    return cluster.model_copy(update={"is_ha": len(nodes) > 1})


CLUSTER_MAPPING = TypeMapping(
    name="Cluster",
    model_class=ClusterInfo,
    api_endpoint="/cluster?fields=*",
    cli_command="",
    id_field="name",
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
            api_path="contact",
        ),
        FieldMapping(
            cache_attr="location",
            api_path="location",
        ),
        FieldMapping(
            cache_attr="san_optimized",
            api_path="san_optimized",
            default=False,
        ),
        FieldMapping(
            cache_attr="timezone",
            api_path="timezone.name",
        ),
        FieldMapping(
            cache_attr="dns_domains",
            api_path="dns_domains",
            default=[],
        ),
        FieldMapping(
            cache_attr="name_servers",
            api_path="name_servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="ntp_servers",
            api_path="ntp_servers",
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
            api_path="disaggregated",
            default=False,
        ),
        FieldMapping(
            cache_attr="auto_enable_activity_tracking",
            api_path="auto_enable_activity_tracking",
            default=False,
        ),
        FieldMapping(
            cache_attr="auto_enable_analytics",
            api_path="auto_enable_analytics",
            default=False,
        ),
        FieldMapping(
            cache_attr="is_ha",
            cache_strategy="derived",
            default=False,
            post_collection=compute_is_ha,
        ),
    ),
)

model_registry.register_mapping("Cluster", CLUSTER_MAPPING)
