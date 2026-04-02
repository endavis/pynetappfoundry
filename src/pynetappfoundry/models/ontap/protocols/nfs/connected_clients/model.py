"""OntapNfsClients information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNfsClientsExportPolicy(OntapModel):
    """OntapNfsClientsExportPolicy sub-model for export_policy."""

    id: int = 0
    name: str = ""


class OntapNfsClientsNode(OntapModel):
    """OntapNfsClientsNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapNfsClientsSvm(OntapModel):
    """OntapNfsClientsSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNfsClientsVolume(OntapModel):
    """OntapNfsClientsVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapNfsClients(OntapModel):
    """OntapNfsClients information."""

    client_ip: str = ""
    export_policy: OntapNfsClientsExportPolicy = Field(default_factory=OntapNfsClientsExportPolicy)
    idle_duration: str = ""
    local_request_count: int = 0
    node: OntapNfsClientsNode = Field(default_factory=OntapNfsClientsNode)
    protocol: str = ""
    remote_request_count: int = 0
    server_ip: str = ""
    svm: OntapNfsClientsSvm = Field(default_factory=OntapNfsClientsSvm)
    trunking_enabled: bool = False
    volume: OntapNfsClientsVolume = Field(default_factory=OntapNfsClientsVolume)
