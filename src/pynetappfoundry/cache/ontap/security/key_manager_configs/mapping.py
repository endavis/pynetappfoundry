"""OntapKeyManagerConfig type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.key_manager_configs.model import OntapKeyManagerConfig

ONTAPKEYMANAGERCONFIG_MAPPING = TypeMapping(
    name="OntapKeyManagerConfig",
    model_class=OntapKeyManagerConfig,
    api_endpoint="/security/key-manager-configs?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="cc_mode_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="cloud_kms_retry_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="health_monitor_policy.akv.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="health_monitor_policy.akv.manage_volume_offline",
            default=False,
        ),
        FieldMapping(
            cache_attr="health_monitor_policy.aws.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="health_monitor_policy.aws.manage_volume_offline",
            default=False,
        ),
        FieldMapping(
            cache_attr="health_monitor_policy.gcp.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="health_monitor_policy.gcp.manage_volume_offline",
            default=False,
        ),
        FieldMapping(
            cache_attr="health_monitor_policy.ikp.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="health_monitor_policy.ikp.manage_volume_offline",
            default=False,
        ),
        FieldMapping(
            cache_attr="health_monitor_policy.kmip.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="health_monitor_policy.kmip.manage_volume_offline",
            default=False,
        ),
        FieldMapping(
            cache_attr="health_monitor_policy.okm.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="health_monitor_policy.okm.manage_volume_offline",
            default=False,
        ),
        FieldMapping(
            cache_attr="health_monitor_polling_interval",
            default=0,
        ),
        FieldMapping(
            cache_attr="passphrase",
        ),
    ),
)

model_registry.register_mapping("OntapKeyManagerConfig", ONTAPKEYMANAGERCONFIG_MAPPING)
