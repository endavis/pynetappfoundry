"""OntapNetgroupFile type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.name_services.netgroup_files.model import OntapNetgroupFile

ONTAPNETGROUPFILE_MAPPING = TypeMapping(
    name="OntapNetgroupFile",
    model_class=OntapNetgroupFile,
    api_endpoint="/name-services/netgroup-files/{svm.uuid}?fields=*",
    api_type="ontap",
    parent_mapping="OntapNameServicesNetgroupFile",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="file_size",
            api_path="file_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="hash_value",
            api_path="hash_value",
        ),
        FieldMapping(
            cache_attr="hash_value_by_host",
            api_path="hash_value_by_host",
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
            cache_attr="timestamp",
            api_path="timestamp",
        ),
    ),
)

model_registry.register_mapping("OntapNetgroupFile", ONTAPNETGROUPFILE_MAPPING)
