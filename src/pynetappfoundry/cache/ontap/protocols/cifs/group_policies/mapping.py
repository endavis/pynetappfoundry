# ruff: noqa: E501
"""OntapPoliciesAndRulesToBeApplied type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.group_policies.model import (
    OntapPoliciesAndRulesToBeApplied,
    OntapPoliciesAndRulesToBeAppliedAccessPolicy,
    OntapPoliciesAndRulesToBeAppliedAccessRule,
    OntapPoliciesAndRulesToBeAppliedObject,
    OntapPoliciesAndRulesToBeAppliedRestrictedGroup,
)


def _transform_to_be_applied_access_policies(
    record: dict[str, Any],
) -> list[OntapPoliciesAndRulesToBeAppliedAccessPolicy]:
    """Transform to_be_applied.access_policies into OntapPoliciesAndRulesToBeAppliedAccessPolicy list."""
    return [
        OntapPoliciesAndRulesToBeAppliedAccessPolicy(**item)
        for item in record.get("to_be_applied.access_policies", [])
    ]


def _transform_to_be_applied_access_rules(
    record: dict[str, Any],
) -> list[OntapPoliciesAndRulesToBeAppliedAccessRule]:
    """Transform to_be_applied.access_rules into OntapPoliciesAndRulesToBeAppliedAccessRule list."""
    return [
        OntapPoliciesAndRulesToBeAppliedAccessRule(**item)
        for item in record.get("to_be_applied.access_rules", [])
    ]


def _transform_to_be_applied_objects(
    record: dict[str, Any],
) -> list[OntapPoliciesAndRulesToBeAppliedObject]:
    """Transform to_be_applied.objects into OntapPoliciesAndRulesToBeAppliedObject list."""
    return [
        OntapPoliciesAndRulesToBeAppliedObject(**item)
        for item in record.get("to_be_applied.objects", [])
    ]


def _transform_to_be_applied_restricted_groups(
    record: dict[str, Any],
) -> list[OntapPoliciesAndRulesToBeAppliedRestrictedGroup]:
    """Transform to_be_applied.restricted_groups into OntapPoliciesAndRulesToBeAppliedRestrictedGroup list."""
    return [
        OntapPoliciesAndRulesToBeAppliedRestrictedGroup(**item)
        for item in record.get("to_be_applied.restricted_groups", [])
    ]


ONTAPPOLICIESANDRULESTOBEAPPLIED_MAPPING = TypeMapping(
    name="OntapPoliciesAndRulesToBeApplied",
    model_class=OntapPoliciesAndRulesToBeApplied,
    api_endpoint="/protocols/cifs/group-policies?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="to_be_applied_access_policies",
            api_path="to_be_applied.access_policies",
            transform=_transform_to_be_applied_access_policies,
            default=[],
        ),
        FieldMapping(
            cache_attr="to_be_applied_access_rules",
            api_path="to_be_applied.access_rules",
            transform=_transform_to_be_applied_access_rules,
            default=[],
        ),
        FieldMapping(
            cache_attr="to_be_applied_objects",
            api_path="to_be_applied.objects",
            transform=_transform_to_be_applied_objects,
            default=[],
        ),
        FieldMapping(
            cache_attr="to_be_applied_restricted_groups",
            api_path="to_be_applied.restricted_groups",
            transform=_transform_to_be_applied_restricted_groups,
            default=[],
        ),
    ),
)

model_registry.register_mapping(
    "OntapPoliciesAndRulesToBeApplied", ONTAPPOLICIESANDRULESTOBEAPPLIED_MAPPING
)
