"""OntapVscanScannerPool information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapVscanScannerPoolCluster(OntapModel):
    """OntapVscanScannerPoolCluster sub-model for cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapVscanScannerPoolSvm(OntapModel):
    """OntapVscanScannerPoolSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapVscanScannerPool(OntapModel):
    """OntapVscanScannerPool information."""

    cluster: OntapVscanScannerPoolCluster = Field(default_factory=OntapVscanScannerPoolCluster)
    name: str = ""
    privileged_users: list[str] = Field(default_factory=list)
    role: str = ""
    servers: list[str] = Field(default_factory=list)
    svm: OntapVscanScannerPoolSvm = Field(default_factory=OntapVscanScannerPoolSvm)
