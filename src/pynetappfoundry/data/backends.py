"""Backends for the unified DataSource accessor.

Defines the :class:`Backend` ABC that all data sources implement, plus
the Phase 3 :class:`OntapBackend`: a thin delegator that routes
``query()`` calls to either the cache database, the generic
:func:`pynetappfoundry.cache.fetch` dispatcher (for whole-model live
reads), or a small filtered-live helper (for filtered / field-restricted
live reads). A live read of a parent-keyed mapping fetches its parents first
(recursively) and sends one request per parent (#975).

Per ADR-0013 §6-§9, ``Backend.get()`` has been removed;
``DataSource.get()`` is now a thin ``query().filter().first()`` wrapper.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections.abc import Iterator
from functools import cached_property
from typing import TYPE_CHECKING, Any, TypeVar

import requests
from pydantic import BaseModel

from pynetappfoundry.cache import fetch
from pynetappfoundry.cache.fetchers import (
    _path_placeholders,
    call_singleton_endpoint,
    fetch_parents,
    iter_parent_urls,
    pinned_parent_ids,
)
from pynetappfoundry.cache.field_mapping import parse_api_record, parse_api_response
from pynetappfoundry.core.models import PaginationConfig
from pynetappfoundry.data._merge import merge_models
from pynetappfoundry.utils.dict_path import (
    PathNotFoundError,
    get_dotted_attr,
    get_nested_value,
)

if TYPE_CHECKING:
    from pynetappfoundry.cache.db import ClusterMetadataDB
    from pynetappfoundry.cache.field_mapping import TypeMapping
    from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
    from pynetappfoundry.clients.ontap.cli import ONTAPCLI
    from pynetappfoundry.core.config import Config
    from pynetappfoundry.data._routing import RoutingDecision

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

_BATCH_SIZE = 100

# Raw ONTAP query-string control params that can arrive in the ``filters``
# dict (QuerySet merges ``order_by`` / ``max_records`` into it). They are not
# record fields, so a singleton GET must not treat them as equality filters.
_ONTAP_CONTROL_KEYS = frozenset(
    {"fields", "return_records", "return_timeout", "order_by", "max_records"}
)
"""Default chunk size for identifier-filtered live fetches.

``_fetch_live_by_identifiers`` and ``_fetch_live_by_parent`` split
identifier lists into chunks of this size.  Each chunk produces one
ONTAP REST call using pipe-OR syntax (``?uuid=id1|id2|id3``).  The
value balances ONTAP URL-length limits (approx 8 KiB for most
controllers) against the number of round-trips.

Per-mapping override: set ``TypeMapping(batch_size=N)`` to override
for endpoints with narrower URL limits.  When ``batch_size`` is
``None`` (the default), this constant is used.

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

    Each backend translates a :class:`RoutingDecision` plus a filter
    dict into concrete fetches against its upstream system and returns
    populated model instances with ``_fetched_fields`` set.

    Class attribute :attr:`supports_where_expressions` controls whether
    the backend accepts SQL-like where-expression strings from
    :meth:`QueryBuilder.where` and non-equality typed DSL operators.
    Defaults to ``False`` so that any new backend that does not
    explicitly opt in rejects where-expressions early (at chain time)
    rather than failing silently at iteration time.

    Args:
        config: The :class:`pynetappfoundry.core.config.Config` instance.
    """

    #: Set to ``True`` on backends whose cache substrate supports
    #: SQL-like where-expression strings (e.g. :class:`OntapBackend`).
    supports_where_expressions: bool = False

    #: Set to ``True`` on backends that accept caller-supplied endpoint path
    #: values through ``query(path_params=...)`` (e.g. :class:`DiiBackend`).
    supports_path_params: bool = False

    def __init__(self, config: Config) -> None:
        self._config = config

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
        path_params: dict[str, Any] | None = None,
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
            path_params: Caller-supplied values for ``{placeholder}`` path
                segments of the mapping's endpoint. Only backends with
                :attr:`supports_path_params` accept a non-empty dict.
                Defaults to ``None``.
        """


class OntapBackend(Backend):
    """Backend that routes against the ONTAP cache DB and REST API.

    Clients (cache DB, API client) are constructed lazily on first
    use to avoid opening files or making HTTP calls when not needed.

    Args:
        config: The :class:`pynetappfoundry.core.config.Config` instance.
    """

    supports_where_expressions: bool = True

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self._api_clients: dict[str, ONTAPAPIClient] = {}
        self._cli_clients: dict[str, ONTAPCLI] = {}

    @cached_property
    def _cache_db(self) -> ClusterMetadataDB:
        """Lazily open the cluster metadata cache DB."""
        from pynetappfoundry.cache.db import ClusterMetadataDB

        return ClusterMetadataDB(config=self._config)

    def _get_api_client(self, cluster: str) -> ONTAPAPIClient:
        """Lazily create an ONTAP API client for *cluster*.

        Cached per-cluster so multiple ``query()`` calls against the
        same cluster reuse the same connection pool.
        """
        if cluster not in self._api_clients:
            from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
            from pynetappfoundry.core.models import ClusterConfig

            cluster_data = self._config.data.get("clusters", {}).get(cluster, {})
            cluster_obj = ClusterConfig(name=cluster, ip=cluster_data.get("ip", cluster))
            self._api_clients[cluster] = ONTAPAPIClient(cluster=cluster_obj, config=self._config)
        return self._api_clients[cluster]

    def _get_cli_client(self, cluster: str) -> ONTAPCLI:
        """Lazily create an ONTAP CLI (SSH) client for *cluster*.

        Cached per-cluster so multiple ``query()`` calls against the
        same cluster reuse the same connection.

        Credentials are resolved via ``Config.get_user`` and the
        cluster's ``ip`` from the configuration data, mirroring
        the pattern used by ``pynetappfoundry.cache.refresher``.
        """
        if cluster not in self._cli_clients:
            from pynetappfoundry.clients.ontap.cli import ONTAPCLI

            cluster_data = self._config.data.get("clusters", {}).get(cluster, {})
            user, password = self._config.get_user("clusters", cluster)
            self._cli_clients[cluster] = ONTAPCLI(
                name=cluster,
                host_or_ip=cluster_data.get("ip", cluster),
                username=user,
                password=password,
                trust_store=self._config.get_trust_store(),
            )
        return self._cli_clients[cluster]

    def _is_cloud_cluster(self, cluster: str) -> bool:
        """Return ``True`` if *cluster* is a cloud (CVO) cluster.

        Queries ``ClusterTraits`` from the cache DB and checks the
        ``is_cloud`` flag. If the cache has no data for the cluster
        (e.g. never refreshed), defaults to ``False`` to avoid SSH
        timeouts on unknown clusters.
        """
        from pynetappfoundry.models.ontap.cluster.traits.model import ClusterTraits

        try:
            metadata_path = self._resolve_metadata_path(ClusterTraits)
            results = self._cache_db.query_with_filters(cluster, metadata_path, [])
            for item in results:
                if isinstance(item, ClusterTraits):
                    return item.is_cloud
        except (ValueError, Exception):
            logger.debug(
                "OntapBackend: cannot determine is_cloud for %s, defaulting to False",
                cluster,
            )
        return False

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
    def _is_full_live_scan(
        mapping: TypeMapping,
        decision: RoutingDecision,
        filters: dict[str, Any],
    ) -> bool:
        """Return True when the live path should delegate to :func:`fetch`.

        The generic :func:`fetch` dispatcher is filterless and fetches
        every instance with every (non-derived) field populated. We
        delegate to it only when:

        - There are no equality filters.
        - The routing decision's ``live_fields`` covers every live-
          eligible (non-derived) field in the mapping.

        Any field restriction or filter falls through to
        :meth:`_fetch_live_filtered`, which builds a URL with the
        narrower ``fields=`` and query-string params.
        """
        if filters:
            return False
        if not decision.live_fields:
            return False
        live_eligible = {f.cache_attr for f in mapping.fields if f.cache_strategy != "derived"}
        return live_eligible.issubset(set(decision.live_fields))

    def _count_live(
        self,
        mapping: TypeMapping,
        cluster: str,
        filters: dict[str, Any],
    ) -> int:
        """Count records via the live REST API without fetching them.

        Builds a URL with ``return_records=false`` via the same URL
        builder used by :meth:`_fetch_live_filtered`, calls
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
        if mapping.parent_mapping:
            return self._count_live_children(mapping, cluster, filters)
        if mapping.response_shape == "singleton":
            return 0 if self._fetch_singleton_raw(mapping, cluster, filters, ()) is None else 1
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

    def _count_live_children(
        self,
        mapping: TypeMapping,
        cluster: str,
        filters: dict[str, Any],
    ) -> int:
        """Count a parent-keyed mapping's records by summing the counts per parent.

        When *filters* pin every path placeholder to literal values, the
        parent fetch is skipped (see :meth:`_child_targets`). A failing parent
        is logged as ``CHILD_FETCH_FAILED`` and skipped; a 404 on a pinned
        target counts as zero.
        """
        client = self._get_api_client(cluster)
        prefix = f"OntapBackend<{mapping.name}>"
        targets, narrowed = self._child_targets(mapping, client, filters, prefix)
        query_filters = self._child_query_filters(mapping, filters, narrowed)
        total = 0
        for label, base_url in targets:
            try:
                if mapping.response_shape == "singleton":
                    record = self._fetch_singleton_raw(
                        mapping, cluster, filters, (), base_url=base_url
                    )
                    total += 0 if record is None else 1
                    continue
                url = self._build_live_url(
                    mapping, query_filters, (), return_records=False, base_url=base_url
                )
                response = client.call_endpoint(url)
                if isinstance(response, dict):
                    total += int(response.get("num_records", 0))
            except requests.HTTPError as e:
                if narrowed and e.response is not None and e.response.status_code == 404:
                    logger.debug("%s pinned target %s answered 404: no records", prefix, label)
                    continue
                self._log_child_failure(prefix, mapping, label, e)
            except Exception as e:
                self._log_child_failure(prefix, mapping, label, e)
        return total

    @staticmethod
    def _log_child_failure(prefix: str, mapping: TypeMapping, label: str, error: Exception) -> None:
        """Log a failed per-parent request as ``CHILD_FETCH_FAILED``."""
        logger.warning(
            "%s CHILD_FETCH_FAILED: %s for parent %s - %s: %s",
            prefix,
            mapping.name,
            label,
            type(error).__name__,
            error,
        )

    @staticmethod
    def _child_targets(
        mapping: TypeMapping,
        client: Any,
        filters: dict[str, Any],
        prefix: str,
    ) -> tuple[list[tuple[str, str]], bool]:
        """Resolve the ``(label, base_url)`` pairs a live child query must request.

        When *filters* pin every path placeholder to literal values (see
        :func:`pynetappfoundry.cache.fetchers.pinned_parent_ids`) the URLs are
        built straight from those values and the parent collection is not
        fetched. Otherwise the parents are fetched and each usable one yields a
        URL.

        Returns:
            ``(targets, narrowed)``; *narrowed* is ``True`` on the pinned path.
        """
        pinned = pinned_parent_ids(mapping, filters)
        if pinned is not None:
            return [
                (
                    ", ".join(values),
                    mapping.build_parameterized_url(values[0] if len(values) == 1 else values),
                )
                for values in pinned
            ], True
        parents = fetch_parents(mapping, client, {}, prefix)
        return [
            (str(getattr(parent, "name", repr(parent))), url)
            for parent, url in iter_parent_urls(mapping, parents, prefix)
        ], False

    @staticmethod
    def _child_query_filters(
        mapping: TypeMapping, filters: dict[str, Any], narrowed: bool
    ) -> dict[str, Any]:
        """Return *filters* for a child query string, minus pinned keys when narrowed.

        The pinned placeholder names are already in the URL path, and whether
        ONTAP accepts them as query filters is not established, so they are
        dropped from the query string on the narrowed path.
        """
        if not narrowed:
            return filters
        pinned_keys = set(_path_placeholders(mapping))
        return {k: v for k, v in filters.items() if k not in pinned_keys}

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

    @staticmethod
    def _build_live_url(
        mapping: TypeMapping,
        params: dict[str, Any],
        live_field_paths: tuple[str, ...],
        *,
        return_records: bool = True,
        base_url: str | None = None,
    ) -> str:
        """Build a live REST URL from a mapping plus params and field set.

        Strips ``{id}`` placeholders from the endpoint, appends each
        param as a query string entry, and overrides the ``fields``
        parameter with the live field set's ``api_path`` values.

        A parent-keyed mapping must be given *base_url*, its endpoint with the
        parent ids already substituted (see
        :func:`pynetappfoundry.cache.fetchers.iter_parent_urls`); stripping the
        placeholder instead would request the wrong collection (#975).

        Raises:
            ValueError: If *mapping* is parent-keyed and *base_url* is ``None``.

        When *return_records* is ``False``, ``return_records=false`` is
        appended to the query string. This is used by :meth:`_count_live`
        to ask ONTAP for ``num_records`` only.

        This helper is also used by :meth:`_fetch_live_filtered` to
        construct the filtered / field-restricted live read URL.
        """
        from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

        if base_url is None:
            if mapping.parent_mapping:
                raise ValueError(
                    f"{mapping.name}: a parent-keyed mapping needs a resolved base_url; "
                    f"fetch its parents first"
                )
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
            existing = query.get("fields", [""])[0]
            if not existing.startswith("*"):
                query["fields"] = [",".join(api_paths)]

        for key, value in params.items():
            query[key] = [str(value)]

        if not return_records:
            query["return_records"] = ["false"]

        return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))

    def _fetch_singleton_raw(
        self,
        mapping: TypeMapping,
        cluster: str,
        filters: dict[str, Any],
        live_fields: tuple[str, ...],
        *,
        base_url: str | None = None,
    ) -> dict[str, Any] | None:
        """GET a singleton endpoint and return its record, or ``None``.

        Mirrors :func:`pynetappfoundry.cache.fetchers.fetch` for singleton
        mappings: ``call_endpoint`` (no pagination, no ``records`` envelope).
        ``live_fields`` narrows the ``fields=`` query. A singleton GET has no
        server-side filtering, so equality *filters* (dotted API paths) are
        applied client-side, comparing as strings like the URL path does;
        a non-matching record yields ``None``.

        ONTAP control keys (:data:`_ONTAP_CONTROL_KEYS`) in *filters* are not
        record fields: they are neither sent nor matched. A singleton has one
        record, so ``order_by`` and ``max_records >= 1`` are no-ops, while
        ``max_records <= 0`` asks for zero records and returns ``None``
        without any network call.
        """
        max_records = filters.get("max_records")
        if max_records is not None and int(max_records) <= 0:
            return None
        client = self._get_api_client(cluster)
        url = self._build_live_url(mapping, {}, live_fields, base_url=base_url)
        response = call_singleton_endpoint(client, url)
        if not response or not isinstance(response, dict):
            return None
        for key, expected in filters.items():
            if key in _ONTAP_CONTROL_KEYS:
                continue
            try:
                actual = get_nested_value(response, key)
            except PathNotFoundError:
                return None
            if str(actual) != str(expected):
                return None
        return response

    def _fetch_live_filtered(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        cluster: str,
        filters: dict[str, Any],
        live_fields: tuple[str, ...],
    ) -> list[T]:
        """Filtered / field-restricted live read for a model.

        This is the narrow live path used when :func:`fetch` cannot
        apply (the caller restricted the field set or supplied an
        equality filter). Builds a URL via :meth:`_build_live_url`,
        calls :meth:`ONTAPAPIClient.get_all_records`, and parses the
        response with :func:`parse_api_response`.

        ONTAP treats a ``max_records`` filter as the page size, so it is
        also passed to :class:`PaginationConfig` to stop paging once that
        many records are collected (#872).
        """
        if mapping.parent_mapping:
            return self._fetch_live_filtered_children(
                model_class, mapping, cluster, filters, live_fields
            )
        if mapping.response_shape == "singleton":
            record = self._fetch_singleton_raw(mapping, cluster, filters, live_fields)
            if record is None:
                return []
            parsed_one = parse_api_record(mapping, record, f"OntapBackend<{mapping.name}>")
            return [parsed_one] if isinstance(parsed_one, model_class) else []
        client = self._get_api_client(cluster)
        url = self._build_live_url(mapping, filters, live_fields)
        max_records = filters.get("max_records")
        if max_records is not None:
            response = client.get_all_records(
                url,
                pagination_config=PaginationConfig(max_records=int(max_records)),
            )
        else:
            response = client.get_all_records(url)
        parsed = parse_api_response(
            mapping,
            response,
            f"OntapBackend<{mapping.name}>",
            _log_missing_fields,
        )
        return [r for r in parsed if isinstance(r, model_class)]

    def _fetch_live_filtered_children(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        cluster: str,
        filters: dict[str, Any],
        live_fields: tuple[str, ...],
    ) -> list[T]:
        """Filtered live read of a parent-keyed mapping, one request per parent.

        Fetches the parents first (recursively, via :func:`fetch_parents`),
        then sends one filtered request per parent. When *filters* pin every
        path placeholder to literal values the parent fetch is skipped and the
        URLs are built from those values (:meth:`_child_targets`); a 404 on
        such a target means no records. ``order_by`` and
        ``max_records`` apply per parent; ``max_records`` is also a running
        total, so no further parent is requested once it is reached. A parent
        whose request fails is logged as ``CHILD_FETCH_FAILED`` and skipped.
        """
        prefix = f"OntapBackend<{mapping.name}>"
        max_records_raw = filters.get("max_records")
        limit = None if max_records_raw is None else int(max_records_raw)
        if limit is not None and limit <= 0:
            return []
        client = self._get_api_client(cluster)
        targets, narrowed = self._child_targets(mapping, client, filters, prefix)
        query_filters = self._child_query_filters(mapping, filters, narrowed)
        results: list[T] = []
        for label, base_url in targets:
            remaining = None if limit is None else limit - len(results)
            if remaining is not None and remaining <= 0:
                break
            parent_filters = dict(filters)
            query_parent_filters = dict(query_filters)
            if remaining is not None:
                parent_filters["max_records"] = remaining
                query_parent_filters["max_records"] = remaining
            try:
                if mapping.response_shape == "singleton":
                    record = self._fetch_singleton_raw(
                        mapping, cluster, parent_filters, live_fields, base_url=base_url
                    )
                    parsed = [] if record is None else [parse_api_record(mapping, record, prefix)]
                else:
                    url = self._build_live_url(
                        mapping, query_parent_filters, live_fields, base_url=base_url
                    )
                    if remaining is not None:
                        response = client.get_all_records(
                            url, pagination_config=PaginationConfig(max_records=remaining)
                        )
                    else:
                        response = client.get_all_records(url)
                    parsed = parse_api_response(mapping, response, prefix, _log_missing_fields)
            except requests.HTTPError as e:
                if narrowed and e.response is not None and e.response.status_code == 404:
                    logger.debug("%s pinned target %s answered 404: no records", prefix, label)
                else:
                    self._log_child_failure(prefix, mapping, label, e)
                continue
            except Exception as e:
                self._log_child_failure(prefix, mapping, label, e)
                continue
            results.extend(r for r in parsed if isinstance(r, model_class))
        return results if limit is None else results[:limit]

    def query(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        decision: RoutingDecision,
        cluster: str,
        filters: dict[str, Any],
        *,
        where_expressions: tuple[str, ...] = (),
        path_params: dict[str, Any] | None = None,
    ) -> list[T]:
        """Fetch a list of instances matching *filters*.

        *path_params* is accepted for signature compatibility with
        :meth:`Backend.query`; ONTAP endpoints take no caller-supplied path
        values, so a non-empty dict raises :class:`ValueError` before any I/O.

        When the routing decision is *partial* (mix of cache and live
        fields), implements the Approach C algorithm: the cache query
        defines membership, a single batched live fetch enriches by
        identifier, and results are merged by identifier. See the design
        notes on issue #495 for the full rationale.

        When the decision is whole-model live (no filters, no field
        restriction), delegates to :func:`pynetappfoundry.cache.fetch`.
        Otherwise filtered/field-restricted live reads go through
        :meth:`_fetch_live_filtered`.

        *where_expressions* adds SQL-like filter strings that are ANDed
        with the dict-derived equality fragments on the cache path. Live
        and partial-fetch routes raise :class:`NotImplementedError` when
        *where_expressions* is non-empty; see issue #512.
        """
        if path_params:
            msg = "OntapBackend does not support path_params; it is only available on DiiBackend"
            raise ValueError(msg)
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

            if mapping.cli_command:
                # CLI-only mapping (e.g. CloudMetadata). Skip non-cloud
                # clusters to avoid SSH timeouts on on-prem hardware.
                if not self._is_cloud_cluster(cluster):
                    logger.debug(
                        "OntapBackend: skipping CLI-only %s for non-cloud cluster %s",
                        mapping.name,
                        cluster,
                    )
                    return []
                fetched = fetch(
                    model_class,
                    cluster=cluster,
                    config=self._config,
                    api_client=self._get_api_client(cluster),
                    cli_client=self._get_cli_client(cluster),
                )
                results = list(fetched) if isinstance(fetched, list) else [fetched]
            elif self._is_full_live_scan(mapping, decision, filters):
                # Whole-model unfiltered live read: delegate to the
                # generic fetcher (ADR-0013 §6/§7).
                fetched = fetch(
                    model_class,
                    cluster=cluster,
                    config=self._config,
                    api_client=self._get_api_client(cluster),
                )
                results = list(fetched) if isinstance(fetched, list) else [fetched]
            else:
                results = self._fetch_live_filtered(
                    model_class,
                    mapping,
                    cluster,
                    filters,
                    decision.live_fields,
                )

            for instance in results:
                self._mark_fetched(instance, decision.live_fields)
            return results

        return []

    @staticmethod
    def _mark_fetched(instance: BaseModel, paths: tuple[str, ...]) -> None:
        """Populate ``_fetched_fields`` on a model instance."""
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
        5. Branch on parent-keyed vs standard mappings:
           - Parent-keyed: group by parent, per-parent batched live fetch.
           - Standard: single batched live fetch by identifier.
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

        if mapping.parent_mapping is not None:
            parent_ref_fields = self._extract_parent_ref_fields(mapping)
            parent_groups = self._resolve_parent_uuids(
                mapping, cached_instances, cluster, parent_ref_fields
            )
            live_instances = self._fetch_live_by_parent(
                model_class,
                mapping,
                cluster,
                parent_groups,
                identifier_field,
                decision.live_fields,
            )
        else:
            identifiers = [get_dotted_attr(inst, identifier_field) for inst in cached_instances]
            live_instances = self._fetch_live_by_identifiers(
                model_class,
                mapping,
                cluster,
                identifiers,
                identifier_field,
                decision.live_fields,
            )

        live_index: dict[str, T] = {
            get_dotted_attr(inst, identifier_field): inst for inst in live_instances
        }
        return self._merge_partial_collection(
            cached_instances,
            live_index,
            identifier_field,
            decision,
        )

    @staticmethod
    def _extract_parent_ref_fields(mapping: TypeMapping) -> tuple[str, ...]:
        """Parse every ``{placeholder}`` from a parameterized ``api_endpoint``.

        Returns the dotted attribute paths inside the ``{...}`` placeholders,
        in order (e.g. ``("volume.uuid",)`` from
        ``"/storage/volumes/{volume.uuid}/snapshots"``), or an empty tuple if
        no placeholder is found.
        """
        import re as _re

        return tuple(_re.findall(r"\{([^}]+)\}", mapping.api_endpoint.split("?", 1)[0]))

    @staticmethod
    def _extract_parent_ref_field(mapping: TypeMapping) -> str | None:
        """Parse the first ``{placeholder}`` from a parameterized ``api_endpoint``.

        Returns the dotted attribute path inside the first ``{...}``
        placeholder (e.g. ``"volume.uuid"`` from
        ``"/storage/volumes/{volume.uuid}/snapshots"``), or ``None`` if no
        placeholder is found.
        """
        fields = OntapBackend._extract_parent_ref_fields(mapping)
        return fields[0] if fields else None

    def _resolve_parent_uuids(
        self,
        mapping: TypeMapping,
        cached_instances: list[T],
        cluster: str,
        parent_ref_fields: tuple[str, ...],
    ) -> dict[tuple[str, ...], list[T]]:
        """Group *cached_instances* by parent UUID for parent-keyed live fetch.

        For each cached child, resolves every field of *parent_ref_fields* via
        dotted-attr lookup.  Children where any ref resolves to ``None`` or
        empty string are logged as warnings and excluded from the grouped result.

        If **all** children yield ``None`` (the SvmMigrationVolume case,
        where the child model has no back-reference to the parent), falls
        back to querying the parent model from cache and returning all
        children under each parent UUID.

        Returns:
            ``{(parent_value, ...): [children]}`` dict, one value per path
            placeholder, suitable for
            :meth:`_fetch_live_by_parent`.
        """
        from collections import defaultdict

        groups: dict[tuple[str, ...], list[T]] = defaultdict(list)
        orphans: list[T] = []

        for child in cached_instances:
            ref_values = [get_dotted_attr(child, f) for f in parent_ref_fields]
            if parent_ref_fields and all(ref_values):
                groups[tuple(str(v) for v in ref_values)].append(child)
            else:
                orphans.append(child)

        if groups:
            # Some children resolved — orphans are logged and excluded.
            if orphans:
                logger.warning(
                    "DataSource %s: %d cached children have no parent ref "
                    "via %r; they will pass through unmerged",
                    mapping.name,
                    len(orphans),
                    ", ".join(parent_ref_fields),
                )
            return dict(groups)

        # ALL children yielded None — fall back to parent model cache query.
        from pynetappfoundry.cache._registry import model_registry

        parent_type_mapping = model_registry.get_mapping(mapping.parent_mapping or "")
        if parent_type_mapping is None:
            logger.warning(
                "DataSource %s: parent mapping %r not found in registry; "
                "cannot resolve parent UUIDs for cache-fallback path",
                mapping.name,
                mapping.parent_mapping,
            )
            return {}

        parent_model_class = parent_type_mapping.model_class
        parent_instances = self._fetch_cache(parent_model_class, cluster, [])

        parent_id_fields = mapping.effective_parent_id_fields() or ("uuid",)
        for parent in parent_instances:
            pids = [get_dotted_attr(parent, f) for f in parent_id_fields]
            if all(pids):
                groups[tuple(str(p) for p in pids)] = list(cached_instances)

        return dict(groups)

    def _fetch_live_by_parent(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        cluster: str,
        parent_groups: dict[tuple[str, ...], list[T]],
        identifier_field: str,
        live_field_paths: tuple[str, ...],
    ) -> list[T]:
        """Per-parent batched live fetch for parent-keyed mappings.

        For each parent key (one value per placeholder) and its children, builds a resolved URL via
        :meth:`TypeMapping.build_parameterized_url`, overrides ``fields=``
        with the live field paths (preserving ``fields=*`` when present),
        adds pipe-OR identifier filters chunked by batch size, and
        fetches via :meth:`ONTAPAPIClient.get_all_records`.

        Assumptions:

        - **Pipe-OR filter syntax** is ONTAP-specific.  Non-ONTAP
          backends (#533) will need a different batching strategy.
        - **Single identifier field only.**  Composite identifiers
          (#535) are not supported in the batched path.
        - **``mapping.batch_size`` override** — when set, overrides the
          module-level ``_BATCH_SIZE`` constant (100) for this mapping.

        Chunk failures propagate atomically — if any chunk's call raises,
        the whole fetch raises. There is no partial result.

        Returns:
            Aggregated list of parsed model instances across all parents
            and chunks.
        """
        from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

        client = self._get_api_client(cluster)

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

        chunk_size = mapping.batch_size or _BATCH_SIZE
        results: list[T] = []
        for parent_key, children in parent_groups.items():
            base_url = mapping.build_parameterized_url(
                parent_key[0] if len(parent_key) == 1 else parent_key
            )
            parsed = urlparse(base_url)
            base_query: dict[str, list[str]] = parse_qs(parsed.query, keep_blank_values=True)

            # Extract child identifiers, filtering out None/empty.
            child_ids = [
                str(cid) for child in children if (cid := get_dotted_attr(child, identifier_field))
            ]
            if not child_ids:
                continue

            for chunk in self._chunked(child_ids, chunk_size):
                query = {k: list(v) for k, v in base_query.items()}
                if api_paths:
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
        """Batch-fetch live data for *identifiers*, chunked by batch size.

        For each chunk, builds one URL using ONTAP REST pipe-OR syntax
        on the identifier filter (``?{identifier_field}=id1|id2|id3``)
        with the ``fields=`` query parameter restricted to the
        ``api_path`` values of *live_field_paths*. Results across all
        chunks are concatenated into a single list.

        Assumptions:

        - **Pipe-OR filter syntax** is ONTAP-specific.  Non-ONTAP
          backends (#533) will need a different batching strategy.
        - **Single identifier field only.**  Composite identifiers
          (#535) are not supported in the batched path.
        - **``mapping.batch_size`` override** — when set, overrides the
          module-level ``_BATCH_SIZE`` constant (100) for this mapping.

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

        chunk_size = mapping.batch_size or _BATCH_SIZE
        results: list[T] = []
        for chunk in self._chunked(list(identifiers), chunk_size):
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
            key = get_dotted_attr(cached, identifier_field)
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
