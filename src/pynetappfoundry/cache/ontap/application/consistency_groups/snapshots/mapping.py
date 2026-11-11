"""OntapConsistencyGroupSnapshotResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.application.consistency_groups.snapshots.model import (
    OntapConsistencyGroupSnapshotResponse,
    OntapConsistencyGroupSnapshotResponseLun,
    OntapConsistencyGroupSnapshotResponseMissingLun,
    OntapConsistencyGroupSnapshotResponseMissingNamespace,
    OntapConsistencyGroupSnapshotResponseMissingVolume,
    OntapConsistencyGroupSnapshotResponseNamespace,
)

ONTAPCONSISTENCYGROUPSNAPSHOTRESPONSE_MAPPING = TypeMapping(
    name="OntapConsistencyGroupSnapshotResponse",
    model_class=OntapConsistencyGroupSnapshotResponse,
    api_endpoint="/application/consistency-groups/{consistency_group.uuid}/snapshots?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    parent_mapping="OntapConsistencyGroupResponse",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="consistency_group.name",
        ),
        FieldMapping(
            cache_attr="consistency_group.uuid",
        ),
        FieldMapping(
            cache_attr="consistency_type",
        ),
        FieldMapping(
            cache_attr="create_time",
        ),
        FieldMapping(
            cache_attr="is_partial",
            default=False,
        ),
        FieldMapping(
            cache_attr="luns",
            item_model=OntapConsistencyGroupSnapshotResponseLun,
            default=[],
        ),
        FieldMapping(
            cache_attr="missing_luns",
            item_model=OntapConsistencyGroupSnapshotResponseMissingLun,
            default=[],
        ),
        FieldMapping(
            cache_attr="missing_namespaces",
            item_model=OntapConsistencyGroupSnapshotResponseMissingNamespace,
            default=[],
        ),
        FieldMapping(
            cache_attr="missing_volumes",
            item_model=OntapConsistencyGroupSnapshotResponseMissingVolume,
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="namespaces",
            item_model=OntapConsistencyGroupSnapshotResponseNamespace,
            default=[],
        ),
        FieldMapping(
            cache_attr="reclaimable_space",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="restore_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="snapmirror_label",
        ),
        FieldMapping(
            cache_attr="snapshot_volumes",
            default=[],
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
            cache_attr="write_fence",
            default=False,
        ),
    ),
)

model_registry.register_mapping(
    "OntapConsistencyGroupSnapshotResponse", ONTAPCONSISTENCYGROUPSNAPSHOTRESPONSE_MAPPING
)
