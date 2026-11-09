# ruff: noqa: E501, N802
"""DiiAuOnetimetoken type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.au.oneTimeToken.model import (
    DiiAuOnetimetoken,
    DiiAuOnetimetokenAdditionalinstructionsformanualinstallation,
)


def _transform_additionalInstructionsForManualInstallation(
    record: dict[str, Any],
) -> list[DiiAuOnetimetokenAdditionalinstructionsformanualinstallation]:
    """Transform additionalInstructionsForManualInstallation into DiiAuOnetimetokenAdditionalinstructionsformanualinstallation list."""
    return [
        DiiAuOnetimetokenAdditionalinstructionsformanualinstallation(**item)
        for item in record.get("additionalInstructionsForManualInstallation", [])
    ]


DIIAUONETIMETOKEN_MAPPING = TypeMapping(
    name="DiiAuOnetimetoken",
    model_class=DiiAuOnetimetoken,
    api_endpoint="/au/oneTimeToken",
    api_type="dii",
    records_path=".",
    fields=(
        FieldMapping(
            cache_attr="additionalInstructionsForManualInstallation",
            transform=_transform_additionalInstructionsForManualInstallation,
            default=[],
        ),
        FieldMapping(
            cache_attr="requirements",
        ),
        FieldMapping(
            cache_attr="installCommand",
        ),
        FieldMapping(
            cache_attr="imageZipUrl",
        ),
        FieldMapping(
            cache_attr="dsWarDownloadUrl",
        ),
        FieldMapping(
            cache_attr="supportedOS",
        ),
        FieldMapping(
            cache_attr="proxySettingCommand",
        ),
        FieldMapping(
            cache_attr="token",
        ),
    ),
)

model_registry.register_mapping("DiiAuOnetimetoken", DIIAUONETIMETOKEN_MAPPING)
