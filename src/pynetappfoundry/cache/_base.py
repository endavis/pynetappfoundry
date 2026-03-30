"""Base class and utilities for cache models.

Re-exports OntapModel as CacheModel for backward compatibility within
the cache layer.  Schema versioning functions live here as they are
cache-specific concerns.
"""

from __future__ import annotations

from datetime import UTC, datetime

from pynetappfoundry.models._base import HasUUID, OntapModel, OntapUUID, _validate_ontap_uuid

# Re-export OntapModel as CacheModel for cache-layer compatibility
CacheModel = OntapModel

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


__all__ = [
    "METADATA_SCHEMA_MIN_COMPATIBLE",
    "METADATA_SCHEMA_VERSION",
    "CacheModel",
    "HasUUID",
    "OntapUUID",
    "_utcnow",
    "_validate_ontap_uuid",
    "is_schema_compatible",
    "parse_schema_version",
]
