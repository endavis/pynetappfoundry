"""Shared JSON serialization helpers for the cache module.

The cache layer persists Pydantic models, diff summaries, and ad-hoc
extra fields to SQLite as JSON strings. Several call sites need to
serialize values that may contain ``pydantic.BaseModel`` instances
that the stdlib ``json`` encoder cannot handle natively. ``json_default``
is a single ``default=`` callable they can share so the behaviour stays
consistent (and lossless) across the cache.
"""

from __future__ import annotations

from pydantic import BaseModel


def json_default(obj: object) -> object:
    """JSON encoder fallback for cache serialization paths.

    Converts ``pydantic.BaseModel`` instances to plain dicts via
    ``model_dump(mode="json")`` so the resulting JSON is lossless and
    round-trippable. Anything else falls back to ``str``.
    """
    if isinstance(obj, BaseModel):
        return obj.model_dump(mode="json")
    return str(obj)
