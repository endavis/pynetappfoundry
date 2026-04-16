"""DiiAuInstallcommand type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.au.installCommand.model import (
    DiiAuInstallcommand,
    DiiAuInstallcommandCommand,
)


def _transform_commands(record: dict[str, Any]) -> list[DiiAuInstallcommandCommand]:
    """Transform commands into DiiAuInstallcommandCommand list."""
    return [DiiAuInstallcommandCommand(**item) for item in record.get("commands", [])]


DIIAUINSTALLCOMMAND_MAPPING = TypeMapping(
    name="DiiAuInstallcommand",
    model_class=DiiAuInstallcommand,
    api_endpoint="/au/installCommand/{platform}",
    api_type="dii",
    records_path="additionalInstructionsForManualInstallation",
    fields=(
        FieldMapping(
            cache_attr="download",
        ),
        FieldMapping(
            cache_attr="heading",
        ),
        FieldMapping(
            cache_attr="footer",
        ),
        FieldMapping(
            cache_attr="downloadTitle",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="commands",
            transform=_transform_commands,
            default=[],
        ),
    ),
)

model_registry.register_mapping("DiiAuInstallcommand", DIIAUINSTALLCOMMAND_MAPPING)
