"""OntapCloudStore information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCloudStoreAggregate(OntapModel):
    """OntapCloudStoreAggregate sub-model for aggregate."""

    name: str = ""


class OntapCloudStoreTarget(OntapModel):
    """OntapCloudStoreTarget sub-model for target."""

    name: str = ""
    uuid: str = ""


class OntapCloudStoreUnavailableReason(OntapModel):
    """OntapCloudStoreUnavailableReason sub-model for unavailable_reason."""

    message: str = ""


class OntapCloudStore(OntapModel):
    """OntapCloudStore information."""

    aggregate: OntapCloudStoreAggregate = Field(default_factory=OntapCloudStoreAggregate)
    availability: str = ""
    availability_at_partner: str = ""
    mirror_degraded: bool = False
    primary: bool = False
    resync_progress: int = 0
    target: OntapCloudStoreTarget = Field(default_factory=OntapCloudStoreTarget)
    unavailable_reason: OntapCloudStoreUnavailableReason = Field(
        default_factory=OntapCloudStoreUnavailableReason
    )
    unreclaimed_space_threshold: int = 0
    used: int = 0
