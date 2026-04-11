"""ClusterEntry: lazy per-namespace cache wrapper for cluster config data.

Wraps a cluster's TOML config dict with a dict-like interface for backward
compatibility, and provides lazy ``@cached_property`` accessors for
per-namespace cached metadata (e.g. ``.ontap``, ``.occm``).

The cache database is never opened until a namespace property is accessed.

When a :class:`~pynetappfoundry.core.config.Config` reference is available,
accessing ``.ontap`` on a cluster with no cache DB will transparently
create a :class:`~pynetappfoundry.cache._fetcher.FieldGroupFetcher` so
that field groups can be fetched live from the ONTAP API/CLI.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator, MutableMapping
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pynetappfoundry.cache._lazy import LazyClusterMetadata

if TYPE_CHECKING:
    from pynetappfoundry.cache._fetcher import FieldGroupFetcher
    from pynetappfoundry.core.config import Config

_file_name = Path(__file__).name


class ClusterEntry(MutableMapping[str, Any]):
    """Dict-like wrapper around a cluster's TOML config with lazy cache accessors.

    Provides full dict-interface compatibility (``__getitem__``, ``get``,
    ``keys``, ``items``, etc.) so existing code that treats cluster data
    as a plain dict continues to work unchanged.

    Namespace accessors (``.ontap``, ``.occm``, ``.aiqum``, ``.dii``)
    are ``@cached_property`` attributes that lazily load cached metadata
    on first access.

    Args:
        name: Cluster name (key in the clusters dict).
        config_data: The raw TOML config dict for this cluster.
        cache_db_path: Path to the cluster metadata cache database file.
        config: Optional Config instance for live API/CLI fetching.
        no_cache: When True, ``.ontap`` bypasses the cache database entirely
            and returns a fetcher-only proxy that fetches every field group
            live from the ONTAP API/CLI. Requires ``config`` to be set.
    """

    __slots__ = (
        "__dict__",
        "_cache_db_path",
        "_config",
        "_data",
        "_name",
        "_no_cache",
    )

    def __init__(
        self,
        name: str,
        config_data: dict[str, Any],
        cache_db_path: Path,
        config: Config | None = None,
        *,
        no_cache: bool = False,
    ) -> None:
        self._name = name
        self._data = config_data
        self._cache_db_path = cache_db_path
        self._config = config
        self._no_cache = no_cache

    # ------------------------------------------------------------------
    # Dict-like interface
    # ------------------------------------------------------------------

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        del self._data[key]

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value by key with an optional default."""
        return self._data.get(key, default)

    def keys(self) -> Any:
        """Return the keys of the underlying config dict."""
        return self._data.keys()

    def values(self) -> Any:
        """Return the values of the underlying config dict."""
        return self._data.values()

    def items(self) -> Any:
        """Return the items of the underlying config dict."""
        return self._data.items()

    def copy(self) -> dict[str, Any]:
        """Return a shallow copy of the underlying config dict."""
        return self._data.copy()

    # ------------------------------------------------------------------
    # Attribute access fallback
    # ------------------------------------------------------------------

    def __getattr__(self, name: str) -> Any:
        # Only called when normal attribute lookup fails.
        # Delegate to the underlying data dict.
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute {name!r}"
            ) from None

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"ClusterEntry({self._name!r}, {self._data!r})"

    # ------------------------------------------------------------------
    # Lazy namespace accessors
    # ------------------------------------------------------------------

    @cached_property
    def ontap(self) -> LazyClusterMetadata | None:
        """Lazily load ONTAP metadata for this cluster.

        Opens the cache database on first access, retrieves a lazy-loading
        proxy that defers per-field-group queries until attribute access,
        closes the database, and caches the result.

        When ``no_cache=True`` was passed to the constructor (typically via
        :class:`~pynetappfoundry.core.config.Config`), this returns a
        fetcher-only proxy that bypasses the cache database entirely and
        fetches every field group live from the ONTAP API/CLI.

        Returns:
            LazyClusterMetadata proxy if cache data exists or a live fetcher
            can be built, None otherwise.
        """
        if self._no_cache:
            return self._build_live_metadata()
        return self._load_cached_metadata()

    @cached_property
    def occm(self) -> None:
        """Reserved for future BlueXP/OCCM data."""
        return None

    @cached_property
    def aiqum(self) -> None:
        """Reserved for future AIQUM data."""
        return None

    @cached_property
    def dii(self) -> None:
        """Reserved for future Data Infrastructure Insights data."""
        return None

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_cached_metadata(self) -> LazyClusterMetadata | None:
        """Open the cache DB, fetch lazy metadata for this cluster, close, return.

        Fallback order:

        1. **Cache DB exists** — load from DB with an optional fetcher
           attached for missing/stale field groups.
        2. **No cache DB, Config available** — return a DB-less
           ``LazyClusterMetadata`` backed entirely by a live fetcher.
        3. **No cache DB, no Config** — return ``None`` (original behaviour).
        """
        fetcher = self._build_fetcher()

        if self._cache_db_path.exists():
            from pynetappfoundry.cache.db import ClusterMetadataDB

            db: ClusterMetadataDB | None = None
            result: LazyClusterMetadata | None = None
            try:
                db = ClusterMetadataDB(db_path=self._cache_db_path, config=self._config)
                result = db.get_lazy(self._name)
            except Exception as e:
                if db is not None:
                    db.close()
                logging.debug(f"{_file_name} : could not load cache for {self._name}: {e}")
                result = None
            else:
                logging.debug(
                    f"{_file_name} : loaded cache for {self._name}: "
                    f"{'found' if result else 'not found'}"
                )
            if result is not None:
                # Attach fetcher so missing groups can be fetched live.
                if fetcher is not None:
                    result._fetcher = fetcher
                return result  # caller owns the db via the shim
            # No shim — close the db before falling through.
            if db is not None:
                db.close()
            # Fall through to fetcher-only path below.

        # No cache DB (or DB load failed) — try fetcher-only mode.
        live = self._build_live_metadata(fetcher=fetcher)
        if live is not None:
            logging.debug(f"{_file_name} : no cache DB for {self._name}, using live fetcher")
            return live

        logging.debug(f"{_file_name} : no cache DB at {self._cache_db_path} for {self._name}")
        return None

    def _build_live_metadata(
        self, fetcher: FieldGroupFetcher | None = None
    ) -> LazyClusterMetadata | None:
        """Construct a fetcher-only :class:`LazyClusterMetadata` (no cache DB).

        Args:
            fetcher: Optional pre-built fetcher. If None, one is built from
                the cluster's Config.

        Returns:
            Fetcher-backed LazyClusterMetadata, or None when no fetcher
            can be built (no Config or no cluster IP).
        """
        if fetcher is None:
            fetcher = self._build_fetcher()
        if fetcher is None:
            return None

        from pynetappfoundry.cache._base import METADATA_SCHEMA_VERSION, _utcnow
        from pynetappfoundry.cache.db_schema import _ensure_registry

        return LazyClusterMetadata(
            cluster_name=self._name,
            cached_at=_utcnow().isoformat(),
            cache_version=METADATA_SCHEMA_VERSION,
            db_path=None,
            registry=_ensure_registry(),
            config=self._config,
            fetcher=fetcher,
        )

    def _build_fetcher(self) -> FieldGroupFetcher | None:
        """Create a :class:`FieldGroupFetcher` if Config is available.

        Returns ``None`` when no Config is set or the cluster has no ``ip``
        in its config data.
        """
        if self._config is None:
            return None

        cluster_ip = self._data.get("ip", "")
        if not cluster_ip:
            logging.debug(f"{_file_name} : no IP for {self._name}, cannot create fetcher")
            return None

        from pynetappfoundry.cache._fetcher import FieldGroupFetcher

        return FieldGroupFetcher(
            cluster_name=self._name,
            cluster_ip=cluster_ip,
            config=self._config,
        )
