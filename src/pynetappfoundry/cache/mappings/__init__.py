"""Declarative type mapping definitions for ONTAP object types.

Each sub-module defines a TypeMapping constant for one ONTAP object type.
"""

from pynetappfoundry.cache.mappings.aggregate import AGGREGATE_MAPPING
from pynetappfoundry.cache.mappings.cloud_metadata import CLOUD_METADATA_MAPPING
from pynetappfoundry.cache.mappings.cluster_peer import CLUSTER_PEER_MAPPING
from pynetappfoundry.cache.mappings.node import NODE_MAPPING
from pynetappfoundry.cache.mappings.snapmirror import SNAPMIRROR_MAPPING
from pynetappfoundry.cache.mappings.volume import VOLUME_MAPPING

__all__ = [
    "AGGREGATE_MAPPING",
    "CLOUD_METADATA_MAPPING",
    "CLUSTER_PEER_MAPPING",
    "NODE_MAPPING",
    "SNAPMIRROR_MAPPING",
    "VOLUME_MAPPING",
]
