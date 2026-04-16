"""DII (Data Infrastructure Insights) backend for the unified DataSource accessor.

Implements :class:`DiiBackend`, a live-only backend that queries the DII
REST API.  DII has no local cache database; all queries go directly to
the remote API.

DII endpoints return bare JSON arrays (not envelope dicts), so this
backend calls :meth:`DIIAPIClient.call_endpoint` and feeds each record
through :func:`parse_api_record` individually rather than using the
envelope-oriented :func:`parse_api_response`.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import BaseModel

from pynetappfoundry.cache.field_mapping import parse_api_record
from pynetappfoundry.data.backends import Backend

if TYPE_CHECKING:
    from pynetappfoundry.cache.field_mapping import TypeMapping
    from pynetappfoundry.clients.dii.api import DIIAPIClient
    from pynetappfoundry.core.config import Config
    from pynetappfoundry.data._routing import RoutingDecision

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class DiiBackend(Backend):
    """Live-only backend that queries the DII REST API.

    DII has no local cache database.  Every ``query()`` call hits the
    remote API directly.  Cache-only routing decisions and
    ``where_expressions`` are rejected with :class:`NotImplementedError`.

    API clients are lazily constructed and cached per-cluster (DII tenant)
    for the lifetime of the backend instance.

    Args:
        config: The :class:`pynetappfoundry.core.config.Config` instance.
    """

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

        DII endpoints return bare JSON arrays.  Each element is parsed
        individually via :func:`parse_api_record` and stamped with
        ``_fetched_fields``.
        """
        if decision.cache_fields and not decision.live_fields:
            msg = "DII backend does not support cache-only queries"
            raise NotImplementedError(msg)

        if where_expressions:
            msg = "DII backend does not support where_expressions"
            raise NotImplementedError(msg)

        if not decision.live_fields:
            return []

        client = self._get_api_client(cluster)
        url = mapping.api_endpoint
        query_params: dict[str, Any] = dict(filters) if filters else {}

        response = client.call_endpoint(url, query_params=query_params)

        records: list[dict[str, Any]]
        if isinstance(response, list):
            records = response
        elif response is None:
            records = []
        else:
            # Unexpected shape -- treat as empty.
            logger.warning(
                "DiiBackend %s: unexpected response type %s, returning empty",
                mapping.name,
                type(response).__name__,
            )
            records = []

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
