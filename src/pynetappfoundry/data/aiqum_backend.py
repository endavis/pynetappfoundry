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

from pydantic import BaseModel

from pynetappfoundry.cache.field_mapping import parse_api_record
from pynetappfoundry.data._path_params import caller_path_params as _caller_path_params
from pynetappfoundry.data._path_params import placeholders as _placeholders
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
    segments of an endpoint (#1054); fetching once per parent object is not
    supported (#1057).  API clients are built lazily and cached per instance
    name.

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
        with placeholders and no *path_params* also raises :class:`ValueError`:
        fetching once per parent object is tracked in #1057.
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
        elif placeholders:
            names = ", ".join("{" + p + "}" for p in placeholders)
            msg = (
                f"{mapping.name}: endpoint {mapping.api_endpoint} has path "
                f"placeholder(s) {names}; pass path_params to supply them. "
                "Fetching once per parent object is not supported yet (#1057)"
            )
            raise ValueError(msg)

        client = self._get_api_client(cluster)
        query_params: dict[str, Any] = dict(filters) if filters else {}
        # Only pass path_params when supplied, so mocks that predate it still work.
        extra: dict[str, Any] = {"path_params": encoded} if encoded is not None else {}
        records: list[Any]
        if mapping.response_shape == "singleton":
            response = client.call_endpoint(
                mapping.api_endpoint, query_params=query_params, **extra
            )
            if isinstance(response, dict):
                records = [response]
            else:
                logger.warning(
                    "AiqumBackend %s: singleton response is %s, expected dict, returning empty",
                    mapping.name,
                    type(response).__name__,
                )
                records = []
        else:
            response = client.get_all_records(
                mapping.api_endpoint, "GET", query_params=query_params, **extra
            )
            records = _records_at_path(mapping, response)
        return self._parse_records(model_class, mapping, decision, records)

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
