"""SnapMirror type mapping definition for the declarative field mapping framework.

Defines SNAPMIRROR_MAPPING which maps ONTAP REST API SnapMirror relationship
data to SnapMirrorRelationship cache model attributes. SnapMirror is API-only
-- there is no CLI command for this data.

All fields use simple ``api_path`` dot notation with no transform functions.
The ``source.path`` and ``destination.path`` fields already contain the full
``"svm:volume"`` formatted string per the ONTAP REST API.
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.snapmirror.relationships.model import SnapMirrorRelationship

SNAPMIRROR_MAPPING = TypeMapping(
    name="SnapMirror",
    model_class=SnapMirrorRelationship,
    api_endpoint=(
        "/snapmirror/relationships"
        "?fields=uuid,source.path,destination.path,policy.type,policy.uuid,"
        "throttle,group_type,transfer_schedule.uuid"
    ),
    cli_command="",
    id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="source_path",
            api_path="source.path",
        ),
        FieldMapping(
            cache_attr="destination_path",
            api_path="destination.path",
        ),
        FieldMapping(
            cache_attr="relationship_type",
            api_path="policy.type",
        ),
        FieldMapping(
            cache_attr="policy_uuid",
            api_path="policy.uuid",
        ),
        FieldMapping(
            cache_attr="throttle",
            api_path="throttle",
            default=0,
        ),
        FieldMapping(
            cache_attr="group_type",
            api_path="group_type",
        ),
        FieldMapping(
            cache_attr="transfer_schedule_uuid",
            api_path="transfer_schedule.uuid",
        ),
    ),
)

model_registry.register_mapping("SnapMirror", SNAPMIRROR_MAPPING)
