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
            api_path="igroups",
            transform=_transform_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="initiator.aliases",
            api_path="initiator.aliases",
            default=[],
        ),
        FieldMapping(
            cache_attr="initiator.comment",
            api_path="initiator.comment",
        ),
        FieldMapping(
            cache_attr="initiator.port_address",
            api_path="initiator.port_address",
        ),
        FieldMapping(
            cache_attr="initiator.wwnn",
            api_path="initiator.wwnn",
        ),
        FieldMapping(
            cache_attr="initiator.wwpn",
            api_path="initiator.wwpn",
        ),
        FieldMapping(
            cache_attr="interface.name",
            api_path="interface.name",
        ),
        FieldMapping(
            cache_attr="interface.uuid",
            api_path="interface.uuid",
        ),
        FieldMapping(
            cache_attr="interface.wwpn",
            api_path="interface.wwpn",
        ),
        FieldMapping(
            cache_attr="protocol",
            api_path="protocol",
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapFcLogin", ONTAPFCLOGIN_MAPPING)
