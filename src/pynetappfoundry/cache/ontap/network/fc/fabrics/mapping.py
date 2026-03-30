"""OntapFabric type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.fc.fabrics.model import OntapFabric, OntapFabricConnection


def _transform_connections(record: dict[str, Any]) -> list[OntapFabricConnection]:
    """Transform connections into OntapFabricConnection list."""
    return [OntapFabricConnection(**item) for item in record.get("connections", [])]


ONTAPFABRIC_MAPPING = TypeMapping(
    name="OntapFabric",
    model_class=OntapFabric,
    api_endpoint="/network/fc/fabrics?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="cache_age",
            api_path="cache.age",
        ),
        FieldMapping(
            cache_attr="cache_is_current",
            api_path="cache.is_current",
            default=False,
        ),
        FieldMapping(
            cache_attr="cache_update_time",
            api_path="cache.update_time",
        ),
        FieldMapping(
            cache_attr="connections",
            api_path="connections",
            transform=_transform_connections,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="zoneset_name",
            api_path="zoneset.name",
        ),
    ),
)

model_registry.register_mapping("OntapFabric", ONTAPFABRIC_MAPPING)
