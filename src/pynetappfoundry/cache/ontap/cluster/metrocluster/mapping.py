"""OntapMetrocluster type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.metrocluster.model import OntapMetrocluster

ONTAPMETROCLUSTER_MAPPING = TypeMapping(
    name="OntapMetrocluster",
    model_class=OntapMetrocluster,
    api_endpoint="/cluster/metrocluster?fields=*",
    api_type="ontap",
    records_path="dr_pairs",
    fields=(
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="partner.name",
        ),
        FieldMapping(
            cache_attr="partner.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapMetrocluster", ONTAPMETROCLUSTER_MAPPING)
