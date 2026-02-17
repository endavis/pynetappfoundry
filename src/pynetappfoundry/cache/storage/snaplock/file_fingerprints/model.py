"""OntapSnaplockFileFingerprint information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSnaplockFileFingerprint(CacheModel):
    """OntapSnaplockFileFingerprint information."""

    algorithm: str = ""
    data_fingerprint: str = ""
    file_size: int = 0
    file_type: str = ""
    id: int = 0
    metadata_fingerprint: str = ""
    path: str = ""
    scope: str = ""
    state: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    volume_name: str = ""
    volume_uuid: str = ""
