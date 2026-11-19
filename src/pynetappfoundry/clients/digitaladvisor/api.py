"""Active IQ Digital Advisor GraphQL client (read-only).

The client posts GraphQL documents to ``graphql_url`` with a bearer token. It
does not use :class:`~pynetappfoundry.clients.openapi.APIWrapper`: Digital Advisor
publishes no OpenAPI file, and the REST API it replaces is being phased out. The
token refresh is the only REST call.

Safety properties, each covered by tests:

* no mutation or subscription is ever sent (:func:`ensure_read_only`);
* tokens, headers and query variables never reach a log line or an exception
  message;
* requests are spread over a client-side sliding window and retried with
  backoff on 429, 502, 503, 504 and connection errors.
"""

from __future__ import annotations

import logging
import re
import threading
import time
import tomllib
from collections import deque
from collections.abc import Callable, Mapping, Sequence
from typing import TYPE_CHECKING, Any

import requests

from pynetappfoundry.clients.digitaladvisor.auth import (
    DigitalAdvisorAuthError,
    DigitalAdvisorError,
    DigitalAdvisorQueryError,
    FallbackTokenProvider,
    RefreshingTokenProvider,
    StaticTokenProvider,
    TokenPersistError,
    TokenProvider,
)
from pynetappfoundry.core.models import DigitalAdvisorAPISettings, RetryConfig
from pynetappfoundry.core.settings_files import find_setting_file, write_toml_values
from pynetappfoundry.utils.sops import (
    encrypt_value,
    get_age_key_path,
    get_public_key_from_file,
    is_encrypted,
)

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config

logger = logging.getLogger(__name__)

#: Upper bound on pages fetched for one call, a guard against a server that never ends.
DIGITAL_ADVISOR_MAX_PAGES = 1000

#: The service allows 300 requests per 5 minutes per IP (NetApp docs) and sends no
#: rate-limit headers, so the client keeps its own window.
RATE_LIMIT_REQUESTS = 300
RATE_LIMIT_WINDOW = 300.0

#: Retry defaults, sized for a 5-minute rate-limit window.
DEFAULT_RETRY = RetryConfig(
    max_attempts=5,
    initial_wait=5.0,
    max_wait=120.0,
    retryable_status_codes=[429, 502, 503, 504],
)

_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

INTROSPECTION_QUERY = """
query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types {
      ...FullType
    }
    directives {
      name
      description
      locations
      args {
        ...InputValue
      }
    }
  }
}

fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}

fragment InputValue on __InputValue {
  name
  description
  type { ...TypeRef }
  defaultValue
}

fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
  }
}
"""

# Scalar fields of System and Volume that the probe confirmed (the nested object
# shapes were not measured).
SYSTEM_FIELDS: tuple[str, ...] = (
    "systemId",
    "serialNumber",
    "systemState",
    "model",
    "productType",
    "platformType",
    "systemShipmentDate",
    "serviceTier",
    "hasPvr",
    "supportAddOns",
    "hostName",
    "osVersion",
    "osType",
    "ageInYears",
)
VOLUME_FIELDS: tuple[str, ...] = (
    "id",
    "name",
    "instanceUUID",
    "state",
    "tieringPolicy",
    "autoSizeMode",
    "snapLockMode",
    "snapshotCount",
    "usedCapacityPercentage",
    "isRoot",
    "isEncrypted",
    "isAutoSizeEnabled",
    "isARPEnabled",
    "protocols",
    "enabledEfficiencyFeatures",
)

# Filter argument names the probe listed. The types of ``platformType`` and
# ``operatingMode`` come from the downloaded schema (#1124); the others are inferred
# from the names, and a wrong one surfaces as the server's GRAPHQL_VALIDATION_FAILED.
SYSTEM_FILTER_TYPES: dict[str, str] = {
    "customerId": "String",
    "siteId": "String",
    "clusterId": "String",
    "clusterIds": "[String!]",
    "clusterName": "String",
    "hostName": "String",
    "uuids": "[String!]",
    "watchlistId": "String",
    "platformType": "[SystemPlatformType!]",
    "operatingMode": "[SystemOperatingMode!]",
}
VOLUME_FILTER_TYPES: dict[str, str] = {
    "clusterId": "String",
    "vserverId": "String",
    "aggregateId": "String",
    "name": "String",
    "isRoot": "Boolean",
    "isEncrypted": "Boolean",
}


def ensure_read_only(document: str) -> None:
    """Reject a GraphQL document that holds anything but queries and fragments.

    A brace-depth scan over the document, skipping comments and strings: every
    top-level definition must start with ``query``, ``fragment`` or ``{``. A
    ``mutation`` or ``subscription`` keyword, or an unknown one, is rejected. Names
    inside a selection set (a field called ``mutationType``) are never looked at.

    Raises:
        DigitalAdvisorQueryError: If the document has a non-query operation or
            no definition at all.
    """
    depth = 0
    parens = 0
    expect_definition = True
    seen_definition = False
    i = 0
    n = len(document)
    while i < n:
        ch = document[i]
        if ch == "#":
            while i < n and document[i] not in "\r\n":
                i += 1
            continue
        if ch == '"':
            if document.startswith('"""', i):
                end = document.find('"""', i + 3)
                while end != -1 and document[end - 1] == "\\":
                    end = document.find('"""', end + 1)
                i = n if end == -1 else end + 3
            else:
                i += 1
                while i < n and document[i] != '"':
                    i += 2 if document[i] == "\\" else 1
                i += 1
            continue
        if ch == "(":
            parens += 1
        elif ch == ")":
            parens = max(0, parens - 1)
        elif ch == "{":
            if depth == 0:
                expect_definition = False
                seen_definition = True
            depth += 1
        elif ch == "}":
            depth = max(0, depth - 1)
            if depth == 0:
                expect_definition = True
        elif (ch.isalpha() or ch == "_") and depth == 0 and parens == 0:
            j = i
            while j < n and (document[j].isalnum() or document[j] == "_"):
                j += 1
            word = document[i:j]
            if expect_definition:
                if word not in ("query", "fragment"):
                    raise DigitalAdvisorQueryError(
                        f"Only read-only queries are allowed; found a top-level {word!r}"
                    )
                expect_definition = False
                seen_definition = True
            i = j
            continue
        i += 1
    if not seen_definition:
        raise DigitalAdvisorQueryError("The GraphQL document has no query")


class RateLimiter:
    """Sliding-window limiter: at most ``max_requests`` per ``window`` seconds."""

    def __init__(
        self,
        max_requests: int = RATE_LIMIT_REQUESTS,
        window: float = RATE_LIMIT_WINDOW,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        """Initialize the limiter.

        Args:
            max_requests: Requests allowed inside one window.
            window: Window length in seconds.
            clock: Monotonic clock (tests inject a fake one).
            sleep: Sleep function (tests inject a fake one).
        """
        self._max = max_requests
        self._window = window
        self._clock = clock
        self._sleep = sleep
        self._stamps: deque[float] = deque()
        self._lock = threading.Lock()

    def acquire(self) -> None:
        """Block until a request fits in the window, then count it."""
        while True:
            with self._lock:
                now = self._clock()
                while self._stamps and self._stamps[0] <= now - self._window:
                    self._stamps.popleft()
                if len(self._stamps) < self._max:
                    self._stamps.append(now)
                    return
                wait = self._stamps[0] + self._window - now
            logger.debug("Digital Advisor rate limit window full; waiting %.1fs", wait)
            self._sleep(max(wait, 0.0))


def make_token_persister(config: Config) -> Callable[[str, str], None]:
    """Build the callback that writes rotated tokens back to ``digitaladvisorapi.toml``.

    Both tokens are written in one atomic write that keeps comments. They are
    SOPS-encrypted when the file's current ``refresh_token`` is a ``SOPS[...]``
    value, and plain text otherwise, matching the stored form.

    Raises (from the returned callback):
        TokenPersistError: If the write fails. The message names the file and the
            exception type, never a value.
    """

    def persist(access_token: str, refresh_token: str) -> None:
        path_text = "digitaladvisorapi.toml"
        try:
            path = find_setting_file(config.config_dir, "digitaladvisorapi", None)
            path_text = str(path)
            current: Any = None
            if path.exists():
                with open(path, "rb") as f:
                    current = tomllib.load(f).get("general", {}).get("refresh_token")
            values = {"access_token": access_token, "refresh_token": refresh_token}
            if isinstance(current, str) and is_encrypted(current):
                public_key = get_public_key_from_file(get_age_key_path())
                values = {k: encrypt_value(v, public_key) for k, v in values.items()}
            write_toml_values(path, ["general"], values)
        except Exception as e:
            raise TokenPersistError(
                f"could not write the rotated Digital Advisor tokens to {path_text} "
                f"({type(e).__name__})"
            ) from e

    return persist


def _validated_names(names: Sequence[str], what: str) -> list[str]:
    """Return ``names`` as a list, raising ``ValueError`` for any invalid GraphQL name."""
    result = list(names)
    if not result:
        raise ValueError(f"{what} must not be empty")
    for name in result:
        if not isinstance(name, str) or not _NAME_RE.match(name):
            raise ValueError(f"invalid GraphQL field name in {what}: {name!r}")
    return result


def _checked_filters(
    filters: Mapping[str, Any] | None, allowed: Mapping[str, str]
) -> dict[str, Any]:
    """Return ``filters`` as a dict, raising ``ValueError`` for a name not in ``allowed``."""
    result = dict(filters or {})
    unknown = sorted(set(result) - set(allowed))
    if unknown:
        raise ValueError(
            f"unknown filter(s): {', '.join(unknown)}; allowed: {', '.join(sorted(allowed))}"
        )
    return result


def build_token_provider(
    settings: DigitalAdvisorAPISettings,
    *,
    persist: Callable[[str, str], None] | None,
    session: requests.Session | None,
) -> TokenProvider:
    """Build the token provider for the configured credential mode.

    A PAT alone is static, a refresh token alone refreshes, and both give a
    :class:`FallbackTokenProvider` (PAT first, refresh pair once the PAT is
    rejected). Building makes no request and no write.
    """
    static = (
        StaticTokenProvider(settings.personal_access_token.get_secret_value())
        if settings.personal_access_token is not None
        else None
    )
    if settings.refresh_token is None:
        assert static is not None  # the model requires one credential
        return static
    refreshing = RefreshingTokenProvider(
        refresh_token=settings.refresh_token.get_secret_value(),
        access_token=(
            settings.access_token.get_secret_value() if settings.access_token is not None else None
        ),
        token_url=settings.token_url,
        timeout=settings.timeout,
        persist=persist,
        session=session,
    )
    if static is None:
        return refreshing
    return FallbackTokenProvider(static, refreshing)


class DigitalAdvisorAPIClient:
    """Read-only client for the Active IQ Digital Advisor GraphQL API."""

    def __init__(
        self,
        config: Config | None = None,
        *,
        settings: DigitalAdvisorAPISettings | None = None,
        token_provider: TokenProvider | None = None,
        session: requests.Session | None = None,
        retry_config: RetryConfig | None = None,
        rate_limiter: RateLimiter | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        """Initialize the client.

        Args:
            config: Loaded configuration. Supplies the settings, and the file the
                rotated tokens are written back to.
            settings: Explicit settings (tests, or callers that built their own).
            token_provider: Explicit token provider; built from the settings by default.
            session: Optional ``requests.Session``.
            retry_config: Retry policy; ``DEFAULT_RETRY`` by default.
            rate_limiter: Client-side limiter; 300 requests per 300 s by default.
            sleep: Sleep function used for retry backoff.

        Raises:
            ValueError: If neither ``config`` nor ``settings`` is given.
            ConfigurationError: If the settings are missing or invalid.
        """
        if settings is None:
            if config is None:
                raise ValueError("DigitalAdvisorAPIClient needs a config or settings")
            settings = config.get_digital_advisor_api_settings()
        self.settings = settings
        self._session = session if session is not None else requests.Session()
        self._retry = retry_config if retry_config is not None else DEFAULT_RETRY
        self._sleep = sleep
        self._limiter = rate_limiter if rate_limiter is not None else RateLimiter(sleep=sleep)
        if token_provider is None:
            token_provider = self._build_provider(settings, config)
        self._tokens = token_provider

    def _build_provider(
        self, settings: DigitalAdvisorAPISettings, config: Config | None
    ) -> TokenProvider:
        """Build the token provider for the configured credential mode."""
        return build_token_provider(
            settings,
            persist=make_token_persister(config) if config is not None else None,
            session=self._session,
        )

    def __repr__(self) -> str:
        return f"DigitalAdvisorAPIClient(graphql_url={self.settings.graphql_url!r})"

    # -- transport ---------------------------------------------------------

    def _backoff(self, attempt: int, response: requests.Response | None) -> float:
        """Seconds to wait before retry number ``attempt`` (1-based)."""
        if response is not None:
            header = response.headers.get("Retry-After")
            if header is not None:
                try:
                    return min(max(float(header), 0.0), self._retry.max_wait)
                except ValueError:
                    pass
        wait = float(self._retry.initial_wait * self._retry.exponential_base ** (attempt - 1))
        return min(wait, self._retry.max_wait)

    def _post(self, document: str, variables: Mapping[str, Any], token: str) -> requests.Response:
        """POST one GraphQL request through the limiter, retrying transient failures.

        Returns:
            The last response, also when a retryable status survives every attempt.

        Raises:
            DigitalAdvisorError: If a connection error survives every attempt.
        """
        retry = self._retry
        attempt = 0
        while True:
            attempt += 1
            self._limiter.acquire()
            try:
                response = self._session.post(
                    self.settings.graphql_url,
                    json={"query": document, "variables": dict(variables)},
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=self.settings.timeout,
                    verify=True,
                )
            except (requests.ConnectionError, requests.Timeout) as e:
                if not (retry.enabled and retry.retry_on_connection_error) or (
                    attempt >= retry.max_attempts
                ):
                    raise DigitalAdvisorError(
                        f"Digital Advisor request failed: {type(e).__name__}"
                    ) from e
                wait = self._backoff(attempt, None)
                logger.warning(
                    "Digital Advisor request failed (%s); retry %d in %.1fs",
                    type(e).__name__,
                    attempt,
                    wait,
                )
                self._sleep(wait)
                continue
            logger.debug("Digital Advisor POST -> HTTP %d", response.status_code)
            if (
                retry.enabled
                and response.status_code in retry.retryable_status_codes
                and attempt < retry.max_attempts
            ):
                wait = self._backoff(attempt, response)
                logger.warning(
                    "Digital Advisor answered HTTP %d; retry %d in %.1fs",
                    response.status_code,
                    attempt,
                    wait,
                )
                self._sleep(wait)
                continue
            return response

    @staticmethod
    def _body(response: requests.Response) -> Any:
        """Return the JSON body, or ``None`` if it is not JSON."""
        try:
            return response.json()
        except ValueError:
            return None

    @staticmethod
    def _errors(body: Any) -> tuple[tuple[str, ...], tuple[str, ...]]:
        """Return the ``(codes, messages)`` of a response's ``errors`` list."""
        codes: list[str] = []
        messages: list[str] = []
        errors = body.get("errors") if isinstance(body, dict) else None
        for err in errors if isinstance(errors, list) else []:
            if not isinstance(err, dict):
                continue
            ext = err.get("extensions")
            code = ext.get("code") if isinstance(ext, dict) else None
            if isinstance(code, str):
                codes.append(code)
            message = err.get("message")
            if isinstance(message, str):
                messages.append(message)
        return tuple(codes), tuple(messages)

    # -- public API --------------------------------------------------------

    def query(self, document: str, variables: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """Run a read-only GraphQL document and return its ``data``.

        An unknown id comes back as ``data.<field> = None``; that is returned, not
        raised. On ``UNAUTHENTICATED`` a refresh-token client refreshes once and
        retries once; with both credentials a rejected PAT switches to the
        refresh pair first (retry once per credential, at most three POSTs).

        Raises:
            DigitalAdvisorQueryError: For a mutation, an HTTP 400 or ``errors[]``.
            DigitalAdvisorAuthError: If authentication fails.
            DigitalAdvisorError: For any other failure, such as a 429 that
                survives every retry.
        """
        ensure_read_only(document)
        sent_variables = variables or {}
        refreshed = False
        while True:
            token = self._tokens.get_token()
            response = self._post(document, sent_variables, token)
            body = self._body(response)
            codes, messages = self._errors(body)
            if "UNAUTHENTICATED" in codes or response.status_code == 401:
                if not self._tokens.refreshable:
                    raise DigitalAdvisorAuthError(
                        "Digital Advisor rejected the personal access token. It is probably "
                        "expired (a PAT is valid for 1-90 days): create a new one and store it "
                        "with 'nf config set-credential --setting "
                        "digitaladvisorapi.personal_access_token'."
                    )
                if refreshed:
                    message = "Digital Advisor rejected the access token again after a refresh"
                    if getattr(self._tokens, "fell_back", False):
                        message += (
                            ", and the personal access token was rejected too. Log in to the "
                            "Digital Advisor portal and store a new refresh token with "
                            "'nf config set-credential --setting digitaladvisorapi.refresh_token'; "
                            "also create a new personal access token and store it with "
                            "'nf config set-credential --setting "
                            "digitaladvisorapi.personal_access_token'"
                        )
                    raise DigitalAdvisorAuthError(message)
                before = getattr(self._tokens, "credential", None)
                self._tokens.invalidate(token)
                if getattr(self._tokens, "credential", None) == before:
                    refreshed = True  # a switch to the fallback credential is not the retry
                continue
            if response.status_code == 429 or response.status_code >= 500:
                raise DigitalAdvisorError(
                    f"Digital Advisor request failed (HTTP {response.status_code}"
                    f"{': ' + ', '.join(codes) if codes else ''})"
                )
            if response.status_code == 400 or codes or messages:
                detail = f": {', '.join(codes)}" if codes else ""
                raise DigitalAdvisorQueryError(
                    f"Digital Advisor query failed (HTTP {response.status_code}{detail})"
                    + "".join(f"\n  {m}" for m in messages),
                    codes=codes,
                    messages=messages,
                )
            if not 200 <= response.status_code < 300:
                raise DigitalAdvisorError(
                    f"Digital Advisor request failed (HTTP {response.status_code})"
                )
            data = body.get("data") if isinstance(body, dict) else None
            if not isinstance(data, dict):
                raise DigitalAdvisorError(
                    f"Digital Advisor response (HTTP {response.status_code}) has no data object"
                )
            return data

    def paginate(
        self,
        document: str,
        variables: Mapping[str, Any] | None,
        connection: str,
        records_key: str,
        page_size: int | None = None,
    ) -> list[Any]:
        """Collect the records of a cursor-paged connection.

        The document must declare ``$pageSize`` and ``$after`` variables and pass
        them to the connection. The loop sends ``pageSize`` and, from the second
        page on, ``after=<cursor>``. It stops on an empty page, when the record
        count reaches ``totalCount`` (``clusters`` has none), on an empty or
        repeated cursor, or after ``DIGITAL_ADVISOR_MAX_PAGES`` pages.

        Args:
            document: The query document.
            variables: Variables other than ``pageSize`` and ``after``.
            connection: Name of the connection field in ``data``.
            records_key: Name of the record list inside the connection.
            page_size: Overrides ``settings.page_size``.

        Returns:
            All records, as plain dicts.
        """
        sent: dict[str, Any] = dict(variables or {})
        sent["pageSize"] = page_size if page_size is not None else self.settings.page_size
        records: list[Any] = []
        seen: set[str] = set()
        for _ in range(DIGITAL_ADVISOR_MAX_PAGES):
            data = self.query(document, sent)
            conn = data.get(connection)
            if not isinstance(conn, dict):
                return records
            page = conn.get(records_key)
            if not isinstance(page, list) or not page:
                return records
            records.extend(page)
            total = conn.get("totalCount")
            if isinstance(total, int) and not isinstance(total, bool) and len(records) >= total:
                return records
            cursor = conn.get("cursor")
            if not isinstance(cursor, str) or not cursor or cursor in seen:
                return records
            seen.add(cursor)
            sent["after"] = cursor
        logger.error(
            "Digital Advisor %s: stopped after %d pages (%d records); results may be incomplete",
            connection,
            DIGITAL_ADVISOR_MAX_PAGES,
            len(records),
        )
        return records

    def list_systems(
        self,
        *,
        product_types: Sequence[str],
        system_states: Sequence[str],
        include_all_states: bool,
        include_storage_grid_nodes: bool,
        filters: Mapping[str, Any] | None = None,
        fields: Sequence[str] | None = None,
    ) -> list[dict[str, Any]]:
        """List systems.

        The four required arguments are the ones the service requires. The enum
        *values* for ``product_types`` and ``system_states`` are not known to the
        client; look them up in the downloaded schema (``nf config download-schema``).

        Args:
            product_types: ``ProductType`` values.
            system_states: ``SystemState`` values.
            include_all_states: The ``includeAllStates`` argument.
            include_storage_grid_nodes: The ``includeStorageGridNodes`` argument.
            filters: Extra filter arguments; names in ``SYSTEM_FILTER_TYPES`` only.
            fields: Replaces the default selection ``SYSTEM_FIELDS``. Each must be
                a plain GraphQL name.

        Raises:
            ValueError: For an invalid field name or an unknown filter.
        """
        selection = _validated_names(fields if fields is not None else SYSTEM_FIELDS, "fields")
        extra = _checked_filters(filters, SYSTEM_FILTER_TYPES)
        declared = [
            "$productTypes: [ProductType!]!",
            "$systemStates: [SystemState!]!",
            "$includeAllStates: Boolean!",
            "$includeStorageGridNodes: Boolean!",
            "$pageSize: Int",
            "$after: String",
            *(f"${name}: {SYSTEM_FILTER_TYPES[name]}" for name in extra),
        ]
        passed = [
            "productTypes: $productTypes",
            "systemStates: $systemStates",
            "includeAllStates: $includeAllStates",
            "includeStorageGridNodes: $includeStorageGridNodes",
            "pageSize: $pageSize",
            "after: $after",
            *(f"{name}: ${name}" for name in extra),
        ]
        document = (
            f"query ListSystems({', '.join(declared)}) {{\n"
            f"  systems({', '.join(passed)}) {{\n"
            f"    totalCount\n    cursor\n    systems {{ {' '.join(selection)} }}\n"
            "  }\n}\n"
        )
        variables: dict[str, Any] = {
            "productTypes": list(product_types),
            "systemStates": list(system_states),
            "includeAllStates": include_all_states,
            "includeStorageGridNodes": include_storage_grid_nodes,
            **extra,
        }
        return self.paginate(document, variables, "systems", "systems")

    def list_volumes(
        self,
        *,
        filters: Mapping[str, Any] | None = None,
        fields: Sequence[str] | None = None,
    ) -> list[dict[str, Any]]:
        """List volumes.

        Args:
            filters: Filter arguments; names in ``VOLUME_FILTER_TYPES`` only. The
                GraphQL types of these filters are inferred from their names.
            fields: Replaces the default selection ``VOLUME_FIELDS``. Each must be
                a plain GraphQL name.

        Raises:
            ValueError: For an invalid field name or an unknown filter.
        """
        selection = _validated_names(fields if fields is not None else VOLUME_FIELDS, "fields")
        extra = _checked_filters(filters, VOLUME_FILTER_TYPES)
        declared = [
            "$pageSize: Int",
            "$after: String",
            *(f"${name}: {VOLUME_FILTER_TYPES[name]}" for name in extra),
        ]
        passed = ["pageSize: $pageSize", "after: $after", *(f"{name}: ${name}" for name in extra)]
        document = (
            f"query ListVolumes({', '.join(declared)}) {{\n"
            f"  volumes({', '.join(passed)}) {{\n"
            f"    totalCount\n    cursor\n    volumes {{ {' '.join(selection)} }}\n"
            "  }\n}\n"
        )
        return self.paginate(document, dict(extra), "volumes", "volumes")


def fetch_schema(
    url: str, timeout: float, session: requests.Session | None = None
) -> dict[str, Any]:
    """Download the GraphQL schema by introspection, without credentials.

    Returns:
        The response's ``data`` object (it holds ``__schema``).

    Raises:
        DigitalAdvisorError: If the response is not HTTP 2xx JSON with ``data.__schema``.
        requests.RequestException: If the request itself fails.
    """
    http = session if session is not None else requests.Session()
    response = http.post(
        url,
        json={"query": INTROSPECTION_QUERY, "variables": {}},
        timeout=timeout,
        verify=True,
    )
    if not 200 <= response.status_code < 300:
        raise DigitalAdvisorError(f"Schema download failed (HTTP {response.status_code})")
    try:
        body: Any = response.json()
    except ValueError:
        body = None
    data = body.get("data") if isinstance(body, dict) else None
    if not isinstance(data, dict) or not isinstance(data.get("__schema"), dict):
        raise DigitalAdvisorError(
            f"Schema download response (HTTP {response.status_code}) has no data.__schema"
        )
    return data
