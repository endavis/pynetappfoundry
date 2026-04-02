"""Lazy-loading wrapper for cached cluster metadata.

``LazyClusterMetadata`` defers per-field-group SQLite queries until the
caller actually accesses a data attribute (``cloud``, ``storage``, etc.).
Envelope fields (``cluster_name``, ``cached_at``, ``cache_version``) are
available immediately without touching the database.

This avoids the overhead of querying all ~29 model tables when the caller
only needs a small subset (e.g. ``entry.ontap.cloud``).

When a :class:`~pynetappfoundry.cache._fetcher.FieldGroupFetcher` is
attached, accessing a field group that is missing from the cache DB
(or when there is no DB at all) will transparently fall back to a live
ONTAP API/CLI fetch.
"""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pynetappfoundry.cache._base import _utcnow
from pynetappfoundry.cache._metadata import CachedClusterMetadata

if TYPE_CHECKING:
    from pynetappfoundry.cache._fetcher import FieldGroupFetcher
    from pynetappfoundry.cache.db_schema import TableSpec

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


class LazyClusterMetadata:
    """Lazy-loading proxy for :class:`CachedClusterMetadata`.

    Envelope data (``cluster_name``, ``cached_at``, ``cache_version``) is
    stored eagerly.  Data field groups are loaded from the SQLite database
    on first attribute access and cached for subsequent reads.

    The class is **not** a Pydantic model.  For full Pydantic compatibility
    call :meth:`_materialize` which returns a real
    :class:`CachedClusterMetadata`.
    """

    __slots__ = (
        "_cache_version",
        "_cached_at",
        "_cluster_name",
        "_db_path",
        "_fetcher",
        "_loaded",
        "_materialized",
        "_registry",
    )

    def __init__(
        self,
        cluster_name: str,
        cached_at: str,
        cache_version: str,
        db_path: Path | str | None,
        registry: dict[str, TableSpec],
        *,
        fetcher: FieldGroupFetcher | None = None,
    ) -> None:
        self._cluster_name = cluster_name
        self._cached_at = cached_at
        self._cache_version = cache_version
        if db_path is None:
            self._db_path: Path | str | None = None
        elif isinstance(db_path, str) and db_path.startswith("file:"):
            self._db_path = db_path  # SQLite URI — keep as string
        else:
            self._db_path = Path(db_path) if not isinstance(db_path, Path) else db_path
        self._registry = registry
        self._fetcher = fetcher
        self._loaded: dict[str, Any] = {}
        self._materialized: CachedClusterMetadata | None = None

    # ------------------------------------------------------------------
    # Envelope properties (no DB access required)
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

    def _load_field_group(self, name: str) -> Any:
        """Load a field group via DB, fetcher, or default — in that order.

        1. **DB** (existing path) — skipped when ``_db_path is None``.
        2. **Fetcher** — live API/CLI fetch when a
           :class:`FieldGroupFetcher` is attached.
        3. **Default** — the ``CachedClusterMetadata`` field default.

        Results are cached in ``_loaded`` for subsequent reads.
        """
        value: Any = None

        # --- Step 1: try the cache DB ---
        if self._db_path is not None:
            value = self._load_from_db(name)

        # --- Step 2: try the live fetcher ---
        if value is None and self._fetcher is not None:
            value = self._fetcher.fetch(name)

        # --- Step 3: fall back to model default ---
        if value is None:
            value = self._get_default(name)

        # For container fields (e.g. storage, network) that are represented
        # as nested dicts, validate them into the actual Pydantic model.
        if isinstance(value, dict):
            field_info = CachedClusterMetadata.model_fields.get(name)
            if field_info is not None:
                model_cls = field_info.annotation
                if isinstance(model_cls, type) and issubclass(model_cls, BaseModel):
                    value = model_cls.model_validate(value)

        self._loaded[name] = value
        return value

    def _load_from_db(self, name: str) -> Any:
        """Query the cache DB for the given field group.

        Returns the value if found, or ``None`` if the DB has no data
        for this group.
        """
        from pynetappfoundry.cache.db import _query_registry_subset

        subset = {
            path: spec
            for path, spec in self._registry.items()
            if path == name or path.startswith(f"{name}.")
        }

        is_uri = isinstance(self._db_path, str) and str(self._db_path).startswith("file:")
        conn = sqlite3.connect(
            self._db_path,  # type: ignore[arg-type]
            detect_types=sqlite3.PARSE_DECLTYPES,
            uri=is_uri,
        )
        conn.row_factory = sqlite3.Row
        try:
            root_kwargs = _query_registry_subset(conn, self._cluster_name, subset)
        finally:
            conn.close()

        return root_kwargs.get(name)

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
        """Check staleness using envelope data only (no materialization).

        Args:
            ttl_days: Number of days before cache is considered stale.

        Returns:
            True if cache is older than *ttl_days*.
        """
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


# Deferred import — must be after class body to avoid circular dependency.
from pydantic import BaseModel  # noqa: E402
