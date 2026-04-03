"""OntapSupportedAlgorithms type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.webauthn.supported_algorithms.model import (
    OntapSupportedAlgorithms,
)

ONTAPSUPPORTEDALGORITHMS_MAPPING = TypeMapping(
    name="OntapSupportedAlgorithms",
    model_class=OntapSupportedAlgorithms,
    api_endpoint="/security/webauthn/supported-algorithms?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="algorithm.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="algorithm.name",
        ),
        FieldMapping(
            cache_attr="algorithm.type_",
            api_path="algorithm.type",
        ),
        FieldMapping(
            cache_attr="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
    ),
)

model_registry.register_mapping("OntapSupportedAlgorithms", ONTAPSUPPORTEDALGORITHMS_MAPPING)
