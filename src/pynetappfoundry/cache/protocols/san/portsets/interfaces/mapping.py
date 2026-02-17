"""OntapPortsetInterface type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.protocols.san.portsets.interfaces.model import (
    OntapPortsetInterface,
    OntapPortsetInterfaceRecord,
)


def _transform_records(record: dict[str, Any]) -> list[OntapPortsetInterfaceRecord]:
    """Transform records into OntapPortsetInterfaceRecord list."""
    return [OntapPortsetInterfaceRecord(**item) for item in record.get("records", [])]


ONTAPPORTSETINTERFACE_MAPPING = TypeMapping(
    name="OntapPortsetInterface",
    model_class=OntapPortsetInterface,
    api_endpoint="/protocols/san/portsets/{portset.uuid}/interfaces?fields=*",
    api_type="ontap",
    parent_mapping="OntapPortset",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="fc_name",
            api_path="fc.name",
        ),
        FieldMapping(
            cache_attr="fc_uuid",
            api_path="fc.uuid",
        ),
        FieldMapping(
            cache_attr="fc_wwpn",
            api_path="fc.wwpn",
        ),
        FieldMapping(
            cache_attr="ip_ip_address",
            api_path="ip.ip.address",
        ),
        FieldMapping(
            cache_attr="ip_name",
            api_path="ip.name",
        ),
        FieldMapping(
            cache_attr="ip_uuid",
            api_path="ip.uuid",
        ),
        FieldMapping(
            cache_attr="portset_uuid",
            api_path="portset.uuid",
        ),
        FieldMapping(
            cache_attr="records",
            transform=_transform_records,
            default=[],
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapPortsetInterface", ONTAPPORTSETINTERFACE_MAPPING)
