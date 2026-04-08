"""Model merge helper for the unified DataSource accessor.

Used by :class:`pynetappfoundry.data.backends.OntapBackend` when a
single ``get()`` request requires both a cache fetch and a live fetch
(e.g. cached scalar fields plus a realtime metric). The two resulting
model instances are merged into one with the union of populated
fields.
"""

from __future__ import annotations

from pydantic import BaseModel


def merge_models[T: BaseModel](cached_instance: T, live_instance: T) -> T:
    """Merge two model instances of the same class.

    Live values win on collision (live data is fresher than cache).
    The returned instance has the union of ``_fetched_fields`` from
    both inputs.

    Args:
        cached_instance: Instance produced by the cache backend.
        live_instance: Instance produced by the live API backend.

    Returns:
        A new instance of the same class containing the merged data.

    Raises:
        TypeError: If the two instances are not the same class.
    """
    if type(cached_instance) is not type(live_instance):
        msg = (
            f"Cannot merge model instances of different classes: "
            f"{type(cached_instance).__name__} vs {type(live_instance).__name__}"
        )
        raise TypeError(msg)

    # Only merge fields that were actually set on each instance, so the
    # other side's defaults don't clobber real values. Live wins on
    # collision because live data is fresher than cache.
    cached_data = cached_instance.model_dump(exclude_unset=True)
    live_data = live_instance.model_dump(exclude_unset=True)
    merged_data = {**cached_data, **live_data}

    model_class = type(cached_instance)
    merged = model_class(**merged_data)
    cached_fetched: set[str] = set(getattr(cached_instance, "_fetched_fields", set()))
    live_fetched: set[str] = set(getattr(live_instance, "_fetched_fields", set()))
    union = cached_fetched | live_fetched
    # Pyright can't see _fetched_fields on the generic BaseModel bound, but
    # OntapModel (the only production caller) declares it as a PrivateAttr.
    # Synthetic test models that inherit from OntapModel get it too. Use
    # object.__setattr__ to set it without triggering Pydantic's instance
    # __setattr__ guard, which would otherwise reject the underscore-prefixed
    # attribute on a non-OntapModel subclass.
    if hasattr(merged, "_fetched_fields"):
        object.__setattr__(merged, "_fetched_fields", union)
    return merged
