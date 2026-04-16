"""DiiAuAcquisitionunit type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.au.acquisitionUnit.model import DiiAuAcquisitionunit

DIIAUACQUISITIONUNIT_MAPPING = TypeMapping(
    name="DiiAuAcquisitionunit",
    model_class=DiiAuAcquisitionunit,
    api_endpoint="/au/acquisitionUnit/{auUuid}",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="auVersion",
        ),
        FieldMapping(
            cache_attr="versionToBeUpgradedTo",
        ),
        FieldMapping(
            cache_attr="isPinned",
            default=False,
        ),
        FieldMapping(
            cache_attr="ip",
        ),
        FieldMapping(
            cache_attr="auUpgradeToImageUploadedTime",
            default=0,
        ),
        FieldMapping(
            cache_attr="restartRequestTime",
            default=0,
        ),
        FieldMapping(
            cache_attr="upgradeOverDueMessage",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="leasePeriod",
            default=0,
        ),
        FieldMapping(
            cache_attr="upgradeOverDue",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="upgradeType",
        ),
        FieldMapping(
            cache_attr="self",
        ),
        FieldMapping(
            cache_attr="id",
        ),
        FieldMapping(
            cache_attr="nextLeaseRenewal",
            default=0,
        ),
        FieldMapping(
            cache_attr="status",
        ),
    ),
)

model_registry.register_mapping("DiiAuAcquisitionunit", DIIAUACQUISITIONUNIT_MAPPING)
