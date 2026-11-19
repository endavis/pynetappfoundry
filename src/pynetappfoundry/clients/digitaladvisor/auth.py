"""Token handling for the Active IQ Digital Advisor client.

Three credential modes:

* a personal access token (PAT), used as is (:class:`StaticTokenProvider`);
* an access/refresh pair, where the access token is a JWT valid for one hour and
  every refresh returns a new refresh token (:class:`RefreshingTokenProvider`);
* both, the PAT first and the refresh pair as the fallback once the PAT is
  rejected (:class:`FallbackTokenProvider`).

Neither the tokens nor the decoded JWT claims are ever logged or put in an
exception message. Only the ``exp`` claim is read.
"""

from __future__ import annotations

import base64
import binascii
import json
import logging
import threading
import time
from collections.abc import Callable
from typing import Any, Protocol

import requests

logger = logging.getLogger(__name__)

#: Statuses of a failed refresh that mean the refresh token is no longer accepted.
#: The service's failure statuses were not measured; this is an inference.
_REFRESH_REJECTED_STATUSES = frozenset({400, 401, 403})


class DigitalAdvisorError(Exception):
    """Base class for Digital Advisor client errors."""


class DigitalAdvisorAuthError(DigitalAdvisorError):
    """A token could not be obtained or was rejected."""


class DigitalAdvisorQueryError(DigitalAdvisorError):
    """The GraphQL server rejected a query or returned errors.

    Attributes:
        codes: The ``extensions.code`` values of the returned errors.
        messages: The error ``message`` texts (never variables, headers or tokens).
    """

    def __init__(
        self, message: str, *, codes: tuple[str, ...] = (), messages: tuple[str, ...] = ()
    ) -> None:
        super().__init__(message)
        self.codes = codes
        self.messages = messages


class TokenPersistError(DigitalAdvisorError):
    """The rotated tokens could not be written back; the message names the file and error type."""


def jwt_expiry(token: str) -> float | None:
    """Return the ``exp`` claim (epoch seconds) of a JWT, or ``None``.

    The signature is not verified and no other claim is read, returned or
    logged. Any decode problem gives ``None``.
    """
    parts = token.split(".")
    if len(parts) != 3:
        return None
    payload = parts[1]
    try:
        raw = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
        claims = json.loads(raw)
    except (binascii.Error, ValueError):
        return None
    if not isinstance(claims, dict):
        return None
    exp = claims.get("exp")
    if isinstance(exp, bool) or not isinstance(exp, (int, float)):
        return None
    return float(exp)


class TokenProvider(Protocol):
    """Supplies the bearer token for GraphQL requests."""

    #: Whether a rejected token can be replaced by refreshing.
    refreshable: bool

    def get_token(self) -> str:
        """Return a token to send."""
        ...

    def invalidate(self, token: str) -> None:
        """Drop ``token`` if it is the current one, so the next call refreshes."""
        ...


class StaticTokenProvider:
    """A personal access token: used as is, never refreshed."""

    refreshable = False
    credential = "personal_access_token"

    def __init__(self, token: str) -> None:
        self._token = token

    def get_token(self) -> str:
        """Return the PAT."""
        return self._token

    def invalidate(self, token: str) -> None:
        """Do nothing: a PAT cannot be refreshed."""

    def __repr__(self) -> str:
        return "StaticTokenProvider()"


class RefreshingTokenProvider:
    """Keeps an access token fresh with a rotating refresh token.

    The access token is renewed ``expiry_skew`` seconds before its JWT ``exp``,
    or when there is none. If ``exp`` cannot be decoded the token is used until
    the server rejects it. After every refresh both new tokens are handed to
    ``persist``; a failure there is logged (without values) and does not stop the
    call.
    """

    refreshable = True
    credential = "refresh_token"

    def __init__(
        self,
        *,
        refresh_token: str,
        access_token: str | None = None,
        token_url: str,
        timeout: float,
        persist: Callable[[str, str], None] | None = None,
        session: requests.Session | None = None,
        clock: Callable[[], float] = time.time,
        expiry_skew: float = 60.0,
    ) -> None:
        """Initialize the provider.

        Args:
            refresh_token: The current refresh token.
            access_token: The stored access token, if any.
            token_url: URL of the token refresh endpoint.
            timeout: Request timeout in seconds.
            persist: Called with ``(access_token, refresh_token)`` after a refresh.
            session: Optional ``requests.Session`` (tests inject one).
            clock: Wall clock in epoch seconds (``exp`` is epoch seconds).
            expiry_skew: Seconds before ``exp`` at which the token is renewed.
        """
        self._refresh_token = refresh_token
        self._access_token = access_token or None
        self._token_url = token_url
        self._timeout = timeout
        self._persist = persist
        self._session = session if session is not None else requests.Session()
        self._clock = clock
        self._expiry_skew = expiry_skew
        self._lock = threading.Lock()
        self._expires_at: float | None = (
            jwt_expiry(self._access_token) if self._access_token else None
        )

    def __repr__(self) -> str:
        return f"RefreshingTokenProvider(token_url={self._token_url!r})"

    def _is_valid(self) -> bool:
        """Whether the cached access token exists and is not due for renewal."""
        if self._access_token is None:
            return False
        return self._expires_at is None or self._clock() < self._expires_at - self._expiry_skew

    def get_token(self) -> str:
        """Return a valid access token, refreshing if needed.

        Raises:
            DigitalAdvisorAuthError: If the refresh fails.
        """
        if self._is_valid() and self._access_token is not None:
            return self._access_token
        with self._lock:
            if self._is_valid() and self._access_token is not None:
                return self._access_token
            return self._refresh()

    def invalidate(self, token: str) -> None:
        """Drop the cached access token if it equals ``token``."""
        with self._lock:
            if self._access_token == token:
                self._access_token = None
                self._expires_at = None

    def _refresh(self) -> str:
        """Exchange the refresh token for a new pair (caller holds the lock)."""
        try:
            resp = self._session.post(
                self._token_url,
                json={"refresh_token": self._refresh_token},
                timeout=self._timeout,
            )
        except requests.RequestException as e:
            raise DigitalAdvisorAuthError(
                f"Digital Advisor token refresh failed: {type(e).__name__} contacting the token URL"
            ) from e

        if resp.status_code in _REFRESH_REJECTED_STATUSES:
            raise DigitalAdvisorAuthError(
                f"Digital Advisor token refresh was rejected (HTTP {resp.status_code}). "
                "The refresh token is probably no longer valid: refreshing works for 90 days "
                "from the portal login. Log in to the Digital Advisor portal again, then store "
                "the new refresh token with "
                "'nf config set-credential --setting digitaladvisorapi.refresh_token'."
            )
        if not 200 <= resp.status_code < 300:
            raise DigitalAdvisorAuthError(
                f"Digital Advisor token refresh failed (HTTP {resp.status_code})"
            )
        try:
            body: Any = resp.json()
        except ValueError:
            body = None
        access = body.get("access_token") if isinstance(body, dict) else None
        refresh = body.get("refresh_token") if isinstance(body, dict) else None
        if not isinstance(access, str) or not access or not isinstance(refresh, str) or not refresh:
            raise DigitalAdvisorAuthError(
                f"Digital Advisor token refresh response (HTTP {resp.status_code}) "
                "has no access_token and refresh_token"
            )

        self._access_token = access
        self._refresh_token = refresh
        self._expires_at = jwt_expiry(access)
        logger.info("refreshed the Digital Advisor access token")
        if self._persist is not None:
            try:
                self._persist(access, refresh)
            except TokenPersistError as e:
                logger.error("%s; the run continues with the in-memory tokens", e)
            except Exception as e:  # the data call goes on with the in-memory tokens
                logger.error(
                    "could not write the rotated Digital Advisor tokens back to the config "
                    "(%s); the run continues with the in-memory tokens",
                    type(e).__name__,
                )
        return access


_SET_PAT_HINT = "'nf config set-credential --setting digitaladvisorapi.personal_access_token'"


class FallbackTokenProvider:
    """A PAT first, with a refresh pair as the fallback.

    The PAT is sent until the server rejects it. The first ``invalidate`` of the
    PAT switches to the refresh provider for the rest of the provider's life and
    logs one warning that names the credentials (never a value). Building the
    refresh provider makes no request and no write, so a working PAT means no
    token request and no config write.
    """

    refreshable = True

    def __init__(self, primary: StaticTokenProvider, fallback: RefreshingTokenProvider) -> None:
        self._primary = primary
        self._fallback = fallback
        self._lock = threading.Lock()
        self._fell_back = False

    def __repr__(self) -> str:
        return f"FallbackTokenProvider(fell_back={self._fell_back!r})"

    @property
    def fell_back(self) -> bool:
        """Whether the PAT was rejected and the refresh pair is in use."""
        return self._fell_back

    @property
    def credential(self) -> str:
        """Name of the credential in use: ``personal_access_token`` or ``refresh_token``."""
        return self._fallback.credential if self._fell_back else self._primary.credential

    def get_token(self) -> str:
        """Return the PAT, or after the switch the refresh provider's token.

        Raises:
            DigitalAdvisorAuthError: If the fallback refresh fails; the message
                names the renewal step for both credentials.
        """
        if not self._fell_back:
            return self._primary.get_token()
        try:
            return self._fallback.get_token()
        except DigitalAdvisorAuthError as e:
            raise DigitalAdvisorAuthError(
                "Digital Advisor rejected the personal access token, and the refresh_token "
                f"fallback failed: {e} Also create a new personal access token and store it "
                f"with {_SET_PAT_HINT}."
            ) from e

    def invalidate(self, token: str) -> None:
        """Switch to the refresh pair when the PAT is rejected, else delegate."""
        with self._lock:
            if not self._fell_back and token == self._primary.get_token():
                self._fell_back = True
                logger.warning(
                    "the Digital Advisor personal_access_token was rejected; "
                    "falling back to the refresh_token"
                )
                return
        self._fallback.invalidate(token)
