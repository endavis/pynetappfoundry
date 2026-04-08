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
    ) -> list[T]:
        """Fetch a list of instances matching *filters*."""


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
    ) -> str:
        """Build a live REST URL from a mapping plus params and field set.

        Strips ``{id}`` placeholders from the endpoint, appends each
        param as a query string entry, and overrides the ``fields``
        parameter with the live field set's ``api_path`` values.
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
            query["fields"] = [",".join(api_paths)]

        for key, value in params.items():
            query[key] = [str(value)]

        return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))

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
    ) -> list[T]:
        """Fetch a list of instances matching *filters*."""
        if decision.partial:
            # Partial-merge for collection queries is out of scope for the
            # spike: collection responses pair up by identifier, which is
            # non-trivial. Phase 3 will address this if real callers need it.
            msg = (
                "OntapBackend.query() does not yet support partial cache+live "
                "routing for collections; request all-cache or all-live."
            )
            raise NotImplementedError(msg)

        if decision.cache_fields:
            filter_expressions = [f"{key} = '{value}'" for key, value in filters.items()]
            results = self._fetch_cache(model_class, cluster, filter_expressions)
            for instance in results:
                self._mark_fetched(instance, decision.cache_fields)
            return results

        if decision.live_fields:
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
