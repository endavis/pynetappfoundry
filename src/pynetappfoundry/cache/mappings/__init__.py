"""Declarative type mapping definitions for ONTAP object types.

Each sub-module defines a TypeMapping constant for one ONTAP object type.
"""

from pynetappfoundry.cache.mappings.volume import VOLUME_MAPPING

__all__ = ["VOLUME_MAPPING"]
