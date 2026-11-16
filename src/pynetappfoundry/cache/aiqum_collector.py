"""Collector for the AIQUM collections served from the cache (#1055, ADR-0026).

A library function only: :class:`AiqumCollector` fetches the collections in
:data:`AIQUM_CACHED_MAPPINGS` from one ``[aiqums]`` instance and
:func:`refresh_aiqum_cache` stores the result in :class:`AiqumCacheDB`.
Collection is all-or-nothing per instance: any failure raises
:class:`CollectionError` before the database is touched.

This module imports nothing from ``pynetappfoundry.data``.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

import requests

from pynetappfoundry.cache._collector_runner import CollectionError
from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.utils.dict_path import PathNotFoundError, get_nested_value

if TYPE_CHECKING:
    from pynetappfoundry.cache.aiqum_db import AiqumCacheDB
    from pynetappfoundry.cache.field_mapping import TypeMapping
    from pynetappfoundry.clients.aiqum.api import AIQUMAPIClient
    from pynetappfoundry.core.config import Config

logger = logging.getLogger(__name__)

#: The AIQUM collections the cache holds.  Everything else stays live-only.
AIQUM_CACHED_MAPPINGS: tuple[str, ...] = ("AiqumCluster", "AiqumSvm", "AiqumVolume")


@dataclass(frozen=True)
class AiqumSnapshot:
    """The collected records of one AIQUM instance.

    Attributes:
        instance: Key of the instance in the ``[aiqums]`` inventory.
        cached_at: When the collection finished.
        records: Raw API records keyed by mapping name.
    """

    instance: str
    cached_at: datetime
    records: dict[str, list[dict[str, Any]]]


def _strip_path(record: dict[str, Any], path: str) -> None:
    """Remove the dotted *path* from *record*, if present."""
    *parents, leaf = path.split(".")
    node: Any = record
    for part in parents:
        node = node.get(part) if isinstance(node, dict) else None
        if node is None:
            return
    if isinstance(node, dict):
        node.pop(leaf, None)


class AiqumCollector:
    """Fetch the cached AIQUM collections from one instance.

    Args:
        api_client: An :class:`AIQUMAPIClient` for the instance.
        mappings: Names of the mappings to collect.
    """

    def __init__(
        self,
        api_client: AIQUMAPIClient,
        mappings: Sequence[str] = AIQUM_CACHED_MAPPINGS,
    ) -> None:
        self._client = api_client
        self._mappings = tuple(mappings)

    def _resolve(self) -> list[TypeMapping]:
        resolved: list[TypeMapping] = []
        for name in self._mappings:
            mapping = model_registry.get_mapping(name)
            if mapping is None:
                raise ValueError(f"Unknown AIQUM mapping {name!r}")
            resolved.append(mapping)
        return resolved

    def _collect_mapping(self, mapping: TypeMapping) -> list[dict[str, Any]]:
        try:
            response = self._client.get_all_records(mapping.api_endpoint, "GET", query_params={})
        except requests.RequestException as exc:
            raise CollectionError(f"{mapping.name}: request failed: {exc}") from exc
        try:
            value = get_nested_value(response, mapping.records_path)
        except PathNotFoundError as exc:
            raise CollectionError(
                f"{mapping.name}: records_path {mapping.records_path!r} not found ({exc.reason})"
            ) from exc
        if not isinstance(value, list):
            raise CollectionError(
                f"{mapping.name}: records_path {mapping.records_path!r} resolved to "
                f"{type(value).__name__}, expected list"
            )
        realtime_paths = [
            f.api_path
            for f in mapping.fields
            if f.cache_strategy == "realtime" and f.api_path is not None
        ]
        records = [dict(rec) for rec in value if isinstance(rec, dict)]
        for rec in records:
            for path in realtime_paths:
                _strip_path(rec, path)
        return records

    def collect(self, instance: str) -> AiqumSnapshot:
        """Collect every mapping from *instance*, all or nothing.

        Raises:
            ValueError: If a mapping name is unknown.
            CollectionError: If any request fails or a response has no record list.
        """
        records = {m.name: self._collect_mapping(m) for m in self._resolve()}
        logger.info(
            "Collected AIQUM instance %s: %s",
            instance,
            {name: len(recs) for name, recs in records.items()},
        )
        return AiqumSnapshot(instance=instance, cached_at=datetime.now(UTC), records=records)


def refresh_aiqum_cache(
    config: Config, instance: str, *, db: AiqumCacheDB | None = None
) -> AiqumSnapshot:
    """Collect *instance* and replace its snapshot in the AIQUM cache.

    Args:
        config: The configuration holding the ``[aiqums]`` inventory.
        instance: Key of the instance in the ``[aiqums]`` inventory.
        db: Database to write to; defaults to ``{config_dir}/.cache/aiqum_cache.db``.

    Raises:
        CollectionError: If collection fails; the database is left unchanged.
    """
    from pynetappfoundry.cache.aiqum_db import AiqumCacheDB
    from pynetappfoundry.clients.aiqum.api import AIQUMAPIClient

    snapshot = AiqumCollector(AIQUMAPIClient(instance, config)).collect(instance)
    if db is not None:
        db.set(instance, snapshot)
    else:
        with AiqumCacheDB(config=config) as owned:
            owned.set(instance, snapshot)
    return snapshot
