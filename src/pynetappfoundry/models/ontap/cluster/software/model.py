# ruff: noqa: E501
"""OntapSoftwareReference information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapSoftwareReferenceFirmwareClusterFwProgressJob(OntapModel):
    """OntapSoftwareReferenceFirmwareClusterFwProgressJob sub-model for job."""

    uuid: OntapUUID = ""


class OntapSoftwareReferenceFirmwareClusterFwProgressUpdateStateWorkerNode(OntapModel):
    """OntapSoftwareReferenceFirmwareClusterFwProgressUpdateStateWorkerNode sub-model for worker_node."""

    name: str = ""
    uuid: str = ""


class OntapSoftwareReferenceFirmwareClusterFwProgressUpdateState(OntapModel):
    """OntapSoftwareReferenceFirmwareClusterFwProgressUpdateState sub-model for update_state."""

    attempts: int = 0
    code: int = 0
    message: str = ""
    status: str = ""
    worker_node: OntapSoftwareReferenceFirmwareClusterFwProgressUpdateStateWorkerNode = Field(
        default_factory=OntapSoftwareReferenceFirmwareClusterFwProgressUpdateStateWorkerNode
    )


class OntapSoftwareReferenceFirmwareClusterFwProgress(OntapModel):
    """OntapSoftwareReferenceFirmwareClusterFwProgress sub-model for cluster_fw_progress."""

    job: OntapSoftwareReferenceFirmwareClusterFwProgressJob = Field(
        default_factory=OntapSoftwareReferenceFirmwareClusterFwProgressJob
    )
    update_state: list[OntapSoftwareReferenceFirmwareClusterFwProgressUpdateState] = Field(
        default_factory=list
    )
    update_type: str = ""
    zip_file_name: str = ""


class OntapSoftwareReferenceFirmwareDisk(OntapModel):
    """OntapSoftwareReferenceFirmwareDisk sub-model for disk."""

    average_duration_per_disk: int = 0
    num_waiting_download: int = 0
    total_completion_estimate: int = 0
    update_status: str = ""


class OntapSoftwareReferenceFirmwareDqpRecordCount(OntapModel):
    """OntapSoftwareReferenceFirmwareDqpRecordCount sub-model for record_count."""

    alias: int = 0
    device: int = 0
    drive: int = 0
    system: int = 0


class OntapSoftwareReferenceFirmwareDqp(OntapModel):
    """OntapSoftwareReferenceFirmwareDqp sub-model for dqp."""

    file_name: str = ""
    record_count: OntapSoftwareReferenceFirmwareDqpRecordCount = Field(
        default_factory=OntapSoftwareReferenceFirmwareDqpRecordCount
    )
    revision: str = ""
    version: str = ""


class OntapSoftwareReferenceFirmwareShelf(OntapModel):
    """OntapSoftwareReferenceFirmwareShelf sub-model for shelf."""

    in_progress_count: int = 0
    update_status: str = ""


class OntapSoftwareReferenceFirmwareSpBmc(OntapModel):
    """OntapSoftwareReferenceFirmwareSpBmc sub-model for sp_bmc."""

    autoupdate: bool = False
    end_time: str = ""
    fw_type: str = ""
    image: str = ""
    in_progress: bool = False
    is_current: bool = False
    last_update_state: str = ""
    percent_done: int = 0
    running_version: str = ""
    start_time: str = ""
    state: str = ""


class OntapSoftwareReferenceFirmware(OntapModel):
    """OntapSoftwareReferenceFirmware sub-model for firmware."""

    cluster_fw_progress: list[OntapSoftwareReferenceFirmwareClusterFwProgress] = Field(
        default_factory=list
    )
    disk: OntapSoftwareReferenceFirmwareDisk = Field(
        default_factory=OntapSoftwareReferenceFirmwareDisk
    )
    dqp: OntapSoftwareReferenceFirmwareDqp = Field(
        default_factory=OntapSoftwareReferenceFirmwareDqp
    )
    shelf: OntapSoftwareReferenceFirmwareShelf = Field(
        default_factory=OntapSoftwareReferenceFirmwareShelf
    )
    sp_bmc: OntapSoftwareReferenceFirmwareSpBmc = Field(
        default_factory=OntapSoftwareReferenceFirmwareSpBmc
    )


class OntapSoftwareReferenceSoftwareImage(OntapModel):
    """OntapSoftwareReferenceSoftwareImage sub-model for software_images."""

    package: str = ""


class OntapSoftwareReference(OntapModel):
    """OntapSoftwareReference information."""

    firmware: OntapSoftwareReferenceFirmware = Field(default_factory=OntapSoftwareReferenceFirmware)
    name: str = ""
    software_images: list[OntapSoftwareReferenceSoftwareImage] = Field(default_factory=list)
    version: str = ""
