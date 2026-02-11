"""Re-export SnapMirror relationship cache models and mappings."""

from __future__ import annotations

from pynetappfoundry.cache.snapmirror.relationships.mapping import SNAPMIRROR_MAPPING
from pynetappfoundry.cache.snapmirror.relationships.model import (
    SnapMirrorRelationship,
)

__all__ = [
    "SNAPMIRROR_MAPPING",
    "SnapMirrorRelationship",
]
