"""OntapLunMap type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.protocols.san.lun_maps.model import OntapLunMap, OntapLunMapReportingNode


def _transform_reporting_nodes(record: dict[str, Any]) -> list[OntapLunMapReportingNode]:
    """Transform reporting_nodes into OntapLunMapReportingNode list."""
    return [OntapLunMapReportingNode(**item) for item in record.get("reporting_nodes", [])]


ONTAPLUNMAP_MAPPING = TypeMapping(
    name="OntapLunMap",
    model_class=OntapLunMap,
    api_endpoint="/protocols/san/lun-maps?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="igroup_initiators",
            api_path="igroup.initiators",
            default=[],
        ),
        FieldMapping(
            cache_attr="igroup_name",
            api_path="igroup.name",
        ),
        FieldMapping(
            cache_attr="igroup_os_type",
            api_path="igroup.os_type",
        ),
        FieldMapping(
            cache_attr="igroup_protocol",
            api_path="igroup.protocol",
        ),
        FieldMapping(
            cache_attr="igroup_replicated",
            api_path="igroup.replicated",
            default=False,
        ),
        FieldMapping(
            cache_attr="igroup_uuid",
            api_path="igroup.uuid",
        ),
        FieldMapping(
            cache_attr="logical_unit_number",
            api_path="logical_unit_number",
            default=0,
        ),
        FieldMapping(
            cache_attr="lun_name",
            api_path="lun.name",
        ),
        FieldMapping(
            cache_attr="lun_node_name",
            api_path="lun.node.name",
        ),
        FieldMapping(
            cache_attr="lun_node_uuid",
            api_path="lun.node.uuid",
        ),
        FieldMapping(
            cache_attr="lun_smbc_replicated",
            api_path="lun.smbc.replicated",
            default=False,
        ),
        FieldMapping(
            cache_attr="lun_uuid",
            api_path="lun.uuid",
        ),
        FieldMapping(
            cache_attr="reporting_nodes",
            transform=_transform_reporting_nodes,
            default=[],
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapLunMap", ONTAPLUNMAP_MAPPING)
