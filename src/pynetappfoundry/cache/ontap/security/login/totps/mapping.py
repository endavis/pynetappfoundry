"""OntapTotp type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.login.totps.model import OntapTotp

ONTAPTOTP_MAPPING = TypeMapping(
    name="OntapTotp",
    model_class=OntapTotp,
    api_endpoint="/security/login/totps?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="account.name",
            api_path="account.name",
        ),
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="owner.name",
            api_path="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
            api_path="owner.uuid",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="sha_fingerprint",
            api_path="sha_fingerprint",
        ),
    ),
)

model_registry.register_mapping("OntapTotp", ONTAPTOTP_MAPPING)
