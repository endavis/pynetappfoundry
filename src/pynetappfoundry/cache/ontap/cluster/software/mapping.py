"""OntapSoftwareReference type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.software.model import (
    OntapSoftwareReference,
    OntapSoftwareReferenceClusterFwProgress,
    OntapSoftwareReferenceSoftwareImage,
)


def _transform_firmware_cluster_fw_progress(
    record: dict[str, Any],
) -> list[OntapSoftwareReferenceClusterFwProgress]:
    """Transform firmware.cluster_fw_progress into OntapSoftwareReferenceClusterFwProgress list."""
    return [
        OntapSoftwareReferenceClusterFwProgress(**item)
        for item in record.get("firmware.cluster_fw_progress", [])
    ]


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
            cache_attr="firmware_cluster_fw_progress",
            api_path="firmware.cluster_fw_progress",
            transform=_transform_firmware_cluster_fw_progress,
            default=[],
        ),
        FieldMapping(
            cache_attr="firmware_disk_average_duration_per_disk",
            api_path="firmware.disk.average_duration_per_disk",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware_disk_num_waiting_download",
            api_path="firmware.disk.num_waiting_download",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware_disk_total_completion_estimate",
            api_path="firmware.disk.total_completion_estimate",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware_disk_update_status",
            api_path="firmware.disk.update_status",
        ),
        FieldMapping(
            cache_attr="firmware_dqp_file_name",
            api_path="firmware.dqp.file_name",
        ),
        FieldMapping(
            cache_attr="firmware_dqp_record_count_alias",
            api_path="firmware.dqp.record_count.alias",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware_dqp_record_count_device",
            api_path="firmware.dqp.record_count.device",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware_dqp_record_count_drive",
            api_path="firmware.dqp.record_count.drive",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware_dqp_record_count_system",
            api_path="firmware.dqp.record_count.system",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware_dqp_revision",
            api_path="firmware.dqp.revision",
        ),
        FieldMapping(
            cache_attr="firmware_dqp_version",
            api_path="firmware.dqp.version",
        ),
        FieldMapping(
            cache_attr="firmware_shelf_in_progress_count",
            api_path="firmware.shelf.in_progress_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware_shelf_update_status",
            api_path="firmware.shelf.update_status",
        ),
        FieldMapping(
            cache_attr="firmware_sp_bmc_autoupdate",
            api_path="firmware.sp_bmc.autoupdate",
            default=False,
        ),
        FieldMapping(
            cache_attr="firmware_sp_bmc_end_time",
            api_path="firmware.sp_bmc.end_time",
        ),
        FieldMapping(
            cache_attr="firmware_sp_bmc_fw_type",
            api_path="firmware.sp_bmc.fw_type",
        ),
        FieldMapping(
            cache_attr="firmware_sp_bmc_image",
            api_path="firmware.sp_bmc.image",
        ),
        FieldMapping(
            cache_attr="firmware_sp_bmc_in_progress",
            api_path="firmware.sp_bmc.in_progress",
            default=False,
        ),
        FieldMapping(
            cache_attr="firmware_sp_bmc_is_current",
            api_path="firmware.sp_bmc.is_current",
            default=False,
        ),
        FieldMapping(
            cache_attr="firmware_sp_bmc_last_update_state",
            api_path="firmware.sp_bmc.last_update_state",
        ),
        FieldMapping(
            cache_attr="firmware_sp_bmc_percent_done",
            api_path="firmware.sp_bmc.percent_done",
            default=0,
        ),
        FieldMapping(
            cache_attr="firmware_sp_bmc_running_version",
            api_path="firmware.sp_bmc.running_version",
        ),
        FieldMapping(
            cache_attr="firmware_sp_bmc_start_time",
            api_path="firmware.sp_bmc.start_time",
        ),
        FieldMapping(
            cache_attr="firmware_sp_bmc_state",
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
