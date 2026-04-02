"""OntapCoredump type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.coredump.coredumps.model import OntapCoredump

ONTAPCOREDUMP_MAPPING = TypeMapping(
    name="OntapCoredump",
    model_class=OntapCoredump,
    api_endpoint="/support/coredump/coredumps?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="is_partial",
            api_path="is_partial",
            default=False,
        ),
        FieldMapping(
            cache_attr="is_saved",
            api_path="is_saved",
            default=False,
        ),
        FieldMapping(
            cache_attr="md5_data_checksum",
            api_path="md5_data_checksum",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="node.name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
            api_path="node.uuid",
        ),
        FieldMapping(
            cache_attr="panic_time",
            api_path="panic_time",
        ),
        FieldMapping(
            cache_attr="size",
            api_path="size",
            default=0,
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
    ),
)

model_registry.register_mapping("OntapCoredump", ONTAPCOREDUMP_MAPPING)
