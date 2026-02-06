"""Volume type mapping definition for the declarative field mapping framework.

Defines VOLUME_MAPPING which maps ONTAP REST API and CLI volume data to
VolumeInfo cache model attributes.
"""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.models import VolumeInfo


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


def _cli_aggregates_list(record: dict[str, Any]) -> list[str]:
    """Parse aggregate list from CLI output.

    CLI returns comma or space-separated aggregate names in ``aggr-list``.

    Args:
        record: Full CLI volume record.

    Returns:
        List of non-empty aggregate names.
    """
    raw = record.get("aggr-list", "")
    if not raw or raw == "-":
        return []
    return [n.strip() for n in raw.replace(",", " ").split() if n.strip()]


VOLUME_MAPPING = TypeMapping(
    name="Volume",
    model_class=VolumeInfo,
    api_endpoint=("/storage/volumes?fields=*,autosize,files,nas.path,nas.security_style"),
    cli_command="volume show",
    fields=(
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
            cli_field="instance-uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
            cli_field="volume",
        ),
        FieldMapping(
            cache_attr="svm",
            api_path="svm.name",
            cli_field="vserver",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
            cli_field="state",
        ),
        FieldMapping(
            cache_attr="type",
            api_path="type",
            cli_field="type",
        ),
        FieldMapping(
            cache_attr="style",
            api_path="style",
            cli_field="volume-style-extended",
        ),
        FieldMapping(
            cache_attr="size",
            api_path="size",
            cli_field="size",
            default=0,
        ),
        FieldMapping(
            cache_attr="autosize_mode",
            api_path="autosize.mode",
            cli_field="autosize-mode",
        ),
        FieldMapping(
            cache_attr="autosize_grow_threshold",
            api_path="autosize.grow_threshold",
            cli_field="autosize-grow-threshold-percent",
            default=0,
        ),
        FieldMapping(
            cache_attr="autosize_shrink_threshold",
            api_path="autosize.shrink_threshold",
            cli_field="autosize-shrink-threshold-percent",
            default=0,
        ),
        FieldMapping(
            cache_attr="autosize_maximum",
            api_path="autosize.maximum",
            cli_field="max-autosize",
            default=0,
        ),
        FieldMapping(
            cache_attr="autosize_minimum",
            api_path="autosize.minimum",
            cli_field="min-autosize",
            default=0,
        ),
        FieldMapping(
            cache_attr="files_maximum",
            api_path="files.maximum",
            cli_field="files",
            default=0,
        ),
        FieldMapping(
            cache_attr="tiering_policy",
            api_path="tiering.policy",
            cli_field="tiering-policy",
        ),
        FieldMapping(
            cache_attr="tiering_minimum_cooling_days",
            api_path="tiering.min_cooling_days",
            cli_field="tiering-minimum-cooling-days",
            default=0,
        ),
        FieldMapping(
            cache_attr="aggregate",
            api_path="aggregates[0].name",
            cli_field="aggregate",
        ),
        FieldMapping(
            cache_attr="aggregates",
            default=[],
            transform=_api_aggregates_list,
            cli_transform=_cli_aggregates_list,
        ),
        FieldMapping(
            cache_attr="snapshot_policy",
            api_path="snapshot_policy.name",
            cli_field="snapshot-policy",
        ),
        FieldMapping(
            cache_attr="export_policy",
            api_path="nas.export_policy.name",
            cli_field="policy",
        ),
        FieldMapping(
            cache_attr="junction_path",
            api_path="nas.path",
            cli_field="junction-path",
        ),
        FieldMapping(
            cache_attr="nas_security_style",
            api_path="nas.security_style",
            cli_field="security-style",
        ),
    ),
)
