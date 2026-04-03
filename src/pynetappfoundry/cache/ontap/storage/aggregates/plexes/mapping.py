"""OntapPlex type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.aggregates.plexes.model import (
    OntapPlex,
    OntapPlexRaidGroup,
)


def _transform_raid_groups(record: dict[str, Any]) -> list[OntapPlexRaidGroup]:
    """Transform raid_groups into OntapPlexRaidGroup list."""
    return [OntapPlexRaidGroup(**item) for item in record.get("raid_groups", [])]


ONTAPPLEX_MAPPING = TypeMapping(
    name="OntapPlex",
    model_class=OntapPlex,
    api_endpoint="/storage/aggregates/{aggregate.uuid}/plexes?fields=*",
    api_type="ontap",
    parent_mapping="OntapAggregate",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="aggregate.name",
        ),
        FieldMapping(
            cache_attr="aggregate.uuid",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="online",
            default=False,
        ),
        FieldMapping(
            cache_attr="pool",
        ),
        FieldMapping(
            cache_attr="raid_groups",
            transform=_transform_raid_groups,
            default=[],
        ),
        FieldMapping(
            cache_attr="resync.active",
            default=False,
        ),
        FieldMapping(
            cache_attr="resync.level",
        ),
        FieldMapping(
            cache_attr="resync.percent",
            default=0,
        ),
        FieldMapping(
            cache_attr="state",
        ),
    ),
)

model_registry.register_mapping("OntapPlex", ONTAPPLEX_MAPPING)
