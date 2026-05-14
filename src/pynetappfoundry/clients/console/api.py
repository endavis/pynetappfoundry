"""Console SaaS API client with per-token-type wrapper isolation (ADR-0019)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pynetappfoundry.clients.openapi import APIWrapper
from pynetappfoundry.models.console.types import Organization

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config


class ConsoleServiceTokenMissingError(RuntimeError):
    """Raised when a service-token endpoint is called without a configured service token."""


class ConsoleAPIClient:
    """Console SaaS API client with per-token-type wrapper isolation (ADR-0019).

    Wraps two internal ``APIWrapper`` instances — one for user-token endpoints
    and one (optional) for service-token endpoints.  ``APIWrapper``'s static
    ``auth_header`` contract is preserved; token selection is resolved at
    construction time, not per-call.
    """

    def __init__(self, config: Config) -> None:
        """Initialize the Console API client.

        Args:
            config: Configuration object with Console API settings.
        """
        self.config = config
        settings = config.get_console_api_settings()
        spec_path = str(config.get_schema_location("console") / "console_openapi.yaml")

        self._user = APIWrapper(
            api_json_file=spec_path,
            base_url=settings.base_url,
            auth_header={"Authorization": f"Bearer {settings.user_token}"},
            base_api_path=settings.base_api_path,
            timeout=settings.timeout,
            name="console-user",
        )

        if settings.service_token:
            self._service: APIWrapper | None = APIWrapper(
                api_json_file=spec_path,
                base_url=settings.base_url,
                auth_header={"Authorization": f"Bearer {settings.service_token}"},
                base_api_path=settings.base_api_path,
                timeout=settings.timeout,
                name="console-service",
            )
        else:
            self._service = None

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

    def get_organization(self, organization_id: str) -> Organization:
        """GET /organizations/{organization_id} (user-token endpoint).

        Args:
            organization_id: The organization UUID.

        Returns:
            Compact Organization instance.
        """
        response: Any = self._user.call_endpoint(
            method="GET",
            path_template="/organizations/{organization_id}",
            path_params={"organization_id": organization_id},
        )
        return Organization.model_validate(response)

    def list_organizations(self) -> list[Organization]:
        """GET /organizations (user-token endpoint).

        Returns all organizations the bound user can see.  Pagination
        (the ``continue`` cursor) is out of scope for v1.

        Returns:
            List of compact Organization instances.
        """
        response: Any = self._user.call_endpoint(
            method="GET",
            path_template="/organizations",
        )
        items: list[Any] = response.get("items", [])
        return [Organization.model_validate(item) for item in items]


__all__ = ["ConsoleAPIClient", "ConsoleServiceTokenMissingError"]
