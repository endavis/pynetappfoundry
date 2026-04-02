"""OntapNvmeSubsystemMap information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNvmeSubsystemMapNamespaceNode(OntapModel):
    """OntapNvmeSubsystemMapNamespaceNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapNvmeSubsystemMapNamespace(OntapModel):
    """OntapNvmeSubsystemMapNamespace sub-model for namespace."""

    name: str = ""
    node: OntapNvmeSubsystemMapNamespaceNode = Field(
        default_factory=OntapNvmeSubsystemMapNamespaceNode
    )
    uuid: str = ""


class OntapNvmeSubsystemMapSubsystem(OntapModel):
    """OntapNvmeSubsystemMapSubsystem sub-model for subsystem."""

    name: str = ""
    uuid: str = ""


class OntapNvmeSubsystemMapSvm(OntapModel):
    """OntapNvmeSubsystemMapSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNvmeSubsystemMap(OntapModel):
    """OntapNvmeSubsystemMap information."""

    anagrpid: str = ""
    namespace: OntapNvmeSubsystemMapNamespace = Field(
        default_factory=OntapNvmeSubsystemMapNamespace
    )
    nsid: str = ""
    subsystem: OntapNvmeSubsystemMapSubsystem = Field(
        default_factory=OntapNvmeSubsystemMapSubsystem
    )
    svm: OntapNvmeSubsystemMapSvm = Field(default_factory=OntapNvmeSubsystemMapSvm)
