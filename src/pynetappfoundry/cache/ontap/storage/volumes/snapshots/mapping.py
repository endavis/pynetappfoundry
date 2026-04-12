"""OntapSnapshot type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.volumes.snapshots.model import OntapSnapshot

ONTAPSNAPSHOT_MAPPING = TypeMapping(
    name="OntapSnapshot",
    model_class=OntapSnapshot,
    api_endpoint="/storage/volumes/{volume.uuid}/snapshots?fields=*",
    api_type="ontap",
    parent_mapping="OntapVolume",
    parent_id_field="uuid",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="compress_savings",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="create_time",
        ),
        FieldMapping(
            cache_attr="dedup_savings",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="delta.size_consumed",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="delta.time_elapsed",
        ),
        FieldMapping(
            cache_attr="expiry_time",
        ),
        FieldMapping(
            cache_attr="logical_size",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="owners",
            default=[],
        ),
        FieldMapping(
            cache_attr="provenance_volume.uuid",
        ),
        FieldMapping(
            cache_attr="reclaimable_space",
            cache_strategy="realtime",
            default=0,
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="size",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="snaplock.expired",
            default=False,
        ),
        FieldMapping(
            cache_attr="snaplock.expiry_time",
        ),
        FieldMapping(
            cache_attr="snaplock.time_until_expiry",
        ),
        FieldMapping(
            cache_attr="snaplock_expiry_time",
        ),
        FieldMapping(
            cache_attr="snapmirror_label",
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="vbn0_savings",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="version_uuid",
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSnapshot", ONTAPSNAPSHOT_MAPPING)
