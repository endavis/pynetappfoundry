"""OntapFpolicyPolicy type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.protocols.fpolicy.policies.model import (
    OntapFpolicyPolicy,
    OntapFpolicyPolicyEvent,
)


def _transform_events(record: dict[str, Any]) -> list[OntapFpolicyPolicyEvent]:
    """Transform events into OntapFpolicyPolicyEvent list."""
    return [OntapFpolicyPolicyEvent(**item) for item in record.get("events", [])]


ONTAPFPOLICYPOLICY_MAPPING = TypeMapping(
    name="OntapFpolicyPolicy",
    model_class=OntapFpolicyPolicy,
    api_endpoint="/protocols/fpolicy/{svm.uuid}/policies?fields=*",
    api_type="ontap",
    parent_mapping="OntapProtocolsFpolicy",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="allow_privileged_access",
            api_path="allow_privileged_access",
            default=False,
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="engine_name",
            api_path="engine.name",
        ),
        FieldMapping(
            cache_attr="events",
            transform=_transform_events,
            default=[],
        ),
        FieldMapping(
            cache_attr="mandatory",
            api_path="mandatory",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="passthrough_read",
            api_path="passthrough_read",
            default=False,
        ),
        FieldMapping(
            cache_attr="persistent_store",
            api_path="persistent_store",
        ),
        FieldMapping(
            cache_attr="priority",
            api_path="priority",
            default=0,
        ),
        FieldMapping(
            cache_attr="privileged_user",
            api_path="privileged_user",
        ),
        FieldMapping(
            cache_attr="scope_check_extensions_on_directories",
            api_path="scope.check_extensions_on_directories",
            default=False,
        ),
        FieldMapping(
            cache_attr="scope_exclude_export_policies",
            api_path="scope.exclude_export_policies",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope_exclude_extension",
            api_path="scope.exclude_extension",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope_exclude_shares",
            api_path="scope.exclude_shares",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope_exclude_volumes",
            api_path="scope.exclude_volumes",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope_include_export_policies",
            api_path="scope.include_export_policies",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope_include_extension",
            api_path="scope.include_extension",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope_include_shares",
            api_path="scope.include_shares",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope_include_volumes",
            api_path="scope.include_volumes",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope_object_monitoring_with_no_extension",
            api_path="scope.object_monitoring_with_no_extension",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapFpolicyPolicy", ONTAPFPOLICYPOLICY_MAPPING)
