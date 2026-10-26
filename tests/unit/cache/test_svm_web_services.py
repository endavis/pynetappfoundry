"""Tests for SVM web services collected through the private CLI passthrough (#866)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cache import CachedClusterMetadata, ClusterMetadataDB, MetadataCollector
from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.diff import compute_diff
from pynetappfoundry.cache.field_mapping import parse_api_response
from pynetappfoundry.cache.ontap.private.cli.vserver.services.web.mapping import (
    ONTAPSVMWEBSERVICE_MAPPING,
)
from pynetappfoundry.cli.main import nf
from pynetappfoundry.models.ontap.private.cli.vserver.services.web.model import (
    OntapSvmWebService,
)
from pynetappfoundry.models.ontap.storage.model import StorageInfo

ENDPOINT = "/private/cli/vserver/services/web?fields=vserver,name,enabled"

# The shape of GET /api/private/cli/vserver/services/web?fields=vserver,name,enabled.
PRIVATE_CLI_RESPONSE: dict[str, Any] = {
    "records": [
        {"vserver": "svm1", "name": "sysmgr", "enabled": True},
        {"vserver": "svm1", "name": "saml", "enabled": False},
        {"vserver": "svm2", "name": "sysmgr", "enabled": True},
    ],
    "num_records": 3,
}


def _noop_log(*_args: Any) -> None:
    return None


def _services(*records: tuple[str, str, bool]) -> list[OntapSvmWebService]:
    return [OntapSvmWebService(vserver=v, name=n, enabled=e) for v, n, e in records]


def _metadata(services: list[OntapSvmWebService]) -> CachedClusterMetadata:
    return CachedClusterMetadata(
        cluster_name="test-cluster",
        cached_at=datetime(2026, 10, 26, tzinfo=UTC),
        storage=StorageInfo(svm_web_services=services),
    )


class TestModel:
    def test_defaults(self) -> None:
        service = OntapSvmWebService()

        assert (service.vserver, service.name, service.enabled) == ("", "", False)

    def test_service_key_combines_vserver_and_name(self) -> None:
        assert OntapSvmWebService(vserver="svm1", name="sysmgr").service_key == "svm1/sysmgr"

    def test_service_key_follows_vserver_and_name(self) -> None:
        """Derived on every validation, so a stored value cannot drift."""
        service = OntapSvmWebService.model_validate(
            {"vserver": "svm2", "name": "saml", "service_key": "stale/value"}
        )

        assert service.service_key == "svm2/saml"


class TestMapping:
    def test_registered_for_the_model(self) -> None:
        assert (
            model_registry.get_mapping_by_model_class(OntapSvmWebService)
            is ONTAPSVMWEBSERVICE_MAPPING
        )

    def test_points_at_the_private_cli_endpoint(self) -> None:
        assert ONTAPSVMWEBSERVICE_MAPPING.api_endpoint == ENDPOINT
        assert ONTAPSVMWEBSERVICE_MAPPING.api_type == "ontap"

    def test_parses_private_cli_records(self) -> None:
        items = parse_api_response(ONTAPSVMWEBSERVICE_MAPPING, PRIVATE_CLI_RESPONSE, "", _noop_log)

        assert items == _services(
            ("svm1", "sysmgr", True), ("svm1", "saml", False), ("svm2", "sysmgr", True)
        )

    def test_missing_enabled_defaults_to_false(self) -> None:
        response = {"records": [{"vserver": "svm1", "name": "sysmgr"}]}

        (item,) = parse_api_response(ONTAPSVMWEBSERVICE_MAPPING, response, "", _noop_log)

        assert isinstance(item, OntapSvmWebService)
        assert item.enabled is False


class TestCollector:
    @staticmethod
    def _collector(web_response: Any) -> MetadataCollector:
        def get_all_records(url: str, method: str = "GET") -> Any:
            if url.startswith("/private/cli/vserver/services/web"):
                if isinstance(web_response, Exception):
                    raise web_response
                return web_response
            if url.startswith("/storage/volumes"):
                return {
                    "records": [{"name": "vol1", "uuid": "11111111-1111-1111-1111-111111111111"}]
                }
            return {"records": [], "num_records": 0}

        client = MagicMock()
        client.get_all_records = MagicMock(side_effect=get_all_records)
        collector = MetadataCollector(api_client=client, parallel=False)
        collector._cluster_name = "test"
        return collector

    def test_storage_phase_collects_web_services(self) -> None:
        storage = self._collector(PRIVATE_CLI_RESPONSE)._collect_storage_via_api()

        assert storage.svm_web_services == _services(
            ("svm1", "sysmgr", True), ("svm1", "saml", False), ("svm2", "sysmgr", True)
        )

    def test_private_cli_failure_leaves_the_rest_of_storage(self) -> None:
        """A role without private CLI access must not fail the storage phase."""
        storage = self._collector(RuntimeError("403 Forbidden"))._collect_storage_via_api()

        assert storage.svm_web_services == []
        assert [v.name for v in storage.volumes] == ["vol1"]


class TestDiff:
    def test_same_service_name_on_two_svms_does_not_collide(self) -> None:
        """Keyed on vserver/name: only svm1's sysmgr changed."""
        before = _metadata(_services(("svm1", "sysmgr", True), ("svm2", "sysmgr", True)))
        after = _metadata(_services(("svm1", "sysmgr", False), ("svm2", "sysmgr", True)))

        changes = [c for c in compute_diff(before, after) if "svm_web_services" in c["category"]]

        assert changes == [
            {
                "category": "storage.svm_web_services",
                "type": "modified",
                "entity": "svm1/sysmgr",
                "field": "enabled",
                "old": True,
                "new": False,
            }
        ]

    def test_service_added_on_one_svm(self) -> None:
        before = _metadata(_services(("svm1", "sysmgr", True)))
        after = _metadata(_services(("svm1", "sysmgr", True), ("svm2", "sysmgr", True)))

        changes = [c for c in compute_diff(before, after) if "svm_web_services" in c["category"]]

        assert changes == [
            {"category": "storage.svm_web_services", "type": "added", "entity": "svm2/sysmgr"}
        ]


class TestCacheRoundTrip:
    def test_db_keeps_web_services(self, tmp_path: Path) -> None:
        services = _services(("svm1", "sysmgr", True), ("svm1", "saml", False))
        db = ClusterMetadataDB(db_path=tmp_path / "cache.db")
        try:
            db.set("test-cluster", _metadata(services))
            loaded = db.get("test-cluster")
        finally:
            db.close()

        assert loaded is not None
        assert loaded.storage.svm_web_services == services


class TestCli:
    @pytest.fixture
    def config_dir(self, tmp_path: Path) -> Path:
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        (config_dir / "settings.toml").write_text(
            '[ontapapi]\n[ontapapi.general]\nbase_api_path = "/api"\n'
        )
        return config_dir

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_documented_query_finds_sysmgr_and_saml(
        self, mock_db_class: MagicMock, config_dir: Path
    ) -> None:
        """The predicate in docs/reference/cli.md, labelled vserver/name."""
        metadata = _metadata(
            _services(
                ("svm1", "sysmgr", True),
                ("svm1", "saml", False),
                ("svm1", "other", True),
                ("svm2", "sysmgr", False),
            )
        )
        lazy = MagicMock()
        lazy.model_dump.return_value = metadata.model_dump()
        mock_db_class.return_value.get_lazy.return_value = lazy

        result = CliRunner().invoke(
            nf,
            [
                "-c",
                str(config_dir),
                "cache",
                "query",
                "test-cluster",
                'storage.svm_web_services["name=sysmgr || name=saml"].enabled',
                "--key",
                "service_key",
                "--raw",
            ],
        )

        assert result.exit_code == 0, result.output
        assert result.output.strip().split("\n") == [
            "svm1/sysmgr\ttrue",
            "svm1/saml\tfalse",
            "svm2/sysmgr\tfalse",
        ]

    @patch("pynetappfoundry.cli.commands.cache.query.ClusterMetadataDB")
    def test_query_filters_by_enabled(self, mock_db_class: MagicMock, config_dir: Path) -> None:
        """Which services are still enabled, on any SVM."""
        metadata = _metadata(
            _services(("svm1", "sysmgr", True), ("svm1", "saml", False), ("svm2", "sysmgr", False))
        )
        lazy = MagicMock()
        lazy.model_dump.return_value = metadata.model_dump()
        mock_db_class.return_value.get_lazy.return_value = lazy

        result = CliRunner().invoke(
            nf,
            [
                "-c",
                str(config_dir),
                "cache",
                "query",
                "test-cluster",
                'storage.svm_web_services["enabled=true"].name',
                "--key",
                "service_key",
                "--raw",
            ],
        )

        assert result.exit_code == 0, result.output
        assert result.output.strip().split("\n") == ["svm1/sysmgr\tsysmgr"]

    def test_schema_lists_the_path(self) -> None:
        result = CliRunner().invoke(nf, ["cache", "schema", "--flat"])

        assert result.exit_code == 0
        assert "storage.svm_web_services[N].enabled: bool" in result.output
        assert "storage.svm_web_services[N].vserver: str" in result.output
