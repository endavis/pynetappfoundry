"""Re-export cluster traits cache models and mappings."""

from __future__ import annotations

from pynetappfoundry.cache.ontap.cluster.traits.mapping import CLUSTERTRAITS_MAPPING
from pynetappfoundry.models.ontap.cluster.traits.model import ClusterTraits

__all__ = [
    "CLUSTERTRAITS_MAPPING",
    "ClusterTraits",
]
