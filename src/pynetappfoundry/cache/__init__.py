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
# Walk the cache.ontap tree and import every mapping.py module so that
# each TypeMapping calls model_registry.register_mapping() at import time.
# The explicit sub-package imports above only load the model sub-modules;
# without this walk, mapping.py modules that are not transitively imported
# elsewhere would never register, and ``fetchers.fetch(model_class)`` /
# ``DataSource._resolve_mapping(model_class)`` would fail at runtime with
# "no TypeMapping registered for model class <...>".
import importlib as _importlib
import pkgutil as _pkgutil

import pynetappfoundry.cache.dii as _dii_pkg
import pynetappfoundry.cache.ontap as _ontap_pkg
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

for _modinfo in _pkgutil.walk_packages(
    _ontap_pkg.__path__,
    prefix="pynetappfoundry.cache.ontap.",
):
    if _modinfo.name.endswith(".mapping"):
        _importlib.import_module(_modinfo.name)

# Walk the cache.dii tree the same way so DII mappings register at
# import time.  This PR lands only two DII endpoints (the minimum
# needed for the shared-schema round-trip test, #603); the full
# ~191-endpoint DII surface is generated under #600.
for _modinfo in _pkgutil.walk_packages(
    _dii_pkg.__path__,
    prefix="pynetappfoundry.cache.dii.",
):
    if _modinfo.name.endswith(".mapping"):
        _importlib.import_module(_modinfo.name)

del _modinfo, _importlib, _pkgutil, _ontap_pkg, _dii_pkg

from pynetappfoundry.cache._registry import model_registry as _reg  # noqa: E402

# Apply package-default TOML overlay field strategies
from pynetappfoundry.cache.overlay_loader import load_overlays as _load_overlays  # noqa: E402

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
