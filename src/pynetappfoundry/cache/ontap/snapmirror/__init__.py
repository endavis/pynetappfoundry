"""Re-export SnapMirror cache models from sub-packages."""

from __future__ import annotations

from pynetappfoundry.cache.ontap.snapmirror.relationships import OntapSnapmirrorRelationship

__all__ = [
    "OntapSnapmirrorRelationship",
]
