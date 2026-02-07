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
    api_endpoint="/storage/aggregates?fields=*,is_spare_low,sidl_enabled",
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
        # block_storage structural fields
        FieldMapping(
            cache_attr="storage_type",
            api_path="block_storage.storage_type",
        ),
        FieldMapping(
            cache_attr="disk_class",
            api_path="block_storage.primary.disk_class",
        ),
        FieldMapping(
            cache_attr="raid_size",
            api_path="block_storage.primary.raid_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="checksum_style",
            api_path="block_storage.primary.checksum_style",
        ),
        FieldMapping(
            cache_attr="uses_partitions",
            api_path="block_storage.uses_partitions",
            default=False,
        ),
        FieldMapping(
            cache_attr="mirror_enabled",
            api_path="block_storage.mirror.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="mirror_state",
            api_path="block_storage.mirror.state",
        ),
        FieldMapping(
            cache_attr="hybrid_cache_enabled",
            api_path="block_storage.hybrid_cache.enabled",
            default=False,
        ),
        # other structural fields
        FieldMapping(
            cache_attr="snaplock_type",
            api_path="snaplock_type",
        ),
        FieldMapping(
            cache_attr="home_node",
            api_path="home_node.name",
        ),
        FieldMapping(
            cache_attr="dr_home_node",
            api_path="dr_home_node.name",
        ),
        FieldMapping(
            cache_attr="create_time",
            api_path="create_time",
        ),
        # config flags
        FieldMapping(
            cache_attr="cloud_attach_eligible",
            api_path="cloud_storage.attach_eligible",
            default=False,
        ),
        FieldMapping(
            cache_attr="encryption_software",
            api_path="data_encryption.software_encryption_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="encryption_drive",
            api_path="data_encryption.drive_protection_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="sidl_enabled",
            api_path="sidl_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="inactive_data_reporting_enabled",
            api_path="inactive_data_reporting.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="volume_count",
            api_path="volume_count",
            cli_field="volcount",
            default=0,
        ),
        # expensive field (needs explicit API request)
        FieldMapping(
            cache_attr="is_spare_low",
            api_path="is_spare_low",
            default=False,
        ),
    ),
)
