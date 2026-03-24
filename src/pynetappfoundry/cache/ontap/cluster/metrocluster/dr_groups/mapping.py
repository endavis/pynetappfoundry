"""OntapMetroclusterDrGroup type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.cluster.metrocluster.dr_groups.model import (
    OntapMetroclusterDrGroup,
    OntapMetroclusterDrGroupDrPair,
    OntapMetroclusterDrGroupMccipPort,
)


def _transform_dr_pairs(record: dict[str, Any]) -> list[OntapMetroclusterDrGroupDrPair]:
    """Transform dr_pairs into OntapMetroclusterDrGroupDrPair list."""
    return [OntapMetroclusterDrGroupDrPair(**item) for item in record.get("dr_pairs", [])]


def _transform_mccip_ports(record: dict[str, Any]) -> list[OntapMetroclusterDrGroupMccipPort]:
    """Transform mccip_ports into OntapMetroclusterDrGroupMccipPort list."""
    return [OntapMetroclusterDrGroupMccipPort(**item) for item in record.get("mccip_ports", [])]


ONTAPMETROCLUSTERDRGROUP_MAPPING = TypeMapping(
    name="OntapMetroclusterDrGroup",
    model_class=OntapMetroclusterDrGroup,
    api_endpoint="/cluster/metrocluster/dr-groups?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="dr_pairs",
            api_path="dr_pairs",
            transform=_transform_dr_pairs,
            default=[],
        ),
        FieldMapping(
            cache_attr="id",
            api_path="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="mccip_ports",
            api_path="mccip_ports",
            transform=_transform_mccip_ports,
            default=[],
        ),
        FieldMapping(
            cache_attr="partner_cluster_name",
            api_path="partner_cluster.name",
        ),
        FieldMapping(
            cache_attr="partner_cluster_uuid",
            api_path="partner_cluster.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapMetroclusterDrGroup", ONTAPMETROCLUSTERDRGROUP_MAPPING)
