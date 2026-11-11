"""OntapAntiRansomware type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.anti_ransomware.model import (
    OntapAntiRansomware,
    OntapAntiRansomwareNode,
)

ONTAPANTIRANSOMWARE_MAPPING = TypeMapping(
    name="OntapAntiRansomware",
    model_class=OntapAntiRansomware,
    api_endpoint="/security/anti-ransomware?fields=*",
    api_type="ontap",
    response_shape="singleton",
    fields=(
        FieldMapping(
            cache_attr="nodes",
            item_model=OntapAntiRansomwareNode,
            default=[],
        ),
        FieldMapping(
            cache_attr="uri",
        ),
    ),
)

model_registry.register_mapping("OntapAntiRansomware", ONTAPANTIRANSOMWARE_MAPPING)
