"""OntapNdmpSvm type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.ndmp.svms.model import OntapNdmpSvm

ONTAPNDMPSVM_MAPPING = TypeMapping(
    name="OntapNdmpSvm",
    model_class=OntapNdmpSvm,
    api_endpoint="/protocols/ndmp/svms?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="authentication_types",
            api_path="authentication_types",
            default=[],
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
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

model_registry.register_mapping("OntapNdmpSvm", ONTAPNDMPSVM_MAPPING)
