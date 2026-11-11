"""REST API phases of the metadata collector (#899).

``ApiPhasesMixin`` holds the cached API call, the generic model fetch and
every API-only collection phase.  Composite phases (network, storage,
relationships, protocols) fan their per-model fetches out through
:func:`~pynetappfoundry.cache._collector_runner.run_tasks`.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from concurrent.futures import Future
from functools import partial
from typing import Any, TypeVar, cast

from pydantic import BaseModel

from pynetappfoundry.cache._collector_base import _CollectorState, logger
from pynetappfoundry.cache._collector_runner import (
    NETWORK_FETCH_WORKERS,
    PROTOCOLS_FETCH_WORKERS,
    RELATIONSHIPS_FETCH_WORKERS,
    STORAGE_FETCH_WORKERS,
    CollectionError,
    run_tasks,
)
from pynetappfoundry.cache._metadata import RelationshipsInfo
from pynetappfoundry.cache.fetchers import _resolve_parent_ids
from pynetappfoundry.cache.fetchers import fetch as _fetch
from pynetappfoundry.cache.field_mapping import TypeMapping
from pynetappfoundry.cache.field_mapping import (
    parse_api_record as _parse_api_record_raw,
)
from pynetappfoundry.cache.field_mapping import (
    parse_api_response as _parse_api_response_raw,
)
from pynetappfoundry.cache.ontap.svm.svms.top_metrics.users.mapping import (
    ONTAPTOPMETRICSSVMUSER_MAPPING,
)
from pynetappfoundry.models.ontap.cloud.targets.model import OntapCloudTarget
from pynetappfoundry.models.ontap.cluster.licensing.licenses.model import (
    OntapLicensePackageResponse,
)
from pynetappfoundry.models.ontap.cluster.mediators.model import OntapMediatorResponse
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse
from pynetappfoundry.models.ontap.cluster.peers.model import OntapClusterPeer
from pynetappfoundry.models.ontap.cluster.schedules.model import OntapSchedule
from pynetappfoundry.models.ontap.cluster.traits.model import ClusterTraits
from pynetappfoundry.models.ontap.name_services.dns.model import OntapDns
from pynetappfoundry.models.ontap.network.ethernet.broadcast_domains.model import (
    OntapBroadcastDomain,
)
from pynetappfoundry.models.ontap.network.ip.interfaces.model import OntapIpInterface
from pynetappfoundry.models.ontap.network.ip.subnets.model import OntapIpSubnet
from pynetappfoundry.models.ontap.network.model import NetworkInfo
from pynetappfoundry.models.ontap.private.cli.vserver.services.web.model import (
    OntapSvmWebService,
)
from pynetappfoundry.models.ontap.protocols.cifs.services.model import OntapCifsService
from pynetappfoundry.models.ontap.protocols.cifs.shares.model import OntapCifsShare
from pynetappfoundry.models.ontap.protocols.model import ProtocolsInfo
from pynetappfoundry.models.ontap.protocols.nfs.export_policies.model import OntapExportPolicy
from pynetappfoundry.models.ontap.protocols.nfs.services.model import OntapNfsService
from pynetappfoundry.models.ontap.protocols.s3.buckets.model import OntapS3Bucket
from pynetappfoundry.models.ontap.protocols.san.igroups.model import OntapIgroup
from pynetappfoundry.models.ontap.snapmirror.relationships.model import (
    OntapSnapmirrorRelationship,
)
from pynetappfoundry.models.ontap.storage.aggregates.model import OntapAggregate
from pynetappfoundry.models.ontap.storage.flexcache.flexcaches.model import OntapFlexcache
from pynetappfoundry.models.ontap.storage.luns.model import OntapLun
from pynetappfoundry.models.ontap.storage.model import StorageInfo
from pynetappfoundry.models.ontap.storage.qos.policies.model import OntapQosPolicy
from pynetappfoundry.models.ontap.storage.qtrees.model import OntapQtree
from pynetappfoundry.models.ontap.storage.snapshot_policies.model import OntapSnapshotPolicy
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume
from pynetappfoundry.models.ontap.svm.peers.model import OntapSvmPeer
from pynetappfoundry.models.ontap.svm.svms.model import OntapSvm
from pynetappfoundry.models.ontap.svm.svms.top_metrics.users.model import OntapTopMetricsSvmUser

# Cache collector skips realtime fields (volatile metrics not persisted).
parse_api_record = partial(_parse_api_record_raw, skip_realtime=True)
parse_api_response = partial(_parse_api_response_raw, skip_realtime=True)

_T = TypeVar("_T")


class ApiPhasesMixin(_CollectorState):
    """Cached API access and the API-only collection phases."""

    # -------------------------------------------------------------------------
    # API access
    # -------------------------------------------------------------------------

    def _cached_api_call(self, endpoint: str, method: str = "GET", *, paginate: bool = True) -> Any:
        """Make an API call with caching to avoid duplicate requests.

        Concurrent callers for the same endpoint share one request: the first
        caller fetches (outside the lock, so other endpoints stay parallel)
        and the rest wait on its in-flight future.  A failed request is
        shared with the waiting callers but never cached, so a later call
        retries.

        Args:
            endpoint: The API endpoint to call.
            method: HTTP method (default GET).
            paginate: When True (default), use ``get_all_records()`` to
                follow pagination and merge all pages.  When False, use
                ``call_endpoint()`` which returns only the first page
                (suitable for single-object endpoints like ``/cluster``).

        Returns:
            API response data (from cache if available).
        """
        if not self.api_client:
            return None

        api_client = self.api_client

        def call() -> Any:
            logger.debug("%s API call: %s %s", self._log_prefix, method, endpoint)
            if paginate:
                return api_client.get_all_records(endpoint, method=method)
            return api_client.call_endpoint(endpoint, method=method)

        return self._single_flight(f"{method}:{endpoint}", call)

    def _single_flight(self, cache_key: str, call: Callable[[], _T]) -> _T:
        """Run ``call`` once per ``cache_key``, sharing and caching its result.

        The first caller runs ``call`` outside the lock (so other keys stay
        parallel) and concurrent callers wait on its in-flight future.  A
        failure is shared with the waiting callers but never cached, so a
        later call retries.  Results live in ``_api_cache`` until
        ``_clear_cache()``.

        Args:
            cache_key: Identity of the call (e.g. ``"GET:/cluster"``).
            call: Zero-argument callable that produces the value.

        Returns:
            The value from ``call`` (from cache if available).
        """
        waiting_on: Future[Any] | None = None
        own_future: Future[Any] | None = None
        with self._cache_lock:
            if cache_key in self._api_cache:
                logger.debug("%s API cache hit: %s", self._log_prefix, cache_key)
                return cast(_T, self._api_cache[cache_key])
            waiting_on = self._inflight.get(cache_key)
            if waiting_on is None:
                own_future = Future()
                self._inflight[cache_key] = own_future

        if own_future is None:
            logger.debug("%s API call in flight, waiting: %s", self._log_prefix, cache_key)
            assert waiting_on is not None
            return cast(_T, waiting_on.result())

        try:
            response = call()
        except BaseException as e:
            with self._cache_lock:
                self._inflight.pop(cache_key, None)
            own_future.set_exception(e)
            raise

        with self._cache_lock:
            self._api_cache[cache_key] = response
            self._inflight.pop(cache_key, None)
        own_future.set_result(response)
        return response

    def _clear_cache(self) -> None:
        """Clear the API response cache."""
        with self._cache_lock:
            self._api_cache.clear()

    def _fetch_model(self, model_class: type[BaseModel]) -> Any:
        """Delegate to the generic ``fetch()`` dispatcher for one model class.

        Thin shim used by composite phase methods so that each per-model
        fetch can be submitted to a ``ThreadPoolExecutor`` (preserving
        the existing parallelism). Always supplies the collector's
        shared ``_results_cache`` so that post-collection hooks can
        short-circuit cross-model dependencies.
        """
        return _fetch(
            model_class,
            cluster=self._cluster_name,
            config=None,
            api_client=self.api_client,  # type: ignore[arg-type]
            cli_client=self.cli_client,
            results_cache=self._results_cache,
            log_prefix=self._log_prefix,
        )

    def _collect_parameterized(
        self,
        mapping: TypeMapping,
        parent_objects: Sequence[BaseModel],
    ) -> list[BaseModel]:
        """Fetch child records from a parameterized endpoint by iterating parents.

        For each parent object, substitutes the parent's identifier into the
        URL placeholder, fetches child records, and aggregates them.

        Args:
            mapping: Child TypeMapping (must have parent_mapping and parent_id_field set).
            parent_objects: List of already-collected parent model instances.

        Returns:
            Aggregated list of child model instances across all parents.

        Raises:
            ValueError: If mapping.parent_mapping or mapping.parent_id_field is not set.
        """
        if not mapping.parent_mapping:
            raise ValueError(
                f"{mapping.name}: parent_mapping must be set for parameterized collection"
            )
        if not mapping.effective_parent_id_fields():
            raise ValueError(
                f"{mapping.name}: parent_id_field must be set for parameterized collection"
            )

        aggregated: list[BaseModel] = []
        for parent in parent_objects:
            values, missing = _resolve_parent_ids(mapping, parent)
            if values is None:
                parent_name = getattr(parent, "name", repr(parent))
                logger.warning(
                    "%s SKIP_PARENT: %s - parent %s has no '%s'",
                    self._log_prefix,
                    mapping.name,
                    parent_name,
                    missing,
                )
                continue

            url = mapping.build_parameterized_url(values[0] if len(values) == 1 else values)
            try:
                response = self._cached_api_call(url)
                children = parse_api_response(
                    mapping, response, self._log_prefix, self._log_missing_fields
                )
                aggregated.extend(children)
            except Exception as e:
                parent_name = getattr(parent, "name", repr(parent))
                logger.warning(
                    "%s CHILD_FETCH_FAILED: %s for parent %s - %s: %s",
                    self._log_prefix,
                    mapping.name,
                    parent_name,
                    type(e).__name__,
                    e,
                )

        return aggregated

    def _api_phase(self, label: str, via: Callable[[], _T]) -> _T:
        """Run an API-only phase: require a client, log and re-raise failures.

        Args:
            label: Human-readable phase label used in the error messages.
            via: The ``_collect_*_via_api`` method to run.

        Raises:
            CollectionError: If no API client is available.
        """
        if not self.api_client:
            raise CollectionError(
                f"{self._log_prefix} API_FAILURE: {label} - no API client available"
            )
        try:
            return via()
        except Exception as e:
            logger.error(
                "%s API_FAILURE: %s - %s: %s",
                self._log_prefix,
                label,
                type(e).__name__,
                e,
            )
            raise

    def _fetch_tasks(
        self, model_tasks: Sequence[tuple[str, type[BaseModel]]]
    ) -> list[tuple[str, Callable[[], Any]]]:
        """Bind each ``(key, model_class)`` to a ``_fetch_model`` call."""
        return [(key, partial(self._fetch_model, mc)) for key, mc in model_tasks]

    # -------------------------------------------------------------------------
    # Cluster Info / Nodes
    # -------------------------------------------------------------------------

    def collect_cluster_info(self) -> ClusterInfo:
        """Collect cluster identity information (API-only).

        Returns:
            ClusterInfo object.

        Raises:
            CollectionError: If no API client is available.
            Exception: If the API call fails.
        """
        return self._api_phase("Cluster info", self._collect_cluster_info_via_api)

    def _collect_cluster_info_via_api(self) -> ClusterInfo:
        """Collect cluster info using REST API.

        Returns:
            ClusterInfo from /cluster endpoint.
        """
        if not self.api_client:
            logger.debug("%s No API client available for cluster info collection", self._log_prefix)
            return ClusterInfo()

        # Nodes first: fills _results_cache so fetch() skips its own dependency
        # fetch of OntapNodeResponse (#929).
        self._collect_nodes_via_api()
        return cast(ClusterInfo, self._fetch_model(ClusterInfo))

    def collect_cluster_traits(self) -> ClusterTraits:
        """Collect the computed cluster traits (``is_ha``, ``is_cloud``).

        Returns:
            ClusterTraits derived from the collected nodes.

        Raises:
            CollectionError: If no API client is available.
            Exception: If the API call fails.
        """
        return self._api_phase("Cluster traits", self._collect_cluster_traits_via_api)

    def _collect_cluster_traits_via_api(self) -> ClusterTraits:
        """Compute cluster traits from the nodes fetched via REST API.

        Returns:
            ClusterTraits; defaults when there is no API client.
        """
        if not self.api_client:
            logger.debug("%s No API client available for cluster traits", self._log_prefix)
            return ClusterTraits()

        # Nodes first: fills _results_cache so fetch() does not fetch them again.
        self._collect_nodes_via_api()
        return cast(ClusterTraits, self._fetch_model(ClusterTraits))

    def collect_nodes(self) -> list[OntapNodeResponse]:
        """Collect node information (API-only).

        Returns:
            List of OntapNodeResponse objects.

        Raises:
            CollectionError: If no API client is available.
            Exception: If the API call fails.
        """
        return self._api_phase("Nodes", self._collect_nodes_via_api)

    def _collect_nodes_via_api(self) -> list[OntapNodeResponse]:
        """Collect nodes using REST API.

        Returns:
            List of OntapNodeResponse from /cluster/nodes endpoint.
        """
        if not self.api_client:
            logger.debug("%s No API client available for nodes collection", self._log_prefix)
            return []

        nodes = self._single_flight(
            "model:OntapNodeResponse",
            lambda: cast(list[OntapNodeResponse], self._fetch_model(OntapNodeResponse)),
        )
        # Publish for downstream phases (e.g. cluster's compute_is_ha hook).
        self._results_cache["OntapNodeResponse"] = nodes
        return nodes

    # -------------------------------------------------------------------------
    # Network
    # -------------------------------------------------------------------------

    def collect_network(self) -> NetworkInfo:
        """Collect network configuration (API-only).

        Returns:
            NetworkInfo object.

        Raises:
            CollectionError: If no API client is available.
            Exception: If the API call fails.
        """
        return self._api_phase("Network", self._collect_network_via_api)

    def _collect_network_via_api(self) -> NetworkInfo:
        """Collect network info using REST API.

        Makes parallel API calls for improved performance.

        Returns:
            NetworkInfo from various network endpoints.
        """
        if not self.api_client:
            logger.debug("%s No API client available for network collection", self._log_prefix)
            return NetworkInfo()

        # Each task fetches one model class via the generic fetch() dispatcher;
        # the IP spaces come from a cached raw call.
        ipspace_url = "/network/ipspaces?fields=*"
        model_tasks: list[tuple[str, type[BaseModel]]] = [
            ("ip_interfaces", OntapIpInterface),
            ("broadcast_domains", OntapBroadcastDomain),
            ("dns", OntapDns),
            ("subnets", OntapIpSubnet),
        ]
        tasks: list[tuple[str, Callable[[], Any]]] = [
            *self._fetch_tasks(model_tasks),
            ("ipspace_response", partial(self._cached_api_call, ipspace_url)),
        ]
        results = run_tasks(tasks, parallel=self.parallel, max_workers=NETWORK_FETCH_WORKERS)

        ipspace_response = results.get("ipspace_response") or {}
        logger.debug(
            "%s API response: %d IPspaces",
            self._log_prefix,
            len(ipspace_response.get("records", [])),
        )
        ipspaces = [r.get("name", "") for r in ipspace_response.get("records", [])]

        return NetworkInfo(
            ip_interfaces=cast(list[OntapIpInterface], results["ip_interfaces"]),
            ethernet_broadcast_domains=cast(
                list[OntapBroadcastDomain], results["broadcast_domains"]
            ),
            ipspaces=ipspaces,
            dns=cast(list[OntapDns], results["dns"]),
            ip_subnets=cast(list[OntapIpSubnet], results["subnets"]),
        )

    # -------------------------------------------------------------------------
    # Storage
    # -------------------------------------------------------------------------

    def collect_storage(self) -> StorageInfo:
        """Collect storage topology information (API-only).

        Returns:
            StorageInfo object.

        Raises:
            CollectionError: If no API client is available.
            Exception: If the API call fails.
        """
        return self._api_phase("Storage", self._collect_storage_via_api)

    def _collect_storage_via_api(self) -> StorageInfo:
        """Collect storage info using REST API.

        Makes parallel API calls for improved performance.

        Returns:
            StorageInfo from aggregate, SVM, and cloud target endpoints.
        """
        if not self.api_client:
            logger.debug("%s No API client available for storage collection", self._log_prefix)
            return StorageInfo()

        # OntapCloudTarget tolerates absence on older ONTAP versions and
        # OntapSvmWebService tolerates a role without private CLI access.
        model_tasks: list[tuple[str, type[BaseModel]]] = [
            ("aggregates", OntapAggregate),
            ("svms", OntapSvm),
            ("cloud_targets", OntapCloudTarget),
            ("volumes", OntapVolume),
            ("qtrees", OntapQtree),
            ("snapshot_policies", OntapSnapshotPolicy),
            ("schedules", OntapSchedule),
            ("luns", OntapLun),
            ("igroups", OntapIgroup),
            ("qos_policies", OntapQosPolicy),
            ("flexcaches", OntapFlexcache),
            ("svm_web_services", OntapSvmWebService),
        ]

        def safe_fetch_model(model_class: type[BaseModel]) -> Any:
            """Fetch a model, returning [] on failure for optional endpoints."""
            try:
                return self._fetch_model(model_class)
            except Exception as e:
                if model_class is OntapCloudTarget:
                    logger.debug("%s Cloud targets endpoint not available: %s", self._log_prefix, e)
                    return []
                if model_class is OntapSvmWebService:
                    logger.debug(
                        "%s SVM web services (private CLI) not available: %s", self._log_prefix, e
                    )
                    return []
                raise

        tasks = [(key, partial(safe_fetch_model, mc)) for key, mc in model_tasks]
        results = run_tasks(tasks, parallel=self.parallel, max_workers=STORAGE_FETCH_WORKERS)

        return StorageInfo(
            aggregates=cast(list[OntapAggregate], results["aggregates"]),
            svms=cast(list[OntapSvm], results["svms"]),
            cloud_targets=cast(list[OntapCloudTarget], results["cloud_targets"]),
            volumes=cast(list[OntapVolume], results["volumes"]),
            qtrees=cast(list[OntapQtree], results["qtrees"]),
            snapshot_policies=cast(list[OntapSnapshotPolicy], results["snapshot_policies"]),
            schedules=cast(list[OntapSchedule], results["schedules"]),
            luns=cast(list[OntapLun], results["luns"]),
            igroups=cast(list[OntapIgroup], results["igroups"]),
            qos_policies=cast(list[OntapQosPolicy], results["qos_policies"]),
            flexcaches=cast(list[OntapFlexcache], results["flexcaches"]),
            svm_web_services=cast(list[OntapSvmWebService], results["svm_web_services"]),
        )

    # -------------------------------------------------------------------------
    # Licenses / Mediator
    # -------------------------------------------------------------------------

    def collect_licenses(self) -> list[OntapLicensePackageResponse]:
        """Collect licensing information (API-only).

        Returns:
            List of OntapLicensePackageResponse objects.

        Raises:
            CollectionError: If no API client is available.
            Exception: If the API call fails.
        """
        return self._api_phase("Licenses", self._collect_licenses_via_api)

    def _collect_licenses_via_api(self) -> list[OntapLicensePackageResponse]:
        """Collect licenses using REST API.

        Returns:
            List of OntapLicensePackageResponse from /cluster/licensing/licenses endpoint.
        """
        if not self.api_client:
            logger.debug("%s No API client available for license collection", self._log_prefix)
            return []

        return cast(
            list[OntapLicensePackageResponse], self._fetch_model(OntapLicensePackageResponse)
        )

    def collect_mediator(self) -> OntapMediatorResponse:
        """Collect ONTAP Mediator information (API-only).

        Returns:
            OntapMediatorResponse object.

        Raises:
            CollectionError: If no API client is available.
        """
        return self._api_phase("Mediator", self._collect_mediator_via_api)

    def _collect_mediator_via_api(self) -> OntapMediatorResponse:
        """Collect mediator info using REST API.

        Returns:
            OntapMediatorResponse from /cluster/mediators endpoint.
        """
        if not self.api_client:
            return OntapMediatorResponse()
        try:
            parsed = cast(list[OntapMediatorResponse], self._fetch_model(OntapMediatorResponse))
            if parsed:
                return parsed[0]
        except Exception as e:
            logger.debug("%s Mediator endpoint not available: %s", self._log_prefix, e)

        return OntapMediatorResponse()

    # -------------------------------------------------------------------------
    # Relationships
    # -------------------------------------------------------------------------

    def collect_relationships(self) -> RelationshipsInfo:
        """Collect cluster relationships information (API-only).

        Returns:
            RelationshipsInfo object.

        Raises:
            CollectionError: If no API client is available.
            Exception: If the API call fails.
        """
        return self._api_phase("Relationships", self._collect_relationships_via_api)

    def _collect_relationships_via_api(self) -> RelationshipsInfo:
        """Collect relationships using REST API.

        Makes parallel API calls for improved performance.

        Returns:
            RelationshipsInfo from snapmirror and cluster peer endpoints.
        """
        if not self.api_client:
            logger.debug(
                "%s No API client available for relationships collection", self._log_prefix
            )
            return RelationshipsInfo()

        model_tasks: list[tuple[str, type[BaseModel]]] = [
            ("snapmirror_destinations", OntapSnapmirrorRelationship),
            ("cluster_peers", OntapClusterPeer),
            ("svm_peers", OntapSvmPeer),
        ]
        results = run_tasks(
            self._fetch_tasks(model_tasks),
            parallel=self.parallel,
            max_workers=RELATIONSHIPS_FETCH_WORKERS,
        )

        return RelationshipsInfo(
            snapmirror_destinations=cast(
                list[OntapSnapmirrorRelationship], results["snapmirror_destinations"]
            ),
            cluster_peers=cast(list[OntapClusterPeer], results["cluster_peers"]),
            svm_peers=cast(list[OntapSvmPeer], results["svm_peers"]),
        )

    # -------------------------------------------------------------------------
    # Parameterized Endpoint Collection
    # -------------------------------------------------------------------------

    def _with_svm_top_metrics_users(self, storage_info: StorageInfo) -> StorageInfo:
        """Return *storage_info* with ``svm_top_metrics_users`` collected for its SVMs."""
        svm_top_metrics_users = self._collect_svm_top_metrics_users(storage_info.svms)
        return storage_info.model_copy(update={"svm_top_metrics_users": svm_top_metrics_users})

    def _collect_svm_top_metrics_users(self, svms: list[OntapSvm]) -> list[OntapTopMetricsSvmUser]:
        """Collect top-metrics users per SVM using parameterized endpoint.

        Args:
            svms: List of collected SVM objects (parents).

        Returns:
            Aggregated list of OntapTopMetricsSvmUser across all SVMs.
        """
        if not self.api_client:
            return []
        return cast(
            list[OntapTopMetricsSvmUser],
            self._collect_parameterized(ONTAPTOPMETRICSSVMUSER_MAPPING, svms),
        )

    # -------------------------------------------------------------------------
    # Protocols
    # -------------------------------------------------------------------------

    def collect_protocols(self) -> ProtocolsInfo:
        """Collect protocol configuration information (API-only).

        Returns:
            ProtocolsInfo object.

        Raises:
            CollectionError: If no API client is available.
            Exception: If the API call fails.
        """
        return self._api_phase("Protocols", self._collect_protocols_via_api)

    def _collect_protocols_via_api(self) -> ProtocolsInfo:
        """Collect protocol info using REST API.

        Makes parallel API calls for improved performance.

        Returns:
            ProtocolsInfo from various protocol endpoints.
        """
        if not self.api_client:
            logger.debug("%s No API client available for protocols collection", self._log_prefix)
            return ProtocolsInfo()

        model_tasks: list[tuple[str, type[BaseModel]]] = [
            ("nfs_export_policies", OntapExportPolicy),
            ("cifs_shares", OntapCifsShare),
            ("nfs_services", OntapNfsService),
            ("cifs_services", OntapCifsService),
            ("s3_buckets", OntapS3Bucket),
        ]
        results = run_tasks(
            self._fetch_tasks(model_tasks),
            parallel=self.parallel,
            max_workers=PROTOCOLS_FETCH_WORKERS,
        )

        return ProtocolsInfo(
            nfs_export_policies=cast(list[OntapExportPolicy], results["nfs_export_policies"]),
            cifs_shares=cast(list[OntapCifsShare], results["cifs_shares"]),
            nfs_services=cast(list[OntapNfsService], results["nfs_services"]),
            cifs_services=cast(list[OntapCifsService], results["cifs_services"]),
            s3_buckets=cast(list[OntapS3Bucket], results["s3_buckets"]),
        )
