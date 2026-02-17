"""Tests for collector endpoint usage — verifies mappings are used instead of hardcoded strings."""

from __future__ import annotations

from pynetappfoundry.cache.ontap.protocols.nfs.export_policies.mapping import (
    ONTAPEXPORTPOLICY_MAPPING,
)
from pynetappfoundry.cache.ontap.storage.snapshot_policies.mapping import (
    ONTAPSNAPSHOTPOLICY_MAPPING,
)


class TestCollectorMappingEndpoints:
    """Verify that collector-relevant mappings have correct endpoints."""

    def test_snapshot_policies_includes_copies(self) -> None:
        """Snapshot-policies mapping includes copies in api_endpoint."""
        assert ",copies" in ONTAPSNAPSHOTPOLICY_MAPPING.api_endpoint

    def test_snapshot_policies_endpoint(self) -> None:
        """Snapshot-policies mapping has the expected full endpoint."""
        assert (
            ONTAPSNAPSHOTPOLICY_MAPPING.api_endpoint == "/storage/snapshot-policies?fields=*,copies"
        )

    def test_export_policies_bulk_endpoint(self) -> None:
        """Export-policies mapping has a bulk collection endpoint (no {id})."""
        assert "{" not in ONTAPEXPORTPOLICY_MAPPING.api_endpoint

    def test_export_policies_includes_rules(self) -> None:
        """Export-policies mapping includes rules in api_endpoint."""
        assert ",rules" in ONTAPEXPORTPOLICY_MAPPING.api_endpoint

    def test_export_policies_endpoint(self) -> None:
        """Export-policies mapping has the expected full endpoint."""
        assert (
            ONTAPEXPORTPOLICY_MAPPING.api_endpoint
            == "/protocols/nfs/export-policies?fields=*,rules"
        )

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
