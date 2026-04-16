# ruff: noqa: N802
"""DiiCollectorDatasourcesAu type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.collector.datasources.au.model import (
    DiiCollectorDatasourcesAu,
    DiiCollectorDatasourcesAuAttribute,
    DiiCollectorDatasourcesAuChangerespons,
)


def _transform_changeResponses(
    record: dict[str, Any],
) -> list[DiiCollectorDatasourcesAuChangerespons]:
    """Transform changeResponses into DiiCollectorDatasourcesAuChangerespons list."""
    return [
        DiiCollectorDatasourcesAuChangerespons(**item) for item in record.get("changeResponses", [])
    ]


def _transform_attributes(record: dict[str, Any]) -> list[DiiCollectorDatasourcesAuAttribute]:
    """Transform attributes into DiiCollectorDatasourcesAuAttribute list."""
    return [DiiCollectorDatasourcesAuAttribute(**item) for item in record.get("attributes", [])]


DIICOLLECTORDATASOURCESAU_MAPPING = TypeMapping(
    name="DiiCollectorDatasourcesAu",
    model_class=DiiCollectorDatasourcesAu,
    api_endpoint="/collector/datasources/au/{auId}",
    api_type="dii",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="lastAcquired",
            default=0,
        ),
        FieldMapping(
            cache_attr="auId",
            default=0,
        ),
        FieldMapping(
            cache_attr="active",
            default=False,
        ),
        FieldMapping(
            cache_attr="changeResponses",
            transform=_transform_changeResponses,
            default=[],
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="manual",
            default=0,
        ),
        FieldMapping(
            cache_attr="vendorModel.modelDescription",
        ),
        FieldMapping(
            cache_attr="vendorModel.modelName",
        ),
        FieldMapping(
            cache_attr="vendorModel.docLink",
        ),
        FieldMapping(
            cache_attr="vendorModel.imageURL",
        ),
        FieldMapping(
            cache_attr="vendorModel.id",
        ),
        FieldMapping(
            cache_attr="vendorModel.vendorName",
        ),
        FieldMapping(
            cache_attr="vendorModel.dataSourceTypeVendorModelId.dsTypeId",
            default=0,
        ),
        FieldMapping(
            cache_attr="vendorModel.dataSourceTypeVendorModelId.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="resumeTime",
            default=0,
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.auVersion",
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.versionToBeUpgradedTo",
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.isPinned",
            default=False,
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.ip",
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.auUpgradeToImageUploadedTime",
            default=0,
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.restartRequestTime",
            default=0,
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.upgradeOverDueMessage",
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.type_",
            api_path="acquisitionUnit.type",
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.uuid",
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.leasePeriod",
            default=0,
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.upgradeOverDue",
            default=False,
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.name",
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.upgradeType",
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.self",
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.id",
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.nextLeaseRenewal",
            default=0,
        ),
        FieldMapping(
            cache_attr="acquisitionUnit.status",
        ),
        FieldMapping(
            cache_attr="lastPoll",
            default=0,
        ),
        FieldMapping(
            cache_attr="statusExt",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="self",
        ),
        FieldMapping(
            cache_attr="attributes",
            transform=_transform_attributes,
            default=[],
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="time",
            default=0,
        ),
        FieldMapping(
            cache_attr="postponed",
            default=False,
        ),
        FieldMapping(
            cache_attr="status",
        ),
    ),
)

model_registry.register_mapping("DiiCollectorDatasourcesAu", DIICOLLECTORDATASOURCESAU_MAPPING)
