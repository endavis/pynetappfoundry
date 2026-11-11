"""OntapChassis type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.chassis.model import (
    OntapChassis,
    OntapChassisFru,
    OntapChassisNode,
    OntapChassisShelve,
)

ONTAPCHASSIS_MAPPING = TypeMapping(
    name="OntapChassis",
    model_class=OntapChassis,
    api_endpoint="/cluster/chassis?fields=*",
    api_type="ontap",
    identifier_field="id",
    fields=(
        FieldMapping(
            cache_attr="frus",
            item_model=OntapChassisFru,
            default=[],
        ),
        FieldMapping(
            cache_attr="id",
        ),
        FieldMapping(
            cache_attr="nodes",
            item_model=OntapChassisNode,
            default=[],
        ),
        FieldMapping(
            cache_attr="shelves",
            item_model=OntapChassisShelve,
            default=[],
        ),
        FieldMapping(
            cache_attr="state",
        ),
    ),
)

model_registry.register_mapping("OntapChassis", ONTAPCHASSIS_MAPPING)
