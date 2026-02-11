"""Volume type mapping definition for the declarative field mapping framework.

Defines VOLUME_MAPPING which maps ONTAP REST API volume data to
VolumeInfo cache model attributes.
"""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.storage.volumes.model import VolumeInfo


def _api_aggregates_list(record: dict[str, Any]) -> list[str]:
    """Extract all aggregate names from API response, filtering empty.

    Args:
        record: Full API volume record.

    Returns:
        List of non-empty aggregate names.
    """
    return [
        a.get("name", "")
        for a in record.get("aggregates", [])
        if isinstance(a, dict) and a.get("name")
    ]


VOLUME_MAPPING = TypeMapping(
    name="Volume",
    model_class=VolumeInfo,
    api_endpoint=("/storage/volumes?fields=*,autosize,files,nas.path,nas.security_style"),
    cli_command="volume show",
    fields=(
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="svm",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="type",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="style",
            api_path="style",
        ),
        FieldMapping(
            cache_attr="size",
            api_path="size",
            default=0,
        ),
        FieldMapping(
            cache_attr="autosize_mode",
            api_path="autosize.mode",
        ),
        FieldMapping(
            cache_attr="autosize_grow_threshold",
            api_path="autosize.grow_threshold",
            default=0,
        ),
        FieldMapping(
            cache_attr="autosize_shrink_threshold",
            api_path="autosize.shrink_threshold",
            default=0,
        ),
        FieldMapping(
            cache_attr="autosize_maximum",
            api_path="autosize.maximum",
            default=0,
        ),
        FieldMapping(
            cache_attr="autosize_minimum",
            api_path="autosize.minimum",
            default=0,
        ),
        FieldMapping(
            cache_attr="files_maximum",
            api_path="files.maximum",
            default=0,
        ),
        FieldMapping(
            cache_attr="tiering_policy",
            api_path="tiering.policy",
        ),
        FieldMapping(
            cache_attr="tiering_minimum_cooling_days",
            api_path="tiering.min_cooling_days",
            default=0,
        ),
        FieldMapping(
            cache_attr="aggregate",
            api_path="aggregates[0].name",
        ),
        FieldMapping(
            cache_attr="aggregates",
            default=[],
            transform=_api_aggregates_list,
        ),
        FieldMapping(
            cache_attr="snapshot_policy",
            api_path="snapshot_policy.name",
        ),
        FieldMapping(
            cache_attr="export_policy",
            api_path="nas.export_policy.name",
        ),
        FieldMapping(
            cache_attr="junction_path",
            api_path="nas.path",
        ),
        FieldMapping(
            cache_attr="nas_security_style",
            api_path="nas.security_style",
        ),
    ),
)
