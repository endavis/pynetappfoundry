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

# Trigger mapping registration -- each sub-package __init__.py imports
# its mapping.py which calls model_registry.register_mapping().
import pynetappfoundry.cache.ontap.cloud.metadata
import pynetappfoundry.cache.ontap.cloud.targets
import pynetappfoundry.cache.ontap.cluster.licensing.licenses
import pynetappfoundry.cache.ontap.cluster.mediators
import pynetappfoundry.cache.ontap.cluster.nodes
import pynetappfoundry.cache.ontap.cluster.peers
import pynetappfoundry.cache.ontap.cluster.schedules
import pynetappfoundry.cache.ontap.name_services.dns
import pynetappfoundry.cache.ontap.network.ethernet.broadcast_domains
import pynetappfoundry.cache.ontap.network.ip.interfaces
import pynetappfoundry.cache.ontap.network.ip.subnets
import pynetappfoundry.cache.ontap.protocols.cifs.services
import pynetappfoundry.cache.ontap.protocols.cifs.shares
import pynetappfoundry.cache.ontap.protocols.nfs.export_policies
import pynetappfoundry.cache.ontap.protocols.nfs.services
import pynetappfoundry.cache.ontap.protocols.s3.buckets
import pynetappfoundry.cache.ontap.protocols.san.igroups
import pynetappfoundry.cache.ontap.snapmirror.relationships
import pynetappfoundry.cache.ontap.storage.aggregates
import pynetappfoundry.cache.ontap.storage.flexcache.flexcaches
import pynetappfoundry.cache.ontap.storage.luns
import pynetappfoundry.cache.ontap.storage.qos.policies
import pynetappfoundry.cache.ontap.storage.qtrees
import pynetappfoundry.cache.ontap.storage.snapshot_policies
import pynetappfoundry.cache.ontap.storage.volumes
import pynetappfoundry.cache.ontap.svm.peers
import pynetappfoundry.cache.ontap.svm.svms  # noqa: F401
from pynetappfoundry.cache._registry import model_registry as _reg

# Apply package-default TOML overlay field strategies
from pynetappfoundry.cache.overlay_loader import load_overlays as _load_overlays

_load_overlays(_reg)
del _load_overlays, _reg

from pynetappfoundry.cache._base import (  # noqa: E402
    METADATA_SCHEMA_MIN_COMPATIBLE,
    METADATA_SCHEMA_VERSION,
    CacheModel,
    HasUUID,
    OntapUUID,
    is_schema_compatible,
    parse_schema_version,
)

# Container models and metadata
from pynetappfoundry.cache._lazy import LazyClusterMetadata  # noqa: E402
from pynetappfoundry.cache._metadata import (  # noqa: E402
    CachedClusterMetadata,
    RelationshipsInfo,
)

# Layer 1: Registry
from pynetappfoundry.cache._registry import model_registry  # noqa: E402

# Infrastructure (collector, db, diff, etc.)
from pynetappfoundry.cache.collector import (  # noqa: E402
    CollectionError,
    CollectionPhase,
    MetadataCollector,
    ProgressCallback,
    ProgressInfo,
)
from pynetappfoundry.cache.db import ClusterMetadataDB  # noqa: E402
from pynetappfoundry.cache.diff import ChangeEntry, compute_diff, format_diff_summary  # noqa: E402
from pynetappfoundry.cache.fetchers import fetch  # noqa: E402
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping  # noqa: E402
from pynetappfoundry.cache.history_db import CacheHistoryDB  # noqa: E402
from pynetappfoundry.cache.query_engine import (  # noqa: E402
    ParsedFilter,
    SQLCondition,
    parse_filter,
    parse_filters,
)
from pynetappfoundry.models.ontap.cluster.mediators.model import OntapMediatorResponse  # noqa: E402

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
