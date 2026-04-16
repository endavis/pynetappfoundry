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
    identifier_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="authentication_types",
            default=[],
        ),
        FieldMapping(
            cache_attr="enabled",
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

model_registry.register_mapping("OntapNdmpSvm", ONTAPNDMPSVM_MAPPING)
