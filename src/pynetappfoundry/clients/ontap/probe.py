"""Shared ONTAP connectivity probe used by ``nf utils validate`` and ``nf doctor``."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
from pynetappfoundry.core.config import Config
from pynetappfoundry.core.models import ClusterConfig


@dataclass(frozen=True)
class ClusterProbe:
    """Result of a successful ``GET /cluster``.

    Attributes:
        client: The client that made the call, reusable for further requests.
        cluster_name: The name the cluster reports, or ``""`` when it reports none.
        name_matches: True when ``cluster_name`` equals the configured name.
    """

    client: ONTAPAPIClient
    cluster_name: str
    name_matches: bool


def probe_cluster(
    name: str,
    details: dict[str, Any],
    config: Config,
    *,
    client_factory: Callable[..., ONTAPAPIClient] | None = None,
) -> ClusterProbe:
    """Connect to one cluster and compare its reported name with the configured one.

    Prints nothing; every failure propagates to the caller.

    Args:
        name: The configured cluster name (its ``[clusters]`` key).
        details: The cluster's configuration table.
        config: Configuration object.
        client_factory: Builds the client, called as ``factory(cluster=..., config=...)``.
            Defaults to :class:`ONTAPAPIClient`.

    Returns:
        The probe result.
    """
    factory = client_factory or ONTAPAPIClient
    client = factory(cluster=ClusterConfig(**details), config=config)
    response = client.call_endpoint("/cluster")
    cluster_name = response.get("name", "") if isinstance(response, dict) else ""
    return ClusterProbe(client=client, cluster_name=cluster_name, name_matches=cluster_name == name)
