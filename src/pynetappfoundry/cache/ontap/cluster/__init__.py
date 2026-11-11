"""Re-export cluster cache models."""

from __future__ import annotations

from pynetappfoundry.cache.ontap.cluster.mapping import ONTAPCLUSTER_MAPPING
from pynetappfoundry.models.ontap.cluster.model import OntapCluster

__all__ = [
    "ONTAPCLUSTER_MAPPING",
    "OntapCluster",
]
