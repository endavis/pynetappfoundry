"""OntapNfsClients information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapNfsClients(OntapModel):
    """OntapNfsClients information."""

    client_ip: str = ""
    export_policy_id: int = 0
    export_policy_name: str = ""
    idle_duration: str = ""
    local_request_count: int = 0
    node_name: str = ""
    node_uuid: str = ""
    protocol: str = ""
    remote_request_count: int = 0
    server_ip: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    trunking_enabled: bool = False
    volume_name: str = ""
    volume_uuid: str = ""
