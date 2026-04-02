"""OntapIgroupNested type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.igroups.igroups.model import (
    OntapIgroupNested,
    OntapIgroupNestedRecord,
)


def _transform_records(record: dict[str, Any]) -> list[OntapIgroupNestedRecord]:
    """Transform records into OntapIgroupNestedRecord list."""
    return [OntapIgroupNestedRecord(**item) for item in record.get("records", [])]


ONTAPIGROUPNESTED_MAPPING = TypeMapping(
    name="OntapIgroupNested",
    model_class=OntapIgroupNested,
    api_endpoint="/protocols/san/igroups/{igroup.uuid}/igroups?fields=*",
    api_type="ontap",
    parent_mapping="OntapIgroup",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="igroup.uuid",
            api_path="igroup.uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="records",
            api_path="records",
            transform=_transform_records,
            default=[],
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapIgroupNested", ONTAPIGROUPNESTED_MAPPING)
