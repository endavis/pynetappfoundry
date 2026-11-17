"""Collector for the Console agent (OCCM) cache (#1076, ADR-0030).

A library function only: :class:`OccmCollector` runs ``ConsoleDiscovery``, then
for each discovered agent (deduplicated by ``agent_id``) lists the working
environments in :data:`OCCM_CACHED_MAPPINGS` through the agent's typed ops, and
:func:`refresh_occm_cache` stores the result in :class:`OccmCacheDB`.

A discovery failure propagates and the database is left untouched.  A failing
agent is logged and recorded in :attr:`OccmSnapshot.failed_agents`; the other
agents are still collected and the failed agent's earlier rows are kept.

This module imports nothing from ``pynetappfoundry.data``.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

import requests

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.clients.console.auth import ConsoleAuthError

if TYPE_CHECKING:
    from pynetappfoundry.cache.field_mapping import TypeMapping
    from pynetappfoundry.cache.occm_db import OccmCacheDB
    from pynetappfoundry.clients.console.agent import ConsoleAgentClient
    from pynetappfoundry.console.discovery import ConsoleDiscovery, ConsoleInventory
    from pynetappfoundry.core.config import Config

logger = logging.getLogger(__name__)

#: The OCCM mappings the cache holds.  The cloud working environments stay live.
OCCM_CACHED_MAPPINGS: tuple[str, ...] = ("OccmOnpremWorkingEnvironment",)

#: ``mapping.api_endpoint`` -> name of the ``ConsoleAgentOps`` method that lists it.
OCCM_LIST_OPS: dict[str, str] = {
    "/occm/api/onprem/working-environments": "list_onprem_working_environments",
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
    """

    cached_at: datetime
    inventory: ConsoleInventory
    agents: tuple[OccmAgentSnapshot, ...] = ()
    failed_agents: tuple[str, ...] = field(default=())


class OccmCollector:
    """Discover the Console agents and list the cached mappings on each.

    Args:
        config: The configuration holding the Console accounts.
        discovery: Discovery to use; defaults to ``ConsoleDiscovery(config)``.
        agent_client_factory: Builds an agent client, called as
            ``factory(config, agent_id)`` or ``factory(config, agent_id, scope=scope)``
            for a scoped agent.  Defaults to ``ConsoleAgentClient``.
        mappings: Names of the mappings to collect.
    """

    def __init__(
        self,
        config: Config,
        *,
        discovery: ConsoleDiscovery | None = None,
        agent_client_factory: Callable[..., ConsoleAgentClient] | None = None,
        mappings: Sequence[str] = OCCM_CACHED_MAPPINGS,
    ) -> None:
        self._config = config
        self._discovery = discovery
        self._factory = agent_client_factory
        self._mappings = tuple(mappings)

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

        Raises:
            ValueError: If a mapping name is unknown or has no list op.
            Exception: Any error discovery raises propagates unchanged.
        """
        resolved = self._resolve()
        discovery = self._discovery
        if discovery is None:
            from pynetappfoundry.console.discovery import ConsoleDiscovery

            discovery = ConsoleDiscovery(self._config)
        inventory = discovery.discover()

        collected: list[OccmAgentSnapshot] = []
        failed: list[str] = []
        seen: set[str] = set()
        for agent in inventory.agents():
            if agent.agent_id in seen:
                continue
            seen.add(agent.agent_id)
            try:
                client = self._client(agent.agent_id, agent.scope)
                records: dict[str, list[dict[str, Any]]] = {}
                for mapping, op_name in resolved:
                    items = getattr(client.ops, op_name)(fields="*")
                    records[mapping.name] = [item.model_dump(mode="json") for item in items]
            except (requests.RequestException, ConsoleAuthError, TypeError, ValueError) as exc:
                logger.warning("OCCM agent %s: collection failed: %s", agent.agent_id, exc)
                failed.append(agent.agent_id)
                continue
            collected.append(
                OccmAgentSnapshot(
                    agent_id=agent.agent_id,
                    scope=agent.scope,
                    organization_id=agent.organization_id,
                    cached_at=datetime.now(UTC),
                    records=records,
                )
            )
        logger.info("Collected OCCM agents: %d collected, %d failed", len(collected), len(failed))
        return OccmSnapshot(
            cached_at=datetime.now(UTC),
            inventory=inventory,
            agents=tuple(collected),
            failed_agents=tuple(failed),
        )


def refresh_occm_cache(
    config: Config,
    *,
    db: OccmCacheDB | None = None,
    discovery: ConsoleDiscovery | None = None,
    agent_client_factory: Callable[..., ConsoleAgentClient] | None = None,
) -> OccmSnapshot:
    """Collect the Console agents and replace the OCCM cache with the result.

    Args:
        config: The configuration holding the Console accounts.
        db: Database to write to; defaults to ``{config_dir}/.cache/occm_cache.db``.
        discovery: Discovery to use; defaults to ``ConsoleDiscovery(config)``.
        agent_client_factory: Builds an agent client; see :class:`OccmCollector`.

    Raises:
        Exception: A discovery failure propagates; the database is left unchanged.
    """
    from pynetappfoundry.cache.occm_db import OccmCacheDB

    snapshot = OccmCollector(
        config, discovery=discovery, agent_client_factory=agent_client_factory
    ).collect()
    if db is not None:
        db.set(snapshot)
    else:
        with OccmCacheDB(config=config) as owned:
            owned.set(snapshot)
    return snapshot
