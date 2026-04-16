"""DiiK8spv information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiK8spv(OntapModel):
    """DiiK8spv information."""

    phase: str = ""
    capacity_bytes: float = 0.0
    pv_type: str = ""
    name: str = ""
    kubernetes_cluster: str = ""
    storageclass: str = ""
