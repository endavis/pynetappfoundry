"""OntapPlex type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.aggregates.plexes.model import (
    OntapPlex,
    OntapPlexRaidGroup,
)

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
            item_model=OntapPlexRaidGroup,
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
