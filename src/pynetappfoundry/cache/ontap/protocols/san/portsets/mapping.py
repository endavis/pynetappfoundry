"""OntapPortset type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.portsets.model import (
    OntapPortset,
    OntapPortsetIgroup,
    OntapPortsetInterface,
)


def _transform_igroups(record: dict[str, Any]) -> list[OntapPortsetIgroup]:
    """Transform igroups into OntapPortsetIgroup list."""
    return [OntapPortsetIgroup(**item) for item in record.get("igroups", [])]


def _transform_interfaces(record: dict[str, Any]) -> list[OntapPortsetInterface]:
    """Transform interfaces into OntapPortsetInterface list."""
    return [OntapPortsetInterface(**item) for item in record.get("interfaces", [])]


ONTAPPORTSET_MAPPING = TypeMapping(
    name="OntapPortset",
    model_class=OntapPortset,
    api_endpoint="/protocols/san/portsets?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="igroups",
            api_path="igroups",
            transform=_transform_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="interfaces",
            api_path="interfaces",
            transform=_transform_interfaces,
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="protocol",
            api_path="protocol",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapPortset", ONTAPPORTSET_MAPPING)
