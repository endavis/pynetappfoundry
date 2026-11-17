"""OCCM (Console agent) backend for the unified DataSource accessor.

Implements :class:`OccmBackend`, a live-only backend that reads the Console agent's
``/occm/api`` through the typed ops on
:class:`pynetappfoundry.clients.console.agent.ConsoleAgentClient` (ADR-0019, ADR-0027).
It is a thin delegator: each mapping endpoint maps to one ``ConsoleAgentOps`` method
(:data:`_OPS`) that returns validated model instances.

The agent has no server-side filtering this backend relies on, so equality filters are
applied in memory on dotted paths.  Fields the agent returns only on request
(``requires_explicit_fetch``) are sent as a ``fields=`` CSV.
"""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import BaseModel

from pynetappfoundry.data.backends import Backend
from pynetappfoundry.utils.dict_path import PathNotFoundError, get_nested_value

if TYPE_CHECKING:
    from pynetappfoundry.cache.field_mapping import TypeMapping
    from pynetappfoundry.clients.console.agent import ConsoleAgentClient
    from pynetappfoundry.core.config import Config
    from pynetappfoundry.data._routing import RoutingDecision

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

# ``mapping.api_endpoint`` -> name of the ``ConsoleAgentOps`` method that lists it.
_OPS: dict[str, str] = {
    "/occm/api/onprem/working-environments": "list_onprem_working_environments",
}

_TOP_LEVEL_SPLIT = re.compile(r"[.\[]")


def _top_level(key: str) -> str:
    """Return the first path segment of a dotted filter *key*."""
    return _TOP_LEVEL_SPLIT.split(key, maxsplit=1)[0]


class OccmBackend(Backend):
    """Live-only backend that reads a Console agent through its typed ops.

    ``cluster`` names the agent: a key of ``[connectors]`` resolves to that entry's
    ``agent_id``; any other value is used as the agent id itself.  Clients are created
    lazily and cached per agent id.

    ``where_expressions``, ``path_params`` and ``parent_filters`` are not supported.

    Args:
        config: The :class:`pynetappfoundry.core.config.Config` instance.
    """

    supports_where_expressions: bool = False
    supports_path_params: bool = False
    supports_parent_filters: bool = False
    # No cache: auto routing goes live, source="cache" is rejected.
    live_only: bool = True

    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self._api_clients: dict[tuple[str | None, str], ConsoleAgentClient] = {}

    def _resolve_agent_id(self, cluster: str) -> str:
        """Return the agent id for *cluster* (a ``[connectors]`` name or an agent id).

        Raises:
            ValueError: If *cluster* is a connector without a non-blank ``agent_id``.
        """
        connectors = self._config.data.get("connectors", {})
        if isinstance(connectors, dict) and cluster in connectors:
            entry = connectors[cluster]
            agent_id = entry.get("agent_id") if isinstance(entry, dict) else None
            if not isinstance(agent_id, str) or not agent_id.strip():
                msg = (
                    f"connectors.{cluster} has no 'agent_id'; set it to the Console "
                    "agent id to query this agent"
                )
                raise ValueError(msg)
            return agent_id
        return cluster

    def _resolve_scope(self, cluster: str) -> str | None:
        """Return the config scope of a ``[connectors]`` entry, else None.

        A raw agent id, or a connector outside any scope, uses the root Console account.
        """
        connectors = self._config.data.get("connectors", {})
        if not (isinstance(connectors, dict) and cluster in connectors):
            return None
        scope = self._config.get_scope("connectors", cluster)
        return scope if isinstance(scope, str) else None

    def _get_api_client(self, agent_id: str, scope: str | None = None) -> ConsoleAgentClient:
        """Lazily create a :class:`ConsoleAgentClient`, cached per scope and *agent_id*.

        A scoped client uses that scope's Console account; ``scope=None`` the root one.
        """
        key = (scope, agent_id)
        if key not in self._api_clients:
            from pynetappfoundry.clients.console.agent import ConsoleAgentClient

            if scope is None:
                self._api_clients[key] = ConsoleAgentClient(self._config, agent_id)
            else:
                self._api_clients[key] = ConsoleAgentClient(self._config, agent_id, scope=scope)
        return self._api_clients[key]

    @staticmethod
    def _fields_param(
        mapping: TypeMapping, decision: RoutingDecision, filters: dict[str, Any]
    ) -> str:
        """Return the ``fields=`` CSV: the explicit-fetch fields the call needs, or ``""``."""
        wanted = set(decision.live_fields) | {_top_level(key) for key in filters}
        return ",".join(f for f in mapping.explicit_fetch_fields() if f in wanted)

    @staticmethod
    def _matches(item: BaseModel, filters: dict[str, Any]) -> bool:
        """Return whether every equality filter matches *item* (missing path: no match)."""
        dumped = item.model_dump()
        for key, expected in filters.items():
            try:
                actual = get_nested_value(dumped, key)
            except PathNotFoundError:
                return False
            if actual != expected:
                return False
        return True

    def query(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        decision: RoutingDecision,
        cluster: str,
        filters: dict[str, Any],
        *,
        where_expressions: tuple[str, ...] = (),
        path_params: dict[str, Any] | None = None,
    ) -> list[T]:
        """List the agent's records for *mapping* and filter them in memory.

        Raises:
            NotImplementedError: For a cache-only decision, ``where_expressions``, or
                an endpoint with no entry in :data:`_OPS`.
            ValueError: For non-empty ``path_params``, or an unresolvable connector.
            TypeError: If the op returns an item that is not a *model_class*.
        """
        if decision.cache_fields and not decision.live_fields:
            msg = "OCCM backend does not support cache-only queries"
            raise NotImplementedError(msg)
        if where_expressions:
            msg = "OCCM backend does not support where_expressions"
            raise NotImplementedError(msg)
        if path_params:
            msg = f"{mapping.name}: OCCM backend does not support path_params"
            raise ValueError(msg)
        if not decision.live_fields:
            return []

        op_name = _OPS.get(mapping.api_endpoint)
        if op_name is None:
            msg = f"OCCM backend has no op for endpoint {mapping.api_endpoint}"
            raise NotImplementedError(msg)

        scope = self._resolve_scope(cluster)
        agent_id = self._resolve_agent_id(cluster)
        client = (
            self._get_api_client(agent_id)
            if scope is None
            else self._get_api_client(agent_id, scope)
        )
        fields = self._fields_param(mapping, decision, filters)
        kwargs: dict[str, Any] = {"fields": fields} if fields else {}
        items = getattr(client.ops, op_name)(**kwargs)

        results: list[T] = []
        for item in items:
            if not isinstance(item, model_class):
                msg = (
                    f"{mapping.name}: op {op_name} returned {type(item).__name__}, "
                    f"expected {model_class.__name__}"
                )
                raise TypeError(msg)
            if not self._matches(item, filters):
                continue
            fetched = getattr(item, "_fetched_fields", None)
            if fetched is not None:
                fetched.update(decision.live_fields)
            results.append(item)
        return results
