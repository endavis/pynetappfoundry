"""Discover Console organizations, working environments and agents (#1078, ADR-0029).

Each configured Console account (the root and every scope with its own
``consoleapi.toml``, see ``Config.console_account_scopes``) is a service account.
Discovery walks each account to the organizations it can see and, for each
organization, lists its working environments (organization resources of type
``ON_PREM``) and its agents.  Every object is reported under the account that
listed it.  Discovery does not map a working environment to an agent: that mapping
lives in the OCCM cache (``src/pynetappfoundry/cache/occm_db.py``, #1076, ADR-0030).
It does not reconcile agents against ``[connectors]``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

from pynetappfoundry.clients.console.api import ConsoleAPIClient
from pynetappfoundry.models.console_types import (
    ConsoleAgentInfo,
    ConsoleWorkingEnvironment,
    Organization,
)

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config

ON_PREM_RESOURCE_TYPE = "ON_PREM"
"""The organization resource type of a working environment."""


class AccountInventory(BaseModel):
    """What one Console account can see."""

    scope: str | None
    """The account's scope, or None for the root account."""
    organizations: list[Organization] = Field(default_factory=list)
    agents: list[ConsoleAgentInfo] = Field(default_factory=list)
    working_environments: list[ConsoleWorkingEnvironment] = Field(default_factory=list)


class ConsoleInventory(BaseModel):
    """The inventories of every configured Console account."""

    accounts: list[AccountInventory] = Field(default_factory=list)

    def agents(self) -> list[ConsoleAgentInfo]:
        """Return the agents of every account, in account order."""
        return [agent for account in self.accounts for agent in account.agents]

    def working_environments(self) -> list[ConsoleWorkingEnvironment]:
        """Return the working environments of every account, in account order."""
        return [env for account in self.accounts for env in account.working_environments]


class ConsoleDiscovery:
    """Walk the configured Console accounts and report what each can see.

    Errors from an account's own calls propagate: a failing account is not
    skipped, because a partial inventory would look complete.
    """

    def __init__(
        self,
        config: Config,
        *,
        api_client_factory: Callable[..., ConsoleAPIClient] | None = None,
    ) -> None:
        """Initialize discovery.

        Args:
            config: Configuration object.
            api_client_factory: Builds the API client of an account.  It is called
                as ``factory(config)`` for the root account and
                ``factory(config, scope=scope)`` for a scope.  Defaults to
                ``ConsoleAPIClient``.
        """
        self._config = config
        self._factory: Callable[..., ConsoleAPIClient] = api_client_factory or ConsoleAPIClient

    def accounts(self) -> list[str | None]:
        """Return the configured accounts: None for the root, then scope names."""
        return self._config.console_account_scopes()

    def _client(self, scope: str | None) -> ConsoleAPIClient:
        kwargs: dict[str, Any] = {} if scope is None else {"scope": scope}
        return self._factory(self._config, **kwargs)

    def discover_account(self, scope: str | None) -> AccountInventory:
        """Walk one account: its organizations, and each one's resources and agents.

        Args:
            scope: The account's scope, or None for the root account.

        Returns:
            The account's inventory; empty when it sees no organizations.
        """
        client = self._client(scope)
        inventory = AccountInventory(scope=scope, organizations=client.list_organizations())
        for organization in inventory.organizations:
            for resource in client.list_organization_resources(organization.id):
                if resource.resourceType == ON_PREM_RESOURCE_TYPE:
                    inventory.working_environments.append(
                        ConsoleWorkingEnvironment.from_resource(
                            resource, scope=scope, organization_id=organization.id
                        )
                    )
            inventory.agents.extend(client.list_agents(organization.id))
        return inventory

    def discover(self) -> ConsoleInventory:
        """Walk every configured account.

        Returns:
            One inventory per account, in ``accounts()`` order.
        """
        return ConsoleInventory(accounts=[self.discover_account(s) for s in self.accounts()])


__all__ = [
    "ON_PREM_RESOURCE_TYPE",
    "AccountInventory",
    "ConsoleDiscovery",
    "ConsoleInventory",
]
