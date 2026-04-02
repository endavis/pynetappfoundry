"""Live field-group fetcher for ONTAP cluster metadata.

``FieldGroupFetcher`` lazily creates API/CLI clients and delegates to
:class:`MetadataCollector` methods to fetch individual field groups
on demand.  Results are returned in-memory only — nothing is persisted
to the cache database.
"""

from __future__ import annotations

import logging
from functools import cached_property
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pynetappfoundry.cache.collector import MetadataCollector
    from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
    from pynetappfoundry.clients.ontap.cli import ONTAPCLI
    from pynetappfoundry.core.config import Config

logger = logging.getLogger(__name__)

# Maps field group names to MetadataCollector method names.
_FIELD_GROUP_METHODS: dict[str, str] = {
    "cloud": "collect_cloud_metadata",
    "cluster": "collect_cluster_info",
    "nodes": "collect_nodes",
    "network": "collect_network",
    "storage": "collect_storage",
    "license_packages": "collect_licenses",
    "mediator": "collect_mediator",
    "relationships": "collect_relationships",
    "protocols": "collect_protocols",
}


class FieldGroupFetcher:
    """Fetch individual field groups from ONTAP API/CLI on demand.

    Clients and the collector are created lazily on first :meth:`fetch`
    call to avoid unnecessary network connections when the cache DB
    already has the data.

    Args:
        cluster_name: Name of the cluster (used for credentials lookup).
        cluster_ip: Management IP of the cluster.
        config: Config instance for credentials and API settings.
    """

    __slots__ = (
        "__dict__",  # needed for cached_property
        "_cluster_ip",
        "_cluster_name",
        "_config",
    )

    def __init__(
        self,
        cluster_name: str,
        cluster_ip: str,
        config: Config,
    ) -> None:
        self._cluster_name = cluster_name
        self._cluster_ip = cluster_ip
        self._config = config

    @cached_property
    def api_client(self) -> ONTAPAPIClient | None:
        """Lazily create the ONTAP REST API client.

        Returns ``None`` if client creation fails (missing credentials,
        unreachable cluster, etc.).
        """
        try:
            from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
            from pynetappfoundry.core.models import ClusterConfig

            cluster_obj = ClusterConfig(name=self._cluster_name, ip=self._cluster_ip)
            return ONTAPAPIClient(cluster=cluster_obj, config=self._config)
        except Exception:
            logger.debug(
                "Could not create API client for %s: credentials or config unavailable",
                self._cluster_name,
                exc_info=True,
            )
            return None

    @cached_property
    def cli_client(self) -> ONTAPCLI | None:
        """Lazily create the ONTAP CLI (SSH) client.

        Returns ``None`` if client creation fails (missing credentials, etc.).
        """
        try:
            from pynetappfoundry.clients.ontap.cli import ONTAPCLI

            user, password = self._config.get_user("clusters", self._cluster_name)
            return ONTAPCLI(
                name=self._cluster_name,
                host_or_ip=self._cluster_ip,
                username=user,
                password=password,
            )
        except Exception:
            logger.debug(
                "Could not create CLI client for %s: credentials unavailable",
                self._cluster_name,
                exc_info=True,
            )
            return None

    @cached_property
    def collector(self) -> MetadataCollector:
        """Lazily create the :class:`MetadataCollector`."""
        from pynetappfoundry.cache.collector import MetadataCollector

        return MetadataCollector(
            api_client=self.api_client,
            cli_client=self.cli_client,
            parallel=False,
        )

    def fetch(self, field_group: str) -> Any:
        """Fetch a single field group from the live ONTAP system.

        Args:
            field_group: One of the keys in :data:`_FIELD_GROUP_METHODS`
                (e.g. ``"cluster"``, ``"storage"``).

        Returns:
            The collected data (model instance, list, etc.) or ``None``
            if the field group is unknown or fetching fails.
        """
        method_name = _FIELD_GROUP_METHODS.get(field_group)
        if method_name is None:
            logger.warning("Unknown field group: %s", field_group)
            return None

        try:
            method = getattr(self.collector, method_name)
            result = method()
            logger.debug(
                "Fetched field group '%s' for %s via live API/CLI",
                field_group,
                self._cluster_name,
            )
            return result
        except Exception:
            logger.debug(
                "Failed to fetch field group '%s' for %s",
                field_group,
                self._cluster_name,
                exc_info=True,
            )
            return None
