"""OntapSnapmirrorTransfer information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapSnapmirrorTransferFile(OntapModel):
    """OntapSnapmirrorTransferFile sub-model for files."""

    files_destination_path: str = ""
    files_source_path: str = ""


class OntapSnapmirrorTransferConsistencyGroupVolume(OntapModel):
    """OntapSnapmirrorTransferConsistencyGroupVolume sub-model for consistency_group_volumes."""

    relationship_destination_consistency_group_volumes_name: str = ""
    relationship_destination_consistency_group_volumes_uuid: str = ""


class OntapSnapmirrorTransfer(OntapModel):
    """OntapSnapmirrorTransfer information."""

    bytes_transferred: int = 0
    checkpoint_size: int = 0
    end_time: str = ""
    error_info_code: int = 0
    error_info_message: str = ""
    files: list[OntapSnapmirrorTransferFile] = Field(default_factory=list)
    last_updated_time: str = ""
    network_compression_ratio: str = ""
    on_demand_attrs: str = ""
    options: list[dict[str, Any]] = Field(default_factory=list)
    relationship_destination_cluster_name: str = ""
    relationship_destination_cluster_uuid: OntapUUID = ""
    relationship_destination_consistency_group_volumes: list[
        OntapSnapmirrorTransferConsistencyGroupVolume
    ] = Field(default_factory=list)
    relationship_destination_ipspace: str = ""
    relationship_destination_luns_name: str = ""
    relationship_destination_luns_uuid: str = ""
    relationship_destination_path: str = ""
    relationship_destination_svm_name: str = ""
    relationship_destination_svm_uuid: str = ""
    relationship_restore: bool = False
    relationship_uuid: OntapUUID = ""
    snapshot: str = ""
    source_snapshot: str = ""
    state: str = ""
    storage_efficiency_enabled: bool = False
    throttle: int = 0
    total_duration: str = ""
    uuid: OntapUUID = ""
