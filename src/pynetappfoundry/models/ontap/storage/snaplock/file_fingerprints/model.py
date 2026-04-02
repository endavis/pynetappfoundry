"""OntapSnaplockFileFingerprint information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSnaplockFileFingerprintSvm(OntapModel):
    """OntapSnaplockFileFingerprintSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSnaplockFileFingerprintVolume(OntapModel):
    """OntapSnaplockFileFingerprintVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapSnaplockFileFingerprint(OntapModel):
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
    svm: OntapSnaplockFileFingerprintSvm = Field(default_factory=OntapSnaplockFileFingerprintSvm)
    volume: OntapSnaplockFileFingerprintVolume = Field(
        default_factory=OntapSnaplockFileFingerprintVolume
    )
