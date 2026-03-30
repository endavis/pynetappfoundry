"""OntapNvmeSubsystemMap information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapNvmeSubsystemMap(OntapModel):
    """OntapNvmeSubsystemMap information."""

    anagrpid: str = ""
    namespace_name: str = ""
    namespace_node_name: str = ""
    namespace_node_uuid: str = ""
    namespace_uuid: str = ""
    nsid: str = ""
    subsystem_name: str = ""
    subsystem_uuid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
