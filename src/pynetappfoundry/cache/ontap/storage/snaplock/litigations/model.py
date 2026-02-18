"""OntapSnaplockLitigation information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSnaplockLitigation(CacheModel):
    """OntapSnaplockLitigation information."""

    id: int = 0
    num_files_failed: str = ""
    num_files_processed: str = ""
    num_files_skipped: str = ""
    num_inodes_ignored: str = ""
    path: str = ""
    state: str = ""
    type_: str = ""
