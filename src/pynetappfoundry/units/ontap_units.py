"""ONTAP field unit registrations for currently mapped fields.

Populates ``ontap_registry`` with entries for all ONTAP REST API fields
that have measurement units in the existing mapping definitions.

Each API type (ONTAP, DII, AIQUM) maintains its own ``UnitRegistry``
instance.  This module owns the ONTAP instance.
"""

from __future__ import annotations

from pynetappfoundry.units.dimensions import BYTES, DAYS, PERCENT
from pynetappfoundry.units.registry import UnitEntry, UnitRegistry

_SRC_ONTAP_REST = "ONTAP REST API: field value is in {unit}"


def _populate(registry: UnitRegistry) -> None:
    """Register unit entries for all known ONTAP measurement fields.

    Args:
        registry: The UnitRegistry to populate.
    """
    registry.register_many(
        (
            # --- /storage/volumes ---
            UnitEntry(
                endpoint="/storage/volumes",
                api_field_path="size",
                unit=BYTES,
                source=_SRC_ONTAP_REST.format(unit="bytes"),
            ),
            UnitEntry(
                endpoint="/storage/volumes",
                api_field_path="autosize.maximum",
                unit=BYTES,
                source=_SRC_ONTAP_REST.format(unit="bytes"),
            ),
            UnitEntry(
                endpoint="/storage/volumes",
                api_field_path="autosize.minimum",
                unit=BYTES,
                source=_SRC_ONTAP_REST.format(unit="bytes"),
            ),
            UnitEntry(
                endpoint="/storage/volumes",
                api_field_path="autosize.grow_threshold",
                unit=PERCENT,
                source=_SRC_ONTAP_REST.format(unit="percent"),
            ),
            UnitEntry(
                endpoint="/storage/volumes",
                api_field_path="autosize.shrink_threshold",
                unit=PERCENT,
                source=_SRC_ONTAP_REST.format(unit="percent"),
            ),
            UnitEntry(
                endpoint="/storage/volumes",
                api_field_path="tiering.min_cooling_days",
                unit=DAYS,
                source=_SRC_ONTAP_REST.format(unit="days"),
            ),
            # --- /storage/aggregates ---
            UnitEntry(
                endpoint="/storage/aggregates",
                api_field_path="space.block_storage.size",
                unit=BYTES,
                source=_SRC_ONTAP_REST.format(unit="bytes"),
            ),
            # --- /cluster/nodes ---
            UnitEntry(
                endpoint="/cluster/nodes",
                api_field_path="controller.memory_size",
                unit=BYTES,
                source=("ONTAP REST API: 'Memory available on the node, in bytes'"),
            ),
        )
    )


ontap_registry = UnitRegistry()
_populate(ontap_registry)
