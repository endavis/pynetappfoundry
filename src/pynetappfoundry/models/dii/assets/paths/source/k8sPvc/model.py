"""DiiK8spvc information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiK8spvc(OntapModel):
    """DiiK8spvc information."""

    namespace: str = ""
    name: str = ""
    kubernetes_cluster: str = ""
