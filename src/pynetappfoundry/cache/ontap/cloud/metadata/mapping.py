"""CloudMetadata type mapping definition for the declarative field mapping framework.

Defines CLOUD_METADATA_MAPPING which maps ONTAP CLI virtual-machine instance
data to CloudMetadata cache model attributes. CloudMetadata is CLI-only —
there is no REST API endpoint for this data.

The computed link fields (``instance_link``, ``resource_group_link``) are
derived via ``post_collection`` hooks so that :func:`fetch` populates them
automatically. ``instance_sso_link`` depends on collector-only state
(``aws_sso_config``) and is therefore left to the collector's post-
processing; the DataSource path returns it as an empty string.
"""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata
from pynetappfoundry.utils.cloud import (
    build_cloud_instance_link,
    build_cloud_resource_group_link,
)


def _compute_instance_link(instance: CloudMetadata, _results: dict[str, Any]) -> CloudMetadata:
    """Derive ``instance_link`` from the instance's own fields."""
    region = instance.region or instance.availability_zone
    link = build_cloud_instance_link(
        provider=instance.provider,
        instance_id=instance.instance_id,
        region=region,
        account_id=instance.account_id,
        resource_group=instance.resource_group_name,
    )
    return instance.model_copy(update={"instance_link": link})


def _compute_resource_group_link(
    instance: CloudMetadata, _results: dict[str, Any]
) -> CloudMetadata:
    """Derive ``resource_group_link`` from the instance's own fields."""
    link = build_cloud_resource_group_link(
        provider=instance.provider,
        account_id=instance.account_id,
        resource_group=instance.resource_group_name,
    )
    return instance.model_copy(update={"resource_group_link": link})


CLOUD_METADATA_MAPPING = TypeMapping(
    name="CloudMetadata",
    model_class=CloudMetadata,
    api_endpoint="",
    cli_command="virtual-machine instance show",
    id_field="node",
    fields=(
        FieldMapping(
            cache_attr="node",
            cli_field="node",
        ),
        FieldMapping(
            cache_attr="instance_id",
            cli_field="instance_id",
        ),
        FieldMapping(
            cache_attr="account_id",
            cli_field="account_id",
        ),
        FieldMapping(
            cache_attr="image_id",
            cli_field="image_id",
        ),
        FieldMapping(
            cache_attr="instance_type",
            cli_field="instance_type",
        ),
        FieldMapping(
            cache_attr="cpu_platform",
            cli_field="cpu_platform",
        ),
        FieldMapping(
            cache_attr="region",
            cli_field="region",
        ),
        FieldMapping(
            cache_attr="provider",
            cli_field="provider",
        ),
        FieldMapping(
            cache_attr="consumer",
            cli_field="consumer",
        ),
        FieldMapping(
            cache_attr="primary_ip",
            cli_field="primary_ip",
        ),
        FieldMapping(
            cache_attr="metadata_version",
            cli_field="metadata_version",
        ),
        # AWS-specific
        FieldMapping(
            cache_attr="availability_zone",
            cli_field="availability_zone",
        ),
        FieldMapping(
            cache_attr="availability_zone_id",
            cli_field="availability_zone_id",
        ),
        # Azure-specific
        FieldMapping(
            cache_attr="fault_domain",
            cli_field="fault_domain",
        ),
        FieldMapping(
            cache_attr="update_domain",
            cli_field="update_domain",
        ),
        FieldMapping(
            cache_attr="resource_group_name",
            cli_field="resource_group_name",
        ),
        FieldMapping(
            cache_attr="offer",
            cli_field="offer",
        ),
        FieldMapping(
            cache_attr="sku",
            cli_field="sku",
        ),
        FieldMapping(
            cache_attr="sku_version",
            cli_field="sku_version",
        ),
        # Derived link fields — populated by post_collection hooks.
        FieldMapping(
            cache_attr="instance_link",
            cache_strategy="derived",
            post_collection=_compute_instance_link,
        ),
        FieldMapping(
            cache_attr="resource_group_link",
            cache_strategy="derived",
            post_collection=_compute_resource_group_link,
        ),
    ),
)

model_registry.register_mapping("CloudMetadata", CLOUD_METADATA_MAPPING)
