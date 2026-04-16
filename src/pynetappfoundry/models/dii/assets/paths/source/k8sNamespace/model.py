"""DiiK8snamespace information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiK8snamespace(OntapModel):
    """DiiK8snamespace information."""

    name: str = ""
    kubernetes_cluster: str = ""
