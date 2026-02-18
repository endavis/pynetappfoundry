"""OntapWebauthnGlobal type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.security.webauthn.global_settings.model import OntapWebauthnGlobal

ONTAPWEBAUTHNGLOBAL_MAPPING = TypeMapping(
    name="OntapWebauthnGlobal",
    model_class=OntapWebauthnGlobal,
    api_endpoint="/security/webauthn/global-settings?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="attestation",
            api_path="attestation",
        ),
        FieldMapping(
            cache_attr="owner_name",
            api_path="owner.name",
        ),
        FieldMapping(
            cache_attr="owner_uuid",
            api_path="owner.uuid",
        ),
        FieldMapping(
            cache_attr="require_rk",
            api_path="require_rk",
            default=False,
        ),
        FieldMapping(
            cache_attr="resident_key",
            api_path="resident_key",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="timeout",
            api_path="timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="user_verification",
            api_path="user_verification",
        ),
    ),
)

model_registry.register_mapping("OntapWebauthnGlobal", ONTAPWEBAUTHNGLOBAL_MAPPING)
