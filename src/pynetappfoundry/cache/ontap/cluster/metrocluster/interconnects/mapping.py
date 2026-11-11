"""OntapMetroclusterInterconnect type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.metrocluster.interconnects.model import (
    OntapMetroclusterInterconnect,
    OntapMetroclusterInterconnectInterface,
)

ONTAPMETROCLUSTERINTERCONNECT_MAPPING = TypeMapping(
    name="OntapMetroclusterInterconnect",
    model_class=OntapMetroclusterInterconnect,
    api_endpoint="/cluster/metrocluster/interconnects?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="adapter",
        ),
        FieldMapping(
            cache_attr="interfaces",
            item_model=OntapMetroclusterInterconnectInterface,
            default=[],
        ),
        FieldMapping(
            cache_attr="mirror.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="mirror.state",
        ),
        FieldMapping(
            cache_attr="multipath_policy",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="partner_type",
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="vlan_id",
            default=0,
        ),
    ),
)

model_registry.register_mapping(
    "OntapMetroclusterInterconnect", ONTAPMETROCLUSTERINTERCONNECT_MAPPING
)
