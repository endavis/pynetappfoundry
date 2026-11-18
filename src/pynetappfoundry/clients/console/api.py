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
from pynetappfoundry.models.console_types import (
    AccountSubscription,
    ConsoleAgentInfo,
    Folder,
    Organization,
    Project,
)

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config
    from pynetappfoundry.models.console.tenancyv4 import get_organizations_resources


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

    def __init__(
        self,
        config: Config,
        *,
        token_session: requests.Session | None = None,
        scope: str | None = None,
    ) -> None:
        """Initialize the Console API client.

        Args:
            config: Configuration object with Console API settings.
            token_session: Optional ``requests.Session`` used for the token
                exchange (tests inject one).
            scope: Use this scope's Console account instead of the root one.

        Raises:
            ConsoleAuthError: If client credentials are configured and the
                initial token exchange fails.
        """
        self.config = config
        self.scope = scope
        settings = (
            config.get_console_api_settings()
            if scope is None
            else config.get_console_api_settings(scope=scope)
        )
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
        return Organization.model_validate(self.ops.get_organization(organization_id).model_dump())

    def list_organizations(self) -> list[Organization]:
        """GET /v1/management/organizations (user or service token).

        Returns all organizations the bound user or service account can see.
        Pagination (the ``continue`` cursor) is out of scope for v1.

        Returns:
            List of compact Organization instances.
        """
        items = self.ops.list_organizations().items or []
        return [Organization.from_resource(item) for item in items]

    def list_organization_resources(
        self, organization_id: str
    ) -> list[get_organizations_resources.Resource10GetResponseBody]:
        """GET /v1/management/organizations/{organization_id}/resources, all pages.

        Follows the ``continue`` cursor until a page has none.

        Args:
            organization_id: The organization UUID.

        Returns:
            Every resource of the organization, in page order.

        Raises:
            RuntimeError: If the service returns a cursor it already returned,
                which would loop forever.
        """
        resources: list[get_organizations_resources.Resource10GetResponseBody] = []
        seen: set[str] = set()
        cursor: str | None = None
        while True:
            page = self.ops.list_organization_resources(organization_id, continue_=cursor)
            resources.extend(page.items or [])
            cursor = page.continue_
            if not cursor:
                return resources
            if cursor in seen:
                raise RuntimeError(
                    f"Console returned the same continue cursor twice while listing the "
                    f"resources of organization {organization_id!r}; stopping."
                )
            seen.add(cursor)

    def list_agents(self, organization_id: str) -> list[ConsoleAgentInfo]:
        """GET /agents-mgmt/list-connectors/{organization_id} (user or service token).

        The endpoint is not paginated: one call returns every agent of the
        organization.  ``agent.status`` (``active`` or ``inactive`` as measured)
        identifies inactive agents; the item ``status`` was ``active`` throughout.
        See ADR-0029 (#1083).

        Args:
            organization_id: The organization UUID.

        Returns:
            The organization's agents, tagged with this client's scope.
        """
        occms = self.ops.list_connectors(organization_id).occms or []
        return [
            ConsoleAgentInfo.from_occm(occm, scope=self.scope, organization_id=organization_id)
            for occm in occms
        ]

    def get_agent(self, agent_id: str) -> ConsoleAgentInfo:
        """GET /agents-mgmt/agent/{agent_id} (user or service token).

        Args:
            agent_id: The Console agent id.

        Returns:
            The compact agent, tagged with this client's scope.
        """
        return ConsoleAgentInfo.from_agent(self.ops.get_agent(agent_id), scope=self.scope)

    def get_folder(self, folder_id: str) -> Folder:
        """GET /v1/management/folders/{folder_id} (user or service token).

        Args:
            folder_id: The folder UUID.

        Returns:
            Compact Folder instance.
        """
        return Folder.model_validate(self.ops.get_folder(folder_id).model_dump())

    def get_project(self, project_id: str) -> Project:
        """GET /v1/management/projects/{project_id} (user or service token).

        Args:
            project_id: The project UUID.

        Returns:
            Compact Project instance.
        """
        return Project.model_validate(self.ops.get_project(project_id).model_dump())

    def list_preferred_subscriptions(
        self, account_id: str, cloud_provider: str | None = None
    ) -> list[AccountSubscription]:
        """GET /license/account/{accountId}/subscriptions/preferred (user or service token).

        ``account_id`` is the Console account id; it equals the tenancyv4
        organization id (measured live, ADR-0019). The response is a JSON array,
        empty when the account has no preferred subscription.

        Args:
            account_id: The Console account id.
            cloud_provider: Optional cloud provider filter.

        Returns:
            The account's preferred subscriptions as compact AccountSubscription instances.
        """
        items = self.ops.list_preferred_subscriptions(account_id, cloud_provider=cloud_provider)
        return [AccountSubscription.from_preferred(item) for item in items]


__all__ = [
    "ConsoleAPIClient",
    "ConsoleServiceTokenMissingError",
    "ConsoleUserTokenMissingError",
    "call_with_token",
]
