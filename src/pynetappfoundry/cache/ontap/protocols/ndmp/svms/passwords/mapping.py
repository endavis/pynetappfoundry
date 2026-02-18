"""OntapNdmpPassword type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.ndmp.svms.passwords.model import OntapNdmpPassword

ONTAPNDMPPASSWORD_MAPPING = TypeMapping(
    name="OntapNdmpPassword",
    model_class=OntapNdmpPassword,
    api_endpoint="/protocols/ndmp/svms/{svm.uuid}/passwords/{user}?fields=*",
    api_type="ontap",
    parent_mapping="OntapNdmpSvm",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="password",
            api_path="password",
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
            cache_attr="user",
            api_path="user",
        ),
    ),
)

model_registry.register_mapping("OntapNdmpPassword", ONTAPNDMPPASSWORD_MAPPING)
