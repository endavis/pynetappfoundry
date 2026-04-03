"""OntapEmsRoleConfigResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.ems.role_configs.model import OntapEmsRoleConfigResponse

ONTAPEMSROLECONFIGRESPONSE_MAPPING = TypeMapping(
    name="OntapEmsRoleConfigResponse",
    model_class=OntapEmsRoleConfigResponse,
    api_endpoint="/support/ems/role-configs?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="access_control_role.name",
        ),
        FieldMapping(
            cache_attr="event_filter.name",
        ),
        FieldMapping(
            cache_attr="limit_access_to_global_configs",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapEmsRoleConfigResponse", ONTAPEMSROLECONFIGRESPONSE_MAPPING)
