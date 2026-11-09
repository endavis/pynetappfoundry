"""OntapClusterNisService type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.authentication.cluster.nis.model import (
    OntapClusterNisService,
    OntapClusterNisServiceBindingDetail,
)


def _transform_binding_details(record: dict[str, Any]) -> list[OntapClusterNisServiceBindingDetail]:
    """Transform binding_details into OntapClusterNisServiceBindingDetail list."""
    return [
        OntapClusterNisServiceBindingDetail(**item) for item in record.get("binding_details", [])
    ]


ONTAPCLUSTERNISSERVICE_MAPPING = TypeMapping(
    name="OntapClusterNisService",
    model_class=OntapClusterNisService,
    api_endpoint="/security/authentication/cluster/nis?fields=*",
    api_type="ontap",
    response_shape="singleton",
    fields=(
        FieldMapping(
            cache_attr="binding_details",
            transform=_transform_binding_details,
            default=[],
        ),
        FieldMapping(
            cache_attr="bound_servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="domain",
        ),
        FieldMapping(
            cache_attr="servers",
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapClusterNisService", ONTAPCLUSTERNISSERVICE_MAPPING)
