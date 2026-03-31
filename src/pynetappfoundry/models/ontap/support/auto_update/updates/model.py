"""OntapAutoUpdateStatus information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapAutoUpdateStatusArgument(OntapModel):
    """OntapAutoUpdateStatusArgument sub-model for arguments."""

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
    status_arguments: list[OntapAutoUpdateStatusArgument] = Field(default_factory=list)
    status_code: str = ""
    status_message: str = ""
    uuid: str = ""
