"""OntapVscanOnAccess type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.vscan.on_access_policies.model import OntapVscanOnAccess

ONTAPVSCANONACCESS_MAPPING = TypeMapping(
    name="OntapVscanOnAccess",
    model_class=OntapVscanOnAccess,
    api_endpoint="/protocols/vscan/{svm.uuid}/on-access-policies?fields=*",
    api_type="ontap",
    parent_mapping="OntapProtocolsVscan",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="mandatory",
            api_path="mandatory",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="scope_exclude_extensions",
            api_path="scope.exclude_extensions",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope_exclude_paths",
            api_path="scope.exclude_paths",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope_include_extensions",
            api_path="scope.include_extensions",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope_max_file_size",
            api_path="scope.max_file_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="scope_only_execute_access",
            api_path="scope.only_execute_access",
            default=False,
        ),
        FieldMapping(
            cache_attr="scope_scan_readonly_volumes",
            api_path="scope.scan_readonly_volumes",
            default=False,
        ),
        FieldMapping(
            cache_attr="scope_scan_without_extension",
            api_path="scope.scan_without_extension",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapVscanOnAccess", ONTAPVSCANONACCESS_MAPPING)
