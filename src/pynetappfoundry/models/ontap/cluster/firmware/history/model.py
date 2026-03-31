"""OntapFirmwareHistory information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapFirmwareHistoryUpdateStatu(OntapModel):
    """OntapFirmwareHistoryUpdateStatu sub-model for update_status."""

    worker_error_code: int = 0
    worker_error_message: str = ""
    worker_node_name: str = ""
    worker_node_uuid: str = ""
    worker_state: str = ""


class OntapFirmwareHistory(OntapModel):
    """OntapFirmwareHistory information."""

    end_time: str = ""
    fw_file_name: str = ""
    fw_update_state: str = ""
    job_uuid: OntapUUID = ""
    node_name: str = ""
    node_uuid: str = ""
    start_time: str = ""
    update_status: list[OntapFirmwareHistoryUpdateStatu] = Field(default_factory=list)
