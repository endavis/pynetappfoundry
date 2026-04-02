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
    fields=(
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
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
            cache_attr="ttl",
            api_path="ttl",
        ),
    ),
)

model_registry.register_mapping(
    "OntapGroupMembershipSettings", ONTAPGROUPMEMBERSHIPSETTINGS_MAPPING
)
