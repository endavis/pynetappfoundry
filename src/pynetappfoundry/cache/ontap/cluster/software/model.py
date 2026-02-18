"""OntapSoftwareReference information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel, OntapUUID


class OntapSoftwareReferenceClusterFwProgress(CacheModel):
    """OntapSoftwareReferenceClusterFwProgress sub-model for cluster_fw_progress."""

    firmware_cluster_fw_progress_job_uuid: OntapUUID = ""
    firmware_cluster_fw_progress_update_state: list[dict[str, Any]] = Field(default_factory=list)
    firmware_cluster_fw_progress_update_type: str = ""
    firmware_cluster_fw_progress_zip_file_name: str = ""


class OntapSoftwareReferenceSoftwareImage(CacheModel):
    """OntapSoftwareReferenceSoftwareImage sub-model for software_images."""

    software_images_package: str = ""


class OntapSoftwareReference(CacheModel):
    """OntapSoftwareReference information."""

    firmware_cluster_fw_progress: list[OntapSoftwareReferenceClusterFwProgress] = Field(
        default_factory=list
    )
    firmware_disk_average_duration_per_disk: int = 0
    firmware_disk_num_waiting_download: int = 0
    firmware_disk_total_completion_estimate: int = 0
    firmware_disk_update_status: str = ""
    firmware_dqp_file_name: str = ""
    firmware_dqp_record_count_alias: int = 0
    firmware_dqp_record_count_device: int = 0
    firmware_dqp_record_count_drive: int = 0
    firmware_dqp_record_count_system: int = 0
    firmware_dqp_revision: str = ""
    firmware_dqp_version: str = ""
    firmware_shelf_in_progress_count: int = 0
    firmware_shelf_update_status: str = ""
    firmware_sp_bmc_autoupdate: bool = False
    firmware_sp_bmc_end_time: str = ""
    firmware_sp_bmc_fw_type: str = ""
    firmware_sp_bmc_image: str = ""
    firmware_sp_bmc_in_progress: bool = False
    firmware_sp_bmc_is_current: bool = False
    firmware_sp_bmc_last_update_state: str = ""
    firmware_sp_bmc_percent_done: int = 0
    firmware_sp_bmc_running_version: str = ""
    firmware_sp_bmc_start_time: str = ""
    firmware_sp_bmc_state: str = ""
    name: str = ""
    software_images: list[OntapSoftwareReferenceSoftwareImage] = Field(default_factory=list)
    version: str = ""
