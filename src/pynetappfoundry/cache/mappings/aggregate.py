"""Aggregate type mapping definition for the declarative field mapping framework.

Defines AGGREGATE_MAPPING which maps ONTAP REST API and CLI aggregate data to
AggregateInfo cache model attributes.
"""

from __future__ import annotations

from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.models import AggregateInfo

AGGREGATE_MAPPING = TypeMapping(
    name="Aggregate",
    model_class=AggregateInfo,
    api_endpoint="/storage/aggregates?fields=*",
    cli_command="aggr show",
    fields=(
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
            cli_field="aggregate",
        ),
        FieldMapping(
            cache_attr="node",
            api_path="node.name",
            cli_field="node",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
            cli_field="state",
        ),
        FieldMapping(
            cache_attr="type",
            api_path="block_storage.primary.disk_type",
            cli_field="type",
        ),
        FieldMapping(
            cache_attr="total_size",
            api_path="space.block_storage.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="disk_count",
            api_path="block_storage.primary.disk_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="disk_type",
            api_path="block_storage.primary.disk_type",
        ),
        FieldMapping(
            cache_attr="raid_type",
            api_path="block_storage.primary.raid_type",
        ),
    ),
)
