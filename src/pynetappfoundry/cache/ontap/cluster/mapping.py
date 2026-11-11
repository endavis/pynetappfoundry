"""Cluster type mapping definition for the declarative field mapping framework.

Defines CLUSTER_MAPPING which maps ONTAP REST API /cluster data to
ClusterInfo cache model attributes.
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.cluster.traits.mapping import (
    _CLOUD_MODEL_PREFIXES,
    _CLOUD_SERIAL_PREFIXES,
    _is_cloud_node,
    compute_is_cloud,
    compute_is_ha,
)
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse

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

# The CVO hooks moved to the traits module (ADR-0024); keep the old names importable.
__all__ = [
    "CLUSTER_MAPPING",
    "_CLOUD_MODEL_PREFIXES",
    "_CLOUD_SERIAL_PREFIXES",
    "_is_cloud_node",
    "compute_is_cloud",
    "compute_is_ha",
]
