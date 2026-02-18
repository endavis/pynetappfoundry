"""OntapPlex type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.aggregates.plexes.model import (
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
            cache_attr="aggregate_name",
            api_path="aggregate.name",
        ),
        FieldMapping(
            cache_attr="aggregate_uuid",
            api_path="aggregate.uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="online",
            api_path="online",
            default=False,
        ),
        FieldMapping(
            cache_attr="pool",
            api_path="pool",
        ),
        FieldMapping(
            cache_attr="raid_groups",
            transform=_transform_raid_groups,
            default=[],
        ),
        FieldMapping(
            cache_attr="resync_active",
            api_path="resync.active",
            default=False,
        ),
        FieldMapping(
            cache_attr="resync_level",
            api_path="resync.level",
        ),
        FieldMapping(
            cache_attr="resync_percent",
            api_path="resync.percent",
            default=0,
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
    ),
)

model_registry.register_mapping("OntapPlex", ONTAPPLEX_MAPPING)
