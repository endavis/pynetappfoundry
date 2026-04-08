"""Unified DataSource accessor (Phase 2 spike, see ADR-0012).

Public surface for fetching model instances across cache + live API
through one consistent interface. The spike targets ``OntapVolume``;
existing surfaces (``LazyClusterMetadata``, ``QuerySet``,
``fetch_realtime``, CLI commands) are not yet migrated.
"""

from pynetappfoundry.data._routing import SourceMode
from pynetappfoundry.data.backends import Backend, OntapBackend
from pynetappfoundry.data.source import DataSource, QueryBuilder

__all__ = [
    "Backend",
    "DataSource",
    "OntapBackend",
    "QueryBuilder",
    "SourceMode",
]
