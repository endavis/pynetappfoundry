"""Routing logic for the unified DataSource accessor.

Pure functions that decide, given a :class:`TypeMapping`, a list of
requested field paths, and a per-call ``source`` mode, which fields
should be served from the cache and which should be fetched live from
the upstream API.

This module has no I/O and no side effects -- it is just a routing
table on top of the :class:`FieldMapping.cache_strategy` /
:class:`FieldMapping.requires_explicit_fetch` metadata.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from pynetappfoundry.cache.field_mapping import TypeMapping

SourceMode = Literal["auto", "cache", "live"]
"""Per-call routing override.

- ``"auto"`` -- the default. Use the cache for cached/derived fields and
  the live API only for fields explicitly named that are realtime or
  ``requires_explicit_fetch``.
- ``"cache"`` -- force every requested field through the cache. Raises
  if any requested field cannot be served from the cache.
- ``"live"`` -- force every requested field through the live API.
  Raises if any requested field is derived (derived fields exist only
  in the cache).
"""


@dataclass(frozen=True)
class RoutingDecision:
    """Result of :func:`decide_path`.

    Attributes:
        cache_fields: Tuple of ``cache_attr`` paths to fetch from the cache.
        live_fields: Tuple of ``cache_attr`` paths to fetch from the live API.
    """

    cache_fields: tuple[str, ...]
    live_fields: tuple[str, ...]

    @property
    def partial(self) -> bool:
        """True if the request requires both a cache and a live fetch."""
        return bool(self.cache_fields) and bool(self.live_fields)


def decide_path(
    mapping: TypeMapping,
    requested_fields: list[str] | None,
    source: SourceMode,
) -> RoutingDecision:
    """Decide which backend path each requested field should take.

    Args:
        mapping: The :class:`TypeMapping` for the model being fetched.
        requested_fields: Optional list of ``cache_attr`` paths the caller
            wants populated. ``None`` means "use the default field set"
            (all non-explicit-fetch cached fields plus derived fields,
            matching today's bulk-collection behavior).
        source: Per-call override -- ``"auto"``, ``"cache"``, or
            ``"live"``.

    Returns:
        A :class:`RoutingDecision` describing how to satisfy the request.

    Raises:
        ValueError: If the request is impossible to satisfy under the
            given ``source`` mode (e.g. ``source="cache"`` asking for a
            realtime field, or ``source="live"`` asking for a derived
            field).
    """
    fields_by_attr = {f.cache_attr: f for f in mapping.fields}

    if requested_fields is None:
        # Default field set: cached (non-explicit-fetch) + derived.
        defaults = [
            f.cache_attr
            for f in mapping.fields
            if (f.cache_strategy == "cache" and not f.requires_explicit_fetch)
            or f.cache_strategy == "derived"
        ]
        requested = defaults
        explicit = False
    else:
        requested = list(requested_fields)
        explicit = True

    cache_fields: list[str] = []
    live_fields: list[str] = []

    if source == "cache":
        for attr in requested:
            field = fields_by_attr.get(attr)
            if field is None or field.cache_strategy == "realtime":
                msg = (
                    f"Cannot serve field {attr!r} from cache: "
                    f"field is realtime-only or unknown to mapping {mapping.name!r}"
                )
                raise ValueError(msg)
            cache_fields.append(attr)
        return RoutingDecision(
            cache_fields=tuple(cache_fields),
            live_fields=(),
        )

    if source == "live":
        for attr in requested:
            field = fields_by_attr.get(attr)
            if field is not None and field.cache_strategy == "derived":
                msg = (
                    f"Cannot fetch field {attr!r} live: "
                    f"derived fields exist only in the cache "
                    f"(mapping {mapping.name!r})"
                )
                raise ValueError(msg)
            live_fields.append(attr)
        return RoutingDecision(
            cache_fields=(),
            live_fields=tuple(live_fields),
        )

    # source == "auto"
    for attr in requested:
        field = fields_by_attr.get(attr)
        if field is None:
            # Unknown attribute: assume it's a top-level scalar served by the
            # cache. The backend will surface a clearer error if it doesn't
            # exist on the model.
            cache_fields.append(attr)
            continue
        strategy = field.cache_strategy
        if strategy == "derived" or (strategy == "cache" and not field.requires_explicit_fetch):
            cache_fields.append(attr)
        elif strategy == "cache" and field.requires_explicit_fetch:
            # Only included if the caller explicitly named it.
            if explicit:
                live_fields.append(attr)
            # Otherwise excluded from both lists.
        elif strategy == "realtime" and explicit:
            # Realtime fields only appear when explicitly requested.
            live_fields.append(attr)

    return RoutingDecision(
        cache_fields=tuple(cache_fields),
        live_fields=tuple(live_fields),
    )
