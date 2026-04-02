# ruff: noqa: E501
"""OntapSnapmirrorTransfer information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapSnapmirrorTransferErrorInfo(OntapModel):
    """OntapSnapmirrorTransferErrorInfo sub-model for error_info."""

    code: int = 0
    message: str = ""


class OntapSnapmirrorTransferFile(OntapModel):
    """OntapSnapmirrorTransferFile sub-model for files."""

    destination_path: str = ""
    source_path: str = ""


class OntapSnapmirrorTransferRelationshipDestinationCluster(OntapModel):
    """OntapSnapmirrorTransferRelationshipDestinationCluster sub-model for cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapSnapmirrorTransferRelationshipDestinationConsistencyGroupVolume(OntapModel):
    """OntapSnapmirrorTransferRelationshipDestinationConsistencyGroupVolume sub-model for consistency_group_volumes."""

    name: str = ""
    uuid: str = ""


class OntapSnapmirrorTransferRelationshipDestinationLuns(OntapModel):
    """OntapSnapmirrorTransferRelationshipDestinationLuns sub-model for luns."""

    name: str = ""
    uuid: str = ""


class OntapSnapmirrorTransferRelationshipDestinationSvm(OntapModel):
    """OntapSnapmirrorTransferRelationshipDestinationSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSnapmirrorTransferRelationshipDestination(OntapModel):
    """OntapSnapmirrorTransferRelationshipDestination sub-model for destination."""

    cluster: OntapSnapmirrorTransferRelationshipDestinationCluster = Field(
        default_factory=OntapSnapmirrorTransferRelationshipDestinationCluster
    )
    consistency_group_volumes: list[
        OntapSnapmirrorTransferRelationshipDestinationConsistencyGroupVolume
    ] = Field(default_factory=list)
    ipspace: str = ""
    luns: OntapSnapmirrorTransferRelationshipDestinationLuns = Field(
        default_factory=OntapSnapmirrorTransferRelationshipDestinationLuns
    )
    path: str = ""
    svm: OntapSnapmirrorTransferRelationshipDestinationSvm = Field(
        default_factory=OntapSnapmirrorTransferRelationshipDestinationSvm
    )


class OntapSnapmirrorTransferRelationship(OntapModel):
    """OntapSnapmirrorTransferRelationship sub-model for relationship."""

    destination: OntapSnapmirrorTransferRelationshipDestination = Field(
        default_factory=OntapSnapmirrorTransferRelationshipDestination
    )
    restore: bool = False
    uuid: OntapUUID = ""


class OntapSnapmirrorTransfer(OntapModel):
    """OntapSnapmirrorTransfer information."""

    bytes_transferred: int = 0
    checkpoint_size: int = 0
    end_time: str = ""
    error_info: OntapSnapmirrorTransferErrorInfo = Field(
        default_factory=OntapSnapmirrorTransferErrorInfo
    )
    files: list[OntapSnapmirrorTransferFile] = Field(default_factory=list)
    last_updated_time: str = ""
    network_compression_ratio: str = ""
    on_demand_attrs: str = ""
    options: list[dict[str, Any]] = Field(default_factory=list)
    relationship: OntapSnapmirrorTransferRelationship = Field(
        default_factory=OntapSnapmirrorTransferRelationship
    )
    snapshot: str = ""
    source_snapshot: str = ""
    state: str = ""
    storage_efficiency_enabled: bool = False
    throttle: int = 0
    total_duration: str = ""
    uuid: OntapUUID = ""
