"""OntapIscsiCredentials type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.iscsi.credentials.model import (
    OntapIscsiCredentials,
    OntapIscsiCredentialsInitiatorAddressMask,
    OntapIscsiCredentialsInitiatorAddressRange,
)

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
            item_model=OntapIscsiCredentialsInitiatorAddressMask,
            default=[],
        ),
        FieldMapping(
            cache_attr="initiator_address.ranges",
            item_model=OntapIscsiCredentialsInitiatorAddressRange,
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
