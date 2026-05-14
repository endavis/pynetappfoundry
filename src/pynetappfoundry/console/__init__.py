"""Org-scoped Console SaaS facade (ADR-0019).

Primary entry point for callers:

    from pynetappfoundry.console import Console

    console = Console(config, org_id="org-abc123")
    org = console.get_organization()
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pynetappfoundry.clients.console import ConsoleAPIClient, ConsoleServiceTokenMissingError
from pynetappfoundry.models.console.types import Organization

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config


class Console:
    """Org-scoped facade for the Console SaaS API (ADR-0019).

    Per ADR-0019 §1, Console primary access is *org-scoped*.  Instantiate
    with an org_id (either directly or via consoleapi.toml ``org_id``).
    There is intentionally no ``ClusterEntry.console`` accessor in v1.
    """

    def __init__(self, config: Config, org_id: str | None = None) -> None:
        """Initialize the org-scoped Console facade.

        Args:
            config: Configuration object.
            org_id: The organization UUID to bind to.  If omitted, falls back
                    to ``org_id`` from ``consoleapi.toml [general]``.

        Raises:
            ValueError: If no org_id is available from either source.
        """
        self._client = ConsoleAPIClient(config)
        settings = config.get_console_api_settings()
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


__all__ = ["Console", "ConsoleAPIClient", "ConsoleServiceTokenMissingError", "Organization"]
