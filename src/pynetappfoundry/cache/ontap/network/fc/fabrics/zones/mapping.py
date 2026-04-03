"""OntapFcZone type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.fc.fabrics.zones.model import (
    OntapFcZone,
    OntapFcZoneMember,
)


def _transform_members(record: dict[str, Any]) -> list[OntapFcZoneMember]:
    """Transform members into OntapFcZoneMember list."""
    return [OntapFcZoneMember(**item) for item in record.get("members", [])]


ONTAPFCZONE_MAPPING = TypeMapping(
    name="OntapFcZone",
    model_class=OntapFcZone,
    api_endpoint="/network/fc/fabrics/{fabric.name}/zones?fields=*",
    api_type="ontap",
    parent_mapping="OntapFabric",
    parent_id_field="name",
    fields=(
        FieldMapping(
            cache_attr="cache.age",
        ),
        FieldMapping(
            cache_attr="cache.is_current",
            default=False,
        ),
        FieldMapping(
            cache_attr="cache.update_time",
        ),
        FieldMapping(
            cache_attr="fabric.name",
        ),
        FieldMapping(
            cache_attr="members",
            transform=_transform_members,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="name",
        ),
    ),
)

model_registry.register_mapping("OntapFcZone", ONTAPFCZONE_MAPPING)
