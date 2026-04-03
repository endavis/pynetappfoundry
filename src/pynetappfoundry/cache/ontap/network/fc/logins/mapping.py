"""OntapFcLogin type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.fc.logins.model import OntapFcLogin, OntapFcLoginIgroup


def _transform_igroups(record: dict[str, Any]) -> list[OntapFcLoginIgroup]:
    """Transform igroups into OntapFcLoginIgroup list."""
    return [OntapFcLoginIgroup(**item) for item in record.get("igroups", [])]


ONTAPFCLOGIN_MAPPING = TypeMapping(
    name="OntapFcLogin",
    model_class=OntapFcLogin,
    api_endpoint="/network/fc/logins?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="igroups",
            transform=_transform_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="initiator.aliases",
            default=[],
        ),
        FieldMapping(
            cache_attr="initiator.comment",
        ),
        FieldMapping(
            cache_attr="initiator.port_address",
        ),
        FieldMapping(
            cache_attr="initiator.wwnn",
        ),
        FieldMapping(
            cache_attr="initiator.wwpn",
        ),
        FieldMapping(
            cache_attr="interface.name",
        ),
        FieldMapping(
            cache_attr="interface.uuid",
        ),
        FieldMapping(
            cache_attr="interface.wwpn",
        ),
        FieldMapping(
            cache_attr="protocol",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapFcLogin", ONTAPFCLOGIN_MAPPING)
