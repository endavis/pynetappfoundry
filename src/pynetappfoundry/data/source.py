"""Top-level :class:`DataSource` accessor and :class:`QueryBuilder`.

The unified entry point for fetching model instances regardless of
whether they live in the cache, the live REST API, or both.

See ADR-0012 for the design rationale; this module is the Phase 2
spike implementation against ``OntapVolume``.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.data._routing import SourceMode, decide_path
from pynetappfoundry.data.backends import Backend, OntapBackend

if TYPE_CHECKING:
    from collections.abc import Iterator

    from pynetappfoundry.cache.field_mapping import TypeMapping
    from pynetappfoundry.core.config import Config

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


# Backend registry: maps TypeMapping.api_type → Backend subclass.
# Phase 2 ships only with the ONTAP backend; future phases register
# AIQUM, OCCM, DII, etc., here.
_BACKENDS: dict[str, type[Backend]] = {
    "ontap": OntapBackend,
}


def _field_strategy(mapping: TypeMapping, cache_attr: str) -> str | None:
    """Return the ``cache_strategy`` for *cache_attr*, or ``None`` if unknown."""
    for f in mapping.fields:
        if f.cache_attr == cache_attr:
            return f.cache_strategy
    return None


class DataSource:
    """Unified accessor for model instances across cache and live API.

    Holds a :class:`Config` instance and lazily instantiates one
    :class:`Backend` per :attr:`TypeMapping.api_type`. Backends are
    cached for the lifetime of the ``DataSource``.

    Example::

        ds = DataSource(config)
        vol = ds.get(OntapVolume, cluster="prod1", id="abc-123")
        vols = list(ds.query(OntapVolume, cluster="prod1").filter({"svm.name": "vs1"}))

    Args:
        config: Configuration object passed through to backends.
    """

    def __init__(self, config: Config) -> None:
        self._config = config
        self._backends: dict[str, Backend] = {}

    def _get_backend(self, api_type: str) -> Backend:
        """Lazily instantiate the backend for *api_type*."""
        if api_type not in self._backends:
            backend_cls = _BACKENDS.get(api_type)
            if backend_cls is None:
                msg = (
                    f"No backend registered for api_type {api_type!r}. "
                    f"Known backends: {sorted(_BACKENDS.keys())}"
                )
                raise ValueError(msg)
            self._backends[api_type] = backend_cls(self._config)
        return self._backends[api_type]

    @staticmethod
    def _resolve_mapping(model_class: type[T]) -> TypeMapping:
        mapping = model_registry.get_mapping(model_class.__name__)
        if mapping is None:
            msg = (
                f"No TypeMapping registered for {model_class.__name__!r}. "
                f"Ensure the model's mapping module has been imported."
            )
            raise ValueError(msg)
        return mapping

    @staticmethod
    def _normalize_identifier(
        mapping: TypeMapping, id_value: str | dict[str, Any]
    ) -> dict[str, Any]:
        """Normalize *id_value* against ``mapping.identifier_field``.

        Returns a dict suitable for passing to ``Backend.get()``.

        Raises:
            ValueError: If the mapping has no identifier_field declared,
                or if *id_value* doesn't match the declared shape.
        """
        identifier_field = mapping.identifier_field
        if identifier_field is None:
            msg = (
                f"Model {mapping.name!r} has no identifier_field declared in "
                f"its TypeMapping; use query() or add identifier_field to the "
                f"mapping."
            )
            raise ValueError(msg)

        if isinstance(identifier_field, str):
            if isinstance(id_value, str):
                return {identifier_field: id_value}
            # id_value is a dict here per the public type signature.
            if identifier_field not in id_value:
                msg = (
                    f"id dict for {mapping.name!r} must contain "
                    f"{identifier_field!r}; got keys {sorted(id_value.keys())}"
                )
                raise ValueError(msg)
            return {identifier_field: id_value[identifier_field]}

        # Composite key (tuple)
        if isinstance(id_value, str):
            msg = (
                f"Model {mapping.name!r} has a composite identifier "
                f"{identifier_field!r}; pass id= as a dict, not a str."
            )
            raise ValueError(msg)
        missing = [k for k in identifier_field if k not in id_value]
        if missing:
            msg = (
                f"id dict for {mapping.name!r} is missing required key(s) "
                f"{missing}; required: {list(identifier_field)}"
            )
            raise ValueError(msg)
        return {k: id_value[k] for k in identifier_field}

    def get(
        self,
        model_class: type[T],
        *,
        cluster: str,
        id: str | dict[str, Any],
        source: SourceMode = "auto",
        fields: list[str] | None = None,
    ) -> T | None:
        """Fetch one instance of *model_class* by identifier.

        Internally this is a thin wrapper over
        ``self.query(model_class, cluster=cluster, source=source)
        .filter({identifier_field: id}).first()``. Cache-miss fallback
        behavior is inherited from the shared query-iteration path.

        Args:
            model_class: The Pydantic model class to fetch.
            cluster: Name of the cluster to fetch from.
            id: The identifier value (string for single-key models, dict
                for composite-key models).
            source: Per-call routing override (``"auto"``, ``"cache"``,
                or ``"live"``).
            fields: Optional list of ``cache_attr`` paths to populate.
                ``None`` means use the default field set.

        Returns:
            A populated model instance, or ``None`` if no match exists.
        """
        mapping = self._resolve_mapping(model_class)
        identifier = self._normalize_identifier(mapping, id)
        qb = self.query(model_class, cluster=cluster, source=source).filter(identifier)
        if fields is not None:
            qb = qb.fields(*fields)
        return qb.first()

    def query(
        self,
        model_class: type[T],
        *,
        cluster: str,
        source: SourceMode = "auto",
    ) -> QueryBuilder[T]:
        """Build a query for instances of *model_class*.

        Returns a :class:`QueryBuilder` that supports ``.filter()`` and
        ``.fields()`` chaining; iterating it triggers execution.
        """
        mapping = self._resolve_mapping(model_class)
        return QueryBuilder(
            source=self,
            model_class=model_class,
            mapping=mapping,
            cluster=cluster,
            source_mode=source,
        )


class QueryBuilder[T: BaseModel]:
    """Lazy, chainable query builder returned by :meth:`DataSource.query`.

    Iteration triggers execution. Filters and field projections may be
    chained before iteration.
    """

    def __init__(
        self,
        source: DataSource,
        model_class: type[T],
        mapping: TypeMapping,
        cluster: str,
        source_mode: SourceMode,
    ) -> None:
        self._source = source
        self._model_class = model_class
        self._mapping = mapping
        self._cluster = cluster
        self._source_mode: SourceMode = source_mode
        self._filters: dict[str, Any] = {}
        self._fields: list[str] | None = None
        self._where_expressions: list[str] = []

    def where(self, *expressions: str) -> QueryBuilder[T]:
        """Add SQL-like filter expressions to the query.

        Accepts one or more string expressions (e.g. ``"size > 1000000000"``,
        ``"state != 'offline'"``) that are ANDed together with any equality
        filters added via :meth:`filter`. Multiple ``.where()`` calls
        accumulate; an empty call (``.where()``) is a no-op.

        Expressions are evaluated by the backend's cache substrate
        (:meth:`ClusterMetadataDB.query_with_filters`) and are only
        supported on the cache-only path. Using ``.where()`` with a
        routing decision that requires the live REST API (``source="live"``)
        or a partial-fetch mix (``source="auto"`` when the model has both
        cached and realtime fields) raises :class:`NotImplementedError`
        at iteration time. Use ``source="cache"`` to opt into the
        cache-only path and apply ``.where()`` expressions there.

        Composes freely with :meth:`filter` — the final filter list is
        the dict entries translated to ``key = 'value'`` followed by the
        accumulated where-expressions, in a single ANDed list.

        Args:
            *expressions: One or more filter expression strings to AND
                into the query.

        Returns:
            ``self`` for chaining.
        """
        self._where_expressions.extend(expressions)
        return self

    def filter(
        self,
        filters: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> QueryBuilder[T]:
        """Add filters to the query.

        Accepts a positional dict (canonical -- supports dotted keys
        like ``"svm.name"``) and/or keyword arguments (convenience for
        top-level scalars). On collision, ``kwargs`` win.
        """
        if filters:
            self._filters.update(filters)
        if kwargs:
            self._filters.update(kwargs)
        return self

    def fields(self, *paths: str) -> QueryBuilder[T]:
        """Restrict the query to a subset of fields."""
        self._fields = list(paths)
        return self

    def first(self) -> T | None:
        """Return the first result or ``None`` if the query is empty.

        Iterates at most once over the underlying query results. Cache-miss
        fallback is inherited from :meth:`__iter__`.
        """
        return next(iter(self), None)

    def __iter__(self) -> Iterator[T]:
        """Execute the query and yield results."""
        backend = self._source._get_backend(self._mapping.api_type)
        decision = decide_path(self._mapping, self._fields, self._source_mode)
        results = backend.query(
            self._model_class,
            self._mapping,
            decision,
            self._cluster,
            self._filters,
            where_expressions=tuple(self._where_expressions),
        )
        # Cache-miss fallback: if auto routed to cache and got nothing, try live.
        # Skip if where_expressions are present (cache-only, would raise on live).
        # Pass the cache_fields explicitly so derived fields are excluded
        # (derived fields cannot be fetched live and would raise ValueError).
        if (
            not results
            and self._source_mode == "auto"
            and decision.cache_fields
            and not self._where_expressions
        ):
            live_fields = [
                f for f in decision.cache_fields if _field_strategy(self._mapping, f) != "derived"
            ]
            if live_fields:
                live_decision = decide_path(self._mapping, live_fields, "live")
                results = backend.query(
                    self._model_class,
                    self._mapping,
                    live_decision,
                    self._cluster,
                    self._filters,
                    where_expressions=(),
                )
        return iter(results)
