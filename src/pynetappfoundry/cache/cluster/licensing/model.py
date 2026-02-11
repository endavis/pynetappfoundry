"""License information — /cluster/licensing/licenses."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class LicenseFeature(CacheModel):
    """License feature information."""

    name: str = ""
    state: str = ""  # compliant, noncompliant
    scope: str = ""  # cluster, node


class CapacityLicense(CacheModel):
    """Capacity-based license information."""

    name: str = ""
    licensed_capacity: int = 0  # bytes
    used_capacity: int = 0  # bytes


class LicenseInfo(CacheModel):
    """Licensing information.

    Contains feature and capacity licenses.
    """

    feature_licenses: list[LicenseFeature] = Field(default_factory=list)
    capacity_licenses: list[CapacityLicense] = Field(default_factory=list)
