"""Resolve one ONTAP cluster across the ONTAP, AIQUM and OCCM caches (#1097, ADR-0032).

The three caches are keyed differently (cluster name, AIQUM instance, Console agent id plus
working-environment ``publicId``) and nothing joins them.  :class:`ClusterResolver` takes a
cluster name and returns where each cache holds that cluster (:class:`ClusterLocation`), and
reads the cached data of every source with its snapshot age (:class:`ClusterData`).

The module reads only the three cache databases.  It imports nothing from
``pynetappfoundry.data`` or ``pynetappfoundry.clients``, so it cannot make a live call.  Cached
record contents are never logged.

The linking fields live in one table, :data:`LINK_RULES`: a measurement result changes that table
only.  The cluster UUID is authoritative; the name is the fallback for a record without a UUID.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any, Literal, Self

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.aiqum_collector import AIQUM_CACHED_MAPPINGS
from pynetappfoundry.cache.aiqum_db import AiqumCacheDB
from pynetappfoundry.cache.db import ClusterMetadataDB, _validate_cluster_name
from pynetappfoundry.cache.field_mapping import parse_api_record
from pynetappfoundry.cache.occm_collector import OCCM_WORKING_ENVIRONMENT_MAPPINGS
from pynetappfoundry.cache.occm_db import OccmCacheDB

if TYPE_CHECKING:
    from collections.abc import Mapping
    from types import TracebackType

    from pydantic import BaseModel

    from pynetappfoundry.cache._metadata import CachedClusterMetadata
    from pynetappfoundry.core.config import Config

MatchedBy = Literal["uuid", "name"]

_AIQUM_CLUSTER = "AiqumCluster"
_AIQUM_CHILDREN: tuple[str, ...] = tuple(m for m in AIQUM_CACHED_MAPPINGS if m != _AIQUM_CLUSTER)
_ON_PREM = "OccmOnpremWorkingEnvironment"


@dataclass(frozen=True)
class LinkRule:
    """The fields that link one cached record type to an ONTAP cluster.

    Attributes:
        uuid_paths: Dotted record paths tried in order; the first non-empty value is the
            record's cluster UUID.
        name_paths: Dotted record paths of the cluster name, the fallback; matched exactly and
            case-sensitively.
    """

    uuid_paths: tuple[str, ...]
    name_paths: tuple[str, ...]


_CLOUD_RULE = LinkRule(
    uuid_paths=("ontapClusterProperties.clusterUuid",),
    name_paths=("ontapClusterProperties.clusterName", "clusterProperties.clusterName"),
)

#: The linking rule of every cached record type that carries a cluster identity.
LINK_RULES: Mapping[str, LinkRule] = {
    _AIQUM_CLUSTER: LinkRule(uuid_paths=("uuid",), name_paths=("name",)),
    _ON_PREM: LinkRule(
        uuid_paths=("ontapClusterProperties.clusterUuid", "clusterProperties.clusterUuid"),
        name_paths=("ontapClusterProperties.clusterName", "clusterProperties.clusterName"),
    ),
    **{m: _CLOUD_RULE for m in OCCM_WORKING_ENVIRONMENT_MAPPINGS if m != _ON_PREM},
}


@dataclass(frozen=True)
class OntapLocation:
    """Where the ONTAP cache holds the cluster.

    Attributes:
        cluster_name: The cache key (the inventory cluster name).
        cluster_uuid: The cluster UUID, or ``None`` when the cache has none.
        ontap_cluster_name: The cluster's own name, which can differ from the key.
    """

    cluster_name: str
    cluster_uuid: str | None
    ontap_cluster_name: str | None


@dataclass(frozen=True)
class AiqumLocation:
    """One AIQUM instance that holds the cluster.

    Attributes:
        instance: The ``[aiqums]`` inventory key.
        cluster_key: The AIQUM cluster key (links the instance's SVMs and volumes).
        cluster_uuid: The cluster UUID AIQUM holds, or ``None``.
        matched_by: Whether the record matched on UUID or on name.
    """

    instance: str
    cluster_key: str
    cluster_uuid: str | None
    matched_by: MatchedBy


@dataclass(frozen=True)
class OccmLocation:
    """One working environment, under one agent, that describes the cluster.

    Attributes:
        agent_id: The Console agent id.
        agent_name: The agent name from the cached discovery, or ``None``.
        scopes: The Console account scopes the agent was discovered in (``None`` is the root).
        mapping: The working-environment mapping name (on-prem or one of the cloud lists).
        public_id: The working environment ``publicId``.
        matched_by: Whether the record matched on UUID or on name.
    """

    agent_id: str
    agent_name: str | None
    scopes: tuple[str | None, ...]
    mapping: str
    public_id: str
    matched_by: MatchedBy


@dataclass(frozen=True)
class ClusterLocation:
    """The per-source keys of one cluster.  An absent source is ``None`` or ``()``.

    Attributes:
        cluster_name: The name that was resolved.
        cluster_uuid: The ONTAP cache's cluster UUID, or ``None`` when unknown.
        ontap: The ONTAP cache entry.
        aiqum: Every AIQUM instance holding the cluster, sorted.
        occm: Every agent and working environment describing the cluster, sorted.
    """

    cluster_name: str
    cluster_uuid: str | None
    ontap: OntapLocation | None
    aiqum: tuple[AiqumLocation, ...]
    occm: tuple[OccmLocation, ...]

    @property
    def found(self) -> bool:
        """Whether any source holds the cluster."""
        return self.ontap is not None or bool(self.aiqum) or bool(self.occm)


@dataclass(frozen=True)
class CachedPart:
    """Common to every cached part: when it was collected and whether it is past the TTL.

    Age never filters: a stale part is still returned.
    """

    cached_at: datetime
    is_stale: bool


@dataclass(frozen=True)
class OntapData(CachedPart):
    """The ONTAP cache's metadata of the cluster (including its CLI-parsed cloud metadata)."""

    location: OntapLocation
    metadata: CachedClusterMetadata


@dataclass(frozen=True)
class AiqumData(CachedPart):
    """One AIQUM instance's cluster record with its own SVMs and volumes."""

    location: AiqumLocation
    cluster: BaseModel
    svms: tuple[BaseModel, ...]
    volumes: tuple[BaseModel, ...]


@dataclass(frozen=True)
class OccmData(CachedPart):
    """One working-environment record, parsed with its generated model."""

    location: OccmLocation
    record: BaseModel


@dataclass(frozen=True)
class ClusterData:
    """The cached data of every source for one cluster.

    Both the ONTAP ``CloudMetadata`` (inside ``ontap.metadata``) and the OCCM cloud records are
    returned; neither is picked (#1086).
    """

    location: ClusterLocation
    ontap: OntapData | None
    aiqum: tuple[AiqumData, ...]
    occm: tuple[OccmData, ...]


def _value_at(record: Mapping[str, Any], path: str) -> str | None:
    """Return the non-empty string at the dotted *path* of *record*, else ``None``."""
    current: Any = record
    for segment in path.split("."):
        if not isinstance(current, dict) or segment not in current:
            return None
        current = current[segment]
    if isinstance(current, str) and current:
        return current
    return None


def _record_uuid(record: Mapping[str, Any], rule: LinkRule) -> str | None:
    """Return the record's cluster UUID: the first non-empty value of the rule's paths."""
    for path in rule.uuid_paths:
        value = _value_at(record, path)
        if value is not None:
            return value
    return None


def _classify(
    record: Mapping[str, Any], rule: LinkRule, uuid: str | None, name: str
) -> MatchedBy | None:
    """Return how *record* matches the cluster, or ``None`` when it does not.

    With the ONTAP *uuid* known, a record that has a UUID matches only on an equal UUID, never
    by name.  A record without a UUID, or any record when *uuid* is unknown, matches by name.
    """
    record_uuid = _record_uuid(record, rule)
    if record_uuid is not None and uuid is not None:
        return "uuid" if record_uuid == uuid else None
    if any(_value_at(record, path) == name for path in rule.name_paths):
        return "name"
    return None


def _candidates(
    rule: LinkRule, uuid: str | None, name: str, query: Any
) -> list[tuple[dict[str, Any], MatchedBy]]:
    """Run *query* for each linking path and return the classified, de-duplicated hits."""
    seen: set[str] = set()
    hits: list[tuple[dict[str, Any], MatchedBy]] = []
    filters: list[dict[str, Any]] = []
    if uuid is not None:
        filters.extend({path: uuid} for path in rule.uuid_paths)
    filters.extend({path: name} for path in rule.name_paths)
    for flt in filters:
        for record in query(flt):
            matched = _classify(record, rule, uuid, name)
            if matched is None:
                continue
            marker = repr(sorted(record.items(), key=lambda kv: kv[0]))
            if marker in seen:
                continue
            seen.add(marker)
            hits.append((record, matched))
    return hits


def _utc(moment: datetime) -> datetime:
    """Return *moment* as timezone-aware UTC (naive values are taken as UTC)."""
    return moment if moment.tzinfo is not None else moment.replace(tzinfo=UTC)


def _is_stale(cached_at: datetime, ttl_days: int) -> bool:
    return datetime.now(UTC) - _utc(cached_at) > timedelta(days=ttl_days)


class ClusterResolver:
    """Resolve and read one cluster across the ONTAP, AIQUM and OCCM caches.

    Any cache may be ``None``: it is then absent from every result.  The resolver does not close
    databases passed in; :meth:`from_config` opens the cache files that already exist and the
    context manager closes those.

    Args:
        ontap_db: The ONTAP cluster-metadata cache.
        aiqum_db: The AIQUM cache.
        occm_db: The OCCM cache.
    """

    def __init__(
        self,
        *,
        ontap_db: ClusterMetadataDB | None = None,
        aiqum_db: AiqumCacheDB | None = None,
        occm_db: OccmCacheDB | None = None,
    ) -> None:
        self._ontap_db = ontap_db
        self._aiqum_db = aiqum_db
        self._occm_db = occm_db
        self._owned: list[ClusterMetadataDB | AiqumCacheDB | OccmCacheDB] = []

    @classmethod
    def from_config(cls, config: Config) -> Self:
        """Open the cache files of *config* that already exist; never create one."""
        ontap_path = ClusterMetadataDB.default_path(config)
        aiqum_path = AiqumCacheDB.default_path(config)
        occm_path = OccmCacheDB.default_path(config)
        ontap_db = ClusterMetadataDB(db_path=ontap_path) if ontap_path.exists() else None
        aiqum_db = AiqumCacheDB(db_path=aiqum_path) if aiqum_path.exists() else None
        occm_db = OccmCacheDB(db_path=occm_path) if occm_path.exists() else None
        resolver = cls(ontap_db=ontap_db, aiqum_db=aiqum_db, occm_db=occm_db)
        resolver._owned = [db for db in (ontap_db, aiqum_db, occm_db) if db is not None]
        return resolver

    def close(self) -> None:
        """Close the databases :meth:`from_config` opened."""
        for db in self._owned:
            db.close()
        self._owned = []

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Resolve
    # ------------------------------------------------------------------

    def resolve(self, cluster_name: str) -> ClusterLocation:
        """Return where each cache holds *cluster_name*.

        A missing cache file, no rows or no match is absent, never an exception.

        Raises:
            ValueError: If *cluster_name* is not a valid cluster name.
        """
        return self._resolve(cluster_name)[0]

    def _resolve(
        self, cluster_name: str
    ) -> tuple[ClusterLocation, CachedClusterMetadata | None, dict[str, list[dict[str, Any]]]]:
        """Resolve and also return the ONTAP metadata and the matched raw records."""
        _validate_cluster_name(cluster_name)
        metadata = self._ontap_db.get(cluster_name) if self._ontap_db is not None else None
        ontap: OntapLocation | None = None
        uuid: str | None = None
        match_name = cluster_name
        if metadata is not None:
            uuid = metadata.cluster.uuid or None
            ontap_name = metadata.cluster.name or None
            ontap = OntapLocation(cluster_name, uuid, ontap_name)
            match_name = ontap_name or cluster_name
        aiqum, aiqum_records = self._resolve_aiqum(uuid, match_name)
        occm, occm_records = self._resolve_occm(uuid, match_name)
        location = ClusterLocation(cluster_name, uuid, ontap, aiqum, occm)
        return location, metadata, {**aiqum_records, **occm_records}

    def _resolve_aiqum(
        self, uuid: str | None, name: str
    ) -> tuple[tuple[AiqumLocation, ...], dict[str, list[dict[str, Any]]]]:
        db = self._aiqum_db
        if db is None:
            return (), {}
        rule = LINK_RULES[_AIQUM_CLUSTER]
        found: list[AiqumLocation] = []
        records: dict[str, list[dict[str, Any]]] = {}
        for instance in db.list_instances():
            for record, matched in _candidates(
                rule, uuid, name, lambda f, i=instance: db.query_records(i, _AIQUM_CLUSTER, f)
            ):
                key = record.get("key")
                if not isinstance(key, str) or not key:
                    continue
                found.append(AiqumLocation(instance, key, _record_uuid(record, rule), matched))
                records[f"aiqum:{instance}:{key}"] = [record]
        return tuple(sorted(found, key=lambda a: (a.instance, a.cluster_key))), records

    def _resolve_occm(
        self, uuid: str | None, name: str
    ) -> tuple[tuple[OccmLocation, ...], dict[str, list[dict[str, Any]]]]:
        db = self._occm_db
        if db is None:
            return (), {}
        names = {a.agent_id: a.name for a in reversed(db.agents())}
        found: list[OccmLocation] = []
        records: dict[str, list[dict[str, Any]]] = {}
        for agent_id in db.list_agents():
            scopes = tuple(db.agent_scopes(agent_id))
            for mapping in OCCM_WORKING_ENVIRONMENT_MAPPINGS:
                rule = LINK_RULES[mapping]
                for record, matched in _candidates(
                    rule,
                    uuid,
                    name,
                    lambda f, a=agent_id, m=mapping: db.query_records(a, m, f),
                ):
                    public_id = record.get("publicId")
                    if not isinstance(public_id, str) or not public_id:
                        continue
                    found.append(
                        OccmLocation(
                            agent_id, names.get(agent_id), scopes, mapping, public_id, matched
                        )
                    )
                    records[f"occm:{agent_id}:{mapping}:{public_id}"] = [record]
        deduped = {(o.agent_id, o.mapping, o.public_id): o for o in found}
        return tuple(
            sorted(deduped.values(), key=lambda o: (o.agent_id, o.mapping, o.public_id))
        ), (records)

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def read(self, cluster_name: str, ttl_days: int = 30) -> ClusterData:
        """Return the cached data of every source for *cluster_name*, with each part's age.

        Staleness is reported on each part (older than *ttl_days*) and never filters.

        Raises:
            ValueError: If *cluster_name* is not a valid cluster name.
        """
        location, metadata, matched = self._resolve(cluster_name)
        ontap: OntapData | None = None
        if location.ontap is not None and metadata is not None:
            ontap = OntapData(
                cached_at=metadata.cached_at,
                is_stale=_is_stale(metadata.cached_at, ttl_days),
                location=location.ontap,
                metadata=metadata,
            )
        aiqum = tuple(self._read_aiqum(loc, matched, ttl_days) for loc in location.aiqum)
        occm = tuple(self._read_occm(loc, matched, ttl_days) for loc in location.occm)
        return ClusterData(location, ontap, aiqum, occm)

    def _read_aiqum(
        self,
        loc: AiqumLocation,
        matched: dict[str, list[dict[str, Any]]],
        ttl_days: int,
    ) -> AiqumData:
        db = self._aiqum_db
        assert db is not None  # a location only exists when the cache is open
        cluster = self._parse(_AIQUM_CLUSTER, matched[f"aiqum:{loc.instance}:{loc.cluster_key}"][0])
        children: dict[str, tuple[BaseModel, ...]] = {}
        for mapping_name in _AIQUM_CHILDREN:
            rows = db.query_records(loc.instance, mapping_name, {"cluster.key": loc.cluster_key})
            children[mapping_name] = tuple(self._parse(mapping_name, row) for row in rows)
        collected = [
            datetime.fromisoformat(c["cached_at"])
            for c in db.list_collections(loc.instance)
            if c["mapping"] in AIQUM_CACHED_MAPPINGS
        ]
        cached_at = min(collected) if collected else datetime.now(UTC)
        return AiqumData(
            cached_at=cached_at,
            is_stale=_is_stale(cached_at, ttl_days),
            location=loc,
            cluster=cluster,
            svms=children.get("AiqumSvm", ()),
            volumes=children.get("AiqumVolume", ()),
        )

    def _read_occm(
        self,
        loc: OccmLocation,
        matched: dict[str, list[dict[str, Any]]],
        ttl_days: int,
    ) -> OccmData:
        db = self._occm_db
        assert db is not None  # a location only exists when the cache is open
        mapping = model_registry.get_mapping(loc.mapping)
        if mapping is None:
            raise LookupError(f"No mapping registered for {loc.mapping}")
        record = mapping.model_class.model_validate(
            matched[f"occm:{loc.agent_id}:{loc.mapping}:{loc.public_id}"][0]
        )
        status = next((s for s in db.agent_status(ttl_days) if s.agent_id == loc.agent_id), None)
        cached_at = status.oldest_cached_at if status is not None else datetime.now(UTC)
        return OccmData(
            cached_at=cached_at,
            is_stale=status.is_stale if status is not None else False,
            location=loc,
            record=record,
        )

    @staticmethod
    def _parse(mapping_name: str, record: dict[str, Any]) -> BaseModel:
        """Parse a raw AIQUM *record* with its registered mapping."""
        mapping = model_registry.get_mapping(mapping_name)
        if mapping is None:
            raise LookupError(f"No mapping registered for {mapping_name}")
        return parse_api_record(mapping, record, f"ClusterResolver<{mapping_name}>")
