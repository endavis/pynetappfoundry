"""Base class and utilities for cache models.

Provides CacheModel (auto-registering Pydantic base), HasUUID protocol,
OntapUUID validated type, and schema versioning functions. This module is
Layer 1 of the import hierarchy and MUST NOT import from any cache sub-module.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Annotated, Any, Protocol, runtime_checkable

from pydantic import AfterValidator, BaseModel, ConfigDict

_UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def _validate_ontap_uuid(v: str) -> str:
    """Validate an ONTAP UUID string.

    Allows empty strings (ONTAP returns ``""`` for optional UUID fields).

    Args:
        v: The string value to validate.

    Returns:
        The validated string.

    Raises:
        ValueError: If the string is non-empty and not a valid UUID format.
    """
    if v and not _UUID_PATTERN.match(v):
        raise ValueError(f"Invalid UUID: {v}")
    return v


OntapUUID = Annotated[str, AfterValidator(_validate_ontap_uuid)]
"""Dedicated type for ONTAP UUID fields.

A plain ``str`` at runtime with Pydantic validation that rejects malformed
UUIDs on model construction.  Empty strings are allowed because ONTAP
returns ``""`` for optional UUID fields.
"""


# Schema version for CachedClusterMetadata model.
# Increment MINOR for backward-compatible changes (new optional fields).
# Increment MAJOR for breaking changes (removed/renamed fields, type changes).
# Format: "MAJOR.MINOR"
METADATA_SCHEMA_VERSION = "2.0"

# Minimum schema version that can be loaded without migration.
# Snapshots older than this may fail to deserialize or have missing data.
METADATA_SCHEMA_MIN_COMPATIBLE = "2.0"


def parse_schema_version(version: str) -> tuple[int, int]:
    """Parse a schema version string into (major, minor) tuple.

    Args:
        version: Version string in "MAJOR.MINOR" format.

    Returns:
        Tuple of (major, minor) integers.

    Raises:
        ValueError: If version string is invalid.
    """
    try:
        parts = version.split(".")
        return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid schema version: {version!r}") from e


def is_schema_compatible(snapshot_version: str | None) -> bool:
    """Check if a snapshot schema version is compatible with current code.

    Args:
        snapshot_version: The cache_version from a stored snapshot, or None.

    Returns:
        True if the snapshot can be safely loaded, False otherwise.
    """
    if snapshot_version is None:
        # Very old snapshots without version - assume incompatible
        return False

    try:
        snap_major, snap_minor = parse_schema_version(snapshot_version)
        min_major, min_minor = parse_schema_version(METADATA_SCHEMA_MIN_COMPATIBLE)

        # Compatible if snapshot version >= minimum compatible version
        return (snap_major, snap_minor) >= (min_major, min_minor)
    except ValueError:
        return False


def _utcnow() -> datetime:
    """Get current UTC time as timezone-aware datetime."""
    return datetime.now(UTC)


class CacheModel(BaseModel):
    """Base class for all cache models.

    Provides:
    - ``model_config = ConfigDict(extra="allow")`` inherited by all subclasses
    - Automatic registration in the ``ModelRegistry`` via ``__init_subclass__``

    Opt out of registration by passing ``register=False``::

        class MyContainer(CacheModel, register=False):
            ...
    """

    model_config = ConfigDict(extra="allow")

    def __init_subclass__(cls, register: bool = True, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if register:
            from pynetappfoundry.cache._registry import model_registry

            model_registry.register_model(cls)


@runtime_checkable
class HasUUID(Protocol):
    """Protocol for models that have a uuid field."""

    uuid: str
