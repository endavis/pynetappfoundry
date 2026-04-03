"""OntapVscanOnDemand type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.vscan.on_demand_policies.model import OntapVscanOnDemand

ONTAPVSCANONDEMAND_MAPPING = TypeMapping(
    name="OntapVscanOnDemand",
    model_class=OntapVscanOnDemand,
    api_endpoint="/protocols/vscan/{svm.uuid}/on-demand-policies?fields=*",
    api_type="ontap",
    parent_mapping="OntapSvm",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="log_path",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="scan_paths",
            default=[],
        ),
        FieldMapping(
            cache_attr="schedule.name",
        ),
        FieldMapping(
            cache_attr="schedule.uuid",
        ),
        FieldMapping(
            cache_attr="scope.exclude_extensions",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope.exclude_paths",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope.include_extensions",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope.max_file_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="scope.scan_without_extension",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapVscanOnDemand", ONTAPVSCANONDEMAND_MAPPING)
