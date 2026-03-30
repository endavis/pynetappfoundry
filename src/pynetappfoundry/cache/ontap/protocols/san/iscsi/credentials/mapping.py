"""OntapIscsiCredentials type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.iscsi.credentials.model import (
    OntapIscsiCredentials,
    OntapIscsiCredentialsMask,
    OntapIscsiCredentialsRange,
)


def _transform_initiator_address_masks(record: dict[str, Any]) -> list[OntapIscsiCredentialsMask]:
    """Transform initiator_address.masks into OntapIscsiCredentialsMask list."""
    return [OntapIscsiCredentialsMask(**item) for item in record.get("initiator_address.masks", [])]


def _transform_initiator_address_ranges(record: dict[str, Any]) -> list[OntapIscsiCredentialsRange]:
    """Transform initiator_address.ranges into OntapIscsiCredentialsRange list."""
    return [
        OntapIscsiCredentialsRange(**item) for item in record.get("initiator_address.ranges", [])
    ]


ONTAPISCSICREDENTIALS_MAPPING = TypeMapping(
    name="OntapIscsiCredentials",
    model_class=OntapIscsiCredentials,
    api_endpoint="/protocols/san/iscsi/credentials?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="authentication_type",
            api_path="authentication_type",
        ),
        FieldMapping(
            cache_attr="chap_inbound_password",
            api_path="chap.inbound.password",
        ),
        FieldMapping(
            cache_attr="chap_inbound_user",
            api_path="chap.inbound.user",
        ),
        FieldMapping(
            cache_attr="chap_outbound_password",
            api_path="chap.outbound.password",
        ),
        FieldMapping(
            cache_attr="chap_outbound_user",
            api_path="chap.outbound.user",
        ),
        FieldMapping(
            cache_attr="initiator",
            api_path="initiator",
        ),
        FieldMapping(
            cache_attr="initiator_address_masks",
            api_path="initiator_address.masks",
            transform=_transform_initiator_address_masks,
            default=[],
        ),
        FieldMapping(
            cache_attr="initiator_address_ranges",
            api_path="initiator_address.ranges",
            transform=_transform_initiator_address_ranges,
            default=[],
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapIscsiCredentials", ONTAPISCSICREDENTIALS_MAPPING)
