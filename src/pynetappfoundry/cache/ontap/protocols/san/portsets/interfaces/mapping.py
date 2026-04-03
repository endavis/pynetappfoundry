"""OntapPortsetInterface type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.portsets.interfaces.model import (
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
            cache_attr="fc.name",
        ),
        FieldMapping(
            cache_attr="fc.uuid",
        ),
        FieldMapping(
            cache_attr="fc.wwpn",
        ),
        FieldMapping(
            cache_attr="ip.ip.address",
        ),
        FieldMapping(
            cache_attr="ip.name",
        ),
        FieldMapping(
            cache_attr="ip.uuid",
        ),
        FieldMapping(
            cache_attr="portset.uuid",
        ),
        FieldMapping(
            cache_attr="records",
            transform=_transform_records,
            default=[],
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapPortsetInterface", ONTAPPORTSETINTERFACE_MAPPING)
