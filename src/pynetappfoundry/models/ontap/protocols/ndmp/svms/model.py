"""OntapNdmpSvm information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNdmpSvm(OntapModel):
    """OntapNdmpSvm information."""

    authentication_types: list[str] = Field(default_factory=list)
    enabled: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
