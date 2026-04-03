"""OntapNdmpPassword type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.ndmp.svms.passwords.model import OntapNdmpPassword

ONTAPNDMPPASSWORD_MAPPING = TypeMapping(
    name="OntapNdmpPassword",
    model_class=OntapNdmpPassword,
    api_endpoint="/protocols/ndmp/svms/{svm.uuid}/passwords/{user}?fields=*",
    api_type="ontap",
    parent_mapping="OntapNdmpSvm",
    parent_id_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="password",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="user",
        ),
    ),
)

model_registry.register_mapping("OntapNdmpPassword", ONTAPNDMPPASSWORD_MAPPING)
