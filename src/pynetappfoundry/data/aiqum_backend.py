"""AIQUM (Active IQ Unified Manager) backend for the unified DataSource accessor.

Implements :class:`AiqumBackend`, a live-only backend that queries the AIQUM
REST API (ADR-0026).  AIQUM has no local cache database; ``source="auto"``
goes live and ``source="cache"`` is rejected by :class:`QueryBuilder`.

AIQUM list endpoints return a HAL envelope ``{_links, num_records, records,
total_records}`` with ``_links.next.href`` paging, so this backend calls
:meth:`AIQUMAPIClient.get_all_records` (which follows the links and merges
``records``) and reads the records at ``mapping.records_path``.  A mapping with
``response_shape == "singleton"`` marks an endpoint whose dict response is
itself one record; it is fetched with ``call_endpoint`` and wrapped as
``[response]``.

The ``cluster=`` argument of ``DataSource.query()`` is the key of the instance
in the ``[aiqums]`` inventory.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, TypeVar
from urllib.parse import quote

import requests
from pydantic import BaseModel

from pynetappfoundry.cache.field_mapping import parse_api_record
from pynetappfoundry.data._path_params import caller_path_params as _caller_path_params
from pynetappfoundry.data._path_params import placeholders as _placeholders
from pynetappfoundry.data._per_parent import fetch_per_parent
from pynetappfoundry.data.backends import Backend
from pynetappfoundry.utils.dict_path import PathNotFoundError, get_nested_value

if TYPE_CHECKING:
    from pynetappfoundry.cache.field_mapping import TypeMapping
    from pynetappfoundry.clients.aiqum.api import AIQUMAPIClient
    from pynetappfoundry.core.config import Config
    from pynetappfoundry.data._routing import RoutingDecision

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def _records_at_path(mapping: TypeMapping, response: Any) -> list[Any]:
    """Return the records at ``mapping.records_path`` in *response*.

    Logs a warning and returns ``[]`` when the path is missing or does not
    resolve to a list.
    """
    try:
        value = get_nested_value(response, mapping.records_path)
    except PathNotFoundError as exc:
        logger.warning(
            "AiqumBackend %s: records_path %r not found in response (%s), returning empty",
            mapping.name,
            mapping.records_path,
            exc.reason,
        )
        return []
    if not isinstance(value, list):
        logger.warning(
            "AiqumBackend %s: records_path %r resolved to %s, expected list, returning empty",
            mapping.name,
            mapping.records_path,
            type(value).__name__,
        )
        return []
    return value


class AiqumBackend(Backend):
    """Live-only backend that queries an AIQUM instance's REST API.

    Cache-only routing decisions and ``where_expressions`` are rejected with
    :class:`NotImplementedError`.  ``path_params`` fill the ``{placeholder}``
    segments of an endpoint (#1054); without them a mapping with a
    ``parent_mapping`` is fetched once per parent (#1057).  API clients are built lazily
    and cached per instance name.

    Args:
        config: The :class:`pynetappfoundry.core.config.Config` instance.
    """

    supports_where_expressions: bool = False
    supports_path_params: bool = True
    live_only: bool = True

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self._api_clients: dict[str, AIQUMAPIClient] = {}

    def _get_api_client(self, name: str) -> AIQUMAPIClient:
        """Lazily create an AIQUM API client for the ``[aiqums]`` instance *name*."""
        if name not in self._api_clients:
            from pynetappfoundry.clients.aiqum.api import AIQUMAPIClient

            self._api_clients[name] = AIQUMAPIClient(name, self._config)
        return self._api_clients[name]

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
        """Fetch a list of AIQUM instances matching *filters*.

        *cluster* names the ``[aiqums]`` instance.  *filters* become query
        parameters.  *path_params* supplies every ``{placeholder}`` value of
        the endpoint (percent-encoded); an unknown key or missing placeholder
        raises :class:`ValueError` before any client is built.  An endpoint
        with placeholders, a ``parent_mapping`` and no *path_params* is fetched
        once per parent (#1057); without a ``parent_mapping`` it raises
        :class:`ValueError`.

        A single ``{identifier_field: <str>}`` filter on a collection whose
        runtime spec has a ``<collection>/{key}`` GET operation is fetched
        from that item endpoint (#1060): one request, the bare object wrapped
        as ``[response]``, and a 404 returns ``[]``.
        """
        if decision.cache_fields and not decision.live_fields:
            msg = "AIQUM backend does not support cache-only queries"
            raise NotImplementedError(msg)

        if where_expressions:
            msg = "AIQUM backend does not support where_expressions"
            raise NotImplementedError(msg)

        if not decision.live_fields:
            return []

        placeholders = _placeholders(mapping)
        encoded: dict[str, str] | None = None
        if path_params:
            encoded = _caller_path_params(mapping, placeholders, path_params)
        elif placeholders and not mapping.parent_mapping:
            names = ", ".join("{" + p + "}" for p in placeholders)
            msg = (
                f"{mapping.name}: endpoint {mapping.api_endpoint} has unfilled path "
                f"placeholder(s) {names} and no parent_mapping to supply them; "
                "pass path_params to supply them"
            )
            raise ValueError(msg)
        elif placeholders:
            return self._query_per_parent(
                model_class, mapping, decision, cluster, filters, placeholders
            )

        if encoded is None and not placeholders:
            client = self._get_api_client(cluster)
            item = self._item_endpoint(mapping, filters, client)
            if item is not None:
                return self._parse_records(
                    model_class, mapping, decision, self._fetch_by_key(mapping, client, *item)
                )

        records = self._fetch_records(mapping, cluster, filters, encoded)
        return self._parse_records(model_class, mapping, decision, records)

    def _fetch_records(
        self,
        mapping: TypeMapping,
        cluster: str,
        filters: dict[str, Any],
        encoded: dict[str, str] | None,
    ) -> list[Any]:
        """Issue one request for *mapping* and return its raw records."""
        client = self._get_api_client(cluster)
        query_params: dict[str, Any] = dict(filters) if filters else {}
        # Only pass path_params when supplied, so mocks that predate it still work.
        extra: dict[str, Any] = {"path_params": encoded} if encoded is not None else {}
        if mapping.response_shape == "singleton":
            response = client.call_endpoint(
                mapping.api_endpoint, query_params=query_params, **extra
            )
            if isinstance(response, dict):
                return [response]
            logger.warning(
                "AiqumBackend %s: singleton response is %s, expected dict, returning empty",
                mapping.name,
                type(response).__name__,
            )
            return []
        response = client.get_all_records(
            mapping.api_endpoint, "GET", query_params=query_params, **extra
        )
        return _records_at_path(mapping, response)

    def _query_per_parent(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        decision: RoutingDecision,
        cluster: str,
        filters: dict[str, Any],
        placeholders: list[str],
    ) -> list[T]:
        """Fetch a parent-keyed mapping, one request per parent (#1057).

        The parents come from a recursive :meth:`query` of the parent mapping on
        the same instance, unfiltered; *filters* go to the child requests only.
        Each parent's identifier is percent-encoded into ``path_params``.  A
        parent without an identifier is skipped (``SKIP_PARENT``) and a failing
        child request is logged as ``CHILD_FETCH_FAILED`` and skipped.  More
        parents than ``max_parent_requests`` (``aiqumapi.toml``; 0 = unlimited)
        raises :class:`ValueError` before any child request.
        """
        max_parents = self._config.get_aiqum_api_settings().max_parent_requests

        def query_parents(parent_map: TypeMapping, parent_decision: RoutingDecision) -> list[Any]:
            return list(
                self.query(parent_map.model_class, parent_map, parent_decision, cluster, {})
            )

        def fetch_child(path_params: dict[str, str]) -> list[Any]:
            return self._fetch_records(mapping, cluster, filters, path_params)

        records = fetch_per_parent(
            mapping,
            placeholders,
            query_parents=query_parents,
            fetch_child=fetch_child,
            log_prefix=f"AiqumBackend<{mapping.name}>",
            encode=True,
            max_parents=max_parents,
        )
        return self._parse_records(model_class, mapping, decision, records)

    @staticmethod
    def _item_endpoint(
        mapping: TypeMapping, filters: dict[str, Any], client: AIQUMAPIClient
    ) -> tuple[str, str] | None:
        """Return ``(item_path, key)`` when *filters* is one lookup by the identifier field.

        The lookup routes to ``<collection>/{<identifier_field>}`` (#1060) only
        when the mapping has a ``str`` identifier field, *filters* is exactly
        ``{identifier_field: <str>}`` with a value that is not ``""``, ``.`` or
        ``..``, and the client's runtime spec declares a GET operation for the
        item path.  Otherwise returns ``None`` and the caller uses the collection.
        """
        field = mapping.identifier_field
        if not isinstance(field, str) or list(filters) != [field]:
            return None
        value = filters[field]
        if not isinstance(value, str) or value in ("", ".", ".."):
            return None
        spec = getattr(client, "api_spec", None)
        if not isinstance(spec, dict):
            return None
        paths = spec.get("paths")
        if not isinstance(paths, dict):
            return None
        item_path = f"{mapping.api_endpoint}/{{{field}}}"
        operations = paths.get(item_path)
        if not isinstance(operations, dict) or "get" not in operations:
            return None
        return item_path, value

    @staticmethod
    def _fetch_by_key(
        mapping: TypeMapping, client: AIQUMAPIClient, item_path: str, value: str
    ) -> list[Any]:
        """GET *item_path* for *value* and wrap the bare object as ``[response]``.

        A 404 means no such object and returns ``[]``; any other error
        propagates.  *value* is percent-encoded with no safe characters.
        """
        field = str(mapping.identifier_field)
        try:
            response = client.call_endpoint(item_path, path_params={field: quote(value, safe="")})
        except requests.HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 404:
                logger.debug("AiqumBackend %s: %s answered 404: no record", mapping.name, item_path)
                return []
            raise
        if isinstance(response, dict):
            return [response]
        logger.warning(
            "AiqumBackend %s: item response is %s, expected dict, returning empty",
            mapping.name,
            type(response).__name__,
        )
        return []

    @staticmethod
    def _parse_records(
        model_class: type[T],
        mapping: TypeMapping,
        decision: RoutingDecision,
        records: list[Any],
    ) -> list[T]:
        """Parse *records* into *model_class* instances stamped with the live fields."""
        log_prefix = f"AiqumBackend<{mapping.name}>"
        results: list[T] = []
        for record in records:
            instance = parse_api_record(mapping, record, log_prefix)
            if isinstance(instance, model_class):
                fetched = getattr(instance, "_fetched_fields", None)
                if fetched is not None:
                    fetched.update(decision.live_fields)
                results.append(instance)
        return results
