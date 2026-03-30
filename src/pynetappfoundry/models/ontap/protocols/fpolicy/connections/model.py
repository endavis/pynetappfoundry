"""OntapFpolicyConnection information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapFpolicyConnection(OntapModel):
    """OntapFpolicyConnection information."""

    disconnected_reason_code: int = 0
    disconnected_reason_message: str = ""
    node_name: str = ""
    node_uuid: str = ""
    policy_name: str = ""
    server: str = ""
    session_uuid: str = ""
    state: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    type_: str = ""
    update_time: str = ""
