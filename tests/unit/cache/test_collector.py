"""Tests for collector endpoint usage — verifies mappings produce correct collection URLs."""

from __future__ import annotations

from pynetappfoundry.cache.ontap.protocols.nfs.export_policies.mapping import (
    ONTAPEXPORTPOLICY_MAPPING,
)
from pynetappfoundry.cache.ontap.storage.snapshot_policies.mapping import (
    ONTAPSNAPSHOTPOLICY_MAPPING,
)


class TestCollectorMappingEndpoints:
    """Verify that collector-relevant mappings have correct endpoints."""

    def test_snapshot_policies_api_endpoint_simplified(self) -> None:
        """Snapshot-policies api_endpoint is now simplified to ?fields=*."""
        assert ONTAPSNAPSHOTPOLICY_MAPPING.api_endpoint == "/storage/snapshot-policies?fields=*"

    def test_snapshot_policies_build_collection_url_includes_copies(self) -> None:
        """build_collection_url() dynamically appends copies."""
        url = ONTAPSNAPSHOTPOLICY_MAPPING.build_collection_url()
        assert ",copies" in url

    def test_snapshot_policies_collection_url(self) -> None:
        """Snapshot-policies build_collection_url() has the expected full URL."""
        assert (
            ONTAPSNAPSHOTPOLICY_MAPPING.build_collection_url()
            == "/storage/snapshot-policies?fields=*,copies"
        )

    def test_export_policies_bulk_endpoint(self) -> None:
        """Export-policies api_endpoint has no {id} placeholder."""
        assert "{" not in ONTAPEXPORTPOLICY_MAPPING.api_endpoint

    def test_export_policies_api_endpoint_simplified(self) -> None:
        """Export-policies api_endpoint is now simplified to ?fields=*."""
        assert ONTAPEXPORTPOLICY_MAPPING.api_endpoint == "/protocols/nfs/export-policies?fields=*"

    def test_export_policies_build_collection_url(self) -> None:
        """build_collection_url() returns base endpoint (no expensive fields annotated)."""
        url = ONTAPEXPORTPOLICY_MAPPING.build_collection_url()
        assert url == "/protocols/nfs/export-policies?fields=*"

    def test_export_policies_records_path(self) -> None:
        """Export-policies mapping uses standard records path."""
        assert ONTAPEXPORTPOLICY_MAPPING.records_path == "records"

    def test_export_policies_no_parent_mapping(self) -> None:
        """Export-policies mapping has no parent_mapping for bulk collection."""
        assert ONTAPEXPORTPOLICY_MAPPING.parent_mapping is None

    def test_snapshot_policies_copies_requires_explicit_fetch(self) -> None:
        """Snapshot-policies copies field has requires_explicit_fetch=True."""
        copies_field = next(
            f for f in ONTAPSNAPSHOTPOLICY_MAPPING.fields if f.cache_attr == "copies"
        )
        assert copies_field.requires_explicit_fetch is True
