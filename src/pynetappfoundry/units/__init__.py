"""Standalone unit registry for ONTAP API field measurements.

Provides unit definitions, conversion utilities, and a registry that maps
API fields to their units of measurement.  Each API type (ONTAP, DII,
AIQUM) maintains its own ``UnitRegistry`` instance.

Example:
    >>> from pynetappfoundry.units import ontap_registry, convert, BYTES, GIB
    >>> entry = ontap_registry.get("/storage/volumes", "size")
    >>> entry.unit.symbol
    'B'
    >>> convert(1073741824, BYTES, GIB)
    1.0
"""

from pynetappfoundry.units.conversion import (
    IncompatibleUnitsError,
    convert,
    format_value,
)
from pynetappfoundry.units.dimensions import (
    ALL_UNITS,
    BYTES,
    BYTES_PER_SEC,
    DAYS,
    GB,
    GIB,
    HOURS,
    KB,
    KB_PER_SEC,
    KIB,
    MB,
    MB_PER_SEC,
    MIB,
    MINUTES,
    PB,
    PERCENT,
    PIB,
    SECONDS,
    TB,
    TIB,
    Dimension,
    Unit,
    get_unit,
)
from pynetappfoundry.units.ontap_units import ontap_registry
from pynetappfoundry.units.registry import UnitEntry, UnitRegistry

__all__ = [
    "ALL_UNITS",
    "BYTES",
    "BYTES_PER_SEC",
    "DAYS",
    "GB",
    "GIB",
    "HOURS",
    "KB",
    "KB_PER_SEC",
    "KIB",
    "MB",
    "MB_PER_SEC",
    "MIB",
    "MINUTES",
    "PB",
    "PERCENT",
    "PIB",
    "SECONDS",
    "TB",
    "TIB",
    "Dimension",
    "IncompatibleUnitsError",
    "Unit",
    "UnitEntry",
    "UnitRegistry",
    "convert",
    "format_value",
    "get_unit",
    "ontap_registry",
]
