"""SQLite cache for the Console agent (OCCM) inventory (#1076, ADR-0030).

A separate database file (``occm_cache.db``) from the ONTAP cache and the AIQUM
cache.  It holds three tables:

* ``occm_collections``: one row per ``(agent_id, mapping)`` with its ``cached_at``;
* ``occm_records``: the raw JSON records each agent returned, keyed by
  ``agent_id`` and the mapping's identifier (``record_key``);
* ``occm_inventory``: what ``ConsoleDiscovery`` found (organizations, agents and
  working environments), replaced on every :meth:`OccmCacheDB.set`.

The working environment -> agent mapping is derived from the records: the agents
whose list contains a working environment's ``publicId`` are the agents that
manage it.  Equality filters become ``json_extract(record, ?) = ?`` with both the
path and the value bound, so no caller text reaches the SQL string.  Indexed
``json_extract`` paths are not supported.  The ONTAP cache and its
``SCHEMA_VERSION`` are untouched (ADR-0018 scope paragraph).
"""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from pynetappfoundry.cache._json_records import json_path
from pynetappfoundry.db.base import SQLiteDB
from pynetappfoundry.models.console_types import (
    ConsoleAgentInfo,
    ConsoleWorkingEnvironment,
    Organization,
)

if TYPE_CHECKING:
    from pynetappfoundry.cache.occm_collector import OccmSnapshot
    from pynetappfoundry.core.config import Config

_COLLECTIONS = "occm_collections"
_RECORDS = "occm_records"
_INVENTORY = "occm_inventory"

#: The mapping whose records define the working environment -> agent mapping.
_WORKING_ENVIRONMENT_MAPPING = "OccmOnpremWorkingEnvironment"

_ORGANIZATION = "organization"
_AGENT = "agent"
_WORKING_ENVIRONMENT = "working_environment"


class OccmCacheDB(SQLiteDB):
    """SQLite database holding collected Console agent data, keyed by agent id.

    Args:
        db_path: Direct path to the database file, ``":memory:"`` or a
            ``file:`` URI.
        config: Configuration whose ``config_dir`` holds
            ``.cache/occm_cache.db`` when *db_path* is not given.

    Raises:
        ValueError: If neither *db_path* nor *config* is provided.
    """

    SCHEMA_VERSION: ClassVar[int] = 1

    def __init__(
        self,
        db_path: Path | str | None = None,
        config: Config | None = None,
    ) -> None:
        if db_path:
            self.db_path: Path | str = db_path
        elif config:
            cache_dir = config.config_dir / ".cache"
            cache_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = cache_dir / "occm_cache.db"
        else:
            raise ValueError("Either db_path or config must be provided")

        is_uri = isinstance(self.db_path, str) and self.db_path.startswith("file:")
        self.conn = sqlite3.connect(self.db_path, uri=is_uri)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _create_schema(self) -> None:
        """Create the collection, record and inventory tables."""
        self.conn.execute(f"""
            CREATE TABLE {_COLLECTIONS} (
                agent_id TEXT NOT NULL,
                mapping TEXT NOT NULL,
                scope TEXT,
                organization_id TEXT,
                cached_at TEXT NOT NULL,
                PRIMARY KEY (agent_id, mapping)
            )
        """)
        self.conn.execute(f"""
            CREATE TABLE {_RECORDS} (
                _row_id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                mapping TEXT NOT NULL,
                record_key TEXT,
                record TEXT NOT NULL
            )
        """)
        self.conn.execute(f"""
            CREATE TABLE {_INVENTORY} (
                _row_id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL,
                scope TEXT,
                organization_id TEXT,
                object_id TEXT NOT NULL,
                record TEXT NOT NULL,
                cached_at TEXT NOT NULL
            )
        """)
        self.conn.execute(f"CREATE INDEX idx_occm_records_map ON {_RECORDS}(agent_id, mapping)")
        self.conn.execute(f"CREATE INDEX idx_occm_records_key ON {_RECORDS}(mapping, record_key)")

    def set(self, snapshot: OccmSnapshot) -> None:
        """Store *snapshot* in one transaction.

        The inventory is replaced.  Each collected agent's records are replaced.
        Agents no longer discovered are pruned; a failed or skipped agent keeps
        its rows.
        """
        from pynetappfoundry.cache._registry import model_registry

        cached_at = snapshot.cached_at.isoformat()
        discovered = (
            {a.agent_id for a in snapshot.agents}
            | set(snapshot.failed_agents)
            | set(snapshot.skipped_agents)
        )
        with self.conn:
            self.conn.execute(f"DELETE FROM {_INVENTORY}")
            rows: list[tuple[str, str | None, str | None, str, str, str]] = []
            for account in snapshot.inventory.accounts:
                for org in account.organizations:
                    rows.append(
                        (
                            _ORGANIZATION,
                            account.scope,
                            org.id,
                            org.id,
                            json.dumps(org.model_dump(mode="json", by_alias=False)),
                            cached_at,
                        )
                    )
                for agent in account.agents:
                    rows.append(
                        (
                            _AGENT,
                            account.scope,
                            agent.organization_id,
                            agent.agent_id,
                            json.dumps(agent.model_dump(mode="json", by_alias=False)),
                            cached_at,
                        )
                    )
                for env in account.working_environments:
                    rows.append(
                        (
                            _WORKING_ENVIRONMENT,
                            account.scope,
                            env.organization_id,
                            env.id,
                            json.dumps(env.model_dump(mode="json", by_alias=False)),
                            cached_at,
                        )
                    )
            self.conn.executemany(
                f"INSERT INTO {_INVENTORY} "
                "(kind, scope, organization_id, object_id, record, cached_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                rows,
            )

            for stored in self.list_agents():
                if stored not in discovered:
                    self._delete_agent(stored)

            for agent_snapshot in snapshot.agents:
                agent_cached_at = agent_snapshot.cached_at.isoformat()
                for mapping_name, records in agent_snapshot.records.items():
                    mapping = model_registry.get_mapping(mapping_name)
                    identifier = mapping.identifier_field if mapping else None
                    self.conn.execute(
                        f"DELETE FROM {_RECORDS} WHERE agent_id = ? AND mapping = ?",
                        (agent_snapshot.agent_id, mapping_name),
                    )
                    self.conn.executemany(
                        f"INSERT INTO {_RECORDS} (agent_id, mapping, record_key, record) "
                        "VALUES (?, ?, ?, ?)",
                        [
                            (
                                agent_snapshot.agent_id,
                                mapping_name,
                                _record_key(rec, identifier),
                                json.dumps(rec, default=str),
                            )
                            for rec in records
                        ],
                    )
                    self.conn.execute(
                        f"INSERT INTO {_COLLECTIONS} "
                        "(agent_id, mapping, scope, organization_id, cached_at) "
                        "VALUES (?, ?, ?, ?, ?) "
                        "ON CONFLICT(agent_id, mapping) DO UPDATE SET "
                        "scope = excluded.scope, organization_id = excluded.organization_id, "
                        "cached_at = excluded.cached_at",
                        (
                            agent_snapshot.agent_id,
                            mapping_name,
                            agent_snapshot.scope,
                            agent_snapshot.organization_id,
                            agent_cached_at,
                        ),
                    )

    def _delete_agent(self, agent_id: str) -> int:
        """Delete one agent's records and collection rows; return the records removed."""
        cursor = self.conn.execute(f"DELETE FROM {_RECORDS} WHERE agent_id = ?", (agent_id,))
        self.conn.execute(f"DELETE FROM {_COLLECTIONS} WHERE agent_id = ?", (agent_id,))
        return cursor.rowcount

    def query_records(
        self, agent_id: str, mapping: str, filters: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Return the stored records of *mapping* on *agent_id* matching *filters*.

        Each filter is an exact match on a dotted JSON path.  ``None`` matches a
        null or missing value and a bool is compared as an int.

        Raises:
            ValueError: If a filter value is a list or dict.
        """
        sql = f"SELECT record FROM {_RECORDS} WHERE agent_id = ? AND mapping = ?"
        params: list[Any] = [agent_id, mapping]
        for key, value in filters.items():
            if isinstance(value, (list, dict, tuple, set)):
                raise ValueError(
                    f"Cache filter {key!r}: value must be a scalar, got {type(value).__name__}"
                )
            path = json_path(key)
            if path is None:
                return []
            if value is None:
                sql += " AND json_extract(record, ?) IS NULL"
                params.append(path)
            else:
                sql += " AND json_extract(record, ?) = ?"
                params.extend([path, int(value) if isinstance(value, bool) else value])
        sql += " ORDER BY _row_id"
        return [json.loads(row["record"]) for row in self.conn.execute(sql, params)]

    def agents_for_working_environment(self, public_id: str) -> list[str]:
        """Return the sorted ids of the agents whose list holds *public_id*."""
        rows = self.conn.execute(
            f"SELECT DISTINCT agent_id FROM {_RECORDS} "
            "WHERE mapping = ? AND record_key = ? ORDER BY agent_id",
            (_WORKING_ENVIRONMENT_MAPPING, public_id),
        )
        return [str(row["agent_id"]) for row in rows]

    def working_environment_agents(self) -> dict[str, list[str]]:
        """Return every working environment ``publicId`` mapped to its sorted agent ids."""
        rows = self.conn.execute(
            f"SELECT DISTINCT record_key, agent_id FROM {_RECORDS} "
            "WHERE mapping = ? AND record_key IS NOT NULL ORDER BY record_key, agent_id",
            (_WORKING_ENVIRONMENT_MAPPING,),
        )
        result: dict[str, list[str]] = {}
        for row in rows:
            result.setdefault(str(row["record_key"]), []).append(str(row["agent_id"]))
        return result

    def _inventory_records(self, kind: str) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            f"SELECT record FROM {_INVENTORY} WHERE kind = ? ORDER BY _row_id", (kind,)
        )
        return [json.loads(row["record"]) for row in rows]

    def organizations(self) -> list[Organization]:
        """Return the cached organizations."""
        return [Organization.model_validate(r) for r in self._inventory_records(_ORGANIZATION)]

    def agents(self) -> list[ConsoleAgentInfo]:
        """Return the cached agents."""
        return [ConsoleAgentInfo.model_validate(r) for r in self._inventory_records(_AGENT)]

    def working_environments(self) -> list[ConsoleWorkingEnvironment]:
        """Return the cached working environments."""
        return [
            ConsoleWorkingEnvironment.model_validate(r)
            for r in self._inventory_records(_WORKING_ENVIRONMENT)
        ]

    def clear(self, agent_id: str | None = None) -> int:
        """Delete one agent's rows, or everything (inventory too) when *agent_id* is ``None``.

        Returns:
            The number of record rows deleted.
        """
        with self.conn:
            if agent_id is None:
                cursor = self.conn.execute(f"DELETE FROM {_RECORDS}")
                self.conn.execute(f"DELETE FROM {_COLLECTIONS}")
                self.conn.execute(f"DELETE FROM {_INVENTORY}")
                return cursor.rowcount
            return self._delete_agent(agent_id)

    def list_agents(self) -> list[str]:
        """Return the sorted ids of the agents with a collected snapshot."""
        rows = self.conn.execute(f"SELECT DISTINCT agent_id FROM {_COLLECTIONS} ORDER BY agent_id")
        return [str(row["agent_id"]) for row in rows]

    def is_collected(self, agent_id: str, mapping: str) -> bool:
        """Return whether *mapping* has been collected for *agent_id*."""
        row = self.conn.execute(
            f"SELECT 1 FROM {_COLLECTIONS} WHERE agent_id = ? AND mapping = ?",
            (agent_id, mapping),
        ).fetchone()
        return row is not None

    def is_stale(self, agent_id: str, ttl_days: int = 30) -> bool | None:
        """Return whether *agent_id*'s oldest collection is older than *ttl_days*.

        Returns ``None`` when nothing was collected for *agent_id*.  Age never
        affects routing; this only reports it (ADR-0026).
        """
        row = self.conn.execute(
            f"SELECT MIN(cached_at) AS oldest FROM {_COLLECTIONS} WHERE agent_id = ?",
            (agent_id,),
        ).fetchone()
        if row is None or row["oldest"] is None:
            return None
        oldest = datetime.fromisoformat(row["oldest"])
        return datetime.now(UTC) - oldest > timedelta(days=ttl_days)


def _record_key(record: dict[str, Any], identifier: Any) -> str | None:
    """Return the string key of *record* under the mapping's *identifier* field."""
    if not isinstance(identifier, str):
        return None
    value = record.get(identifier)
    return None if value is None else str(value)
