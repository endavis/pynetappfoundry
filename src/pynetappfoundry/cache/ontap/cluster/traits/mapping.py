"""ClusterTraits mapping: values computed from the collected nodes.

Hand-written (not generated).  ``is_ha`` and ``is_cloud`` are not API data,
so they live here instead of on a generated model (ADR-0024).
"""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse
from pynetappfoundry.models.ontap.cluster.traits.model import ClusterTraits

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


def compute_is_ha(cluster: ClusterTraits, results: dict[str, Any]) -> ClusterTraits:
    """Derive ``is_ha`` from the collected node count.

    Args:
        cluster: The ClusterTraits instance to update.
        results: Full collection results dict (needs ``"OntapNodeResponse"`` key).

    Returns:
        Updated ClusterTraits with ``is_ha`` set.
    """
    nodes = results.get("OntapNodeResponse", [])
    return cluster.model_copy(update={"is_ha": len(nodes) > 1})


def compute_is_cloud(cluster: ClusterTraits, results: dict[str, Any]) -> ClusterTraits:
    """Derive ``is_cloud`` from the collected nodes.

    A cluster is flagged cloud when any node reports CVO-style model or
    serial number via :func:`_is_cloud_node`.

    Args:
        cluster: The ClusterTraits instance to update.
        results: Full collection results dict (needs ``"OntapNodeResponse"`` key).

    Returns:
        Updated ClusterTraits with ``is_cloud`` set.
    """
    nodes = results.get("OntapNodeResponse", [])
    return cluster.model_copy(update={"is_cloud": any(_is_cloud_node(n) for n in nodes)})


CLUSTERTRAITS_MAPPING = TypeMapping(
    name="ClusterTraits",
    model_class=ClusterTraits,
    api_endpoint="",
    response_shape="computed",
    fields=(
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

model_registry.register_mapping("ClusterTraits", CLUSTERTRAITS_MAPPING)
