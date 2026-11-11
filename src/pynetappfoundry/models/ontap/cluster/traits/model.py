"""Computed cluster traits - hand-written, not generated from the REST API."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class ClusterTraits(OntapModel):
    """Values computed from other collected data, not returned by ``/cluster``.

    Generated models carry only API data; values derived from other objects
    live in a separate hand-written model like this one (ADR-0024).  Both
    fields are derived from the collected nodes by the hooks in
    ``src/pynetappfoundry/cache/ontap/cluster/traits/mapping.py``.
    """

    is_ha: bool = False  # More than one node in the cluster
    is_cloud: bool = False  # Any node looks like a Cloud Volumes ONTAP node
