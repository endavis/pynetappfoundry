# ruff: noqa: E501
"""OntapPoliciesAndRulesToBeApplied type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.group_policies.model import (
    OntapPoliciesAndRulesToBeApplied,
    OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessPolicy,
    OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessRule,
    OntapPoliciesAndRulesToBeAppliedToBeAppliedObject,
    OntapPoliciesAndRulesToBeAppliedToBeAppliedRestrictedGroup,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_to_be_applied_access_policies(
    record: dict[str, Any],
) -> list[OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessPolicy]:
    """Transform to_be_applied.access_policies into OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessPolicy list."""
    try:
        items = get_nested_value(record, "to_be_applied.access_policies")
    except Exception:
        items = []
    return [OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessPolicy(**item) for item in items]


def _transform_to_be_applied_access_rules(
    record: dict[str, Any],
) -> list[OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessRule]:
    """Transform to_be_applied.access_rules into OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessRule list."""
    try:
        items = get_nested_value(record, "to_be_applied.access_rules")
    except Exception:
        items = []
    return [OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessRule(**item) for item in items]


def _transform_to_be_applied_objects(
    record: dict[str, Any],
) -> list[OntapPoliciesAndRulesToBeAppliedToBeAppliedObject]:
    """Transform to_be_applied.objects into OntapPoliciesAndRulesToBeAppliedToBeAppliedObject list."""
    try:
        items = get_nested_value(record, "to_be_applied.objects")
    except Exception:
        items = []
    return [OntapPoliciesAndRulesToBeAppliedToBeAppliedObject(**item) for item in items]


def _transform_to_be_applied_restricted_groups(
    record: dict[str, Any],
) -> list[OntapPoliciesAndRulesToBeAppliedToBeAppliedRestrictedGroup]:
    """Transform to_be_applied.restricted_groups into OntapPoliciesAndRulesToBeAppliedToBeAppliedRestrictedGroup list."""
    try:
        items = get_nested_value(record, "to_be_applied.restricted_groups")
    except Exception:
        items = []
    return [OntapPoliciesAndRulesToBeAppliedToBeAppliedRestrictedGroup(**item) for item in items]


ONTAPPOLICIESANDRULESTOBEAPPLIED_MAPPING = TypeMapping(
    name="OntapPoliciesAndRulesToBeApplied",
    model_class=OntapPoliciesAndRulesToBeApplied,
    api_endpoint="/protocols/cifs/group-policies?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="to_be_applied.access_policies",
            api_path="to_be_applied.access_policies",
            transform=_transform_to_be_applied_access_policies,
            default=[],
        ),
        FieldMapping(
            cache_attr="to_be_applied.access_rules",
            api_path="to_be_applied.access_rules",
            transform=_transform_to_be_applied_access_rules,
            default=[],
        ),
        FieldMapping(
            cache_attr="to_be_applied.objects",
            api_path="to_be_applied.objects",
            transform=_transform_to_be_applied_objects,
            default=[],
        ),
        FieldMapping(
            cache_attr="to_be_applied.restricted_groups",
            api_path="to_be_applied.restricted_groups",
            transform=_transform_to_be_applied_restricted_groups,
            default=[],
        ),
    ),
)

model_registry.register_mapping(
    "OntapPoliciesAndRulesToBeApplied", ONTAPPOLICIESANDRULESTOBEAPPLIED_MAPPING
)
