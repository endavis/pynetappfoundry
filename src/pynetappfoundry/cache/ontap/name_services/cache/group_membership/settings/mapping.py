"""OntapGroupMembershipSettings type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.name_services.cache.group_membership.settings.model import (
    OntapGroupMembershipSettings,
)

ONTAPGROUPMEMBERSHIPSETTINGS_MAPPING = TypeMapping(
    name="OntapGroupMembershipSettings",
    model_class=OntapGroupMembershipSettings,
    api_endpoint="/name-services/cache/group-membership/settings?fields=*",
    api_type="ontap",
    identifier_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="ttl",
        ),
    ),
)

model_registry.register_mapping(
    "OntapGroupMembershipSettings", ONTAPGROUPMEMBERSHIPSETTINGS_MAPPING
)
