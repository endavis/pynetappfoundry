"""Org-scoped Console SaaS facade (ADR-0019).

Primary entry point for callers:

    from pynetappfoundry.console import Console

    console = Console(config, org_id="org-abc123")
    org = console.get_organization()
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pynetappfoundry.clients.console import (
    ClientCredentialsTokenProvider,
    ConsoleAPIClient,
    ConsoleAuthError,
    ConsoleServiceTokenMissingError,
    ConsoleUserTokenMissingError,
)
from pynetappfoundry.clients.console.agent import ConsoleAgentClient
from pynetappfoundry.models.console_types import (
    AccountSubscription,
    Connector,
    Folder,
    MarketplaceSubscription,
    Organization,
    Project,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from pynetappfoundry.core.config import Config


class Console:
    """Org-scoped facade for the Console SaaS API (ADR-0019).

    Per ADR-0019 §1, Console primary access is *org-scoped*.  Instantiate
    with an org_id (either directly or via consoleapi.toml ``org_id``).
    There is intentionally no ``ClusterEntry.console`` accessor in v1.
    """

    def __init__(
        self, config: Config, org_id: str | None = None, *, scope: str | None = None
    ) -> None:
        """Initialize the org-scoped Console facade.

        Args:
            config: Configuration object.
            org_id: The organization UUID to bind to.  If omitted, falls back
                    to ``org_id`` from ``consoleapi.toml [general]``.
            scope: Use this config scope's Console account (its own
                ``consoleapi.toml`` and refresh token) instead of the root one.

        Raises:
            ValueError: If no org_id is available from either source.
        """
        self._config = config
        self._scope = scope
        if scope is None:
            self._client = ConsoleAPIClient(config)
            settings = config.get_console_api_settings()
        else:
            self._client = ConsoleAPIClient(config, scope=scope)
            settings = config.get_console_api_settings(scope=scope)
        resolved = org_id or settings.org_id
        if not resolved:
            raise ValueError(
                "Console requires an org_id either as a constructor argument "
                "or in consoleapi.toml [general] as 'org_id'."
            )
        self.org_id: str = resolved

    def get_organization(self) -> Organization:
        """Get the organization bound to this Console instance.

        Returns:
            The Organization for ``self.org_id``.
        """
        return self._client.get_organization(self.org_id)

    def list_organizations(self) -> list[Organization]:
        """List all organizations the bound user can see.

        Returns:
            List of Organization instances.
        """
        return self._client.list_organizations()

    def get_folder(self, folder_id: str) -> Folder:
        """Get a folder by ID.

        Args:
            folder_id: The folder UUID.

        Returns:
            The Folder for *folder_id*.
        """
        return self._client.get_folder(folder_id)

    def get_project(self, project_id: str) -> Project:
        """Get a project by ID.

        Args:
            project_id: The project UUID.

        Returns:
            The Project for *project_id*.
        """
        return self._client.get_project(project_id)

    def list_preferred_subscriptions(
        self, account_id: str | None = None, cloud_provider: str | None = None
    ) -> list[AccountSubscription]:
        """List the preferred subscriptions of a Console account.

        Args:
            account_id: The Console account id. Defaults to this facade's org id,
                which equals the account id (measured live, ADR-0019).
            cloud_provider: Optional cloud provider filter.

        Returns:
            The account's preferred subscriptions; empty when it has none.
        """
        return self._client.list_preferred_subscriptions(
            self.org_id if account_id is None else account_id, cloud_provider
        )

    def _agent_client(self, agent_id: str) -> ConsoleAgentClient:
        """Build a Console agent client sharing this facade's token provider.

        The user provider (refresh-token grant) is shared when set, otherwise the
        service provider (client credentials).
        """
        user_provider = self._client.user_token_provider
        provider = (
            user_provider if user_provider is not None else self._client.service_token_provider
        )
        if self._scope is None:
            return ConsoleAgentClient(self._config, agent_id, token_provider=provider)
        return ConsoleAgentClient(
            self._config, agent_id, token_provider=provider, scope=self._scope
        )

    def get_connector(self, agent_id: str) -> Connector:
        """Get a Console agent (connector) by agent ID.

        Args:
            agent_id: The Console agent id.

        Returns:
            The Connector for *agent_id*.
        """
        return self._agent_client(agent_id).get_connector()

    def list_marketplace_subscriptions(self, agent_id: str) -> list[MarketplaceSubscription]:
        """List the account's SaaS marketplace subscriptions through an agent.

        Org-scoped and not cached (ADR-0019).

        Args:
            agent_id: The Console agent id to query.

        Returns:
            The AWS, Azure and GCP subscriptions as one flat list.
        """
        return self._agent_client(agent_id).list_marketplace_subscriptions()

    def find_connector(
        self, cluster_uuid: str, agent_ids: Sequence[str] | None = None
    ) -> Connector | None:
        """Find the connector (Console agent) that manages a cluster.

        Queries each agent in order and stops at the first one with an on-prem
        working environment for the cluster.  Errors propagate.

        Args:
            cluster_uuid: The ONTAP cluster UUID.
            agent_ids: Agent ids to search.  Defaults to ``agent_ids`` from
                ``consoleapi.toml [general]`` when omitted.

        Returns:
            The matching Connector, or ``None`` when no agent manages the cluster.

        Raises:
            ValueError: If no agent ids come from the argument or the settings.
        """
        ids = list(agent_ids) if agent_ids is not None else None
        if ids is None:
            settings = (
                self._config.get_console_api_settings()
                if self._scope is None
                else self._config.get_console_api_settings(scope=self._scope)
            )
            ids = list(settings.agent_ids)
        if not ids:
            raise ValueError(
                "find_connector requires agent ids, either as an argument or in "
                "consoleapi.toml [general] as 'agent_ids'."
            )
        for agent_id in ids:
            agent = self._agent_client(agent_id)
            if agent.find_onprem_working_environment(cluster_uuid) is not None:
                return agent.get_connector()
        return None


__all__ = [
    "AccountSubscription",
    "ClientCredentialsTokenProvider",
    "Connector",
    "Console",
    "ConsoleAPIClient",
    "ConsoleAuthError",
    "ConsoleServiceTokenMissingError",
    "ConsoleUserTokenMissingError",
    "Folder",
    "MarketplaceSubscription",
    "Organization",
    "Project",
]
