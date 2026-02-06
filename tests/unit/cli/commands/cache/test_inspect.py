"""Tests for cache inspect CLI command."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.models import (
    CachedClusterMetadata,
    StorageInfo,
    VolumeInfo,
)
from pynetappfoundry.cli.commands.cache.inspect import (
    INSPECT_TYPES,
    _build_api_endpoint,
    _build_cache_tree,
    _build_cli_command,
    _format_value,
    _resolve_cache_list,
)
from pynetappfoundry.cli.main import nf


class TestResolveCache:
    """Tests for _resolve_cache_list helper."""

    def test_resolve_volumes(self) -> None:
        """Test resolving storage.volumes from metadata."""
        vol = VolumeInfo(name="vol1", uuid="u1")
        meta = CachedClusterMetadata(
            cluster_name="c1",
            storage=StorageInfo(volumes=[vol]),
        )
        result = _resolve_cache_list(meta, "storage.volumes")
        assert len(result) == 1
        assert result[0].name == "vol1"

    def test_resolve_bad_path(self) -> None:
        """Test resolving a non-existent path returns empty list."""
        meta = CachedClusterMetadata(cluster_name="c1")
        assert _resolve_cache_list(meta, "nonexistent.path") == []

    def test_resolve_non_list(self) -> None:
        """Test resolving a path that is not a list returns empty list."""
        meta = CachedClusterMetadata(cluster_name="c1")
        assert _resolve_cache_list(meta, "cluster") == []


class TestFormatValue:
    """Tests for _format_value helper."""

    def test_format_bool(self) -> None:
        """Test boolean formatting."""
        assert "True" in _format_value(True)

    def test_format_int(self) -> None:
        """Test integer formatting."""
        assert "42" in _format_value(42)

    def test_format_empty_string(self) -> None:
        """Test empty string shows (empty)."""
        assert "(empty)" in _format_value("")

    def test_format_nonempty_string(self) -> None:
        """Test non-empty string formatting."""
        assert "hello" in _format_value("hello")

    def test_format_empty_list(self) -> None:
        """Test empty list shows (empty list)."""
        assert "(empty list)" in _format_value([])

    def test_format_nonempty_list(self) -> None:
        """Test non-empty list shows item count."""
        assert "3 items" in _format_value([1, 2, 3])


class TestBuildCacheTree:
    """Tests for _build_cache_tree helper."""

    def test_builds_tree_from_model(self) -> None:
        """Test tree is built from a Pydantic model."""
        vol = VolumeInfo(name="vol1", uuid="u1", size=1024)
        tree = _build_cache_tree(vol)
        assert tree.label == "[bold]CACHE[/bold]"

    def test_builds_tree_from_dict(self) -> None:
        """Test tree is built from a plain dict."""
        tree = _build_cache_tree({"key": "value"})
        assert tree.label == "[bold]CACHE[/bold]"


class TestInspectTypes:
    """Tests for INSPECT_TYPES registry."""

    def test_volume_registered(self) -> None:
        """Test volume type is registered."""
        assert "volume" in INSPECT_TYPES

    def test_volume_cache_path(self) -> None:
        """Test volume cache path is correct."""
        _, cache_path = INSPECT_TYPES["volume"]
        assert cache_path == "storage.volumes"


class TestBuildApiEndpoint:
    """Tests for _build_api_endpoint helper."""

    def test_appends_name_filter_with_ampersand(self) -> None:
        """Test name filter appended with & when endpoint has query params."""
        mapping = TypeMapping(
            name="Volume",
            model_class=VolumeInfo,
            api_endpoint="/storage/volumes?fields=*,autosize",
            cli_command="volume show",
            fields=(FieldMapping(cache_attr="name", api_path="name"),),
        )
        result = _build_api_endpoint(mapping, "vol1")
        assert result == "/storage/volumes?fields=*,autosize&name=vol1"

    def test_appends_name_filter_with_question_mark(self) -> None:
        """Test name filter appended with ? when endpoint has no query params."""
        mapping = TypeMapping(
            name="Test",
            model_class=VolumeInfo,
            api_endpoint="/storage/volumes",
            cli_command="volume show",
            fields=(FieldMapping(cache_attr="name", api_path="name"),),
        )
        result = _build_api_endpoint(mapping, "vol1")
        assert result == "/storage/volumes?name=vol1"


class TestBuildCliCommand:
    """Tests for _build_cli_command helper."""

    def test_builds_cli_command(self) -> None:
        """Test CLI command is built with object name."""
        mapping = TypeMapping(
            name="Volume",
            model_class=VolumeInfo,
            api_endpoint="/storage/volumes",
            cli_command="volume show",
            fields=(FieldMapping(cache_attr="name", api_path="name"),),
        )
        result = _build_cli_command(mapping, "PRODVOL1")
        assert result == "volume show PRODVOL1"


class TestInspectCommand:
    """Tests for nf cache inspect command."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a CLI runner."""
        return CliRunner()

    @pytest.fixture
    def mock_config_dir(self, tmp_path: Path) -> Path:
        """Create a mock config directory."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        (config_dir / "settings.toml").write_text(
            """
[ontapapi]
[ontapapi.general]
base_api_path = "/api"
"""
        )
        return config_dir

    @pytest.fixture
    def sample_metadata(self) -> CachedClusterMetadata:
        """Create sample metadata with a volume."""
        return CachedClusterMetadata(
            cluster_name="test-cluster",
            cached_at=datetime(2024, 1, 15, 10, 30, 0, tzinfo=UTC),
            storage=StorageInfo(
                volumes=[
                    VolumeInfo(
                        uuid="abc-123",
                        name="PRODVOL1",
                        svm="svm_PROD",
                        state="online",
                        type="rw",
                        style="flexvol",
                        size=9064378368,
                    ),
                ],
            ),
        )

    def test_inspect_missing_config(self, runner: CliRunner, tmp_path: Path) -> None:
        """Test inspect with missing config directory."""
        result = runner.invoke(
            nf,
            ["-c", str(tmp_path / "nonexistent"), "cache", "inspect", "cluster1", "vol1"],
        )
        assert result.exit_code != 0
        assert "not found" in result.output

    @patch("pynetappfoundry.cli.commands.cache.inspect.Config")
    def test_inspect_unknown_cluster(
        self,
        mock_config_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test inspect with cluster not in config."""
        mock_config = MagicMock()
        mock_config.data = {"clusters": {}}
        mock_config_class.return_value = mock_config

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "inspect", "unknown", "vol1"],
        )
        assert result.exit_code != 0
        assert "not found in configuration" in result.output

    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.inspect.Config")
    def test_inspect_shows_cache_data(
        self,
        mock_config_class: MagicMock,
        mock_db_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test that inspect shows cached volume data."""
        mock_config = MagicMock()
        mock_config.data = {"clusters": {"test-cluster": {"ip": "10.0.0.1"}}}
        mock_config.get_user.return_value = ("admin", "pass")
        mock_config_class.return_value = mock_config

        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        mock_cli = MagicMock()
        mock_cli.run_a_show_command_and_parse_seperator.return_value = ([], {})
        mock_cli_class.return_value = mock_cli

        mock_api = MagicMock()
        mock_api.call_endpoint.return_value = {"records": []}
        mock_api_class.return_value = mock_api

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "inspect", "test-cluster", "PRODVOL1"],
        )

        assert result.exit_code == 0
        assert "CACHE" in result.output
        assert "PRODVOL1" in result.output
        assert "abc-123" in result.output

    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.inspect.Config")
    def test_inspect_cache_miss(
        self,
        mock_config_class: MagicMock,
        mock_db_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
        sample_metadata: CachedClusterMetadata,
    ) -> None:
        """Test inspect when object is not found in cache."""
        mock_config = MagicMock()
        mock_config.data = {"clusters": {"test-cluster": {"ip": "10.0.0.1"}}}
        mock_config.get_user.return_value = ("admin", "pass")
        mock_config_class.return_value = mock_config

        mock_db = MagicMock()
        mock_db.get.return_value = sample_metadata
        mock_db_class.return_value = mock_db

        mock_cli = MagicMock()
        mock_cli.run_a_show_command_and_parse_seperator.return_value = ([], {})
        mock_cli_class.return_value = mock_cli

        mock_api = MagicMock()
        mock_api.call_endpoint.return_value = {"records": []}
        mock_api_class.return_value = mock_api

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "inspect", "test-cluster", "NONEXISTENT"],
        )

        assert result.exit_code == 0
        assert "not found in cache" in result.output

    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.inspect.Config")
    def test_inspect_no_cache_for_cluster(
        self,
        mock_config_class: MagicMock,
        mock_db_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test inspect when no cache exists for the cluster."""
        mock_config = MagicMock()
        mock_config.data = {"clusters": {"test-cluster": {"ip": "10.0.0.1"}}}
        mock_config.get_user.return_value = ("admin", "pass")
        mock_config_class.return_value = mock_config

        mock_db = MagicMock()
        mock_db.get.return_value = None
        mock_db_class.return_value = mock_db

        mock_cli = MagicMock()
        mock_cli.run_a_show_command_and_parse_seperator.return_value = ([], {})
        mock_cli_class.return_value = mock_cli

        mock_api = MagicMock()
        mock_api.call_endpoint.return_value = {"records": []}
        mock_api_class.return_value = mock_api

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "inspect", "test-cluster", "vol1"],
        )

        assert result.exit_code == 0
        assert "No cached data" in result.output

    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.inspect.Config")
    def test_inspect_shows_cli_data(
        self,
        mock_config_class: MagicMock,
        mock_db_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test that inspect shows CLI data when available."""
        mock_config = MagicMock()
        mock_config.data = {"clusters": {"test-cluster": {"ip": "10.0.0.1"}}}
        mock_config.get_user.return_value = ("admin", "pass")
        mock_config_class.return_value = mock_config

        mock_db = MagicMock()
        mock_db.get.return_value = None
        mock_db_class.return_value = mock_db

        cli_record = {"volume": "vol1", "vserver": "svm1", "state": "online"}
        descriptions = {"volume": "Volume Name", "vserver": "Vserver Name", "state": "State"}
        mock_cli = MagicMock()
        mock_cli.run_a_show_command_and_parse_seperator.return_value = (
            [cli_record],
            descriptions,
        )
        mock_cli_class.return_value = mock_cli

        mock_api = MagicMock()
        mock_api.call_endpoint.return_value = {"records": []}
        mock_api_class.return_value = mock_api

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "inspect", "test-cluster", "vol1"],
        )

        assert result.exit_code == 0
        assert "CLI" in result.output
        assert "vol1" in result.output
        assert "svm1" in result.output

    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.inspect.Config")
    def test_inspect_shows_api_data(
        self,
        mock_config_class: MagicMock,
        mock_db_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test that inspect shows API data when available."""
        mock_config = MagicMock()
        mock_config.data = {"clusters": {"test-cluster": {"ip": "10.0.0.1"}}}
        mock_config.get_user.return_value = ("admin", "pass")
        mock_config_class.return_value = mock_config

        mock_db = MagicMock()
        mock_db.get.return_value = None
        mock_db_class.return_value = mock_db

        mock_cli = MagicMock()
        mock_cli.run_a_show_command_and_parse_seperator.return_value = ([], {})
        mock_cli_class.return_value = mock_cli

        api_record = {"uuid": "abc-123", "name": "vol1", "state": "online"}
        mock_api = MagicMock()
        mock_api.call_endpoint.return_value = {"records": [api_record]}
        mock_api_class.return_value = mock_api

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "inspect", "test-cluster", "vol1"],
        )

        assert result.exit_code == 0
        assert "API" in result.output
        assert "abc-123" in result.output

    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.inspect.Config")
    def test_inspect_cli_failure_handled(
        self,
        mock_config_class: MagicMock,
        mock_db_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test that CLI failure is handled gracefully."""
        mock_config = MagicMock()
        mock_config.data = {"clusters": {"test-cluster": {"ip": "10.0.0.1"}}}
        mock_config.get_user.return_value = ("admin", "pass")
        mock_config_class.return_value = mock_config

        mock_db = MagicMock()
        mock_db.get.return_value = None
        mock_db_class.return_value = mock_db

        mock_cli_class.side_effect = Exception("SSH connection failed")

        mock_api = MagicMock()
        mock_api.call_endpoint.return_value = {"records": []}
        mock_api_class.return_value = mock_api

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "inspect", "test-cluster", "vol1"],
        )

        assert result.exit_code == 0
        assert "CLI query failed" in result.output

    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.inspect.Config")
    def test_inspect_api_failure_handled(
        self,
        mock_config_class: MagicMock,
        mock_db_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test that API failure is handled gracefully."""
        mock_config = MagicMock()
        mock_config.data = {"clusters": {"test-cluster": {"ip": "10.0.0.1"}}}
        mock_config.get_user.return_value = ("admin", "pass")
        mock_config_class.return_value = mock_config

        mock_db = MagicMock()
        mock_db.get.return_value = None
        mock_db_class.return_value = mock_db

        mock_cli = MagicMock()
        mock_cli.run_a_show_command_and_parse_seperator.return_value = ([], {})
        mock_cli_class.return_value = mock_cli

        mock_api_class.side_effect = Exception("API connection failed")

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "inspect", "test-cluster", "vol1"],
        )

        assert result.exit_code == 0
        assert "API query failed" in result.output

    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.inspect.Config")
    def test_inspect_cli_no_data(
        self,
        mock_config_class: MagicMock,
        mock_db_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test inspect when CLI returns no data."""
        mock_config = MagicMock()
        mock_config.data = {"clusters": {"test-cluster": {"ip": "10.0.0.1"}}}
        mock_config.get_user.return_value = ("admin", "pass")
        mock_config_class.return_value = mock_config

        mock_db = MagicMock()
        mock_db.get.return_value = None
        mock_db_class.return_value = mock_db

        mock_cli = MagicMock()
        mock_cli.run_a_show_command_and_parse_seperator.return_value = ([], {})
        mock_cli_class.return_value = mock_cli

        mock_api = MagicMock()
        mock_api.call_endpoint.return_value = {"records": []}
        mock_api_class.return_value = mock_api

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "inspect", "test-cluster", "vol1"],
        )

        assert result.exit_code == 0
        assert "CLI returned no data" in result.output

    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.inspect.Config")
    def test_inspect_api_no_data(
        self,
        mock_config_class: MagicMock,
        mock_db_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test inspect when API returns no data."""
        mock_config = MagicMock()
        mock_config.data = {"clusters": {"test-cluster": {"ip": "10.0.0.1"}}}
        mock_config.get_user.return_value = ("admin", "pass")
        mock_config_class.return_value = mock_config

        mock_db = MagicMock()
        mock_db.get.return_value = None
        mock_db_class.return_value = mock_db

        mock_cli = MagicMock()
        mock_cli.run_a_show_command_and_parse_seperator.return_value = ([], {})
        mock_cli_class.return_value = mock_cli

        mock_api = MagicMock()
        mock_api.call_endpoint.return_value = {"records": []}
        mock_api_class.return_value = mock_api

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "inspect", "test-cluster", "vol1"],
        )

        assert result.exit_code == 0
        assert "API returned no data" in result.output

    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPAPIClient")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ONTAPCLI")
    @patch("pynetappfoundry.cli.commands.cache.inspect.ClusterMetadataDB")
    @patch("pynetappfoundry.cli.commands.cache.inspect.Config")
    def test_inspect_shows_endpoint_and_command(
        self,
        mock_config_class: MagicMock,
        mock_db_class: MagicMock,
        mock_cli_class: MagicMock,
        mock_api_class: MagicMock,
        runner: CliRunner,
        mock_config_dir: Path,
    ) -> None:
        """Test that inspect displays the API endpoint and CLI command used."""
        mock_config = MagicMock()
        mock_config.data = {"clusters": {"test-cluster": {"ip": "10.0.0.1"}}}
        mock_config.get_user.return_value = ("admin", "pass")
        mock_config_class.return_value = mock_config

        mock_db = MagicMock()
        mock_db.get.return_value = None
        mock_db_class.return_value = mock_db

        mock_cli = MagicMock()
        mock_cli.run_a_show_command_and_parse_seperator.return_value = ([], {})
        mock_cli_class.return_value = mock_cli

        mock_api = MagicMock()
        mock_api.call_endpoint.return_value = {"records": []}
        mock_api_class.return_value = mock_api

        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "inspect", "test-cluster", "vol1"],
        )

        assert result.exit_code == 0
        # Should show the API endpoint used
        assert "Endpoint:" in result.output
        assert "/storage/volumes" in result.output
        assert "name=vol1" in result.output
        # Should show the CLI command used
        assert "Command:" in result.output
        assert "volume show vol1" in result.output

    def test_inspect_invalid_type(self, runner: CliRunner, mock_config_dir: Path) -> None:
        """Test inspect with invalid object type."""
        result = runner.invoke(
            nf,
            ["-c", str(mock_config_dir), "cache", "inspect", "c1", "v1", "--type", "badtype"],
        )
        assert result.exit_code != 0
