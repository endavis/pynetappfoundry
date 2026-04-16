"""OntapSplitStatus type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.file.clone.split_status.model import OntapSplitStatus

ONTAPSPLITSTATUS_MAPPING = TypeMapping(
    name="OntapSplitStatus",
    model_class=OntapSplitStatus,
    api_endpoint="/storage/file/clone/split-status?fields=*",
    api_type="ontap",
    identifier_field="volume.uuid",
    fields=(
        FieldMapping(
            cache_attr="pending_splits",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="unsplit_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSplitStatus", ONTAPSPLITSTATUS_MAPPING)
