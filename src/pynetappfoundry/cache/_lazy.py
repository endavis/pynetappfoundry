"""Lazy-loading wrapper for cached cluster metadata.

``LazyClusterMetadata`` defers per-field-group data fetches until the
caller actually accesses a data attribute (``cloud``, ``storage``, etc.).
Envelope fields (``cluster_name``, ``cached_at``, ``cache_version``) are
available immediately without any fetch.

This avoids the overhead of querying all ~29 model tables when the
caller only needs a small subset (e.g. ``entry.ontap.cloud``).

Field-group access resolves the set of cache-table model classes in the
group via :func:`pynetappfoundry.cache.db_schema._ensure_registry` and
delegates each per-model read to ``DataSource.query()``. Results are
reassembled into the corresponding ``CachedClusterMetadata`` sub-model
via ``model_validate()``.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

from pynetappfoundry.cache._base import _utcnow
from pynetappfoundry.cache._metadata import CachedClusterMetadata

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config

# Top-level data field names on CachedClusterMetadata (everything except
# the envelope fields cluster_name, cached_at, cache_version).
_DATA_FIELDS = frozenset(
    {
        "cloud",
        "cluster",
        "nodes",
        "network",
        "storage",
        "license_packages",
        "mediator",
        "relationships",
        "protocols",
    }
)


def _set_by_path(target: dict[str, Any], path: str, value: Any) -> None:
    """Set a value in a nested dict via dot-path, creating intermediate dicts."""
    parts = path.split(".")
    for part in parts[:-1]:
        target = target.setdefault(part, {})
    target[parts[-1]] = value


class LazyClusterMetadata:
    """Lazy-loading proxy for :class:`CachedClusterMetadata`.

    Envelope data (``cluster_name``, ``cached_at``, ``cache_version``) is
    stored eagerly. Data field groups are loaded via
    :class:`~pynetappfoundry.data.source.DataSource` on first attribute
    access and cached for subsequent reads.

    The class is **not** a Pydantic model. For full Pydantic compatibility
    call :meth:`_materialize` which returns a real
    :class:`CachedClusterMetadata`.

    Args:
        cluster_name: Cluster name (envelope).
        cached_at: ISO-8601 timestamp (envelope).
        cache_version: Metadata schema version (envelope).
        config: :class:`Config` used to build the internal
            :class:`DataSource`.
    """

    __slots__ = (
        "_cache_version",
        "_cached_at",
        "_cluster_name",
        "_config",
        "_data_source",
        "_group_models",
        "_loaded",
        "_materialized",
    )

    def __init__(
        self,
        cluster_name: str,
        cached_at: str,
        cache_version: str,
        *,
        config: Config | None = None,
    ) -> None:
        self._cluster_name = cluster_name
        self._cached_at = cached_at
        self._cache_version = cache_version
        self._config = config
        self._loaded: dict[str, Any] = {}
        self._materialized: CachedClusterMetadata | None = None
        # Deferred — built on first field-group access.
        self._data_source: Any = None
        self._group_models: dict[str, list[tuple[str, type[BaseModel], bool]]] | None = None

    # ------------------------------------------------------------------
    # Envelope properties (no data access required)
    # ------------------------------------------------------------------

    @property
    def cluster_name(self) -> str:
        """Cluster name from the envelope table."""
        return self._cluster_name

    @property
    def cached_at(self) -> str:
        """Cache timestamp from the envelope table (ISO-8601 string)."""
        return self._cached_at

    @property
    def cache_version(self) -> str:
        """Metadata schema version from the envelope table."""
        return self._cache_version

    # ------------------------------------------------------------------
    # Lazy data field access
    # ------------------------------------------------------------------

    def __getattr__(self, name: str) -> Any:
        """Intercept data field access and load on demand."""
        if name in _DATA_FIELDS:
            if name in self._loaded:
                return self._loaded[name]
            return self._load_field_group(name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute {name!r}")

    # ------------------------------------------------------------------
    # DataSource routing (Phase 3b shim)
    # ------------------------------------------------------------------

    def _get_data_source(self) -> Any:
        """Lazily build the internal :class:`DataSource`."""
        if self._data_source is None:
            if self._config is None:
                return None
            from pynetappfoundry.data.source import DataSource

            self._data_source = DataSource(self._config)
        return self._data_source

    def _build_group_models(self) -> dict[str, list[tuple[str, type[BaseModel], bool]]]:
        """Build a field-group → list of (path, model_class, is_list) mapping.

        For each top-level data field group, collect every table registry
        entry whose ``metadata_path`` equals the group name or begins with
        ``f"{group_name}."``. This powers per-group routing in
        :meth:`_load_field_group` without re-scanning the registry on
        every access.
        """
        from pynetappfoundry.cache.db_schema import _ensure_registry

        registry = _ensure_registry()
        groups: dict[str, list[tuple[str, type[BaseModel], bool]]] = {
            name: [] for name in _DATA_FIELDS
        }
        for path, spec in registry.items():
            head = path.split(".", 1)[0]
            if head in groups:
                groups[head].append((path, spec.model_class, spec.is_list))
        return groups

    def _query_group_via_datasource(self, name: str) -> Any:
        """Fetch a field group through :class:`DataSource`.

        Returns ``None`` when the group yielded no cache data at all
        (the shim treats this as a cache miss and falls through to the
        fetcher / default chain).
        """
        data_source = self._get_data_source()
        if data_source is None:
            return None

        if self._group_models is None:
            self._group_models = self._build_group_models()
        entries = self._group_models.get(name, [])
        if not entries:
            return None

        from pynetappfoundry.cache._registry import model_registry
        from pynetappfoundry.cache.db import _query_registry_subset
        from pynetappfoundry.cache.db_schema import _ensure_registry

        registry = _ensure_registry()
        root_kwargs: dict[str, Any] = {}
        saw_any_result = False
        fallback_paths: dict[str, Any] = {}

        for path, model_class, is_list in entries:
            # Route through DataSource.query() when a TypeMapping exists.
            # A handful of pure-singleton container models (ClusterInfo,
            # NetworkInfo) don't have a TypeMapping; fall back to
            # ``_query_registry_subset`` over the backend's shared cache
            # DB connection so all I/O still flows through the unified
            # stack.
            mapping = model_registry.get_mapping(model_class.__name__)
            if mapping is not None:
                builder = data_source.query(model_class, cluster=self._cluster_name, source="cache")
                results = list(builder)
                if is_list:
                    _set_by_path(root_kwargs, path, results)
                    if results:
                        saw_any_result = True
                elif results:
                    _set_by_path(root_kwargs, path, results[0])
                    saw_any_result = True
            else:
                fallback_paths[path] = registry[path]

        if fallback_paths:
            backend = data_source._get_backend("ontap")
            cache_db = backend._cache_db
            subset_result = _query_registry_subset(
                cache_db.conn, self._cluster_name, fallback_paths
            )
            # ``subset_result`` is a nested dict keyed by the same paths;
            # merge it into ``root_kwargs``.
            for path in fallback_paths:
                parts = path.split(".")
                src: Any = subset_result
                for part in parts:
                    if isinstance(src, dict) and part in src:
                        src = src[part]
                    else:
                        src = None
                        break
                if src is not None:
                    _set_by_path(root_kwargs, path, src)
                    saw_any_result = True

        if not saw_any_result:
            return None

        return root_kwargs.get(name)

    def _load_field_group(self, name: str) -> Any:
        """Load a field group via DataSource or fall back to default.

        1. **DataSource** — per-model routing through
           :class:`DataSource` for every registry entry in the group.
        2. **Default** — the ``CachedClusterMetadata`` field default.
        """
        value: Any = None

        if self._config is not None:
            value = self._query_group_via_datasource(name)

        if value is None:
            value = self._get_default(name)

        # For container fields (e.g. storage, network) represented as
        # nested dicts, validate them into the actual sub-model.
        if isinstance(value, dict):
            field_info = CachedClusterMetadata.model_fields.get(name)
            if field_info is not None:
                model_cls = field_info.annotation
                if isinstance(model_cls, type) and issubclass(model_cls, BaseModel):
                    value = model_cls.model_validate(value)

        self._loaded[name] = value
        return value

    @staticmethod
    def _get_default(name: str) -> Any:
        """Return the ``CachedClusterMetadata`` default for *name*."""
        field_info = CachedClusterMetadata.model_fields.get(name)
        if field_info is not None and field_info.default_factory is not None:
            factory = field_info.default_factory
            return factory()  # type: ignore[call-arg]
        if field_info is not None:
            return field_info.default
        return None

    # ------------------------------------------------------------------
    # Materialization (full CachedClusterMetadata)
    # ------------------------------------------------------------------

    def _materialize(self) -> CachedClusterMetadata:
        """Force-load all fields and return a real CachedClusterMetadata."""
        if self._materialized is not None:
            return self._materialized

        # Ensure all data fields are loaded.
        for field_name in _DATA_FIELDS:
            if field_name not in self._loaded:
                self._load_field_group(field_name)

        kwargs: dict[str, Any] = {
            "cluster_name": self._cluster_name,
            "cached_at": self._cached_at,
            "cache_version": self._cache_version,
        }
        kwargs.update(self._loaded)

        self._materialized = CachedClusterMetadata.model_validate(kwargs)
        return self._materialized

    # ------------------------------------------------------------------
    # Delegated methods
    # ------------------------------------------------------------------

    def is_stale(self, ttl_days: int = 30) -> bool:
        """Check staleness using envelope data only (no materialization)."""
        cached_at_str = self._cached_at
        if cached_at_str.endswith("Z"):
            cached_at_str = cached_at_str[:-1] + "+00:00"
        if "+" not in cached_at_str and "-" not in cached_at_str[-6:]:
            cached_at = datetime.fromisoformat(cached_at_str).replace(tzinfo=UTC)
        else:
            cached_at = datetime.fromisoformat(cached_at_str)

        age = _utcnow() - cached_at
        return age.days > ttl_days

    def to_flat_dict(self) -> dict[str, str | int | bool | None]:
        """Delegate to materialized metadata."""
        return self._materialize().to_flat_dict()

    @property
    def uuid_index(self) -> dict[str, Any]:
        """Delegate to materialized metadata (triggers full load)."""
        return self._materialize().uuid_index

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        """Delegate to materialized metadata."""
        return self._materialize().model_dump(**kwargs)

    def model_dump_json(self, **kwargs: Any) -> str:
        """Delegate to materialized metadata."""
        return self._materialize().model_dump_json(**kwargs)
