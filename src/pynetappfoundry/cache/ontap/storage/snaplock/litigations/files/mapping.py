"""OntapSnaplockLitigationFileResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.snaplock.litigations.files.model import (
    OntapSnaplockLitigationFileResponse,
)

ONTAPSNAPLOCKLITIGATIONFILERESPONSE_MAPPING = TypeMapping(
    name="OntapSnaplockLitigationFileResponse",
    model_class=OntapSnaplockLitigationFileResponse,
    api_endpoint="/storage/snaplock/litigations/{litigation.id}/files?fields=*",
    api_type="ontap",
    parent_mapping="OntapSnaplockLitigation",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="file",
            default=[],
        ),
        FieldMapping(
            cache_attr="sequence_index",
            default=0,
        ),
    ),
)

model_registry.register_mapping(
    "OntapSnaplockLitigationFileResponse", ONTAPSNAPLOCKLITIGATIONFILERESPONSE_MAPPING
)
