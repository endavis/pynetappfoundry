"""OntapSplitStatus type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.file.clone.split_status.model import OntapSplitStatus

ONTAPSPLITSTATUS_MAPPING = TypeMapping(
    name="OntapSplitStatus",
    model_class=OntapSplitStatus,
    api_endpoint="/storage/file/clone/split-status?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="pending_splits",
            api_path="pending_splits",
            default=0,
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
            cache_attr="unsplit_size",
            api_path="unsplit_size",
            default=0,
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

model_registry.register_mapping("OntapSplitStatus", ONTAPSPLITSTATUS_MAPPING)
