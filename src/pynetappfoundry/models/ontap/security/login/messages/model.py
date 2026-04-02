"""OntapLoginMessages information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLoginMessagesSvm(OntapModel):
    """OntapLoginMessagesSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapLoginMessages(OntapModel):
    """OntapLoginMessages information."""

    banner: str = ""
    message: str = ""
    scope: str = ""
    show_cluster_message: bool = False
    svm: OntapLoginMessagesSvm = Field(default_factory=OntapLoginMessagesSvm)
    uuid: str = ""
