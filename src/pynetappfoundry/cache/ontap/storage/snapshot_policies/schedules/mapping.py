"""OntapSnapshotPolicySchedule type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.snapshot_policies.schedules.model import (
    OntapSnapshotPolicySchedule,
)

ONTAPSNAPSHOTPOLICYSCHEDULE_MAPPING = TypeMapping(
    name="OntapSnapshotPolicySchedule",
    model_class=OntapSnapshotPolicySchedule,
    api_endpoint="/storage/snapshot-policies/{snapshot_policy.uuid}/schedules?fields=*",
    api_type="ontap",
    parent_mapping="OntapSnapshotPolicy",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="count",
            default=0,
        ),
        FieldMapping(
            cache_attr="prefix",
        ),
        FieldMapping(
            cache_attr="retention_period",
        ),
        FieldMapping(
            cache_attr="schedule.name",
        ),
        FieldMapping(
            cache_attr="schedule.uuid",
        ),
        FieldMapping(
            cache_attr="snapmirror_label",
        ),
        FieldMapping(
            cache_attr="snapshot_policy.name",
        ),
        FieldMapping(
            cache_attr="snapshot_policy.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSnapshotPolicySchedule", ONTAPSNAPSHOTPOLICYSCHEDULE_MAPPING)
