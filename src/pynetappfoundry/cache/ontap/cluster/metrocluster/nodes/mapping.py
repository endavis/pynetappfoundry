"""OntapMetroclusterNode type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.metrocluster.nodes.model import OntapMetroclusterNode

ONTAPMETROCLUSTERNODE_MAPPING = TypeMapping(
    name="OntapMetroclusterNode",
    model_class=OntapMetroclusterNode,
    api_endpoint="/cluster/metrocluster/nodes?fields=*",
    api_type="ontap",
    identifier_field="node.uuid",
    fields=(
        FieldMapping(
            cache_attr="automatic_uso",
            default=False,
        ),
        FieldMapping(
            cache_attr="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="configuration_state",
        ),
        FieldMapping(
            cache_attr="dr_auxiliary_cluster.name",
        ),
        FieldMapping(
            cache_attr="dr_auxiliary_cluster.uuid",
        ),
        FieldMapping(
            cache_attr="dr_auxiliary_partner.name",
        ),
        FieldMapping(
            cache_attr="dr_auxiliary_partner.system_id",
        ),
        FieldMapping(
            cache_attr="dr_auxiliary_partner.uuid",
        ),
        FieldMapping(
            cache_attr="dr_group_id",
            default=0,
        ),
        FieldMapping(
            cache_attr="dr_mirroring_state",
        ),
        FieldMapping(
            cache_attr="dr_operation_state",
        ),
        FieldMapping(
            cache_attr="dr_partner.name",
        ),
        FieldMapping(
            cache_attr="dr_partner.system_id",
        ),
        FieldMapping(
            cache_attr="dr_partner.uuid",
        ),
        FieldMapping(
            cache_attr="dr_partner_cluster.name",
        ),
        FieldMapping(
            cache_attr="dr_partner_cluster.uuid",
        ),
        FieldMapping(
            cache_attr="encryption_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="ha_partner.name",
        ),
        FieldMapping(
            cache_attr="ha_partner.system_id",
        ),
        FieldMapping(
            cache_attr="ha_partner.uuid",
        ),
        FieldMapping(
            cache_attr="ha_partner_cluster.name",
        ),
        FieldMapping(
            cache_attr="ha_partner_cluster.uuid",
        ),
        FieldMapping(
            cache_attr="is_mccip",
            default=False,
        ),
        FieldMapping(
            cache_attr="limit_enforcement",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.system_id",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapMetroclusterNode", ONTAPMETROCLUSTERNODE_MAPPING)
