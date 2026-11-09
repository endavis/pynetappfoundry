"""Characterization tests for the cloud phase of the collector (issue #899)."""

from __future__ import annotations

from pynetappfoundry.cache.collector import MetadataCollector
from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata


def _meta(provider: str, node: str) -> CloudMetadata:
    return CloudMetadata(
        node=node,
        instance_id="inst-1",
        account_id="acct",
        provider=provider,
        resource_group_name="rg",
        instance_link="old-link",
        vm_name="old-name",
    )


class TestUpdateAzureCloudLinks:
    def test_azure_items_get_new_link_and_vm_name(self) -> None:
        collector = MetadataCollector()
        [updated] = collector._update_azure_cloud_links(
            [_meta("Azure", "n1")], "mycluster", is_ha=False
        )
        assert updated.vm_name == "mycluster"
        assert updated.instance_link != "old-link"
        assert updated.node == "n1"
        assert updated.resource_group_name == "rg"

    def test_non_azure_items_unchanged(self) -> None:
        collector = MetadataCollector()
        original = _meta("AWS", "n1")
        [updated] = collector._update_azure_cloud_links([original], "mycluster", is_ha=True)
        assert updated is original
        assert updated.instance_link == "old-link"
        assert updated.vm_name == "old-name"
