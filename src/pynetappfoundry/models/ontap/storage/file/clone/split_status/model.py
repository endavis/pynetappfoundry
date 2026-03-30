"""OntapSplitStatus information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSplitStatus(OntapModel):
    """OntapSplitStatus information."""

    pending_splits: int = 0
    svm_name: str = ""
    svm_uuid: str = ""
    unsplit_size: int = 0
    volume_name: str = ""
    volume_uuid: str = ""
