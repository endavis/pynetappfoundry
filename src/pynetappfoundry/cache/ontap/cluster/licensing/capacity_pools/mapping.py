"""OntapCapacityPoolResponse type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.licensing.capacity_pools.model import (
    OntapCapacityPoolResponse,
    OntapCapacityPoolResponseNode,
)


def _transform_nodes(record: dict[str, Any]) -> list[OntapCapacityPoolResponseNode]:
    """Transform nodes into OntapCapacityPoolResponseNode list."""
    return [OntapCapacityPoolResponseNode(**item) for item in record.get("nodes", [])]


ONTAPCAPACITYPOOLRESPONSE_MAPPING = TypeMapping(
    name="OntapCapacityPoolResponse",
    model_class=OntapCapacityPoolResponse,
    api_endpoint="/cluster/licensing/capacity-pools?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="license_manager_uuid",
            api_path="license_manager.uuid",
        ),
        FieldMapping(
            cache_attr="nodes",
            api_path="nodes",
            transform=_transform_nodes,
            default=[],
        ),
        FieldMapping(
            cache_attr="serial_number",
            api_path="serial_number",
        ),
    ),
)

model_registry.register_mapping("OntapCapacityPoolResponse", ONTAPCAPACITYPOOLRESPONSE_MAPPING)
