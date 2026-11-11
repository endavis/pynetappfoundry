"""DiiAuInstallcommand type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.au.installCommand.model import (
    DiiAuInstallcommand,
    DiiAuInstallcommandAdditionalinstructionsformanualinstallation,
)

DIIAUINSTALLCOMMAND_MAPPING = TypeMapping(
    name="DiiAuInstallcommand",
    model_class=DiiAuInstallcommand,
    api_endpoint="/au/installCommand/{platform}",
    api_type="dii",
    records_path=".",
    fields=(
        FieldMapping(
            cache_attr="additionalInstructionsForManualInstallation",
            item_model=DiiAuInstallcommandAdditionalinstructionsformanualinstallation,
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

model_registry.register_mapping("DiiAuInstallcommand", DIIAUINSTALLCOMMAND_MAPPING)
