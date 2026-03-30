"""OntapAutoUpdateInfo type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.auto_update.model import OntapAutoUpdateInfo

ONTAPAUTOUPDATEINFO_MAPPING = TypeMapping(
    name="OntapAutoUpdateInfo",
    model_class=OntapAutoUpdateInfo,
    api_endpoint="/support/auto-update?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="eula_accepted",
            api_path="eula.accepted",
            default=False,
        ),
        FieldMapping(
            cache_attr="eula_accepted_ip_address",
            api_path="eula.accepted_ip_address",
        ),
        FieldMapping(
            cache_attr="eula_accepted_timestamp",
            api_path="eula.accepted_timestamp",
        ),
        FieldMapping(
            cache_attr="eula_user_id_accepted",
            api_path="eula.user_id_accepted",
        ),
    ),
)

model_registry.register_mapping("OntapAutoUpdateInfo", ONTAPAUTOUPDATEINFO_MAPPING)
