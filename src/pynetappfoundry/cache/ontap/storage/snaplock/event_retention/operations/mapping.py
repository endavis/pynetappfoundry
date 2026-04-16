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
    identifier_field="id",
    fields=(
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="num_files_failed",
            default=0,
        ),
        FieldMapping(
            cache_attr="num_files_processed",
            default=0,
        ),
        FieldMapping(
            cache_attr="num_files_skipped",
            default=0,
        ),
        FieldMapping(
            cache_attr="num_inodes_ignored",
            default=0,
        ),
        FieldMapping(
            cache_attr="path",
        ),
        FieldMapping(
            cache_attr="policy.name",
        ),
        FieldMapping(
            cache_attr="policy.retention_period",
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
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapEbrOperation", ONTAPEBROPERATION_MAPPING)
