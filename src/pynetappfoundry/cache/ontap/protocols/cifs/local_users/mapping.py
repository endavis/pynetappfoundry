"""OntapLocalCifsUser type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.local_users.model import (
    OntapLocalCifsUser,
    OntapLocalCifsUserMembership,
)


def _transform_membership(record: dict[str, Any]) -> list[OntapLocalCifsUserMembership]:
    """Transform membership into OntapLocalCifsUserMembership list."""
    return [OntapLocalCifsUserMembership(**item) for item in record.get("membership", [])]


ONTAPLOCALCIFSUSER_MAPPING = TypeMapping(
    name="OntapLocalCifsUser",
    model_class=OntapLocalCifsUser,
    api_endpoint="/protocols/cifs/local-users?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="account_disabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="full_name",
        ),
        FieldMapping(
            cache_attr="membership",
            transform=_transform_membership,
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="password",
        ),
        FieldMapping(
            cache_attr="sid",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapLocalCifsUser", ONTAPLOCALCIFSUSER_MAPPING)
