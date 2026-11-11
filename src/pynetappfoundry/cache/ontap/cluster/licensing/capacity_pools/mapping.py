"""OntapCapacityPoolResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.licensing.capacity_pools.model import (
    OntapCapacityPoolResponse,
    OntapCapacityPoolResponseNode,
)

ONTAPCAPACITYPOOLRESPONSE_MAPPING = TypeMapping(
    name="OntapCapacityPoolResponse",
    model_class=OntapCapacityPoolResponse,
    api_endpoint="/cluster/licensing/capacity-pools?fields=*",
    api_type="ontap",
    identifier_field="serial_number",
    fields=(
        FieldMapping(
            cache_attr="license_manager.uuid",
        ),
        FieldMapping(
            cache_attr="nodes",
            item_model=OntapCapacityPoolResponseNode,
            default=[],
        ),
        FieldMapping(
            cache_attr="serial_number",
        ),
    ),
)

model_registry.register_mapping("OntapCapacityPoolResponse", ONTAPCAPACITYPOOLRESPONSE_MAPPING)
