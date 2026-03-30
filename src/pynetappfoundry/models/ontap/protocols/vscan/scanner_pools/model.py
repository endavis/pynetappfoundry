"""OntapVscanScannerPool information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapVscanScannerPool(OntapModel):
    """OntapVscanScannerPool information."""

    cluster_name: str = ""
    cluster_uuid: OntapUUID = ""
    name: str = ""
    privileged_users: list[str] = Field(default_factory=list)
    role: str = ""
    servers: list[str] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
