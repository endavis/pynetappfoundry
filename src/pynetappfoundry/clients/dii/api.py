"""Data Infrastructure Insights (DII) API client."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from pynetappfoundry.clients.openapi import APIWrapper

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config

logger = logging.getLogger(__name__)

#: Page size requested from DII via the ``limit`` query parameter.
DII_PAGE_SIZE = 500

#: Upper bound on pages fetched for one call, a guard against a server that never ends.
DII_MAX_PAGES = 1000

#: Keys that hold the record list in a DII ``{offset, count, limit, <records>}`` envelope.
ENVELOPE_RECORD_KEYS = ("rows", "results", "values")


def extract_envelope_records(response: Any) -> list[Any] | None:
    """Return the record list of a DII envelope response, else ``None``.

    An envelope is a dict with an ``offset`` key, an integer ``count`` and
    exactly one of :data:`ENVELOPE_RECORD_KEYS` holding a list.
    """
    if not isinstance(response, dict) or "offset" not in response:
        return None
    count = response.get("count")
    if not isinstance(count, int) or isinstance(count, bool):
        return None
    present = [k for k in ENVELOPE_RECORD_KEYS if k in response]
    if len(present) != 1:
        return None
    records = response[present[0]]
    return records if isinstance(records, list) else None


class DIIAPIClient(APIWrapper):
    """API client for Data Infrastructure Insights (formerly Cloud Insights)."""

    def __init__(self, config: Config, **kwargs: Any) -> None:
        """Initialize the DII API client.

        Args:
            config: Configuration object with DII API settings.
            **kwargs: Additional arguments passed to APIWrapper.
        """
        self.config = config

        dii_settings = config.get_dii_api_settings()
        super().__init__(
            api_json_file=str(config.get_schema_location("dii") / "all.json"),
            base_url=dii_settings.base_url,
            auth_header={"X-CloudInsights-ApiKey": dii_settings.api_ro_token.get_secret_value()},
            base_api_path=dii_settings.base_api_path,
            timeout=dii_settings.timeout,
            **kwargs,
        )

    def _supports_pagination(self, path: str) -> bool:
        """Return True if the GET spec for *path* declares ``limit`` and ``offset``."""
        _, query_specs = self._extract_parameters(path, "GET")
        names = {spec.get("name") for spec in query_specs}
        return {"limit", "offset"} <= names

    @staticmethod
    def _envelope_total(page: dict[str, Any]) -> int | None:
        """Return the envelope's total (``objectCount``, else ``count``), integers only."""
        for key in ("objectCount", "count"):
            value = page.get(key)
            if isinstance(value, int) and not isinstance(value, bool):
                return value
        return None

    def _page_envelope(
        self,
        path: str,
        params: dict[str, Any],
        first_records: list[Any],
        first_page: dict[str, Any],
        path_params: dict[str, Any] | None = None,
    ) -> list[Any]:
        """Follow ``offset``/``limit`` paging of an envelope endpoint to the end."""
        extra: dict[str, Any] = {} if path_params is None else {"path_params": path_params}
        records: list[Any] = list(first_records)
        page_records = first_records
        page = first_page
        for page_number in range(DII_MAX_PAGES):
            if page_number > 0:
                page = self.call_endpoint(
                    path,
                    query_params={**params, "offset": len(records), "limit": DII_PAGE_SIZE},
                    **extra,
                )
                extracted = extract_envelope_records(page)
                if extracted is None:
                    return records
                page_records = extracted
                records.extend(page_records)
            total = self._envelope_total(page)
            if not page_records:
                break
            if total is not None:
                if len(records) >= total:
                    break
            elif len(page_records) < DII_PAGE_SIZE:
                break
        else:
            logger.error(
                "DII %s: stopped after %d pages (%d records); results may be incomplete",
                path,
                DII_MAX_PAGES,
                len(records),
            )
        return records

    def get_all_pages(
        self,
        path: str,
        query_params: dict[str, Any] | None = None,
        path_params: dict[str, Any] | None = None,
    ) -> Any:
        """GET *path*, following ``offset``/``limit`` pagination (ADR-0015).

        Pages are requested only when the endpoint's GET spec declares both
        ``limit`` and ``offset``; otherwise one plain request is made. A
        caller-supplied ``offset`` or ``limit`` is explicit: one request, sent
        as given.

        Return contract:

        - Paginating endpoint, bare array: the concatenated list.
        - Paginating endpoint, envelope (``offset``/``count`` plus one of
          ``rows``/``results``/``values``): the concatenated records list,
          envelope metadata dropped. Paging stops at ``objectCount`` (else
          ``count``), an empty page, or, with no total, a short page.
        - Caller-supplied ``offset``/``limit`` or a non-paginating endpoint:
          the raw ``call_endpoint`` result, envelope included.
        - A non-list first page that is not an envelope is returned as is.

        HTTP errors raised by ``call_endpoint`` propagate.

        Args:
            path: The API path template (e.g. ``/assets/storages``).
            query_params: Query parameters to send with every page.
            path_params: Values for the ``{placeholders}`` in *path*, sent
                with every page. *path* stays the template so the spec lookup
                and pagination still apply.

        Returns:
            The concatenated list of records when paginating, otherwise the
            raw ``call_endpoint`` result (see the return contract above).
        """
        params: dict[str, Any] = dict(query_params) if query_params else {}
        extra: dict[str, Any] = {} if path_params is None else {"path_params": path_params}

        if "offset" in params or "limit" in params or not self._supports_pagination(path):
            return self.call_endpoint(path, query_params=params, **extra)

        records: list[Any] = []
        for page_number in range(DII_MAX_PAGES):
            offset = page_number * DII_PAGE_SIZE
            page = self.call_endpoint(
                path,
                query_params={**params, "offset": offset, "limit": DII_PAGE_SIZE},
                **extra,
            )
            if not isinstance(page, list):
                if page_number == 0:
                    envelope = extract_envelope_records(page)
                    if envelope is not None:
                        return self._page_envelope(path, params, envelope, page, path_params)
                    return page
                break
            records.extend(page)
            if len(page) < DII_PAGE_SIZE:
                break
        else:
            logger.error(
                "DII %s: stopped after %d pages (%d records); results may be incomplete",
                path,
                DII_MAX_PAGES,
                len(records),
            )
        return records
