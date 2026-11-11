"""OntapLunMap type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.lun_maps.model import (
    OntapLunMap,
    OntapLunMapReportingNode,
)

ONTAPLUNMAP_MAPPING = TypeMapping(
    name="OntapLunMap",
    model_class=OntapLunMap,
    api_endpoint="/protocols/san/lun-maps?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="igroup.initiators",
            default=[],
        ),
        FieldMapping(
            cache_attr="igroup.name",
        ),
        FieldMapping(
            cache_attr="igroup.os_type",
        ),
        FieldMapping(
            cache_attr="igroup.protocol",
        ),
        FieldMapping(
            cache_attr="igroup.replicated",
            default=False,
        ),
        FieldMapping(
            cache_attr="igroup.uuid",
        ),
        FieldMapping(
            cache_attr="logical_unit_number",
            default=0,
        ),
        FieldMapping(
            cache_attr="lun.name",
        ),
        FieldMapping(
            cache_attr="lun.node.name",
        ),
        FieldMapping(
            cache_attr="lun.node.uuid",
        ),
        FieldMapping(
            cache_attr="lun.smbc.replicated",
            default=False,
        ),
        FieldMapping(
            cache_attr="lun.uuid",
        ),
        FieldMapping(
            cache_attr="reporting_nodes",
            item_model=OntapLunMapReportingNode,
            default=[],
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapLunMap", ONTAPLUNMAP_MAPPING)
