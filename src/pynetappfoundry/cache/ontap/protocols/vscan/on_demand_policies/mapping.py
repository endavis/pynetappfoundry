"""OntapVscanOnDemand type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.vscan.on_demand_policies.model import OntapVscanOnDemand

ONTAPVSCANONDEMAND_MAPPING = TypeMapping(
    name="OntapVscanOnDemand",
    model_class=OntapVscanOnDemand,
    api_endpoint="/protocols/vscan/{svm.uuid}/on-demand-policies?fields=*",
    api_type="ontap",
    parent_mapping="OntapProtocolsVscan",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="log_path",
            api_path="log_path",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="scan_paths",
            api_path="scan_paths",
            default=[],
        ),
        FieldMapping(
            cache_attr="schedule_name",
            api_path="schedule.name",
        ),
        FieldMapping(
            cache_attr="schedule_uuid",
            api_path="schedule.uuid",
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

model_registry.register_mapping("OntapVscanOnDemand", ONTAPVSCANONDEMAND_MAPPING)
