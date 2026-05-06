"""RPC-style POST queries for data-returning endpoints.

Provides :class:`Query`, a lightweight interface for invoking
POST-for-data endpoints (e.g. ``/lake/query/timeseries``) that return
results rather than mutating resources.
"""

from __future__ import annotations

import logging
from typing import Any

from pynetappfoundry.clients.openapi import APIWrapper

logger = logging.getLogger(__name__)


class Query:
    """Interface for RPC-style POST endpoints that return data.

    Unlike :class:`~pynetappfoundry.query.mutation.Mutation`, which
    manages resource lifecycle (create/update/delete), ``Query`` is
    designed for POST-for-data endpoints where the body is a query
    specification and the response is a result set.

    Example::

        q = Query(client, "/lake/query/timeseries")
        results = q.invoke({"metric": "cpu", "interval": "1h"})
    """

    def __init__(self, client: APIWrapper, path: str) -> None:
        """Initialise a ``Query`` bound to a specific endpoint path.

        Args:
            client: API client used to dispatch requests.
            path: Endpoint path (e.g. ``"/lake/query/timeseries"``).
        """
        self._client = client
        self._path = path

    def invoke(
        self,
        body: dict[str, Any] | None = None,
        *,
        query_params: dict[str, Any] | None = None,
    ) -> Any:
        """Execute the query by POSTing *body* to the bound path.

        RPC query endpoints are semantically idempotent reads, so retry is
        enabled by default (unlike :meth:`Mutation.create`, which disables it).

        Args:
            body: Request payload to send as JSON.  ``None`` for endpoints
                that accept no body.
            query_params: Optional query string parameters forwarded to the
                underlying ``call_endpoint`` (e.g. ``{"expand": "true"}``).

        Returns:
            Raw API response — a list of result records, a dict, or any other
            shape returned by the endpoint.
        """
        logger.debug(
            "Query.invoke: POST %s body=%s query_params=%s",
            self._path,
            body,
            query_params,
        )
        return self._client.call_endpoint(
            self._path,
            method="POST",
            body=body,
            query_params=query_params,
        )
