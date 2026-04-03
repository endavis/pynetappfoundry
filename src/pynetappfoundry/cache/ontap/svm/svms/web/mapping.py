"""OntapWebSvm type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.svm.svms.web.model import OntapWebSvm

ONTAPWEBSVM_MAPPING = TypeMapping(
    name="OntapWebSvm",
    model_class=OntapWebSvm,
    api_endpoint="/svm/svms/{svm.uuid}/web?fields=*",
    api_type="ontap",
    parent_mapping="OntapSvm",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="certificate.name",
        ),
        FieldMapping(
            cache_attr="certificate.uuid",
        ),
        FieldMapping(
            cache_attr="client_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="ocsp_enabled",
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

model_registry.register_mapping("OntapWebSvm", ONTAPWEBSVM_MAPPING)
