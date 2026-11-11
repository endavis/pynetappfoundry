"""Cloud-metadata phase of the metadata collector (#899).

Cloud metadata is the one CLI-only phase: ``virtual-machine instance show``
on cloud (CVO) clusters.  Its failure warns but never aborts collection.
"""

from __future__ import annotations

from typing import cast

from pynetappfoundry.cache._collector_base import _CollectorState, logger
from pynetappfoundry.cache._collector_cli import run_vm_instance_show
from pynetappfoundry.cache.fetchers import normalize_cli_key, parse_vm_instance_output
from pynetappfoundry.cache.field_mapping import parse_cli_records
from pynetappfoundry.cache.ontap.cloud.metadata.mapping import CLOUD_METADATA_MAPPING
from pynetappfoundry.cache.ontap.cluster.traits.mapping import _is_cloud_node
from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata
from pynetappfoundry.utils.cloud import (
    build_cloud_instance_link,
    build_cloud_instance_sso_link,
    build_cloud_resource_group_link,
    build_vm_name,
)


class CloudPhaseMixin(_CollectorState):
    """Cloud provider metadata collection (CLI-only, optional)."""

    def collect_cloud_metadata(self) -> list[CloudMetadata]:
        """Collect cloud provider metadata.

        Cloud metadata is only available via CLI (virtual-machine instance show).
        Returns one CloudMetadata per node in the cluster. This is the only
        CLI-only phase — failure warns but does not abort collection.

        Non-cloud (on-prem) clusters skip the CLI call entirely. Detection
        uses the nodes already fetched into ``_results_cache`` — if none
        match :func:`_is_cloud_node`, the method returns an empty list
        without touching the CLI client, avoiding a 10s SSH timeout on
        clusters that do not expose a cloud management service. See #547.

        This phase must run **after** :meth:`collect_nodes` so that
        ``_results_cache["OntapNodeResponse"]`` is populated before CVO
        detection runs.  Both the sequential and parallel runners enforce
        this ordering.

        Returns:
            List of CloudMetadata objects, one per node.
        """
        nodes = self._results_cache.get("OntapNodeResponse", [])
        if not nodes or not any(_is_cloud_node(n) for n in nodes):
            logger.debug(
                "%s Skipping cloud metadata: no CVO nodes detected",
                self._log_prefix,
            )
            return []
        if self.cli_client:
            try:
                return self._collect_cloud_metadata_via_cli()
            except Exception as e:
                logger.error(
                    "%s CLI_FAILURE: Cloud metadata - %s: %s",
                    self._log_prefix,
                    type(e).__name__,
                    e,
                )
        return []

    def _collect_cloud_metadata_via_cli(self) -> list[CloudMetadata]:
        """Collect cloud metadata using CLI.

        Parses the raw CLI text into dict records, feeds them through
        ``parse_cli_records`` via the ``CLOUD_METADATA_MAPPING``, and
        then post-processes the results to build computed link fields
        that depend on collector state (``aws_sso_config``).

        Returns:
            List of CloudMetadata from virtual-machine instance show.
        """
        if not self.cli_client:
            logger.debug(
                "%s No CLI client available for cloud metadata collection", self._log_prefix
            )
            return []

        # A background SSH pre-connect may still be running; wait for it
        # rather than racing it (only CVO clusters reach this point).
        if self._ssh_preconnect is not None:
            self._ssh_preconnect.wait()

        output = run_vm_instance_show(self.cli_client, self._log_prefix)

        records = parse_vm_instance_output(output)
        items = parse_cli_records(
            CLOUD_METADATA_MAPPING,
            records,
            self._log_prefix,
            self._log_missing_fields,
        )
        results = cast(list[CloudMetadata], items)

        for cm in results:
            self._apply_cloud_links(cm)

        return results

    def _apply_cloud_links(self, cm: CloudMetadata) -> None:
        """Build the computed link fields on *cm* in place."""
        region = cm.region or cm.availability_zone
        cm.instance_link = build_cloud_instance_link(
            provider=cm.provider,
            instance_id=cm.instance_id,
            region=region,
            account_id=cm.account_id,
            resource_group=cm.resource_group_name,
        )
        cm.instance_sso_link = build_cloud_instance_sso_link(
            provider=cm.provider,
            instance_link=cm.instance_link,
            account_id=cm.account_id,
            sso_config=self.aws_sso_config,
        )
        cm.resource_group_link = build_cloud_resource_group_link(
            provider=cm.provider,
            account_id=cm.account_id,
            resource_group=cm.resource_group_name,
        )
        # Set vm_name without cluster context; for Azure this is
        # overwritten by _update_azure_cloud_links() which has
        # cluster_name and node info for the proper derivation.
        cm.vm_name = build_vm_name(
            provider=cm.provider,
            instance_id=cm.instance_id,
        )

    def _parse_vm_instance_output(self, output: list[str]) -> list[dict[str, str]]:
        """Parse virtual-machine instance show output into raw records.

        Delegates to :func:`pynetappfoundry.cache.fetchers.parse_vm_instance_output`.

        Args:
            output: Lines of CLI output.

        Returns:
            List of raw record dicts (one per node) with normalized keys.
        """
        return parse_vm_instance_output(output)

    def _update_azure_cloud_links(
        self,
        cloud_metadata: list[CloudMetadata],
        cluster_name: str,
        is_ha: bool,
    ) -> list[CloudMetadata]:
        """Update Azure cloud metadata with correct instance links.

        Azure VM portal links require the VM name derived from cluster name
        and node information, not the instance_id from cloud metadata.

        Args:
            cloud_metadata: List of CloudMetadata objects to update.
            cluster_name: The cluster name.
            is_ha: Whether the cluster is HA.

        Returns:
            Updated list of CloudMetadata with correct Azure instance links.
        """
        updated = []
        for meta in cloud_metadata:
            if meta.provider.lower() != "azure":
                updated.append(meta)
                continue

            # Rebuild the instance link with cluster/node info
            instance_link = build_cloud_instance_link(
                provider=meta.provider,
                instance_id=meta.instance_id,
                account_id=meta.account_id,
                resource_group=meta.resource_group_name,
                cluster_name=cluster_name,
                node_name=meta.node,
                is_ha=is_ha,
            )

            # Rebuild SSO link (not applicable for Azure, but keep for consistency)
            instance_sso_link = build_cloud_instance_sso_link(
                provider=meta.provider,
                instance_link=instance_link,
                account_id=meta.account_id,
                sso_config=self.aws_sso_config,
            )

            vm_name = build_vm_name(
                provider=meta.provider,
                cluster_name=cluster_name,
                node_name=meta.node,
                instance_id=meta.instance_id,
                is_ha=is_ha,
            )

            # Create updated CloudMetadata with new links
            updated.append(
                CloudMetadata(
                    node=meta.node,
                    instance_id=meta.instance_id,
                    account_id=meta.account_id,
                    image_id=meta.image_id,
                    instance_type=meta.instance_type,
                    cpu_platform=meta.cpu_platform,
                    region=meta.region,
                    provider=meta.provider,
                    consumer=meta.consumer,
                    primary_ip=meta.primary_ip,
                    metadata_version=meta.metadata_version,
                    availability_zone=meta.availability_zone,
                    availability_zone_id=meta.availability_zone_id,
                    fault_domain=meta.fault_domain,
                    update_domain=meta.update_domain,
                    resource_group_name=meta.resource_group_name,
                    offer=meta.offer,
                    sku=meta.sku,
                    sku_version=meta.sku_version,
                    instance_link=instance_link,
                    instance_sso_link=instance_sso_link,
                    resource_group_link=meta.resource_group_link,
                    vm_name=vm_name,
                )
            )
        return updated

    @staticmethod
    def _normalize_cli_key(key: str) -> str:
        """Normalize CLI output key to snake_case.

        Delegates to :func:`pynetappfoundry.cache.fetchers.normalize_cli_key`.

        Args:
            key: Original key from CLI output.

        Returns:
            Normalized key name.
        """
        return normalize_cli_key(key)
