"""DiiCollectorDatasource type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.collector.datasources.model import (
    DiiCollectorDatasource,
    DiiCollectorDatasourceChange,
    DiiCollectorDatasourceConfigPackage,
    DiiCollectorDatasourceDevice,
    DiiCollectorDatasourceEvent,
    DiiCollectorDatasourcePackage,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_changes(record: dict[str, Any]) -> list[DiiCollectorDatasourceChange]:
    """Transform changes into DiiCollectorDatasourceChange list."""
    return [DiiCollectorDatasourceChange(**item) for item in record.get("changes", [])]


def _transform_events(record: dict[str, Any]) -> list[DiiCollectorDatasourceEvent]:
    """Transform events into DiiCollectorDatasourceEvent list."""
    return [DiiCollectorDatasourceEvent(**item) for item in record.get("events", [])]


def _transform_devices(record: dict[str, Any]) -> list[DiiCollectorDatasourceDevice]:
    """Transform devices into DiiCollectorDatasourceDevice list."""
    return [DiiCollectorDatasourceDevice(**item) for item in record.get("devices", [])]


def _transform_packages(record: dict[str, Any]) -> list[DiiCollectorDatasourcePackage]:
    """Transform packages into DiiCollectorDatasourcePackage list."""
    return [DiiCollectorDatasourcePackage(**item) for item in record.get("packages", [])]


def _transform_config_packages(record: dict[str, Any]) -> list[DiiCollectorDatasourceConfigPackage]:
    """Transform config.packages into DiiCollectorDatasourceConfigPackage list."""
    try:
        items = get_nested_value(record, "config.packages")
    except Exception:
        items = []
    return [DiiCollectorDatasourceConfigPackage(**item) for item in items]


DIICOLLECTORDATASOURCE_MAPPING = TypeMapping(
    name="DiiCollectorDatasource",
    model_class=DiiCollectorDatasource,
    api_endpoint="/collector/datasources",
    api_type="dii",
    identifier_field="dataSourceId",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="vendorModelId",
        ),
        FieldMapping(
            cache_attr="note",
        ),
        FieldMapping(
            cache_attr="changes",
            transform=_transform_changes,
            default=[],
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="lastSuccessfullyAcquiredMilliSec",
            default=0,
        ),
        FieldMapping(
            cache_attr="resumeTime",
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
            cache_attr="vendor",
        ),
        FieldMapping(
            cache_attr="activePatch.minPatchVersion",
        ),
        FieldMapping(
            cache_attr="activePatch.createTime",
            default=0,
        ),
        FieldMapping(
            cache_attr="activePatch.dataSourceTypeId",
            default=0,
        ),
        FieldMapping(
            cache_attr="activePatch.tenantId",
        ),
        FieldMapping(
            cache_attr="activePatch.name",
        ),
        FieldMapping(
            cache_attr="activePatch.description",
        ),
        FieldMapping(
            cache_attr="activePatch.endTime",
            default=0,
        ),
        FieldMapping(
            cache_attr="activePatch.version",
        ),
        FieldMapping(
            cache_attr="activePatch.patchReadme",
        ),
        FieldMapping(
            cache_attr="activePatch.metadataVersion",
        ),
        FieldMapping(
            cache_attr="model_",
            api_path="model",
        ),
        FieldMapping(
            cache_attr="id",
        ),
        FieldMapping(
            cache_attr="events",
            transform=_transform_events,
            default=[],
        ),
        FieldMapping(
            cache_attr="docLink",
        ),
        FieldMapping(
            cache_attr="resumeTimeMilliSec",
            default=0,
        ),
        FieldMapping(
            cache_attr="impactIndex",
            default=0,
        ),
        FieldMapping(
            cache_attr="devices",
            transform=_transform_devices,
            default=[],
        ),
        FieldMapping(
            cache_attr="packages",
            transform=_transform_packages,
            default=[],
        ),
        FieldMapping(
            cache_attr="lastSuccessfullyAcquired",
        ),
        FieldMapping(
            cache_attr="pollStatus",
        ),
        FieldMapping(
            cache_attr="dsTypeId",
        ),
        FieldMapping(
            cache_attr="foundationIp",
        ),
        FieldMapping(
            cache_attr="statusText",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="self",
        ),
        FieldMapping(
            cache_attr="config_.vendorModelId",
            api_path="config.vendorModelId",
        ),
        FieldMapping(
            cache_attr="config_.dsTypeId",
            api_path="config.dsTypeId",
        ),
        FieldMapping(
            cache_attr="config_.docLink",
            api_path="config.docLink",
        ),
        FieldMapping(
            cache_attr="config_.vendor",
            api_path="config.vendor",
        ),
        FieldMapping(
            cache_attr="config_.self",
            api_path="config.self",
        ),
        FieldMapping(
            cache_attr="config_.model_",
            api_path="config.model",
        ),
        FieldMapping(
            cache_attr="config_.packages",
            api_path="config.packages",
            transform=_transform_config_packages,
            default=[],
        ),
        FieldMapping(
            cache_attr="status",
        ),
    ),
)

model_registry.register_mapping("DiiCollectorDatasource", DIICOLLECTORDATASOURCE_MAPPING)
