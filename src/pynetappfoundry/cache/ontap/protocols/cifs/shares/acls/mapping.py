"""OntapCifsShareAcl type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.shares.acls.model import OntapCifsShareAcl

ONTAPCIFSSHAREACL_MAPPING = TypeMapping(
    name="OntapCifsShareAcl",
    model_class=OntapCifsShareAcl,
    api_endpoint="/protocols/cifs/shares/{svm.uuid}/{share}/acls?fields=*",
    api_type="ontap",
    parent_mapping="OntapCifsShare",
    parent_id_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="permission",
            api_path="permission",
        ),
        FieldMapping(
            cache_attr="share",
            api_path="share",
        ),
        FieldMapping(
            cache_attr="sid",
            api_path="sid",
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="unix_id",
            api_path="unix_id",
            default=0,
        ),
        FieldMapping(
            cache_attr="user_or_group",
            api_path="user_or_group",
        ),
    ),
)

model_registry.register_mapping("OntapCifsShareAcl", ONTAPCIFSSHAREACL_MAPPING)
