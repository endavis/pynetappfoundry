"""OntapEbrOperation type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.snaplock.event_retention.operations.model import (
    OntapEbrOperation,
)

ONTAPEBROPERATION_MAPPING = TypeMapping(
    name="OntapEbrOperation",
    model_class=OntapEbrOperation,
    api_endpoint="/storage/snaplock/event-retention/operations?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="id",
            api_path="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="num_files_failed",
            api_path="num_files_failed",
            default=0,
        ),
        FieldMapping(
            cache_attr="num_files_processed",
            api_path="num_files_processed",
            default=0,
        ),
        FieldMapping(
            cache_attr="num_files_skipped",
            api_path="num_files_skipped",
            default=0,
        ),
        FieldMapping(
            cache_attr="num_inodes_ignored",
            api_path="num_inodes_ignored",
            default=0,
        ),
        FieldMapping(
            cache_attr="path",
            api_path="path",
        ),
        FieldMapping(
            cache_attr="policy_name",
            api_path="policy.name",
        ),
        FieldMapping(
            cache_attr="policy_retention_period",
            api_path="policy.retention_period",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="volume_name",
            api_path="volume.name",
        ),
        FieldMapping(
            cache_attr="volume_uuid",
            api_path="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapEbrOperation", ONTAPEBROPERATION_MAPPING)
