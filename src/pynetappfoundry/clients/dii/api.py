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
            auth_header={"X-CloudInsights-ApiKey": dii_settings.api_ro_token},
            base_api_path=dii_settings.base_api_path,
            timeout=dii_settings.timeout,
            **kwargs,
        )

    def _supports_pagination(self, path: str) -> bool:
        """Return True if the GET spec for *path* declares ``limit`` and ``offset``."""
        _, query_specs = self._extract_parameters(path, "GET")
        names = {spec.get("name") for spec in query_specs}
        return {"limit", "offset"} <= names

    def get_all_pages(self, path: str, query_params: dict[str, Any] | None = None) -> Any:
        """GET *path*, following ``offset``/``limit`` pagination (ADR-0015).

        Pages are requested only when the endpoint's GET spec declares both
        ``limit`` and ``offset``; otherwise one plain request is made. A
        caller-supplied ``offset`` or ``limit`` is explicit: one request, sent
        as given. Pagination covers bare-array responses only.

        Args:
            path: The API path template (e.g. ``/assets/storages``).
            query_params: Query parameters to send with every page.

        Returns:
            The concatenated list of records when paginating, otherwise the
            raw ``call_endpoint`` result.
        """
        params: dict[str, Any] = dict(query_params) if query_params else {}

        if "offset" in params or "limit" in params or not self._supports_pagination(path):
            return self.call_endpoint(path, query_params=params)

        records: list[Any] = []
        for page_number in range(DII_MAX_PAGES):
            offset = page_number * DII_PAGE_SIZE
            page = self.call_endpoint(
                path, query_params={**params, "offset": offset, "limit": DII_PAGE_SIZE}
            )
            if not isinstance(page, list):
                if page_number == 0:
                    return page
                break
            records.extend(page)
            if len(page) < DII_PAGE_SIZE:
                if page_number == 0 and page:
                    logger.warning(
                        "DII %s: first page returned %d records, fewer than the requested "
                        "limit of %d; the server may cap the page size, so results may be "
                        "incomplete",
                        path,
                        len(page),
                        DII_PAGE_SIZE,
                    )
                break
        else:
            logger.error(
                "DII %s: stopped after %d pages (%d records); results may be incomplete",
                path,
                DII_MAX_PAGES,
                len(records),
            )
        return records
