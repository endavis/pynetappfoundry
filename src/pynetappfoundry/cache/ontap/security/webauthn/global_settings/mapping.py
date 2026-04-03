"""OntapWebauthnGlobal type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.webauthn.global_settings.model import OntapWebauthnGlobal

ONTAPWEBAUTHNGLOBAL_MAPPING = TypeMapping(
    name="OntapWebauthnGlobal",
    model_class=OntapWebauthnGlobal,
    api_endpoint="/security/webauthn/global-settings?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="attestation",
        ),
        FieldMapping(
            cache_attr="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
        ),
        FieldMapping(
            cache_attr="require_rk",
            default=False,
        ),
        FieldMapping(
            cache_attr="resident_key",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="user_verification",
        ),
    ),
)

model_registry.register_mapping("OntapWebauthnGlobal", ONTAPWEBAUTHNGLOBAL_MAPPING)
