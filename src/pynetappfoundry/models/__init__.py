"""ONTAP API model definitions.

Canonical Pydantic model classes for ONTAP REST API resources.
These models are consumed by the cache layer and other library components.
"""

from pynetappfoundry.models._base import HasUUID, OntapModel, OntapUUID

__all__ = [
    "HasUUID",
    "OntapModel",
    "OntapUUID",
]
