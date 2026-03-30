"""OntapSnapshot information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSnapshot(OntapModel):
    """OntapSnapshot information."""

    comment: str = ""
    compress_savings: int = 0
    create_time: str = ""
    dedup_savings: int = 0
    delta_size_consumed: int = 0
    delta_time_elapsed: str = ""
    expiry_time: str = ""
    logical_size: int = 0
    name: str = ""
    owners: list[str] = Field(default_factory=list)
    provenance_volume_uuid: str = ""
    reclaimable_space: int = 0
    size: int = 0
    snaplock_expired: bool = False
    snaplock_expiry_time: str = ""
    snaplock_time_until_expiry: str = ""
    snapmirror_label: str = ""
    state: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
    vbn0_savings: int = 0
    version_uuid: str = ""
    volume_name: str = ""
    volume_uuid: str = ""
