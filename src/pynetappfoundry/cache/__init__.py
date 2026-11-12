"""Cluster metadata caching module.

Provides caching infrastructure for ONTAP cluster metadata that
doesn't change frequently. Cache is manually refreshed via CLI.

Models live at ``models/ontap/<api-path>/model.py`` and should be imported
from their sub-package, e.g.::

    from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume
    from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse

Infrastructure (DB, collector, diff, registry) is imported from here::

    from pynetappfoundry.cache import ClusterMetadataDB, MetadataCollector

Every export resolves lazily on first attribute access (PEP 562), so importing this
package loads none of the ``models.ontap`` chain.  Every mapping, hand-written or
generated, registers lazily on first lookup through the generated ``_mapping_index``
(ADR-0023, #960).  Run ``doit mapping_index`` after adding or removing a ``mapping.py``.
"""

import importlib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pynetappfoundry.cache._base import (
        METADATA_SCHEMA_MIN_COMPATIBLE,
        METADATA_SCHEMA_VERSION,
        CacheModel,
        HasUUID,
        OntapUUID,
        is_schema_compatible,
        parse_schema_version,
    )
    from pynetappfoundry.cache._collector_progress import (
        CollectionPhase,
        ProgressCallback,
        ProgressInfo,
    )
    from pynetappfoundry.cache._lazy import LazyClusterMetadata
    from pynetappfoundry.cache._metadata import (
        CachedClusterMetadata,
        RelationshipsInfo,
    )
    from pynetappfoundry.cache._registry import model_registry
    from pynetappfoundry.cache.collector import (
        CollectionError,
        MetadataCollector,
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

_P = "pynetappfoundry.cache"

# Export name -> defining module, resolved on first access by ``__getattr__``.
_LAZY_EXPORTS: dict[str, str] = {
    "METADATA_SCHEMA_MIN_COMPATIBLE": f"{_P}._base",
    "METADATA_SCHEMA_VERSION": f"{_P}._base",
    "CacheModel": f"{_P}._base",
    "HasUUID": f"{_P}._base",
    "OntapUUID": f"{_P}._base",
    "is_schema_compatible": f"{_P}._base",
    "parse_schema_version": f"{_P}._base",
    "LazyClusterMetadata": f"{_P}._lazy",
    "CachedClusterMetadata": f"{_P}._metadata",
    "RelationshipsInfo": f"{_P}._metadata",
    "model_registry": f"{_P}._registry",
    "CollectionPhase": f"{_P}._collector_progress",
    "ProgressCallback": f"{_P}._collector_progress",
    "ProgressInfo": f"{_P}._collector_progress",
    "CollectionError": f"{_P}.collector",
    "MetadataCollector": f"{_P}.collector",
    "ClusterMetadataDB": f"{_P}.db",
    "ChangeEntry": f"{_P}.diff",
    "compute_diff": f"{_P}.diff",
    "format_diff_summary": f"{_P}.diff",
    "fetch": f"{_P}.fetchers",
    "FieldMapping": f"{_P}.field_mapping",
    "TypeMapping": f"{_P}.field_mapping",
    "CacheHistoryDB": f"{_P}.history_db",
    "ParsedFilter": f"{_P}.query_engine",
    "SQLCondition": f"{_P}.query_engine",
    "parse_filter": f"{_P}.query_engine",
    "parse_filters": f"{_P}.query_engine",
    "OntapMediatorResponse": "pynetappfoundry.models.ontap.cluster.mediators.model",
}

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


def __getattr__(name: str) -> Any:
    """Resolve a lazy export on first access and cache it in the module namespace."""
    module_name = _LAZY_EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(importlib.import_module(module_name), name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    """List the lazy exports alongside the loaded module namespace."""
    return sorted(set(globals()) | set(__all__))
