"""DII (Data Infrastructure Insights) backend for the unified DataSource accessor.

Implements :class:`DiiBackend`, a live-only backend that queries the DII
REST API.  DII has no local cache database; all queries go directly to
the remote API.

DII endpoints return bare JSON arrays or ``{offset, count, limit,
rows|results|values}`` envelopes, so this backend calls
:meth:`DIIAPIClient.get_all_pages` and feeds each record through
:func:`parse_api_record` individually rather than using the
envelope-oriented :func:`parse_api_response`.  A mapping with a non-empty
``records_path`` (a wrapper such as ``{"users": [...]}``) has its records
read from that path on a dict response.  A mapping with
``response_shape == "singleton"`` marks an endpoint whose dict response is
itself one record (e.g. ``GET /au/oneTimeToken``); it is wrapped as
``[response]`` (#919, #935, ADR-0015).
"""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.fetchers import iter_parent_ids, validate_parent_chain
from pynetappfoundry.cache.field_mapping import parse_api_record
from pynetappfoundry.clients.dii.api import extract_envelope_records
from pynetappfoundry.data._routing import RoutingDecision
from pynetappfoundry.data.backends import Backend
from pynetappfoundry.utils.dict_path import PathNotFoundError, get_nested_value

if TYPE_CHECKING:
    from pynetappfoundry.cache.field_mapping import TypeMapping
    from pynetappfoundry.clients.dii.api import DIIAPIClient
    from pynetappfoundry.core.config import Config

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def _records_at_path(mapping: TypeMapping, response: dict[str, Any]) -> list[Any]:
    """Return the records at ``mapping.records_path`` in *response*.

    Logs a warning and returns ``[]`` when the path is missing or does not
    resolve to a list.
    """
    try:
        value = get_nested_value(response, mapping.records_path)
    except PathNotFoundError as exc:
        logger.warning(
            "DiiBackend %s: records_path %r not found in response (%s), returning empty",
            mapping.name,
            mapping.records_path,
            exc.reason,
        )
        return []
    if not isinstance(value, list):
        logger.warning(
            "DiiBackend %s: records_path %r resolved to %s, expected list, returning empty",
            mapping.name,
            mapping.records_path,
            type(value).__name__,
        )
        return []
    return value


def _placeholders(mapping: TypeMapping) -> list[str]:
    """Return the ``{name}`` path placeholders of ``mapping.api_endpoint``, in order."""
    return re.findall(r"\{([^}]+)\}", mapping.api_endpoint.split("?", 1)[0])


def _records_from_response(mapping: TypeMapping, response: Any) -> list[Any]:
    """Extract the record list from a ``get_all_pages`` *response* (ADR-0015)."""
    if isinstance(response, list):
        return response
    if response is None:
        return []
    if isinstance(response, dict) and mapping.response_shape == "singleton":
        return [response]
    if isinstance(response, dict) and mapping.records_path:
        return _records_at_path(mapping, response)
    if (envelope := extract_envelope_records(response)) is not None:
        return envelope
    # Unexpected shape -- treat as empty.
    logger.warning(
        "DiiBackend %s: unexpected response type %s, returning empty",
        mapping.name,
        type(response).__name__,
    )
    return []


class DiiBackend(Backend):
    """Live-only backend that queries the DII REST API.

    DII has no local cache database.  Every ``query()`` call hits the
    remote API directly.  Cache-only routing decisions and
    ``where_expressions`` are rejected with :class:`NotImplementedError`.

    ``where_expressions`` are not supported: :attr:`supports_where_expressions`
    is explicitly ``False`` so that :class:`QueryBuilder` raises
    :class:`ValueError` at chain time (before iteration) when a caller
    passes where-strings or non-equality typed DSL operators.

    API clients are lazily constructed and cached per-cluster (DII tenant)
    for the lifetime of the backend instance.

    Args:
        config: The :class:`pynetappfoundry.core.config.Config` instance.
    """

    supports_where_expressions: bool = False

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self._api_clients: dict[str, DIIAPIClient] = {}

    def _get_api_client(self, cluster: str) -> DIIAPIClient:
        """Lazily create a DII API client for *cluster*.

        Cached per-cluster so multiple ``query()`` calls against the
        same cluster reuse the same connection pool.
        """
        if cluster not in self._api_clients:
            from pynetappfoundry.clients.dii.api import DIIAPIClient

            self._api_clients[cluster] = DIIAPIClient(config=self._config)
        return self._api_clients[cluster]

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
        """Fetch a list of DII instances matching *filters*.

        DII is live-only:

        - Cache-only decisions (``decision.cache_fields`` with no
          ``decision.live_fields``) raise :class:`NotImplementedError`.
        - ``where_expressions`` are not supported and raise
          :class:`NotImplementedError`.

        Filters are translated to simple ``key=value`` query parameters
        on the DII endpoint URL.

        DII endpoints return bare JSON arrays or record envelopes.  A dict
        response is read at ``mapping.records_path`` when that is non-empty
        (checked before the envelope shapes); a bare array is used as-is.
        ``mapping.response_shape == "singleton"`` means the dict response is
        one record and is returned as ``[response]`` (checked before the
        named-path branch).  Each element is parsed individually via
        :func:`parse_api_record` and stamped with ``_fetched_fields``.

        A mapping whose endpoint has ``{placeholder}`` path segments and a
        ``parent_mapping`` is fetched per parent (parents queried first, #985).
        Such a mapping without a ``parent_mapping`` raises :class:`ValueError`
        naming the placeholder(s); nothing is requested.
        """
        if decision.cache_fields and not decision.live_fields:
            msg = "DII backend does not support cache-only queries"
            raise NotImplementedError(msg)

        if where_expressions:
            msg = "DII backend does not support where_expressions"
            raise NotImplementedError(msg)

        if not decision.live_fields:
            return []

        placeholders = _placeholders(mapping)
        if placeholders and not mapping.parent_mapping:
            names = ", ".join("{" + p + "}" for p in placeholders)
            msg = (
                f"{mapping.name}: endpoint {mapping.api_endpoint} has unfilled path "
                f"placeholder(s) {names} and no parent_mapping to supply them; "
                "it cannot be queried live"
            )
            raise ValueError(msg)
        if placeholders:
            return self._query_children(
                model_class, mapping, decision, cluster, filters, placeholders
            )

        client = self._get_api_client(cluster)
        query_params: dict[str, Any] = dict(filters) if filters else {}
        response = client.get_all_pages(mapping.api_endpoint, query_params=query_params)
        return self._parse_records(
            model_class, mapping, decision, _records_from_response(mapping, response)
        )

    @staticmethod
    def _parse_records(
        model_class: type[T],
        mapping: TypeMapping,
        decision: RoutingDecision,
        records: list[Any],
    ) -> list[T]:
        """Parse *records* into *model_class* instances stamped with the live fields."""
        log_prefix = f"DiiBackend<{mapping.name}>"
        results: list[T] = []
        for record in records:
            instance = parse_api_record(mapping, record, log_prefix)
            if isinstance(instance, model_class):
                fetched = getattr(instance, "_fetched_fields", None)
                if fetched is not None:
                    fetched.update(decision.live_fields)
                results.append(instance)
        return results

    def _query_children(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        decision: RoutingDecision,
        cluster: str,
        filters: dict[str, Any],
        placeholders: list[str],
    ) -> list[T]:
        """Fetch a parent-keyed mapping, one request per parent.

        The parents come from a recursive :meth:`query` of the parent mapping
        (chain checked first, before any request).  Each parent then fills the
        endpoint's placeholders through ``path_params`` on the endpoint
        template, so spec-driven pagination still applies.  A parent without
        an identifier is skipped (``SKIP_PARENT``); a parent whose request
        fails is logged as ``CHILD_FETCH_FAILED`` and skipped.  *filters* go to
        the child requests only.
        """
        log_prefix = f"DiiBackend<{mapping.name}>"
        validate_parent_chain(mapping)
        parent_map = model_registry.get_mapping(mapping.parent_mapping or "")
        if parent_map is None:  # pragma: no cover - guarded by validate_parent_chain
            msg = f"{mapping.name}: parent mapping {mapping.parent_mapping!r} is not registered"
            raise ValueError(msg)
        if len(mapping.effective_parent_id_fields()) != len(placeholders):
            msg = (
                f"{mapping.name}: {len(mapping.effective_parent_id_fields())} parent id "
                f"field(s) for {len(placeholders)} placeholder(s) in {mapping.api_endpoint}"
            )
            raise ValueError(msg)

        parent_decision = RoutingDecision(
            cache_fields=(), live_fields=tuple(f.cache_attr for f in parent_map.fields)
        )
        parents = self.query(parent_map.model_class, parent_map, parent_decision, cluster, {})
        client = self._get_api_client(cluster)
        query_params: dict[str, Any] = dict(filters) if filters else {}
        results: list[T] = []
        for parent, values in iter_parent_ids(mapping, parents, log_prefix):
            path_params = dict(zip(placeholders, values, strict=True))
            try:
                response = client.get_all_pages(
                    mapping.api_endpoint, query_params=query_params, path_params=path_params
                )
                records = _records_from_response(mapping, response)
            except Exception as e:
                logger.warning(
                    "%s CHILD_FETCH_FAILED: %s for parent %s - %s: %s",
                    log_prefix,
                    mapping.name,
                    getattr(parent, "name", repr(parent)),
                    type(e).__name__,
                    e,
                )
                continue
            results.extend(self._parse_records(model_class, mapping, decision, records))
        return results
