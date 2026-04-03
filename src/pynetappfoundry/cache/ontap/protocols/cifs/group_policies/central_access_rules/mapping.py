"""OntapGroupPolicyObjectCentralAccessRule type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.group_policies.central_access_rules.model import (
    OntapGroupPolicyObjectCentralAccessRule,
)

ONTAPGROUPPOLICYOBJECTCENTRALACCESSRULE_MAPPING = TypeMapping(
    name="OntapGroupPolicyObjectCentralAccessRule",
    model_class=OntapGroupPolicyObjectCentralAccessRule,
    api_endpoint="/protocols/cifs/group-policies/{svm.uuid}/central-access-rules?fields=*",
    api_type="ontap",
    parent_mapping="OntapPoliciesAndRulesToBeApplied",
    parent_id_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="create_time",
        ),
        FieldMapping(
            cache_attr="current_permission",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="proposed_permission",
        ),
        FieldMapping(
            cache_attr="resource_criteria",
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
    "OntapGroupPolicyObjectCentralAccessRule", ONTAPGROUPPOLICYOBJECTCENTRALACCESSRULE_MAPPING
)
