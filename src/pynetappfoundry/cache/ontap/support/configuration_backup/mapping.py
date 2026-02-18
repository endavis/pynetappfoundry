"""OntapConfigurationBackup type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.support.configuration_backup.model import OntapConfigurationBackup

ONTAPCONFIGURATIONBACKUP_MAPPING = TypeMapping(
    name="OntapConfigurationBackup",
    model_class=OntapConfigurationBackup,
    api_endpoint="/support/configuration-backup?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="password",
            api_path="password",
        ),
        FieldMapping(
            cache_attr="url",
            api_path="url",
        ),
        FieldMapping(
            cache_attr="username",
            api_path="username",
        ),
        FieldMapping(
            cache_attr="validate_certificate",
            api_path="validate_certificate",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapConfigurationBackup", ONTAPCONFIGURATIONBACKUP_MAPPING)
