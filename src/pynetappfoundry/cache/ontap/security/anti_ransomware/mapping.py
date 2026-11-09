"""OntapAntiRansomware type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.anti_ransomware.model import (
    OntapAntiRansomware,
    OntapAntiRansomwareNode,
)


def _transform_nodes(record: dict[str, Any]) -> list[OntapAntiRansomwareNode]:
    """Transform nodes into OntapAntiRansomwareNode list."""
    return [OntapAntiRansomwareNode(**item) for item in record.get("nodes", [])]


ONTAPANTIRANSOMWARE_MAPPING = TypeMapping(
    name="OntapAntiRansomware",
    model_class=OntapAntiRansomware,
    api_endpoint="/security/anti-ransomware?fields=*",
    api_type="ontap",
    response_shape="singleton",
    fields=(
        FieldMapping(
            cache_attr="nodes",
            transform=_transform_nodes,
            default=[],
        ),
        FieldMapping(
            cache_attr="uri",
        ),
    ),
)

model_registry.register_mapping("OntapAntiRansomware", ONTAPANTIRANSOMWARE_MAPPING)
