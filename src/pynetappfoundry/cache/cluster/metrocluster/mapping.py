"""OntapMetrocluster type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.cluster.metrocluster.model import OntapMetrocluster
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping

ONTAPMETROCLUSTER_MAPPING = TypeMapping(
    name="OntapMetrocluster",
    model_class=OntapMetrocluster,
    api_endpoint="/cluster/metrocluster?fields=*",
    api_type="ontap",
    records_path="dr_pairs",
    fields=(
        FieldMapping(
            cache_attr="node_name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node_uuid",
            api_path="node.uuid",
        ),
        FieldMapping(
            cache_attr="partner_name",
            api_path="partner.name",
        ),
        FieldMapping(
            cache_attr="partner_uuid",
            api_path="partner.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapMetrocluster", ONTAPMETROCLUSTER_MAPPING)
