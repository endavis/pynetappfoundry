"""OntapLoginMessages information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapLoginMessages(OntapModel):
    """OntapLoginMessages information."""

    banner: str = ""
    message: str = ""
    scope: str = ""
    show_cluster_message: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
