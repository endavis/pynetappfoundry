"""OntapVscanOnAccess type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.vscan.on_access_policies.model import OntapVscanOnAccess

ONTAPVSCANONACCESS_MAPPING = TypeMapping(
    name="OntapVscanOnAccess",
    model_class=OntapVscanOnAccess,
    api_endpoint="/protocols/vscan/{svm.uuid}/on-access-policies?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="mandatory",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
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
            cache_attr="scope.only_execute_access",
            default=False,
        ),
        FieldMapping(
            cache_attr="scope.scan_readonly_volumes",
            default=False,
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

model_registry.register_mapping("OntapVscanOnAccess", ONTAPVSCANONACCESS_MAPPING)
