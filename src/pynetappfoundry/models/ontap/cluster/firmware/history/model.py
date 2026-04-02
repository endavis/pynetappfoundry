"""OntapFirmwareHistory information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapFirmwareHistoryJob(OntapModel):
    """OntapFirmwareHistoryJob sub-model for job."""

    uuid: OntapUUID = ""


class OntapFirmwareHistoryNode(OntapModel):
    """OntapFirmwareHistoryNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapFirmwareHistory(OntapModel):
    """OntapFirmwareHistory information."""

    end_time: str = ""
    fw_file_name: str = ""
    fw_update_state: str = ""
    job: OntapFirmwareHistoryJob = Field(default_factory=OntapFirmwareHistoryJob)
    node: OntapFirmwareHistoryNode = Field(default_factory=OntapFirmwareHistoryNode)
    start_time: str = ""
    update_status: list[dict[str, Any]] = Field(default_factory=list)
