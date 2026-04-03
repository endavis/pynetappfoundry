"""OntapFpolicyPolicy type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.fpolicy.policies.model import (
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
    parent_mapping="OntapSvm",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="allow_privileged_access",
            default=False,
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="engine.name",
        ),
        FieldMapping(
            cache_attr="events",
            transform=_transform_events,
            default=[],
        ),
        FieldMapping(
            cache_attr="mandatory",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="passthrough_read",
            default=False,
        ),
        FieldMapping(
            cache_attr="persistent_store",
        ),
        FieldMapping(
            cache_attr="priority",
            default=0,
        ),
        FieldMapping(
            cache_attr="privileged_user",
        ),
        FieldMapping(
            cache_attr="scope.check_extensions_on_directories",
            default=False,
        ),
        FieldMapping(
            cache_attr="scope.exclude_export_policies",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope.exclude_extension",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope.exclude_shares",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope.exclude_volumes",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope.include_export_policies",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope.include_extension",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope.include_shares",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope.include_volumes",
            default=[],
        ),
        FieldMapping(
            cache_attr="scope.object_monitoring_with_no_extension",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapFpolicyPolicy", ONTAPFPOLICYPOLICY_MAPPING)
