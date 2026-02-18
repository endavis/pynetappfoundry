"""OntapGroupPolicyObjectCentralAccessRule type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.cifs.group_policies.central_access_rules.model import (
    OntapGroupPolicyObjectCentralAccessRule,
)

ONTAPGROUPPOLICYOBJECTCENTRALACCESSRULE_MAPPING = TypeMapping(
    name="OntapGroupPolicyObjectCentralAccessRule",
    model_class=OntapGroupPolicyObjectCentralAccessRule,
    api_endpoint="/protocols/cifs/group-policies/{svm.uuid}/central-access-rules?fields=*",
    api_type="ontap",
    parent_mapping="OntapPoliciesAndRulesToBeApplied",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="create_time",
            api_path="create_time",
        ),
        FieldMapping(
            cache_attr="current_permission",
            api_path="current_permission",
        ),
        FieldMapping(
            cache_attr="description",
            api_path="description",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="proposed_permission",
            api_path="proposed_permission",
        ),
        FieldMapping(
            cache_attr="resource_criteria",
            api_path="resource_criteria",
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
            cache_attr="update_time",
            api_path="update_time",
        ),
    ),
)

model_registry.register_mapping(
    "OntapGroupPolicyObjectCentralAccessRule", ONTAPGROUPPOLICYOBJECTCENTRALACCESSRULE_MAPPING
)
