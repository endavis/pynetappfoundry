"""OntapAutoUpdateStatus information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapAutoUpdateStatusStatusArgument(OntapModel):
    """OntapAutoUpdateStatusStatusArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapAutoUpdateStatusStatus(OntapModel):
    """OntapAutoUpdateStatusStatus sub-model for status."""

    arguments: list[OntapAutoUpdateStatusStatusArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapAutoUpdateStatus(OntapModel):
    """OntapAutoUpdateStatus information."""

    action: str = ""
    content_category: str = ""
    content_type: str = ""
    creation_time: str = ""
    description: str = ""
    end_time: str = ""
    expiry_time: str = ""
    last_state_change_time: str = ""
    package_id: str = ""
    percent_complete: int = 0
    remaining_time: str = ""
    schedule_time: str = ""
    scheduled_time: str = ""
    start_time: str = ""
    state: str = ""
    status: OntapAutoUpdateStatusStatus = Field(default_factory=OntapAutoUpdateStatusStatus)
    uuid: str = ""
