"""OntapIscsiSession type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.iscsi.sessions.model import (
    OntapIscsiSession,
    OntapIscsiSessionConnection,
    OntapIscsiSessionIgroup,
)

ONTAPISCSISESSION_MAPPING = TypeMapping(
    name="OntapIscsiSession",
    model_class=OntapIscsiSession,
    api_endpoint="/protocols/san/iscsi/sessions?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="connections",
            item_model=OntapIscsiSessionConnection,
            default=[],
        ),
        FieldMapping(
            cache_attr="igroups",
            item_model=OntapIscsiSessionIgroup,
            default=[],
        ),
        FieldMapping(
            cache_attr="initiator.alias",
        ),
        FieldMapping(
            cache_attr="initiator.comment",
        ),
        FieldMapping(
            cache_attr="initiator.name",
        ),
        FieldMapping(
            cache_attr="isid",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="target_portal_group",
        ),
        FieldMapping(
            cache_attr="target_portal_group_tag",
            default=0,
        ),
        FieldMapping(
            cache_attr="tsih",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapIscsiSession", ONTAPISCSISESSION_MAPPING)
