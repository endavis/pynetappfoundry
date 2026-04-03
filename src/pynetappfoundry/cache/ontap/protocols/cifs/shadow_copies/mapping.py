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
        ),
        FieldMapping(
            cache_attr="destination_dir",
        ),
        FieldMapping(
            cache_attr="files",
            default=[],
        ),
        FieldMapping(
            cache_attr="shadowcopy_set.uuid",
        ),
        FieldMapping(
            cache_attr="share.name",
        ),
        FieldMapping(
            cache_attr="source_dir",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
        FieldMapping(
            cache_attr="with_content",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapShadowcopy", ONTAPSHADOWCOPY_MAPPING)
