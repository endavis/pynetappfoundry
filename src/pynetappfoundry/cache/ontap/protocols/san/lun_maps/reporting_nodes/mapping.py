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
    parent_mapping="OntapLunMap",
    parent_id_field="lun.uuid",
    fields=(
        FieldMapping(
            cache_attr="igroup.uuid",
            api_path="igroup.uuid",
        ),
        FieldMapping(
            cache_attr="lun.uuid",
            api_path="lun.uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapLunMapReportingNode", ONTAPLUNMAPREPORTINGNODE_MAPPING)
