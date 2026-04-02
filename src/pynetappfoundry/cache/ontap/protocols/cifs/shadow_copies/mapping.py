"""OntapShadowcopy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.shadow_copies.model import OntapShadowcopy

ONTAPSHADOWCOPY_MAPPING = TypeMapping(
    name="OntapShadowcopy",
    model_class=OntapShadowcopy,
    api_endpoint="/protocols/cifs/shadow-copies?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="client_uuid",
            api_path="client_uuid",
        ),
        FieldMapping(
            cache_attr="destination_dir",
            api_path="destination_dir",
        ),
        FieldMapping(
            cache_attr="files",
            api_path="files",
            default=[],
        ),
        FieldMapping(
            cache_attr="shadowcopy_set.uuid",
            api_path="shadowcopy_set.uuid",
        ),
        FieldMapping(
            cache_attr="share.name",
            api_path="share.name",
        ),
        FieldMapping(
            cache_attr="source_dir",
            api_path="source_dir",
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
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="volume.name",
            api_path="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
            api_path="volume.uuid",
        ),
        FieldMapping(
            cache_attr="with_content",
            api_path="with_content",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapShadowcopy", ONTAPSHADOWCOPY_MAPPING)
