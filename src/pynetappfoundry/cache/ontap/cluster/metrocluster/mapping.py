"""OntapMetrocluster type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.metrocluster.model import (
    OntapMetrocluster,
    OntapMetroclusterMccipPort,
)


def _transform_mccip_ports(record: dict[str, Any]) -> list[OntapMetroclusterMccipPort]:
    """Transform mccip_ports into OntapMetroclusterMccipPort list."""
    return [OntapMetroclusterMccipPort(**item) for item in record.get("mccip_ports", [])]


ONTAPMETROCLUSTER_MAPPING = TypeMapping(
    name="OntapMetrocluster",
    model_class=OntapMetrocluster,
    api_endpoint="/cluster/metrocluster?fields=*",
    api_type="ontap",
    response_shape="singleton",
    fields=(
        FieldMapping(
            cache_attr="configuration_type",
        ),
        FieldMapping(
            cache_attr="dr_pairs",
            default=[],
        ),
        FieldMapping(
            cache_attr="encryption_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="local.automatic_uso_failure_domain",
        ),
        FieldMapping(
            cache_attr="local.cluster.name",
        ),
        FieldMapping(
            cache_attr="local.cluster.uuid",
        ),
        FieldMapping(
            cache_attr="local.configuration_state",
        ),
        FieldMapping(
            cache_attr="local.mode",
        ),
        FieldMapping(
            cache_attr="local.partner_cluster_reachable",
            default=False,
        ),
        FieldMapping(
            cache_attr="local.periodic_check_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="mccip_ports",
            transform=_transform_mccip_ports,
            default=[],
        ),
        FieldMapping(
            cache_attr="mediator.ca_certificate",
        ),
        FieldMapping(
            cache_attr="mediator.dr_group.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="mediator.ip_address",
        ),
        FieldMapping(
            cache_attr="mediator.password",
        ),
        FieldMapping(
            cache_attr="mediator.peer_cluster.name",
        ),
        FieldMapping(
            cache_attr="mediator.peer_cluster.uuid",
        ),
        FieldMapping(
            cache_attr="mediator.peer_mediator_connectivity",
        ),
        FieldMapping(
            cache_attr="mediator.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="mediator.reachable",
            default=False,
        ),
        FieldMapping(
            cache_attr="mediator.user",
        ),
        FieldMapping(
            cache_attr="mediator.uuid",
        ),
        FieldMapping(
            cache_attr="partner_cluster.name",
        ),
        FieldMapping(
            cache_attr="partner_cluster.uuid",
        ),
        FieldMapping(
            cache_attr="remote.automatic_uso_failure_domain",
        ),
        FieldMapping(
            cache_attr="remote.cluster.name",
        ),
        FieldMapping(
            cache_attr="remote.cluster.uuid",
        ),
        FieldMapping(
            cache_attr="remote.configuration_state",
        ),
        FieldMapping(
            cache_attr="remote.mode",
        ),
        FieldMapping(
            cache_attr="remote.periodic_check_enabled",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapMetrocluster", ONTAPMETROCLUSTER_MAPPING)
