# The field names are the GraphQL camelCase names, so filter paths equal API paths.
# ruff: noqa: N815
"""Digital Advisor cluster model: the curated scalars and nested objects, no personal data.

The field names are the ones of the ``Cluster`` type in the GraphQL schema. The backend
generates its selection set from these fields (ADR-0037), so a field added here is
fetched and a field left out is never requested. Unbounded per-cluster lists
(``systems``, ``vservers``, ``shelves`` and the like) are out of scope.
"""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DigitalAdvisorCount(OntapModel):
    """A ``{ totalCount }`` sub-selection (an Int or Float in the schema)."""

    totalCount: int | float | None = None


class DigitalAdvisorClusterCapacity(OntapModel):
    """The ``ClusterCapacity`` fields that are scalars."""

    lastAsupId: str | None = None
    reportedOn: str | None = None


class DigitalAdvisorClusterOSRecommendation(OntapModel):
    """The ``ClusterOSRecommendation`` scalar fields."""

    recommendedLatestPatch: str | None = None
    recommendedVersion: str | None = None


class DigitalAdvisorCluster(OntapModel):
    """An Active IQ Digital Advisor cluster."""

    id: str | None = None
    name: str | None = None
    managementIPAddress: str | None = None
    osVersion: str | None = None
    isNodar: bool | None = None
    isBlueXpConnected: bool | None = None
    isHAConfigured: bool | None = None
    vmwareFlag: bool | None = None
    systemsWithCriticalPropensity: float | None = None
    systemsWithHighPropensity: float | None = None
    operationalDate: str | None = None
    ageInYears: int | None = None
    capacity: DigitalAdvisorClusterCapacity | None = None
    osRecommendation: DigitalAdvisorClusterOSRecommendation | None = None
    storageVirtualMachines: DigitalAdvisorCount | None = None
    s3Buckets: DigitalAdvisorCount | None = None
    snapMirrorRelationships: DigitalAdvisorCount | None = None
