"""ClusterEntry: lazy per-namespace cache wrapper for cluster config data.

Wraps a cluster's TOML config dict with a dict-like interface for backward
compatibility, and provides lazy ``@cached_property`` accessors for
per-namespace cached metadata (e.g. ``.ontap``, ``.occm``).

The cache database is never opened until a namespace property is accessed.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator, MutableMapping
from functools import cached_property
from pathlib import Path
from typing import Any

from pynetappfoundry.cache._lazy import LazyClusterMetadata

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
    """

    __slots__ = ("__dict__", "_cache_db_path", "_data", "_name")

    def __init__(
        self,
        name: str,
        config_data: dict[str, Any],
        cache_db_path: Path,
    ) -> None:
        self._name = name
        self._data = config_data
        self._cache_db_path = cache_db_path

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
        """Lazily load ONTAP cached metadata for this cluster.

        Opens the cache database on first access, retrieves a lazy-loading
        proxy that defers per-field-group queries until attribute access,
        closes the database, and caches the result.

        Returns:
            LazyClusterMetadata proxy if cache data exists, None otherwise.
        """
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
        """Open the cache DB, fetch lazy metadata for this cluster, close, return."""
        if not self._cache_db_path.exists():
            logging.debug(f"{_file_name} : no cache DB at {self._cache_db_path} for {self._name}")
            return None

        try:
            from pynetappfoundry.cache.db import ClusterMetadataDB

            db = ClusterMetadataDB(db_path=self._cache_db_path)
            try:
                result = db.get_lazy(self._name)
                logging.debug(
                    f"{_file_name} : loaded cache for {self._name}: "
                    f"{'found' if result else 'not found'}"
                )
                return result
            finally:
                db.close()
        except Exception as e:
            logging.debug(f"{_file_name} : could not load cache for {self._name}: {e}")
            return None
