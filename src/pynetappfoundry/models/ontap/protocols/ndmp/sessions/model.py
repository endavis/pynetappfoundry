"""OntapNdmpSession information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapNdmpSession(OntapModel):
    """OntapNdmpSession information."""

    backup_engine: str = ""
    client_address: str = ""
    client_port: int = 0
    data_bytes_processed: int = 0
    data_connection_address: str = ""
    data_connection_port: int = 0
    data_connection_type: str = ""
    data_operation: str = ""
    data_reason: str = ""
    data_state: str = ""
    data_path: str = ""
    id: str = ""
    mover_bytes_moved: int = 0
    mover_connection_address: str = ""
    mover_connection_port: int = 0
    mover_connection_type: str = ""
    mover_mode: str = ""
    mover_reason: str = ""
    mover_state: str = ""
    node_name: str = ""
    node_uuid: str = ""
    scsi_device_id: str = ""
    scsi_host_adapter: int = 0
    scsi_lun_id: int = 0
    scsi_target_id: int = 0
    source_address: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    tape_device: str = ""
    tape_mode: str = ""
    uuid: str = ""
