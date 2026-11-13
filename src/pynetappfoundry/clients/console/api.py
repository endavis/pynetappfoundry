"""Console SaaS API client with per-token-type wrapper isolation (ADR-0019)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import requests

from pynetappfoundry.clients.console._ops_support import TokenType
from pynetappfoundry.clients.console.auth import (
    ClientCredentialsTokenProvider,
    RefreshTokenProvider,
    TokenProvider,
)
from pynetappfoundry.clients.console.generated import ConsoleTenancyOps
from pynetappfoundry.clients.openapi import APIWrapper
from pynetappfoundry.models.console_types import Folder, Organization, Project

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config


def call_with_token(wrapper: APIWrapper, provider: TokenProvider | None, **kwargs: Any) -> Any:
    """Call an endpoint, supplying and refreshing a dynamic token if needed.

    With no provider the call is exactly ``wrapper.call_endpoint(**kwargs)``.
    With a provider the Bearer token is sent per call; on a 401 the token
    is invalidated, refetched and the call retried once.

    Args:
        wrapper: The wrapper to call through.
        provider: Token provider for the wrapper's slot, or None.
        **kwargs: Arguments for ``APIWrapper.call_endpoint``.

    Returns:
        The decoded response.
    """
    if provider is None:
        return wrapper.call_endpoint(**kwargs)

    token = provider.get_token()
    try:
        return wrapper.call_endpoint(
            **kwargs, additional_headers={"Authorization": f"Bearer {token}"}
        )
    except requests.HTTPError as e:
        if e.response is None or e.response.status_code != 401:
            raise
    provider.invalidate(token)
    token = provider.get_token()
    return wrapper.call_endpoint(**kwargs, additional_headers={"Authorization": f"Bearer {token}"})


class ConsoleServiceTokenMissingError(RuntimeError):
    """Raised when a service-token endpoint is called without a configured service token."""


class ConsoleUserTokenMissingError(RuntimeError):
    """Raised when a user-token endpoint is called without a configured user token."""


class ConsoleAPIClient:
    """Console SaaS API client with per-token-type wrapper isolation (ADR-0019).

    Wraps two internal ``APIWrapper`` instances — one for user-token endpoints
    and one (optional) for service-token endpoints.  ``APIWrapper``'s static
    ``auth_header`` contract is preserved.  A slot backed by a static token
    resolves it at construction time.  A slot backed by an OAuth
    client-credentials grant gets its bearer token per call through
    ``additional_headers``, and a 401 triggers one refresh and retry.
    """

    def __init__(self, config: Config, *, token_session: requests.Session | None = None) -> None:
        """Initialize the Console API client.

        Args:
            config: Configuration object with Console API settings.
            token_session: Optional ``requests.Session`` used for the token
                exchange (tests inject one).

        Raises:
            ConsoleAuthError: If client credentials are configured and the
                initial token exchange fails.
        """
        self.config = config
        settings = config.get_console_api_settings()
        spec_path = str(config.get_schema_location("console") / "console_openapi.yaml")

        self._user: APIWrapper | None
        self._user_provider: TokenProvider | None = None
        if settings.refresh_token is not None:
            self._user = APIWrapper(
                api_json_file=spec_path,
                base_url=settings.base_url,
                auth_header=None,
                base_api_path=settings.base_api_path,
                timeout=settings.timeout,
                name="console-user",
                use_operation_servers=True,
            )
            self._user_provider = RefreshTokenProvider(
                refresh_token=settings.refresh_token,
                client_id=settings.user_client_id,
                token_endpoint=settings.token_endpoint,
                timeout=settings.timeout,
                session=token_session,
            )
            # Fail fast on a bad refresh token rather than on the first API call.
            self._user_provider.get_token()
        elif settings.user_token:
            self._user = APIWrapper(
                api_json_file=spec_path,
                base_url=settings.base_url,
                auth_header={"Authorization": f"Bearer {settings.user_token.get_secret_value()}"},
                base_api_path=settings.base_api_path,
                timeout=settings.timeout,
                name="console-user",
                use_operation_servers=True,
            )
        else:
            self._user = None

        self._service: APIWrapper | None
        self._service_provider: TokenProvider | None = None
        if settings.client_id and settings.client_secret:
            self._service = APIWrapper(
                api_json_file=spec_path,
                base_url=settings.base_url,
                auth_header=None,
                base_api_path=settings.base_api_path,
                timeout=settings.timeout,
                name="console-service",
                use_operation_servers=True,
            )
            self._service_provider = ClientCredentialsTokenProvider(
                client_id=settings.client_id,
                client_secret=settings.client_secret,
                token_endpoint=settings.token_endpoint,
                audience=settings.audience,
                timeout=settings.timeout,
                session=token_session,
            )
            # Fail fast on bad credentials rather than on the first API call.
            self._service_provider.get_token()
        elif settings.service_token:
            self._service = APIWrapper(
                api_json_file=spec_path,
                base_url=settings.base_url,
                auth_header={
                    "Authorization": f"Bearer {settings.service_token.get_secret_value()}"
                },
                base_api_path=settings.base_api_path,
                timeout=settings.timeout,
                name="console-service",
                use_operation_servers=True,
            )
        else:
            self._service = None

        self.ops = ConsoleTenancyOps(self._dispatch)

    @property
    def user_token_provider(self) -> TokenProvider | None:
        """The user-slot token provider, or None for a static or absent token."""
        return self._user_provider

    @property
    def service_token_provider(self) -> TokenProvider | None:
        """The service-slot token provider, or None for a static or absent token."""
        return self._service_provider

    def _require_service(self) -> APIWrapper:
        """Return the service-token wrapper, or raise if not configured.

        Returns:
            The service-token ``APIWrapper``.

        Raises:
            ConsoleServiceTokenMissingError: If no service_token was provided.
        """
        if self._service is None:
            raise ConsoleServiceTokenMissingError(
                "This Console endpoint requires a service token, but no "
                "service_token was provided in settings. Add service_token to "
                "consoleapi.toml [general]."
            )
        return self._service

    def _require_user(self) -> APIWrapper:
        """Return the user-token wrapper, or raise if not configured.

        Returns:
            The user-token ``APIWrapper``.

        Raises:
            ConsoleUserTokenMissingError: If no user_token was provided.
        """
        if self._user is None:
            raise ConsoleUserTokenMissingError(
                "This Console endpoint requires a user token, but no "
                "user_token was provided in settings. Add user_token to "
                "consoleapi.toml [general], or a refresh token in users.toml [console]."
            )
        return self._user

    def _route_any(self) -> tuple[APIWrapper, TokenProvider | None]:
        """Pick the wrapper for an operation that accepts either token type.

        Prefers the user token and falls back to the service token.

        Returns:
            The wrapper and its token provider (None for a static token).

        Raises:
            ConsoleUserTokenMissingError: If neither token type is configured.
        """
        if self._user is not None:
            return self._user, self._user_provider
        if self._service is not None:
            return self._service, self._service_provider
        return self._require_user(), None

    def _dispatch(self, token_type: TokenType, /, **call_kwargs: Any) -> Any:
        """Send a generated operation through the wrapper for its token type.

        Args:
            token_type: The operation's ``x-token-type``: ``"user"``, ``"service"``,
                or ``None`` when either token works (the user token is preferred).
            **call_kwargs: Arguments for ``APIWrapper.call_endpoint``.

        Returns:
            The decoded response.

        Raises:
            ConsoleUserTokenMissingError: For a user operation without a user token.
            ConsoleServiceTokenMissingError: For a service operation without a service token.
        """
        if token_type == "user":  # nosec B105  # token kind name, not a credential
            return call_with_token(self._require_user(), self._user_provider, **call_kwargs)
        if token_type == "service":  # nosec B105  # token kind name, not a credential
            return call_with_token(self._require_service(), self._service_provider, **call_kwargs)
        wrapper, provider = self._route_any()
        return call_with_token(wrapper, provider, **call_kwargs)

    @staticmethod
    def _call(wrapper: APIWrapper, provider: TokenProvider | None, **kwargs: Any) -> Any:
        """Call an endpoint, supplying and refreshing a dynamic token if needed.

        With no provider the call is exactly ``wrapper.call_endpoint(**kwargs)``.
        With a provider the Bearer token is sent per call; on a 401 the token
        is invalidated, refetched and the call retried once.

        Args:
            wrapper: The wrapper to call through.
            provider: Token provider for the wrapper's slot, or None.
            **kwargs: Arguments for ``APIWrapper.call_endpoint``.

        Returns:
            The decoded response.
        """
        return call_with_token(wrapper, provider, **kwargs)

    def get_organization(self, organization_id: str) -> Organization:
        """GET /v1/management/organizations/{organization_id} (user or service token).

        Args:
            organization_id: The organization UUID.

        Returns:
            Compact Organization instance.
        """
        return Organization.model_validate(self.ops.get_organization(organization_id))

    def list_organizations(self) -> list[Organization]:
        """GET /v1/management/organizations (user or service token).

        Returns all organizations the bound user or service account can see.
        Pagination (the ``continue`` cursor) is out of scope for v1.

        Returns:
            List of compact Organization instances.
        """
        items: list[Any] = self.ops.list_organizations().get("items", [])
        return [Organization.model_validate(item) for item in items]

    def get_folder(self, folder_id: str) -> Folder:
        """GET /v1/management/folders/{folder_id} (user or service token).

        Args:
            folder_id: The folder UUID.

        Returns:
            Compact Folder instance.
        """
        return Folder.model_validate(self.ops.get_folder(folder_id))

    def get_project(self, project_id: str) -> Project:
        """GET /v1/management/projects/{project_id} (user or service token).

        Args:
            project_id: The project UUID.

        Returns:
            Compact Project instance.
        """
        return Project.model_validate(self.ops.get_project(project_id))


__all__ = [
    "ConsoleAPIClient",
    "ConsoleServiceTokenMissingError",
    "ConsoleUserTokenMissingError",
    "call_with_token",
]
