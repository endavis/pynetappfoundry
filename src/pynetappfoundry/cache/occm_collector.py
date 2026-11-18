"""Collector for the Console agent (OCCM) cache (#1076, ADR-0030).

A library function only: :class:`OccmCollector` runs ``ConsoleDiscovery``, then
for each discovered agent (deduplicated by ``agent_id``) lists the working
environments in :data:`OCCM_CACHED_MAPPINGS` through the agent's typed ops, and
:func:`refresh_occm_cache` stores the result in :class:`OccmCacheDB`.

A discovery failure propagates and the database is left untouched.  A failing
agent is logged and recorded in :attr:`OccmSnapshot.failed_agents`; the other
agents are still collected and the failed agent's earlier rows are kept.  A transport
or auth error fails the whole agent; a ``TypeError`` or ``ValueError`` (including a
pydantic ``ValidationError``) fails only that mapping, which is recorded in
:attr:`OccmSnapshot.failed_mappings` and keeps its earlier rows.  When every mapping
fails the agent is failed.  An agent
whose status is set and is not ``active`` is not contacted; it is recorded in
:attr:`OccmSnapshot.skipped_agents` and keeps its earlier rows too (#1091).

This module imports nothing from ``pynetappfoundry.data``.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

import requests
from tenacity import RetryError

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.clients.console.auth import ConsoleAuthError

if TYPE_CHECKING:
    from pynetappfoundry.cache.field_mapping import TypeMapping
    from pynetappfoundry.cache.occm_db import OccmCacheDB
    from pynetappfoundry.clients.console.agent import ConsoleAgentClient
    from pynetappfoundry.console.discovery import ConsoleDiscovery, ConsoleInventory
    from pynetappfoundry.core.config import Config

logger = logging.getLogger(__name__)

#: The working-environment mappings: on-prem plus the six cloud lists (#1074).
OCCM_WORKING_ENVIRONMENT_MAPPINGS: tuple[str, ...] = (
    "OccmOnpremWorkingEnvironment",
    "OccmAwsWorkingEnvironment",
    "OccmAwsHaWorkingEnvironment",
    "OccmAzureWorkingEnvironment",
    "OccmAzureHaWorkingEnvironment",
    "OccmGcpWorkingEnvironment",
    "OccmGcpHaWorkingEnvironment",
)

#: The OCCM mappings the cache holds.
OCCM_CACHED_MAPPINGS: tuple[str, ...] = OCCM_WORKING_ENVIRONMENT_MAPPINGS

#: ``mapping.api_endpoint`` -> name of the ``ConsoleAgentOps`` method that lists it.
OCCM_LIST_OPS: dict[str, str] = {
    "/occm/api/onprem/working-environments": "list_onprem_working_environments",
    "/occm/api/vsa/working-environments": "list_vsa_working_environments",
    "/occm/api/aws/ha/working-environments": "list_aws_ha_working_environments",
    "/occm/api/azure/vsa/working-environments": "list_azure_vsa_working_environments",
    "/occm/api/azure/ha/working-environments": "list_azure_ha_working_environments",
    "/occm/api/gcp/vsa/working-environments": "list_gcp_vsa_working_environments",
    "/occm/api/gcp/ha/working-environments": "list_gcp_ha_working_environments",
}


@dataclass(frozen=True)
class OccmAgentSnapshot:
    """The collected records of one Console agent.

    Attributes:
        agent_id: The agent id.
        scope: The Console account scope that listed the agent, or None for the root.
        organization_id: The organization the agent was listed under, if known.
        cached_at: When the agent's collection finished.
        records: Raw JSON records keyed by mapping name.
    """

    agent_id: str
    scope: str | None
    organization_id: str | None
    cached_at: datetime
    records: dict[str, list[dict[str, Any]]]


@dataclass(frozen=True)
class OccmSnapshot:
    """The result of one OCCM collection run.

    Attributes:
        cached_at: When the run finished.
        inventory: What discovery found.
        agents: The agents that were collected.
        failed_agents: Ids of the agents whose collection failed.
        skipped_agents: Ids of the agents not contacted because their status
            is set and is not ``active``.
        failed_mappings: ``(agent_id, mapping)`` pairs whose list failed with a
            ``TypeError`` or ``ValueError`` while the agent itself was collected;
            the mapping keeps its earlier rows.
        scopes: The Console account scopes the run was limited to (``None`` is the
            root account), or ``None`` when every account was collected.
    """

    cached_at: datetime
    inventory: ConsoleInventory
    agents: tuple[OccmAgentSnapshot, ...] = ()
    failed_agents: tuple[str, ...] = field(default=())
    skipped_agents: tuple[str, ...] = field(default=())
    failed_mappings: tuple[tuple[str, str], ...] = field(default=())
    scopes: tuple[str | None, ...] | None = None


class OccmCollector:
    """Discover the Console agents and list the cached mappings on each.

    Args:
        config: The configuration holding the Console accounts.
        discovery: Discovery to use; defaults to ``ConsoleDiscovery(config)``.
        agent_client_factory: Builds an agent client, called as
            ``factory(config, agent_id)`` or ``factory(config, agent_id, scope=scope)``
            for a scoped agent.  Defaults to ``ConsoleAgentClient``.
        mappings: Names of the mappings to collect.
        scopes: Limit discovery to these Console account scopes (``None`` is the
            root account); ``None`` collects every configured account.
    """

    def __init__(
        self,
        config: Config,
        *,
        discovery: ConsoleDiscovery | None = None,
        agent_client_factory: Callable[..., ConsoleAgentClient] | None = None,
        mappings: Sequence[str] = OCCM_CACHED_MAPPINGS,
        scopes: Sequence[str | None] | None = None,
    ) -> None:
        self._config = config
        self._discovery = discovery
        self._factory = agent_client_factory
        self._mappings = tuple(mappings)
        self._scopes = None if scopes is None else tuple(scopes)

    def _resolve(self) -> list[tuple[TypeMapping, str]]:
        resolved: list[tuple[TypeMapping, str]] = []
        for name in self._mappings:
            mapping = model_registry.get_mapping(name)
            if mapping is None:
                raise ValueError(f"Unknown OCCM mapping {name!r}")
            op_name = OCCM_LIST_OPS.get(mapping.api_endpoint)
            if op_name is None:
                raise ValueError(f"OCCM mapping {name!r} has no list op for {mapping.api_endpoint}")
            resolved.append((mapping, op_name))
        return resolved

    def _client(self, agent_id: str, scope: str | None) -> ConsoleAgentClient:
        factory = self._factory
        if factory is None:
            from pynetappfoundry.clients.console.agent import ConsoleAgentClient

            factory = ConsoleAgentClient
        if scope is None:
            return factory(self._config, agent_id)
        return factory(self._config, agent_id, scope=scope)

    def collect(self) -> OccmSnapshot:
        """Discover, then collect every cached mapping from each unique agent.

        An agent whose status is set and is not ``active`` (case-insensitive) is
        skipped without being contacted and recorded in ``skipped_agents``.

        Raises:
            ValueError: If a mapping name is unknown or has no list op.
            Exception: Any error discovery raises propagates unchanged.
        """
        resolved = self._resolve()
        discovery = self._discovery
        if discovery is None:
            from pynetappfoundry.console.discovery import ConsoleDiscovery

            discovery = ConsoleDiscovery(self._config)
        if self._scopes is None:
            inventory = discovery.discover()
        else:
            from pynetappfoundry.console.discovery import ConsoleInventory

            inventory = ConsoleInventory(
                accounts=[discovery.discover_account(scope) for scope in self._scopes]
            )

        collected: list[OccmAgentSnapshot] = []
        failed: list[str] = []
        skipped: list[str] = []
        failed_mappings: list[tuple[str, str]] = []
        seen: set[str] = set()
        for agent in inventory.agents():
            if agent.agent_id in seen:
                continue
            seen.add(agent.agent_id)
            if agent.status is not None and agent.status.lower() != "active":
                logger.info("OCCM agent %s: skipped, status %r", agent.agent_id, agent.status)
                skipped.append(agent.agent_id)
                continue
            records: dict[str, list[dict[str, Any]]] = {}
            agent_failed_mappings: list[tuple[str, str]] = []
            try:
                client = self._client(agent.agent_id, agent.scope)
                for mapping, op_name in resolved:
                    try:
                        items = getattr(client.ops, op_name)(fields="*")
                        records[mapping.name] = [item.model_dump(mode="json") for item in items]
                    except (TypeError, ValueError) as exc:
                        logger.warning(
                            "OCCM agent %s: mapping %s failed: %s",
                            agent.agent_id,
                            mapping.name,
                            exc,
                        )
                        agent_failed_mappings.append((agent.agent_id, mapping.name))
            except (
                requests.RequestException,
                ConsoleAuthError,
                RetryError,
                TypeError,
                ValueError,
            ) as exc:
                logger.warning("OCCM agent %s: collection failed: %s", agent.agent_id, exc)
                failed.append(agent.agent_id)
                continue
            if resolved and len(agent_failed_mappings) == len(resolved):
                logger.warning("OCCM agent %s: every mapping failed", agent.agent_id)
                failed.append(agent.agent_id)
                continue
            failed_mappings.extend(agent_failed_mappings)
            collected.append(
                OccmAgentSnapshot(
                    agent_id=agent.agent_id,
                    scope=agent.scope,
                    organization_id=agent.organization_id,
                    cached_at=datetime.now(UTC),
                    records=records,
                )
            )
        logger.info(
            "Collected OCCM agents: %d collected, %d failed, %d skipped",
            len(collected),
            len(failed),
            len(skipped),
        )
        return OccmSnapshot(
            cached_at=datetime.now(UTC),
            inventory=inventory,
            agents=tuple(collected),
            failed_agents=tuple(failed),
            skipped_agents=tuple(skipped),
            failed_mappings=tuple(failed_mappings),
            scopes=self._scopes,
        )


def refresh_occm_cache(
    config: Config,
    *,
    db: OccmCacheDB | None = None,
    discovery: ConsoleDiscovery | None = None,
    agent_client_factory: Callable[..., ConsoleAgentClient] | None = None,
    scopes: Sequence[str | None] | None = None,
) -> OccmSnapshot:
    """Collect the Console agents and replace the OCCM cache with the result.

    Args:
        config: The configuration holding the Console accounts.
        db: Database to write to; defaults to ``{config_dir}/.cache/occm_cache.db``.
        discovery: Discovery to use; defaults to ``ConsoleDiscovery(config)``.
        agent_client_factory: Builds an agent client; see :class:`OccmCollector`.
        scopes: Refresh only these Console account scopes; other scopes' cached
            inventory and agents are kept.  ``None`` refreshes every account.

    Raises:
        Exception: A discovery failure propagates; the database is left unchanged.
    """
    from pynetappfoundry.cache.occm_db import OccmCacheDB

    snapshot = OccmCollector(
        config, discovery=discovery, agent_client_factory=agent_client_factory, scopes=scopes
    ).collect()
    if db is not None:
        db.set(snapshot)
    else:
        with OccmCacheDB(config=config) as owned:
            owned.set(snapshot)
    return snapshot
