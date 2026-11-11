"""OntapSvmMigration type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.svm.migrations.model import (
    OntapSvmMigration,
    OntapSvmMigrationDestinationVolumePlacementAggregate,
    OntapSvmMigrationMessage,
)

ONTAPSVMMIGRATION_MAPPING = TypeMapping(
    name="OntapSvmMigration",
    model_class=OntapSvmMigration,
    api_endpoint="/svm/migrations?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="auto_cutover",
            default=False,
        ),
        FieldMapping(
            cache_attr="auto_source_cleanup",
            default=False,
        ),
        FieldMapping(
            cache_attr="check_only",
            default=False,
        ),
        FieldMapping(
            cache_attr="current_operation",
        ),
        FieldMapping(
            cache_attr="destination.ipspace.name",
        ),
        FieldMapping(
            cache_attr="destination.ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="destination.volume_placement.aggregates",
            item_model=OntapSvmMigrationDestinationVolumePlacementAggregate,
            default=[],
        ),
        FieldMapping(
            cache_attr="destination.volume_placement.volume_aggregate_pairs",
            default=[],
        ),
        FieldMapping(
            cache_attr="ip_interface_placement.ip_interfaces",
            default=[],
        ),
        FieldMapping(
            cache_attr="last_failed_state",
        ),
        FieldMapping(
            cache_attr="last_operation",
        ),
        FieldMapping(
            cache_attr="messages",
            item_model=OntapSvmMigrationMessage,
            default=[],
        ),
        FieldMapping(
            cache_attr="point_of_no_return",
            default=False,
        ),
        FieldMapping(
            cache_attr="restart_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="source.cluster.name",
        ),
        FieldMapping(
            cache_attr="source.cluster.uuid",
        ),
        FieldMapping(
            cache_attr="source.svm.name",
        ),
        FieldMapping(
            cache_attr="source.svm.uuid",
        ),
        FieldMapping(
            cache_attr="throttle",
            default=0,
        ),
        FieldMapping(
            cache_attr="time_metrics.cutover_complete_time",
        ),
        FieldMapping(
            cache_attr="time_metrics.cutover_start_time",
        ),
        FieldMapping(
            cache_attr="time_metrics.cutover_trigger_time",
        ),
        FieldMapping(
            cache_attr="time_metrics.end_time",
        ),
        FieldMapping(
            cache_attr="time_metrics.last_pause_time",
        ),
        FieldMapping(
            cache_attr="time_metrics.last_resume_time",
        ),
        FieldMapping(
            cache_attr="time_metrics.start_time",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSvmMigration", ONTAPSVMMIGRATION_MAPPING)
