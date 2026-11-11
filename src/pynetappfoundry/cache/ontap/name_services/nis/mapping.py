"""OntapNisService type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.name_services.nis.model import (
    OntapNisService,
    OntapNisServiceBindingDetail,
)

ONTAPNISSERVICE_MAPPING = TypeMapping(
    name="OntapNisService",
    model_class=OntapNisService,
    api_endpoint="/name-services/nis?fields=*",
    api_type="ontap",
    identifier_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="binding_details",
            item_model=OntapNisServiceBindingDetail,
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
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapNisService", ONTAPNISSERVICE_MAPPING)
