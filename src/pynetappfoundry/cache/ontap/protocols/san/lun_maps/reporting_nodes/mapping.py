"""OntapLunMapReportingNode type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.lun_maps.reporting_nodes.model import (
    OntapLunMapReportingNode,
)

ONTAPLUNMAPREPORTINGNODE_MAPPING = TypeMapping(
    name="OntapLunMapReportingNode",
    model_class=OntapLunMapReportingNode,
    api_endpoint="/protocols/san/lun-maps/{lun.uuid}/{igroup.uuid}/reporting-nodes?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="igroup.uuid",
        ),
        FieldMapping(
            cache_attr="lun.uuid",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapLunMapReportingNode", ONTAPLUNMAPREPORTINGNODE_MAPPING)
