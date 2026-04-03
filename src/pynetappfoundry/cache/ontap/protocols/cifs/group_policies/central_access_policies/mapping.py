# ruff: noqa: E501
"""OntapGroupPolicyObjectCentralAccessPolicy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.group_policies.central_access_policies.model import (
    OntapGroupPolicyObjectCentralAccessPolicy,
)

ONTAPGROUPPOLICYOBJECTCENTRALACCESSPOLICY_MAPPING = TypeMapping(
    name="OntapGroupPolicyObjectCentralAccessPolicy",
    model_class=OntapGroupPolicyObjectCentralAccessPolicy,
    api_endpoint="/protocols/cifs/group-policies/{svm.uuid}/central-access-policies?fields=*",
    api_type="ontap",
    parent_mapping="OntapPoliciesAndRulesToBeApplied",
    parent_id_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="create_time",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="member_rules",
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="sid",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="update_time",
        ),
    ),
)

model_registry.register_mapping(
    "OntapGroupPolicyObjectCentralAccessPolicy", ONTAPGROUPPOLICYOBJECTCENTRALACCESSPOLICY_MAPPING
)
