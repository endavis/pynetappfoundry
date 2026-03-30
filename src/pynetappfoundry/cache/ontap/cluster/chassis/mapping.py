"""OntapChassis type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.chassis.model import (
    OntapChassis,
    OntapChassisFru,
    OntapChassisNode,
    OntapChassisShelve,
)


def _transform_frus(record: dict[str, Any]) -> list[OntapChassisFru]:
    """Transform frus into OntapChassisFru list."""
    return [OntapChassisFru(**item) for item in record.get("frus", [])]


def _transform_nodes(record: dict[str, Any]) -> list[OntapChassisNode]:
    """Transform nodes into OntapChassisNode list."""
    return [OntapChassisNode(**item) for item in record.get("nodes", [])]


def _transform_shelves(record: dict[str, Any]) -> list[OntapChassisShelve]:
    """Transform shelves into OntapChassisShelve list."""
    return [OntapChassisShelve(**item) for item in record.get("shelves", [])]


ONTAPCHASSIS_MAPPING = TypeMapping(
    name="OntapChassis",
    model_class=OntapChassis,
    api_endpoint="/cluster/chassis?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="frus",
            api_path="frus",
            transform=_transform_frus,
            default=[],
        ),
        FieldMapping(
            cache_attr="id",
            api_path="id",
        ),
        FieldMapping(
            cache_attr="nodes",
            api_path="nodes",
            transform=_transform_nodes,
            default=[],
        ),
        FieldMapping(
            cache_attr="shelves",
            api_path="shelves",
            transform=_transform_shelves,
            default=[],
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
    ),
)

model_registry.register_mapping("OntapChassis", ONTAPCHASSIS_MAPPING)
