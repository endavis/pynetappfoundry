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
            api_path="create_time",
        ),
        FieldMapping(
            cache_attr="description",
            api_path="description",
        ),
        FieldMapping(
            cache_attr="member_rules",
            api_path="member_rules",
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="sid",
            api_path="sid",
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="update_time",
            api_path="update_time",
        ),
    ),
)

model_registry.register_mapping(
    "OntapGroupPolicyObjectCentralAccessPolicy", ONTAPGROUPPOLICYOBJECTCENTRALACCESSPOLICY_MAPPING
)
