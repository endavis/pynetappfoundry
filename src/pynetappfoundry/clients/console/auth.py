"""OAuth token providers for the Console API client (ADR-0019).

``TokenProvider`` is the small seam the Console client uses for tokens that are
fetched and renewed at runtime, as opposed to static tokens pasted into
``consoleapi.toml``.  ``ClientCredentialsTokenProvider`` implements the OAuth
client-credentials grant, which yields a Console *service* token.
``RefreshTokenProvider`` implements the OAuth refresh-token grant, which yields
a Console *user* token from a long-lived NetApp refresh token.

Secrets and tokens are never logged and never appear in error messages.
"""

from __future__ import annotations

import logging
import threading
import time
from collections.abc import Callable
from typing import Any, Protocol

import requests
from pydantic import SecretStr


class ConsoleAuthError(RuntimeError):
    """Raised when a Console access token cannot be obtained.

    The message carries the HTTP status and the OAuth ``error`` /
    ``error_description`` when present.  It never includes the request body,
    the client secret, a refresh token or an access token.
    """


class TokenProvider(Protocol):
    """A source of bearer tokens that can be told a token was rejected."""

    def get_token(self) -> str:
        """Return a currently valid access token."""
        ...

    def invalidate(self, token: str) -> None:
        """Drop the cached token if it equals ``token``.

        Comparing against the rejected token keeps concurrent 401s from each
        triggering a refresh: only the first drops the stale token.
        """
        ...


class _OAuthTokenProvider:
    """Shared cache, expiry, locking and token-endpoint exchange for OAuth grants.

    Subclasses supply the request body through ``_payload`` and a ``_kind``
    label (``"service"`` or ``"user"``) used in the log line.
    """

    _kind: str = "service"

    def __init__(
        self,
        *,
        token_endpoint: str,
        timeout: float,
        session: requests.Session | None = None,
        clock: Callable[[], float] = time.monotonic,
        expiry_skew: float = 60.0,
    ) -> None:
        """Initialize the shared state.

        Args:
            token_endpoint: URL of the token endpoint.
            timeout: Request timeout in seconds.
            session: Optional ``requests.Session`` (tests inject one).
            clock: Monotonic clock returning seconds.
            expiry_skew: Seconds before expiry at which the token is renewed.
        """
        self._token_endpoint = token_endpoint
        self._timeout = timeout
        self._session = session if session is not None else requests.Session()
        self._clock = clock
        self._expiry_skew = expiry_skew
        self._lock = threading.Lock()
        self._token: str | None = None
        self._expires_at: float | None = None

    def _payload(self) -> dict[str, str]:
        """Return the token request body (subclasses implement)."""
        raise NotImplementedError

    def _is_valid(self) -> bool:
        """Whether a cached token exists and has not reached its renewal time."""
        if self._token is None:
            return False
        return self._expires_at is None or self._clock() < self._expires_at

    def get_token(self) -> str:
        """Return a valid access token, fetching a new one if needed.

        Raises:
            ConsoleAuthError: If the token exchange fails.
        """
        if self._is_valid() and self._token is not None:
            return self._token
        with self._lock:
            if self._is_valid() and self._token is not None:
                return self._token
            return self._fetch()

    def invalidate(self, token: str) -> None:
        """Drop the cached token if it equals ``token``."""
        with self._lock:
            if self._token == token:
                self._token = None
                self._expires_at = None

    def _fetch(self) -> str:
        """Exchange the credentials for a token (caller holds the lock)."""
        try:
            resp = self._session.post(
                self._token_endpoint, json=self._payload(), timeout=self._timeout
            )
        except requests.RequestException as e:
            raise ConsoleAuthError(
                f"Console token request failed: {type(e).__name__} contacting the token endpoint"
            ) from e

        body = self._parse_body(resp)
        if not 200 <= resp.status_code < 300:
            raise ConsoleAuthError(self._describe_failure(resp.status_code, body))

        token = body.get("access_token") if isinstance(body, dict) else None
        if not isinstance(token, str) or not token:
            raise ConsoleAuthError(
                f"Console token response (HTTP {resp.status_code}) has no access_token"
            )

        expires_in = body.get("expires_in")
        if isinstance(expires_in, (int, float)) and not isinstance(expires_in, bool):
            now = self._clock()
            expires_at = now + expires_in - self._expiry_skew
            if expires_at <= now:
                expires_at = now + expires_in / 2
            self._expires_at = expires_at
            logging.info(f"fetched Console {self._kind} token (expires in {int(expires_in)}s)")
        else:
            self._expires_at = None
            logging.info(f"fetched Console {self._kind} token (no expiry reported)")
        self._token = token
        return token

    @staticmethod
    def _parse_body(resp: requests.Response) -> Any:
        """Return the JSON body, or None if it is not JSON."""
        try:
            return resp.json()
        except ValueError:
            return None

    @staticmethod
    def _describe_failure(status: int, body: Any) -> str:
        """Build an error message from the status and OAuth error fields only."""
        message = f"Console token request failed (HTTP {status})"
        if isinstance(body, dict):
            error = body.get("error")
            description = body.get("error_description")
            if isinstance(error, str) and error:
                message += f": {error}"
            if isinstance(description, str) and description:
                message += f" - {description}"
        return message


class ClientCredentialsTokenProvider(_OAuthTokenProvider):
    """Fetch and cache an access token via the OAuth client-credentials grant."""

    _kind = "service"

    def __init__(
        self,
        *,
        client_id: str,
        client_secret: SecretStr,
        token_endpoint: str,
        audience: str,
        timeout: float,
        session: requests.Session | None = None,
        clock: Callable[[], float] = time.monotonic,
        expiry_skew: float = 60.0,
    ) -> None:
        """Initialize the provider.

        Args:
            client_id: OAuth client ID of the service account.
            client_secret: OAuth client secret of the service account.
            token_endpoint: URL of the token endpoint.
            audience: Audience requested for the token.
            timeout: Request timeout in seconds.
            session: Optional ``requests.Session`` (tests inject one).
            clock: Monotonic clock returning seconds.
            expiry_skew: Seconds before expiry at which the token is renewed.
        """
        super().__init__(
            token_endpoint=token_endpoint,
            timeout=timeout,
            session=session,
            clock=clock,
            expiry_skew=expiry_skew,
        )
        self._client_id = client_id
        self._client_secret = client_secret
        self._audience = audience

    def __repr__(self) -> str:
        """Show the client ID and endpoint only."""
        return (
            f"ClientCredentialsTokenProvider(client_id={self._client_id!r}, "
            f"token_endpoint={self._token_endpoint!r})"
        )

    def _payload(self) -> dict[str, str]:
        """Return the client-credentials request body."""
        return {
            "audience": self._audience,
            "client_id": self._client_id,
            "client_secret": self._client_secret.get_secret_value(),
            "grant_type": "client_credentials",
        }


class RefreshTokenProvider(_OAuthTokenProvider):
    """Fetch and cache a user access token via the OAuth refresh-token grant.

    The refresh token is long-lived and is never rotated by the endpoint: any
    ``refresh_token`` in the response is ignored.
    """

    _kind = "user"

    def __init__(
        self,
        *,
        refresh_token: SecretStr,
        client_id: str,
        token_endpoint: str,
        timeout: float,
        session: requests.Session | None = None,
        clock: Callable[[], float] = time.monotonic,
        expiry_skew: float = 60.0,
    ) -> None:
        """Initialize the provider.

        Args:
            refresh_token: NetApp refresh token.
            client_id: OAuth client ID the refresh token was issued to.
            token_endpoint: URL of the token endpoint.
            timeout: Request timeout in seconds.
            session: Optional ``requests.Session`` (tests inject one).
            clock: Monotonic clock returning seconds.
            expiry_skew: Seconds before expiry at which the token is renewed.
        """
        super().__init__(
            token_endpoint=token_endpoint,
            timeout=timeout,
            session=session,
            clock=clock,
            expiry_skew=expiry_skew,
        )
        self._refresh_token = refresh_token
        self._client_id = client_id

    def __repr__(self) -> str:
        """Show the client ID and endpoint only."""
        return (
            f"RefreshTokenProvider(client_id={self._client_id!r}, "
            f"token_endpoint={self._token_endpoint!r})"
        )

    def _payload(self) -> dict[str, str]:
        """Return the refresh-token request body (no audience)."""
        return {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token.get_secret_value(),
            "client_id": self._client_id,
        }


__all__ = [
    "ClientCredentialsTokenProvider",
    "ConsoleAuthError",
    "RefreshTokenProvider",
    "TokenProvider",
]
