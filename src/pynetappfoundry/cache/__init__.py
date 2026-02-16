"""Cluster metadata caching module.

Provides caching infrastructure for ONTAP cluster metadata that
doesn't change frequently. Cache is manually refreshed via CLI.

Models live at ``cache/<api-path>/model.py`` and should be imported
from their sub-package, e.g.::

    from pynetappfoundry.cache.storage.volumes import VolumeInfo
    from pynetappfoundry.cache.cluster.nodes import NodeInfo

Infrastructure (DB, collector, diff, registry) is imported from here::

    from pynetappfoundry.cache import ClusterMetadataDB, MetadataCollector
"""

# Layer 1: Base class, protocol, schema utilities
# Trigger mapping registration — each sub-package __init__.py imports
# its mapping.py which calls model_registry.register_mapping().
# Models are already registered via CacheModel.__init_subclass__ when
# _metadata.py transitively imports all leaf model.py files above.
import pynetappfoundry.cache.cloud.metadata
import pynetappfoundry.cache.cluster.licensing
import pynetappfoundry.cache.cluster.mediators
import pynetappfoundry.cache.cluster.nodes
import pynetappfoundry.cache.cluster.peers
import pynetappfoundry.cache.name_services.dns
import pynetappfoundry.cache.network.ip.interfaces
import pynetappfoundry.cache.snapmirror.relationships
import pynetappfoundry.cache.storage.aggregates
import pynetappfoundry.cache.storage.volumes
import pynetappfoundry.cache.svm  # noqa: F401
from pynetappfoundry.cache._base import (
    METADATA_SCHEMA_MIN_COMPATIBLE,
    METADATA_SCHEMA_VERSION,
    CacheModel,
    HasUUID,
    OntapUUID,
    is_schema_compatible,
    parse_schema_version,
)

# Layer 3: Container models (importing _metadata triggers the full
# model registration chain via transitive leaf-model imports)
from pynetappfoundry.cache._metadata import (
    CachedClusterMetadata,
    RelationshipsInfo,
)

# Layer 1: Registry
from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.cluster.mediators.model import MediatorInfo

# Infrastructure (collector, db, diff, etc.)
from pynetappfoundry.cache.collector import (
    CollectionError,
    CollectionPhase,
    MetadataCollector,
    ProgressCallback,
    ProgressInfo,
)
from pynetappfoundry.cache.db import ClusterMetadataDB
from pynetappfoundry.cache.diff import ChangeEntry, compute_diff, format_diff_summary
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.history_db import CacheHistoryDB

__all__ = [
    "METADATA_SCHEMA_MIN_COMPATIBLE",
    "METADATA_SCHEMA_VERSION",
    "CacheHistoryDB",
    "CacheModel",
    "CachedClusterMetadata",
    "ChangeEntry",
    "ClusterMetadataDB",
    "CollectionError",
    "CollectionPhase",
    "FieldMapping",
    "HasUUID",
    "MediatorInfo",
    "MetadataCollector",
    "OntapUUID",
    "ProgressCallback",
    "ProgressInfo",
    "RelationshipsInfo",
    "TypeMapping",
    "compute_diff",
    "format_diff_summary",
    "is_schema_compatible",
    "model_registry",
    "parse_schema_version",
]
