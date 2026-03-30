"""OntapSnaplockLitigationFileResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSnaplockLitigationFileResponse(OntapModel):
    """OntapSnaplockLitigationFileResponse information."""

    file: list[str] = Field(default_factory=list)
    sequence_index: int = 0
