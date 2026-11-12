"""Cluster metadata caching module.

Provides caching infrastructure for ONTAP cluster metadata that
doesn't change frequently. Cache is manually refreshed via CLI.

Models live at ``models/ontap/<api-path>/model.py`` and should be imported
from their sub-package, e.g.::

    from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume
    from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse

Infrastructure (DB, collector, diff, registry) is imported from here::

    from pynetappfoundry.cache import ClusterMetadataDB, MetadataCollector
"""

# Hand-written mapping sub-packages are imported explicitly: each sub-package
# ``__init__`` imports its ``mapping.py``.  Every other mapping registers lazily on first
# lookup through the generated ``_mapping_index`` (ADR-0023), so startup does not import
# the ~470 ``mapping.py`` modules.  Run ``doit mapping_index`` after adding or removing one.
import pynetappfoundry.cache.ontap.cloud.metadata  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.cloud.targets  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.cluster.licensing.licenses  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.cluster.mediators  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.cluster.nodes  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.cluster.peers  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.cluster.schedules  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.cluster.traits  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.name_services.dns  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.network.ethernet.broadcast_domains  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.network.ip.interfaces  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.network.ip.subnets  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.protocols.cifs.services  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.protocols.cifs.shares  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.protocols.nfs.export_policies  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.protocols.nfs.services  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.protocols.s3.buckets  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.protocols.san.igroups  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.snapmirror.relationships  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.storage.aggregates  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.storage.flexcache.flexcaches  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.storage.luns  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.storage.qos.policies  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.storage.qtrees  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.storage.snapshot_policies  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.storage.volumes  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.svm.peers  # noqa: F401  # registers mapping on import
import pynetappfoundry.cache.ontap.svm.svms  # noqa: F401  # registers mapping on import
from pynetappfoundry.cache._base import (
    METADATA_SCHEMA_MIN_COMPATIBLE,
    METADATA_SCHEMA_VERSION,
    CacheModel,
    HasUUID,
    OntapUUID,
    is_schema_compatible,
    parse_schema_version,
)

# Container models and metadata
from pynetappfoundry.cache._lazy import LazyClusterMetadata
from pynetappfoundry.cache._metadata import (
    CachedClusterMetadata,
    RelationshipsInfo,
)

# Layer 1: Registry
from pynetappfoundry.cache._registry import model_registry

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
from pynetappfoundry.cache.fetchers import fetch
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.history_db import CacheHistoryDB
from pynetappfoundry.cache.query_engine import (
    ParsedFilter,
    SQLCondition,
    parse_filter,
    parse_filters,
)
from pynetappfoundry.models.ontap.cluster.mediators.model import OntapMediatorResponse

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
    "LazyClusterMetadata",
    "MetadataCollector",
    "OntapMediatorResponse",
    "OntapUUID",
    "ParsedFilter",
    "ProgressCallback",
    "ProgressInfo",
    "RelationshipsInfo",
    "SQLCondition",
    "TypeMapping",
    "compute_diff",
    "fetch",
    "format_diff_summary",
    "is_schema_compatible",
    "model_registry",
    "parse_filter",
    "parse_filters",
    "parse_schema_version",
]
