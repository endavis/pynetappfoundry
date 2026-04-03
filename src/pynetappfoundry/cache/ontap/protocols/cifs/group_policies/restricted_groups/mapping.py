"""OntapGroupPolicyObjectRestrictedGroup type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.group_policies.restricted_groups.model import (
    OntapGroupPolicyObjectRestrictedGroup,
)

ONTAPGROUPPOLICYOBJECTRESTRICTEDGROUP_MAPPING = TypeMapping(
    name="OntapGroupPolicyObjectRestrictedGroup",
    model_class=OntapGroupPolicyObjectRestrictedGroup,
    api_endpoint="/protocols/cifs/group-policies/{svm.uuid}/restricted-groups?fields=*",
    api_type="ontap",
    parent_mapping="OntapPoliciesAndRulesToBeApplied",
    parent_id_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="group_name",
        ),
        FieldMapping(
            cache_attr="link",
        ),
        FieldMapping(
            cache_attr="members",
            default=[],
        ),
        FieldMapping(
            cache_attr="memberships",
            default=[],
        ),
        FieldMapping(
            cache_attr="policy_name",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="version",
            default=0,
        ),
    ),
)

model_registry.register_mapping(
    "OntapGroupPolicyObjectRestrictedGroup", ONTAPGROUPPOLICYOBJECTRESTRICTEDGROUP_MAPPING
)
