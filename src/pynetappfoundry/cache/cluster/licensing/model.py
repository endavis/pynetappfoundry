"""License information — /cluster/licensing/licenses."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class LicenseInstance(CacheModel):
    """Per-node license instance within a license package.

    Each entry in the API ``licenses[]`` array represents a license
    installed on a specific node.
    """

    active: bool = False
    capacity_max: int = 0
    compliance_state: str = ""
    evaluation: bool = False
    expiry_time: str = ""
    host_id: str = ""
    installed_license: str = ""
    owner: str = ""
    serial_number: str = ""
    shutdown_imminent: bool = False
    start_time: str = ""


class LicensePackage(CacheModel):
    """License package from /cluster/licensing/licenses.

    Represents a top-level license package (e.g. NFS, CIFS) with
    nested per-node license instances.
    """

    name: str = ""
    scope: str = ""
    state: str = ""
    description: str = ""
    entitlement_action: str = ""
    entitlement_risk: str = ""
    instances: list[LicenseInstance] = Field(default_factory=list)
