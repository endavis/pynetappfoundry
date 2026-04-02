"""OntapNisService type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.name_services.nis.model import (
    OntapNisService,
    OntapNisServiceBindingDetail,
)


def _transform_binding_details(record: dict[str, Any]) -> list[OntapNisServiceBindingDetail]:
    """Transform binding_details into OntapNisServiceBindingDetail list."""
    return [OntapNisServiceBindingDetail(**item) for item in record.get("binding_details", [])]


ONTAPNISSERVICE_MAPPING = TypeMapping(
    name="OntapNisService",
    model_class=OntapNisService,
    api_endpoint="/name-services/nis?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="binding_details",
            api_path="binding_details",
            transform=_transform_binding_details,
            default=[],
        ),
        FieldMapping(
            cache_attr="bound_servers",
            api_path="bound_servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="domain",
            api_path="domain",
        ),
        FieldMapping(
            cache_attr="servers",
            api_path="servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapNisService", ONTAPNISSERVICE_MAPPING)
