"""DiiAuOnetimetoken type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.au.oneTimeToken.model import (
    DiiAuOnetimetoken,
    DiiAuOnetimetokenCommand,
)


def _transform_commands(record: dict[str, Any]) -> list[DiiAuOnetimetokenCommand]:
    """Transform commands into DiiAuOnetimetokenCommand list."""
    return [DiiAuOnetimetokenCommand(**item) for item in record.get("commands", [])]


DIIAUONETIMETOKEN_MAPPING = TypeMapping(
    name="DiiAuOnetimetoken",
    model_class=DiiAuOnetimetoken,
    api_endpoint="/au/oneTimeToken",
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

model_registry.register_mapping("DiiAuOnetimetoken", DIIAUONETIMETOKEN_MAPPING)
