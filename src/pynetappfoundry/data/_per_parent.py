"""Per-parent fetch loop shared by the live-only DII and AIQUM backends.

A mapping whose endpoint has ``{placeholder}`` path segments and a
``parent_mapping`` is fetched once per parent object (#985, #1057).  The
backend supplies two callables -- one that queries the parent mapping and one
that fetches a single child request -- and this module owns the rest: chain
validation, the parent registry lookup, the id-count check, the optional
request cap, and the skip/log behaviour.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.fetchers import iter_parent_ids, validate_parent_chain
from pynetappfoundry.data._path_params import caller_path_params
from pynetappfoundry.data._routing import RoutingDecision

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from pydantic import BaseModel

    from pynetappfoundry.cache.field_mapping import TypeMapping

logger = logging.getLogger(__name__)


def fetch_per_parent(
    mapping: TypeMapping,
    placeholders: list[str],
    *,
    query_parents: Callable[[TypeMapping, RoutingDecision], Sequence[BaseModel]],
    fetch_child: Callable[[dict[str, str]], list[Any]],
    log_prefix: str,
    encode: bool = False,
    max_parents: int | None = None,
) -> list[Any]:
    """Fetch *mapping* once per parent and return the concatenated raw records.

    The parent chain is validated and the parent mapping looked up before any
    request.  *query_parents* receives the parent mapping and a live
    :class:`RoutingDecision` covering all its fields.  Each usable parent
    (``SKIP_PARENT`` is logged for one without an identifier) fills the
    placeholders; *fetch_child* is called with that ``path_params`` dict.
    With *encode*, the values are validated and percent-encoded first, inside
    the guarded block, so an unusable value is skipped like a failed request.

    A parent whose child request fails is logged as ``CHILD_FETCH_FAILED`` and
    skipped.  A positive *max_parents* smaller than the number of usable
    parents raises :class:`ValueError` before any child request; ``None`` or
    ``0`` means unlimited.
    """
    validate_parent_chain(mapping)
    parent_map = model_registry.get_mapping(mapping.parent_mapping or "")
    if parent_map is None:  # pragma: no cover - guarded by validate_parent_chain
        msg = f"{mapping.name}: parent mapping {mapping.parent_mapping!r} is not registered"
        raise ValueError(msg)
    if len(mapping.effective_parent_id_fields()) != len(placeholders):
        msg = (
            f"{mapping.name}: {len(mapping.effective_parent_id_fields())} parent id "
            f"field(s) for {len(placeholders)} placeholder(s) in {mapping.api_endpoint}"
        )
        raise ValueError(msg)

    parent_decision = RoutingDecision(
        cache_fields=(), live_fields=tuple(f.cache_attr for f in parent_map.fields)
    )
    parents = query_parents(parent_map, parent_decision)
    usable = list(iter_parent_ids(mapping, parents, log_prefix))
    if max_parents and len(usable) > max_parents:
        msg = (
            f"{mapping.name}: {len(usable)} parent objects exceed max_parent_requests="
            f"{max_parents}; pass path_params to fetch one parent, or raise "
            "max_parent_requests (0 = unlimited)"
        )
        raise ValueError(msg)

    results: list[Any] = []
    for parent, values in usable:
        try:
            path_params = dict(zip(placeholders, values, strict=True))
            if encode:
                path_params = caller_path_params(mapping, placeholders, path_params)
            results.extend(fetch_child(path_params))
        except Exception as e:
            logger.warning(
                "%s CHILD_FETCH_FAILED: %s for parent %s - %s: %s",
                log_prefix,
                mapping.name,
                getattr(parent, "name", repr(parent)),
                type(e).__name__,
                e,
            )
            continue
    return results
