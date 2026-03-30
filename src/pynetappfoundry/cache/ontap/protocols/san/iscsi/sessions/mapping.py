"""OntapIscsiSession type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.iscsi.sessions.model import (
    OntapIscsiSession,
    OntapIscsiSessionConnection,
    OntapIscsiSessionIgroup,
)


def _transform_connections(record: dict[str, Any]) -> list[OntapIscsiSessionConnection]:
    """Transform connections into OntapIscsiSessionConnection list."""
    return [OntapIscsiSessionConnection(**item) for item in record.get("connections", [])]


def _transform_igroups(record: dict[str, Any]) -> list[OntapIscsiSessionIgroup]:
    """Transform igroups into OntapIscsiSessionIgroup list."""
    return [OntapIscsiSessionIgroup(**item) for item in record.get("igroups", [])]


ONTAPISCSISESSION_MAPPING = TypeMapping(
    name="OntapIscsiSession",
    model_class=OntapIscsiSession,
    api_endpoint="/protocols/san/iscsi/sessions?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="connections",
            api_path="connections",
            transform=_transform_connections,
            default=[],
        ),
        FieldMapping(
            cache_attr="igroups",
            api_path="igroups",
            transform=_transform_igroups,
            default=[],
        ),
        FieldMapping(
            cache_attr="initiator_alias",
            api_path="initiator.alias",
        ),
        FieldMapping(
            cache_attr="initiator_comment",
            api_path="initiator.comment",
        ),
        FieldMapping(
            cache_attr="initiator_name",
            api_path="initiator.name",
        ),
        FieldMapping(
            cache_attr="isid",
            api_path="isid",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="target_portal_group",
            api_path="target_portal_group",
        ),
        FieldMapping(
            cache_attr="target_portal_group_tag",
            api_path="target_portal_group_tag",
            default=0,
        ),
        FieldMapping(
            cache_attr="tsih",
            api_path="tsih",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapIscsiSession", ONTAPISCSISESSION_MAPPING)
