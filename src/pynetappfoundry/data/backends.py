"""Backends for the unified DataSource accessor.

Defines the :class:`Backend` ABC that all data sources implement, plus
the spike's only concrete implementation, :class:`OntapBackend`, which
routes ``get()`` and ``query()`` calls to either the cache database or
the live ONTAP REST API based on a :class:`RoutingDecision`.

Phase 2 ships with a single backend (``"ontap"``). Future phases add
``"aiqum"``, ``"occm"``, ``"dii"``, etc., behind the same ABC.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import BaseModel

from pynetappfoundry.cache.field_mapping import parse_api_response
from pynetappfoundry.data._merge import merge_models

if TYPE_CHECKING:
    from pynetappfoundry.cache.db import ClusterMetadataDB
    from pynetappfoundry.cache.field_mapping import TypeMapping
    from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
    from pynetappfoundry.core.config import Config
    from pynetappfoundry.data._routing import RoutingDecision

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

_BATCH_SIZE = 100
"""Hardcoded chunk size for batch live fetches in partial-fetch query.

Per design notes on issue #495, this is intentionally a constant for v1.
Promote to a config knob only if a real workload hits the limit.
"""


def _log_missing_fields(
    record: dict[str, Any],
    expected: list[str],
    type_name: str,
    record_id: str,
) -> None:
    """Debug logger callback satisfying ``parse_api_response``'s signature."""
    missing = [f for f in expected if f not in record]
    if missing:
        logger.debug(
            "DataSource %s[%s]: missing fields %s",
            type_name,
            record_id,
            missing,
        )


class Backend(ABC):
    """Abstract base class for DataSource backends.

    Each backend translates a :class:`RoutingDecision` plus an
    identifier or filter set into concrete fetches against its
    upstream system, and returns populated model instances with
    ``_fetched_fields`` set.

    Args:
        config: The :class:`pynetappfoundry.core.config.Config` instance.
    """

    def __init__(self, config: Config) -> None:
        self._config = config

    @abstractmethod
    def get(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        decision: RoutingDecision,
        cluster: str,
        identifier: dict[str, Any],
    ) -> T | None:
        """Fetch exactly one instance by identifier.

        Returns ``None`` if no matching instance exists. Raises
        :class:`ValueError` if more than one match is found.
        """

    @abstractmethod
    def query(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        decision: RoutingDecision,
        cluster: str,
        filters: dict[str, Any],
        *,
        where_expressions: tuple[str, ...] = (),
    ) -> list[T]:
        """Fetch a list of instances matching *filters*.

        Args:
            model_class: The Pydantic model class to fetch.
            mapping: The :class:`TypeMapping` for the model.
            decision: The routing decision driving cache vs live vs partial.
            cluster: Name of the cluster to fetch from.
            filters: Equality filter dict (dotted API paths as keys).
            where_expressions: SQL-like filter expression strings
                (e.g. ``"size > 1000000000"``) ANDed with the dict
                filters. Only supported on the cache path; live and
                partial paths raise :class:`NotImplementedError` when
                non-empty. Defaults to ``()``.
        """


class OntapBackend(Backend):
    """Backend that routes against the ONTAP cache DB and REST API.

    Clients (cache DB, API client) are constructed lazily on first
    use to avoid opening files or making HTTP calls when not needed
    (mirrors :class:`pynetappfoundry.cache._fetcher.FieldGroupFetcher`).

    Args:
        config: The :class:`pynetappfoundry.core.config.Config` instance.
    """

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self._api_clients: dict[str, ONTAPAPIClient] = {}

    @cached_property
    def _cache_db(self) -> ClusterMetadataDB:
        """Lazily open the cluster metadata cache DB."""
        from pynetappfoundry.cache.db import ClusterMetadataDB

        return ClusterMetadataDB(config=self._config)

    def _get_api_client(self, cluster: str) -> ONTAPAPIClient:
        """Lazily create an ONTAP API client for *cluster*.

        Cached per-cluster so multiple ``get()``/``query()`` calls
        against the same cluster reuse the same connection pool.
        """
        if cluster not in self._api_clients:
            from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
            from pynetappfoundry.core.models import ClusterConfig

            cluster_obj = ClusterConfig(name=cluster, ip=cluster)
            self._api_clients[cluster] = ONTAPAPIClient(cluster=cluster_obj, config=self._config)
        return self._api_clients[cluster]

    def _resolve_metadata_path(self, model_class: type[BaseModel]) -> str:
        """Find the cache table's metadata_path for *model_class*.

        The table registry is keyed by metadata_path (e.g.
        ``"storage.volumes"``); this scans for the entry whose
        ``model_class`` matches.
        """
        from pynetappfoundry.cache.db_schema import _ensure_registry

        registry = _ensure_registry()
        for path, spec in registry.items():
            if spec.model_class is model_class:
                return path
        msg = (
            f"No cache table registered for model {model_class.__name__!r}; "
            f"cache fetches are unavailable for this model."
        )
        raise ValueError(msg)

    @staticmethod
    def _identifier_to_filter_expressions(identifier: dict[str, Any]) -> list[str]:
        """Translate an identifier dict to ``query_with_filters`` strings."""
        return [f"{key} = '{value}'" for key, value in identifier.items()]

    @staticmethod
    def _build_live_url(
        mapping: TypeMapping,
        params: dict[str, Any],
        live_field_paths: tuple[str, ...],
        *,
        return_records: bool = True,
    ) -> str:
        """Build a live REST URL from a mapping plus params and field set.

        Strips ``{id}`` placeholders from the endpoint, appends each
        param as a query string entry, and overrides the ``fields``
        parameter with the live field set's ``api_path`` values.

        When *return_records* is ``False``, ``return_records=false`` is
        appended to the query string. This is used by :meth:`_count_live`
        to ask ONTAP for ``num_records`` only.
        """
        from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

        base_url = mapping.collection_endpoint
        parsed = urlparse(base_url)
        query: dict[str, list[str]] = parse_qs(parsed.query, keep_blank_values=True)

        # Translate live cache_attr paths to api_path values for the query.
        api_paths: list[str] = []
        for attr in live_field_paths:
            field = next(
                (f for f in mapping.fields if f.cache_attr == attr),
                None,
            )
            if field is not None and field.api_path is not None:
                api_paths.append(field.api_path)
            else:
                api_paths.append(attr)
        if api_paths:
            # Preserve fields=* from the base endpoint when present.
            # ONTAP's fields=* returns all fields, which is a superset
            # of any explicit field list. Enumerating individual fields
            # can produce URLs too long for ONTAP to accept (400 error).
            # The value may be "*" or "*,nested.path" — both start with *.
            existing = query.get("fields", [""])[0]
            if not existing.startswith("*"):
                query["fields"] = [",".join(api_paths)]

        for key, value in params.items():
            query[key] = [str(value)]

        if not return_records:
            query["return_records"] = ["false"]

        return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))

    def _count_live(
        self,
        mapping: TypeMapping,
        cluster: str,
        filters: dict[str, Any],
    ) -> int:
        """Count records via the live REST API without fetching them.

        Builds a URL via :meth:`_build_live_url` with
        ``return_records=False``, calls
        :meth:`ONTAPAPIClient.call_endpoint` (NOT ``get_all_records``,
        which would fetch the records and defeat the purpose), and
        reads ``num_records`` off the response envelope.

        Args:
            mapping: The :class:`TypeMapping` for the model to count.
            cluster: Name of the cluster to query.
            filters: Query-string filter dict (dotted API paths).

        Returns:
            The count from ``num_records``, or ``0`` if the response is
            empty / not a dict.
        """
        client = self._get_api_client(cluster)
        url = self._build_live_url(
            mapping,
            filters,
            live_field_paths=(),
            return_records=False,
        )
        response = client.call_endpoint(url)
        if isinstance(response, dict):
            return int(response.get("num_records", 0))
        return 0

    def _fetch_cache(
        self,
        model_class: type[T],
        cluster: str,
        filter_expressions: list[str],
    ) -> list[T]:
        """Run a cache query for *model_class* with *filter_expressions*."""
        metadata_path = self._resolve_metadata_path(model_class)
        results = self._cache_db.query_with_filters(cluster, metadata_path, filter_expressions)
        return [r for r in results if isinstance(r, model_class)]

    def _fetch_live(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        cluster: str,
        params: dict[str, Any],
        live_fields: tuple[str, ...],
    ) -> list[T]:
        """Run a live REST fetch and parse the response into model instances."""
        client = self._get_api_client(cluster)
        url = self._build_live_url(mapping, params, live_fields)
        response = client.get_all_records(url)
        parsed = parse_api_response(
            mapping,
            response,
            f"OntapBackend<{mapping.name}>",
            _log_missing_fields,
        )
        return [r for r in parsed if isinstance(r, model_class)]

    def get(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        decision: RoutingDecision,
        cluster: str,
        identifier: dict[str, Any],
    ) -> T | None:
        """Fetch a single instance by identifier dict."""
        cached_instance: T | None = None
        live_instance: T | None = None

        if decision.cache_fields:
            filters = self._identifier_to_filter_expressions(identifier)
            results = self._fetch_cache(model_class, cluster, filters)
            if len(results) == 0:
                return None
            if len(results) > 1:
                msg = (
                    f"Expected exactly one {mapping.name} matching {identifier!r}, "
                    f"got {len(results)}"
                )
                raise ValueError(msg)
            cached_instance = results[0]

        if decision.live_fields:
            results = self._fetch_live(
                model_class,
                mapping,
                cluster,
                identifier,
                decision.live_fields,
            )
            if len(results) == 0:
                return None
            if len(results) > 1:
                msg = (
                    f"Expected exactly one live {mapping.name} matching "
                    f"{identifier!r}, got {len(results)}"
                )
                raise ValueError(msg)
            live_instance = results[0]

        return self._finalize_single(cached_instance, live_instance, decision)

    def query(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        decision: RoutingDecision,
        cluster: str,
        filters: dict[str, Any],
        *,
        where_expressions: tuple[str, ...] = (),
    ) -> list[T]:
        """Fetch a list of instances matching *filters*.

        When the routing decision is *partial* (mix of cache and live
        fields), implements the Approach C algorithm: the cache query
        defines membership, a single batched live fetch enriches by
        identifier, and results are merged by identifier. See the design
        notes on issue #495 for the full rationale.

        *where_expressions* adds SQL-like filter strings that are ANDed
        with the dict-derived equality fragments on the cache path. Live
        and partial-fetch routes raise :class:`NotImplementedError` when
        *where_expressions* is non-empty; see issue #512.
        """
        if decision.partial:
            if where_expressions:
                msg = (
                    f"DataSource.QueryBuilder.where() is not supported for "
                    f"partial-fetch (mixed cache + live) routing decisions in v1; "
                    f"use source='cache' to apply where-expressions on the cache "
                    f"path only. Expressions were: {list(where_expressions)}"
                )
                raise NotImplementedError(msg)
            return self._query_partial(
                model_class,
                mapping,
                decision,
                cluster,
                filters,
            )

        if decision.cache_fields:
            filter_expressions = [f"{key} = '{value}'" for key, value in filters.items()] + list(
                where_expressions
            )
            results = self._fetch_cache(model_class, cluster, filter_expressions)
            for instance in results:
                self._mark_fetched(instance, decision.cache_fields)
            return results

        if decision.live_fields:
            if where_expressions:
                msg = (
                    f"DataSource.QueryBuilder.where() is not supported on the live "
                    f"path in v1; use .filter({{...}}) for equality filters on "
                    f"live queries. SQL-like expression translation is tracked as "
                    f"a follow-up to #512. Expressions were: {list(where_expressions)}"
                )
                raise NotImplementedError(msg)
            results = self._fetch_live(model_class, mapping, cluster, filters, decision.live_fields)
            for instance in results:
                self._mark_fetched(instance, decision.live_fields)
            return results

        return []

    @staticmethod
    def _mark_fetched(instance: BaseModel, paths: tuple[str, ...]) -> None:
        """Populate ``_fetched_fields`` on a model instance."""
        # OntapModel guarantees the attribute exists. Plain BaseModel
        # subclasses (the synthetic test models) inherit from OntapModel
        # in real usage; we still defensively guard.
        existing = getattr(instance, "_fetched_fields", None)
        if existing is None:
            return
        existing.update(paths)

    def _query_partial(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        decision: RoutingDecision,
        cluster: str,
        filters: dict[str, Any],
    ) -> list[T]:
        """Execute the partial-fetch (Approach C) algorithm for collections.

        1. Validate filter keys are cache-side only.
        2. Validate mapping.identifier_field is a single string.
        3. Run the cache query (defines membership).
        4. Short-circuit on empty cache result.
        5. Batch live fetch by identifier, chunked at ``_BATCH_SIZE``.
        6. Merge each cached instance with its live counterpart by
           identifier. Extras from live are silently dropped; cached
           instances without a live match pass through unmerged.
        """
        self._validate_partial_query_filter(mapping, filters)

        identifier_field = mapping.identifier_field
        if identifier_field is None:
            msg = (
                f"Model {mapping.name!r} has no identifier_field declared in "
                f"its TypeMapping; partial-fetch collection queries require "
                f"identifier_field for merging cache and live results"
            )
            raise ValueError(msg)
        if isinstance(identifier_field, tuple):
            msg = (
                f"Partial-fetch collection queries are not yet supported for "
                f"composite-key models like {mapping.name!r}; use "
                f"source='cache' or source='live' for now"
            )
            raise NotImplementedError(msg)

        filter_expressions = [f"{key} = '{value}'" for key, value in filters.items()]
        cached_instances = self._fetch_cache(model_class, cluster, filter_expressions)
        for instance in cached_instances:
            self._mark_fetched(instance, decision.cache_fields)

        if not cached_instances:
            return []

        if not decision.live_fields:
            # Defensive: decision.partial requires both sides, so this
            # branch should be unreachable. Kept to document intent.
            return cached_instances

        identifiers = self._extract_identifiers(cached_instances, identifier_field)
        live_instances = self._fetch_live_by_identifiers(
            model_class,
            mapping,
            cluster,
            identifiers,
            identifier_field,
            decision.live_fields,
        )
        live_index = self._build_identifier_index(live_instances, identifier_field)
        return self._merge_partial_collection(
            cached_instances,
            live_index,
            identifier_field,
            decision,
        )

    @staticmethod
    def _validate_partial_query_filter(
        mapping: TypeMapping,
        filters: dict[str, Any],
    ) -> None:
        """Raise NotImplementedError if any filter key targets a realtime field.

        Filter keys are matched against :attr:`FieldMapping.cache_attr`.
        Unknown filter keys are permitted (they fall through to the cache
        layer, which surfaces its own error).
        """
        fields_by_attr = {f.cache_attr: f for f in mapping.fields}
        for key in filters:
            field = fields_by_attr.get(key)
            if field is not None and field.cache_strategy == "realtime":
                msg = (
                    f"Filtering collection queries on realtime field {key!r} "
                    f"is not yet supported; use source='live' or split the query"
                )
                raise NotImplementedError(msg)

    @staticmethod
    def _extract_identifiers(
        instances: list[T],
        identifier_field: str,
    ) -> list[str]:
        """Return a list of identifier values from *instances*.

        v1 partial-fetch is single-key only, so *identifier_field* is a
        plain string and the returned list is a list of strings.
        """
        return [getattr(inst, identifier_field) for inst in instances]

    @staticmethod
    def _chunked(items: list[Any], size: int) -> Iterator[list[Any]]:
        """Yield successive chunks of *items* of length *size*."""
        for i in range(0, len(items), size):
            yield items[i : i + size]

    def _fetch_live_by_identifiers(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        cluster: str,
        identifiers: list[str],
        identifier_field: str,
        live_field_paths: tuple[str, ...],
    ) -> list[T]:
        """Batch-fetch live data for *identifiers*, chunked at ``_BATCH_SIZE``.

        For each chunk, builds one URL using ONTAP REST pipe-OR syntax
        on the identifier filter (``?{identifier_field}=id1|id2|id3``)
        with the ``fields=`` query parameter restricted to the
        ``api_path`` values of *live_field_paths*. Results across all
        chunks are concatenated into a single list.

        Chunk failures propagate atomically — if any chunk's call raises
        (network error, REST 5xx, parser failure), the whole fetch
        raises. There is no partial result and no exception swallowing.
        """
        from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

        client = self._get_api_client(cluster)
        base_url = mapping.api_endpoint
        parsed = urlparse(base_url)
        base_query: dict[str, list[str]] = parse_qs(parsed.query, keep_blank_values=True)

        # Translate live cache_attr paths to api_path values.
        api_paths: list[str] = []
        for attr in live_field_paths:
            field = next(
                (f for f in mapping.fields if f.cache_attr == attr),
                None,
            )
            if field is not None and field.api_path is not None:
                api_paths.append(field.api_path)
            else:
                api_paths.append(attr)

        results: list[T] = []
        for chunk in self._chunked(list(identifiers), _BATCH_SIZE):
            query = {k: list(v) for k, v in base_query.items()}
            if api_paths:
                # Preserve fields=* from the base endpoint when present.
                existing = query.get("fields", [""])[0]
                if not existing.startswith("*"):
                    query["fields"] = [",".join(api_paths)]
            query[identifier_field] = ["|".join(chunk)]
            url = urlunparse(parsed._replace(query=urlencode(query, doseq=True)))
            response = client.get_all_records(url)
            parsed_records = parse_api_response(
                mapping,
                response,
                f"OntapBackend<{mapping.name}>",
                _log_missing_fields,
            )
            results.extend(r for r in parsed_records if isinstance(r, model_class))
        return results

    @staticmethod
    def _build_identifier_index(
        instances: list[T],
        identifier_field: str,
    ) -> dict[str, T]:
        """Return ``dict[identifier_value, instance]`` for fast lookup."""
        return {getattr(inst, identifier_field): inst for inst in instances}

    def _merge_partial_collection(
        self,
        cached_instances: list[T],
        live_index: dict[str, T],
        identifier_field: str,
        decision: RoutingDecision,
    ) -> list[T]:
        """Walk *cached_instances*, merging in live data by identifier.

        Cached instances without a matching live entry pass through
        unchanged — their ``_fetched_fields`` still reflect only the
        cache fields that were stamped earlier. Live extras that do not
        match any cached identifier are silently dropped via the
        dict-lookup semantics.
        """
        merged_list: list[T] = []
        for cached in cached_instances:
            key = getattr(cached, identifier_field)
            live = live_index.get(key)
            if live is None:
                merged_list.append(cached)
                continue
            merged = merge_models(cached, live)
            # merge_models unions _fetched_fields already, but stamp the
            # live fields explicitly to be defensive.
            self._mark_fetched(merged, decision.live_fields)
            merged_list.append(merged)
        return merged_list

    def _finalize_single(
        self,
        cached: T | None,
        live: T | None,
        decision: RoutingDecision,
    ) -> T | None:
        """Merge optional cache + live instances and stamp _fetched_fields."""
        if cached is not None and live is not None:
            merged = merge_models(cached, live)
            self._mark_fetched(merged, decision.cache_fields + decision.live_fields)
            return merged
        if cached is not None:
            self._mark_fetched(cached, decision.cache_fields)
            return cached
        if live is not None:
            self._mark_fetched(live, decision.live_fields)
            return live
        return None
