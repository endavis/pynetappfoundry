"""OntapMetroclusterInterconnect type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.metrocluster.interconnects.model import (
    OntapMetroclusterInterconnect,
    OntapMetroclusterInterconnectInterface,
)


def _transform_interfaces(record: dict[str, Any]) -> list[OntapMetroclusterInterconnectInterface]:
    """Transform interfaces into OntapMetroclusterInterconnectInterface list."""
    return [OntapMetroclusterInterconnectInterface(**item) for item in record.get("interfaces", [])]


ONTAPMETROCLUSTERINTERCONNECT_MAPPING = TypeMapping(
    name="OntapMetroclusterInterconnect",
    model_class=OntapMetroclusterInterconnect,
    api_endpoint="/cluster/metrocluster/interconnects?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="adapter",
            api_path="adapter",
        ),
        FieldMapping(
            cache_attr="interfaces",
            api_path="interfaces",
            transform=_transform_interfaces,
            default=[],
        ),
        FieldMapping(
            cache_attr="mirror_enabled",
            api_path="mirror.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="mirror_state",
            api_path="mirror.state",
        ),
        FieldMapping(
            cache_attr="multipath_policy",
            api_path="multipath_policy",
        ),
        FieldMapping(
            cache_attr="node_name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node_uuid",
            api_path="node.uuid",
        ),
        FieldMapping(
            cache_attr="partner_type",
            api_path="partner_type",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="vlan_id",
            api_path="vlan_id",
            default=0,
        ),
    ),
)

model_registry.register_mapping(
    "OntapMetroclusterInterconnect", ONTAPMETROCLUSTERINTERCONNECT_MAPPING
)
