"""OntapSnaplockLitigationFileResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapSnaplockLitigationFileResponse(CacheModel):
    """OntapSnaplockLitigationFileResponse information."""

    file: list[str] = Field(default_factory=list)
    sequence_index: int = 0
