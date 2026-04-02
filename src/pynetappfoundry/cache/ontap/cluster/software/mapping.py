# ruff: noqa: E501
"""OntapSoftwareReference type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.software.model import (
    OntapSoftwareReference,
    OntapSoftwareReferenceFirmwareClusterFwProgress,
    OntapSoftwareReferenceSoftwareImage,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_firmware_cluster_fw_progress(
    record: dict[str, Any],
) -> list[OntapSoftwareReferenceFirmwareClusterFwProgress]:
    """Transform firmware.cluster_fw_progress into OntapSoftwareReferenceFirmwareClusterFwProgress list."""
    try:
        items = get_nested_value(record, "firmware.cluster_fw_progress")
    except Exception:
        items = []
    return [OntapSoftwareReferenceFirmwareClusterFwProgress(**item) for item in items]


def _transform_software_images(record: dict[str, Any]) -> list[OntapSoftwareReferenceSoftwareImage]:
    """Transform software_images into OntapSoftwareReferenceSoftwareImage list."""
    return [
        OntapSoftwareReferenceSoftwareImage(**item) for item in record.get("software_images", [])
    ]


ONTAPSOFTWAREREFERENCE_MAPPING = TypeMapping(
    name="OntapSoftwareReference",
    model_class=OntapSoftwareReference,
    api_endpoint="/cluster/software?fields=*",
    api_type="ontap",
    records_path="nodes",
    fields=(
        FieldMapping(
            cache_attr="firmware.cluster_fw_progress",
            api_path="firmware.cluster_fw_progress",
            transform=_transform_firmware_cluster_fw_progress,
            default=[],
        ),
        FieldMapping(
            cache_attr="firmware.disk.average_duration_per_disk",
            api_path="firmware.disk.average_duration_per_disk",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware.disk.num_waiting_download",
            api_path="firmware.disk.num_waiting_download",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware.disk.total_completion_estimate",
            api_path="firmware.disk.total_completion_estimate",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware.disk.update_status",
            api_path="firmware.disk.update_status",
        ),
        FieldMapping(
            cache_attr="firmware.dqp.file_name",
            api_path="firmware.dqp.file_name",
        ),
        FieldMapping(
            cache_attr="firmware.dqp.record_count.alias",
            api_path="firmware.dqp.record_count.alias",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware.dqp.record_count.device",
            api_path="firmware.dqp.record_count.device",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware.dqp.record_count.drive",
            api_path="firmware.dqp.record_count.drive",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware.dqp.record_count.system",
            api_path="firmware.dqp.record_count.system",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware.dqp.revision",
            api_path="firmware.dqp.revision",
        ),
        FieldMapping(
            cache_attr="firmware.dqp.version",
            api_path="firmware.dqp.version",
        ),
        FieldMapping(
            cache_attr="firmware.shelf.in_progress_count",
            api_path="firmware.shelf.in_progress_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware.shelf.update_status",
            api_path="firmware.shelf.update_status",
        ),
        FieldMapping(
            cache_attr="firmware.sp_bmc.autoupdate",
            api_path="firmware.sp_bmc.autoupdate",
            default=False,
        ),
        FieldMapping(
            cache_attr="firmware.sp_bmc.end_time",
            api_path="firmware.sp_bmc.end_time",
        ),
        FieldMapping(
            cache_attr="firmware.sp_bmc.fw_type",
            api_path="firmware.sp_bmc.fw_type",
        ),
        FieldMapping(
            cache_attr="firmware.sp_bmc.image",
            api_path="firmware.sp_bmc.image",
        ),
        FieldMapping(
            cache_attr="firmware.sp_bmc.in_progress",
            api_path="firmware.sp_bmc.in_progress",
            default=False,
        ),
        FieldMapping(
            cache_attr="firmware.sp_bmc.is_current",
            api_path="firmware.sp_bmc.is_current",
            default=False,
        ),
        FieldMapping(
            cache_attr="firmware.sp_bmc.last_update_state",
            api_path="firmware.sp_bmc.last_update_state",
        ),
        FieldMapping(
            cache_attr="firmware.sp_bmc.percent_done",
            api_path="firmware.sp_bmc.percent_done",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware.sp_bmc.running_version",
            api_path="firmware.sp_bmc.running_version",
        ),
        FieldMapping(
            cache_attr="firmware.sp_bmc.start_time",
            api_path="firmware.sp_bmc.start_time",
        ),
        FieldMapping(
            cache_attr="firmware.sp_bmc.state",
            api_path="firmware.sp_bmc.state",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="software_images",
            api_path="software_images",
            transform=_transform_software_images,
            default=[],
        ),
        FieldMapping(
            cache_attr="version",
            api_path="version",
        ),
    ),
)

model_registry.register_mapping("OntapSoftwareReference", ONTAPSOFTWAREREFERENCE_MAPPING)
