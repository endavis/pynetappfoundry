"""OntapAccount type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.accounts.model import (
    OntapAccount,
    OntapAccountApplication,
)

ONTAPACCOUNT_MAPPING = TypeMapping(
    name="OntapAccount",
    model_class=OntapAccount,
    api_endpoint="/security/accounts?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="applications",
            item_model=OntapAccountApplication,
            default=[],
        ),
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="locked",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
        ),
        FieldMapping(
            cache_attr="password",
        ),
        FieldMapping(
            cache_attr="password_hash_algorithm",
        ),
        FieldMapping(
            cache_attr="role.name",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
    ),
)

model_registry.register_mapping("OntapAccount", ONTAPACCOUNT_MAPPING)
