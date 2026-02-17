"""OntapFileMove information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapFileMoveArgument(CacheModel):
    """OntapFileMoveArgument sub-model for arguments."""

    failure_arguments_code: str = ""
    failure_arguments_message: str = ""


class OntapFileMoveDestination(CacheModel):
    """OntapFileMoveDestination sub-model for destinations."""

    files_to_move_destinations_path: str = ""
    files_to_move_destinations_svm_name: str = ""
    files_to_move_destinations_svm_uuid: str = ""
    files_to_move_destinations_volume_name: str = ""
    files_to_move_destinations_volume_uuid: str = ""


class OntapFileMoveSource(CacheModel):
    """OntapFileMoveSource sub-model for sources."""

    files_to_move_sources_path: str = ""
    files_to_move_sources_svm_name: str = ""
    files_to_move_sources_svm_uuid: str = ""
    files_to_move_sources_volume_name: str = ""
    files_to_move_sources_volume_uuid: str = ""


class OntapFileMove(CacheModel):
    """OntapFileMove information."""

    cutover_time: int = 0
    destination_path: str = ""
    destination_svm_name: str = ""
    destination_svm_uuid: str = ""
    destination_volume_name: str = ""
    destination_volume_uuid: str = ""
    elapsed_time: int = 0
    failure_arguments: list[OntapFileMoveArgument] = Field(default_factory=list)
    failure_code: str = ""
    failure_message: str = ""
    files_to_move_destinations: list[OntapFileMoveDestination] = Field(default_factory=list)
    files_to_move_sources: list[OntapFileMoveSource] = Field(default_factory=list)
    index: int = 0
    is_destination_ready: bool = False
    is_flexgroup: bool = False
    is_snapshot_fenced: bool = False
    max_cutover_time: int = 0
    max_throughput: int = 0
    node_name: str = ""
    node_uuid: str = ""
    reference_max_cutover_time: int = 0
    reference_path: str = ""
    reference_svm_name: str = ""
    reference_svm_uuid: str = ""
    reference_volume_name: str = ""
    reference_volume_uuid: str = ""
    scanner_percent: int = 0
    scanner_progress: int = 0
    scanner_state: str = ""
    scanner_total: int = 0
    source_path: str = ""
    source_svm_name: str = ""
    source_svm_uuid: str = ""
    source_volume_name: str = ""
    source_volume_uuid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
    volume_name: str = ""
    volume_uuid: str = ""
