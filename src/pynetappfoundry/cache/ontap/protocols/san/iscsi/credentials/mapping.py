"""OntapIscsiCredentials type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.iscsi.credentials.model import (
    OntapIscsiCredentials,
    OntapIscsiCredentialsInitiatorAddressMask,
    OntapIscsiCredentialsInitiatorAddressRange,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_initiator_address_masks(
    record: dict[str, Any],
) -> list[OntapIscsiCredentialsInitiatorAddressMask]:
    """Transform initiator_address.masks into OntapIscsiCredentialsInitiatorAddressMask list."""
    try:
        items = get_nested_value(record, "initiator_address.masks")
    except Exception:
        items = []
    return [OntapIscsiCredentialsInitiatorAddressMask(**item) for item in items]


def _transform_initiator_address_ranges(
    record: dict[str, Any],
) -> list[OntapIscsiCredentialsInitiatorAddressRange]:
    """Transform initiator_address.ranges into OntapIscsiCredentialsInitiatorAddressRange list."""
    try:
        items = get_nested_value(record, "initiator_address.ranges")
    except Exception:
        items = []
    return [OntapIscsiCredentialsInitiatorAddressRange(**item) for item in items]


ONTAPISCSICREDENTIALS_MAPPING = TypeMapping(
    name="OntapIscsiCredentials",
    model_class=OntapIscsiCredentials,
    api_endpoint="/protocols/san/iscsi/credentials?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="authentication_type",
        ),
        FieldMapping(
            cache_attr="chap.inbound.password",
        ),
        FieldMapping(
            cache_attr="chap.inbound.user",
        ),
        FieldMapping(
            cache_attr="chap.outbound.password",
        ),
        FieldMapping(
            cache_attr="chap.outbound.user",
        ),
        FieldMapping(
            cache_attr="initiator",
        ),
        FieldMapping(
            cache_attr="initiator_address.masks",
            transform=_transform_initiator_address_masks,
            default=[],
        ),
        FieldMapping(
            cache_attr="initiator_address.ranges",
            transform=_transform_initiator_address_ranges,
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

model_registry.register_mapping("OntapIscsiCredentials", ONTAPISCSICREDENTIALS_MAPPING)
