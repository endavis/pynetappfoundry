"""OntapVscan type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.vscan.model import OntapVscan

ONTAPVSCAN_MAPPING = TypeMapping(
    name="OntapVscan",
    model_class=OntapVscan,
    api_endpoint="/protocols/vscan/{svm.uuid}?fields=*",
    api_type="ontap",
    records_path="on_access_policies",
    parent_mapping="OntapSvm",
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
    ),
)

model_registry.register_mapping("OntapVscan", ONTAPVSCAN_MAPPING)
