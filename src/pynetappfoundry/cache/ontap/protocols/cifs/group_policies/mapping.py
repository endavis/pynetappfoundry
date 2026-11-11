"""OntapPoliciesAndRulesToBeApplied type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.group_policies.model import (
    OntapPoliciesAndRulesToBeApplied,
    OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessPolicy,
    OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessRule,
    OntapPoliciesAndRulesToBeAppliedToBeAppliedObject,
    OntapPoliciesAndRulesToBeAppliedToBeAppliedRestrictedGroup,
)

ONTAPPOLICIESANDRULESTOBEAPPLIED_MAPPING = TypeMapping(
    name="OntapPoliciesAndRulesToBeApplied",
    model_class=OntapPoliciesAndRulesToBeApplied,
    api_endpoint="/protocols/cifs/group-policies?fields=*",
    api_type="ontap",
    identifier_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="to_be_applied.access_policies",
            item_model=OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessPolicy,
            default=[],
        ),
        FieldMapping(
            cache_attr="to_be_applied.access_rules",
            item_model=OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessRule,
            default=[],
        ),
        FieldMapping(
            cache_attr="to_be_applied.objects",
            item_model=OntapPoliciesAndRulesToBeAppliedToBeAppliedObject,
            default=[],
        ),
        FieldMapping(
            cache_attr="to_be_applied.restricted_groups",
            item_model=OntapPoliciesAndRulesToBeAppliedToBeAppliedRestrictedGroup,
            default=[],
        ),
    ),
)

model_registry.register_mapping(
    "OntapPoliciesAndRulesToBeApplied", ONTAPPOLICIESANDRULESTOBEAPPLIED_MAPPING
)
