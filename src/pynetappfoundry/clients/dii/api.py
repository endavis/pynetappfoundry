"""Data Infrastructure Insights (DII) API client."""

from __future__ import annotations

import copy
import logging
import re
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

_ID_SCHEMA: dict[str, Any] = {"type": ["string", "integer"]}
_DEFINITION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["id"],
    "properties": {"id": _ID_SCHEMA},
}
_TARGETS_SCHEMA: dict[str, Any] = {"type": "array", "items": _ID_SCHEMA}


def _array_of(item: dict[str, Any]) -> dict[str, Any]:
    """Return an array schema whose items are the object schema *item*."""
    return {"type": "array", "items": item}


#: The spec declares ``{"type": "object"}`` for the request body of the annotation value
#: operations, but DII expects a JSON array (see each operation's ``requestBody.description``).
#: Each entry is (path regex, method, corrected schema). ``rawValue`` has no type
#: constraint and no ``additionalProperties: false`` is set (#1185).
_REQUEST_SCHEMA_FIXES: tuple[tuple[re.Pattern[str], str, dict[str, Any]], ...] = (
    (
        re.compile(r"^/assets/[A-Za-z]+/\{id\}/annotations$"),
        "PUT",
        _array_of(
            {
                "type": "object",
                "required": ["rawValue", "definition"],
                "properties": {"definition": _DEFINITION_SCHEMA},
            }
        ),
    ),
    (
        re.compile(r"^/assets/[A-Za-z]+/\{id\}/annotations$"),
        "DELETE",
        _array_of(
            {
                "type": "object",
                "required": ["definition"],
                "properties": {"definition": _DEFINITION_SCHEMA},
            }
        ),
    ),
    (
        re.compile(r"^/assets/annotations/\{id\}/values$"),
        "PUT",
        _array_of(
            {
                "type": "object",
                "required": ["objectType", "values"],
                "properties": {
                    "objectType": {"type": "string"},
                    "values": _array_of(
                        {
                            "type": "object",
                            "required": ["rawValue", "targets"],
                            "properties": {"targets": _TARGETS_SCHEMA},
                        }
                    ),
                },
            }
        ),
    ),
    (
        re.compile(r"^/assets/annotations/\{id\}/values$"),
        "DELETE",
        _array_of(
            {
                "type": "object",
                "required": ["objectType", "targets"],
                "properties": {
                    "objectType": {"type": "string"},
                    "targets": _TARGETS_SCHEMA,
                },
            }
        ),
    ),
)


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


class DIIWriteTokenMissingError(RuntimeError):
    """Raised when a DII write client is requested without a read-write API key."""


class DIIAPIClient(APIWrapper):
    """API client for Data Infrastructure Insights (formerly Cloud Insights).

    The default client carries only the read-only key. ``read_write=True``
    builds a client that carries only the read-write key, as required by
    :class:`~pynetappfoundry.query.mutation.Mutation` (ADR-0019 key isolation).
    The 36 annotation value operations declare a bare object request body in the
    spec but take a JSON array; :meth:`_get_request_schema` corrects them (#1185).
    """

    def __init__(
        self,
        config: Config,
        name: str | None = None,
        *,
        read_write: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize the DII API client.

        Args:
            config: Configuration object with DII API settings.
            name: Optional ``[cloudinsights.<name>]`` tenant. Its ``base_url`` and
                token override ``diiapi.toml [general]``; without it, ``[general]``
                alone is used.
            read_write: Build a write client that sends ``api_rw_token`` instead of
                ``api_ro_token``.
            **kwargs: Additional arguments passed to APIWrapper.
        """
        self.config = config

        dii_settings = (
            config.get_dii_api_settings() if name is None else config.get_dii_api_settings(name)
        )
        self.read_write = read_write
        if read_write:
            if dii_settings.api_rw_token is None:
                if name is None:
                    hint = (
                        "Add api_rw_token to diiapi.toml [general], for example with "
                        "`nf config set-credential --setting diiapi.api_rw_token`."
                    )
                else:
                    hint = (
                        f"Tenant {name!r} uses the diiapi.toml [general] api_rw_token only "
                        "when it has no key of its own; a separate read-write key per "
                        "tenant is not supported yet."
                    )
                raise DIIWriteTokenMissingError(
                    f"A DII write client needs api_rw_token, but none is configured. {hint}"
                )
            api_key = dii_settings.api_rw_token.get_secret_value()
            log_name = f"{name}:rw" if name else "rw"
        else:
            api_key = dii_settings.api_ro_token.get_secret_value()
            log_name = name or ""
        super().__init__(
            name=log_name,
            api_json_file=str(config.get_schema_location("dii") / "all.json"),
            base_url=dii_settings.base_url,
            auth_header={"X-CloudInsights-ApiKey": api_key},
            base_api_path=dii_settings.base_api_path,
            timeout=dii_settings.timeout,
            **kwargs,
        )

    def _get_request_schema(self, path_template: str, method: str) -> dict[str, Any] | None:
        """Return the request schema, correcting a bare-object annotation value schema.

        A fix applies only while the spec still declares exactly ``{"type": "object"}``,
        so a corrected upstream spec wins.
        """
        schema = super()._get_request_schema(path_template, method)
        if schema == {"type": "object"}:
            verb = method.upper()
            for pattern, fix_method, fix in _REQUEST_SCHEMA_FIXES:
                if fix_method == verb and pattern.match(path_template):
                    return copy.deepcopy(fix)
        return schema

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
