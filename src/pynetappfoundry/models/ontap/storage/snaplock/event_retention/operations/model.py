"""OntapEbrOperation information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapEbrOperation(OntapModel):
    """OntapEbrOperation information."""

    id: int = 0
    num_files_failed: int = 0
    num_files_processed: int = 0
    num_files_skipped: int = 0
    num_inodes_ignored: int = 0
    path: str = ""
    policy_name: str = ""
    policy_retention_period: str = ""
    state: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    volume_name: str = ""
    volume_uuid: str = ""
