"""Tests for FieldGroupFetcher."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cache._fetcher import _FIELD_GROUP_METHODS, FieldGroupFetcher


@pytest.fixture
def mock_config() -> MagicMock:
    """Mock Config instance with get_user and get_ontap_api_settings."""
    config = MagicMock()
    config.get_user.return_value = ("admin", "password123")
    config.get_ontap_api_settings.return_value = MagicMock(
        base_api_path="/api",
        timeout=30,
    )
    config.get_schema_location.return_value = MagicMock(__truediv__=lambda self, x: "/fake/path")
    return config


@pytest.fixture
def fetcher(mock_config: MagicMock) -> FieldGroupFetcher:
    """Create a FieldGroupFetcher instance."""
    return FieldGroupFetcher(
        cluster_name="test-cluster",
        cluster_ip="10.0.0.1",
        config=mock_config,
    )


class TestLazyClientCreation:
    """Clients are not created until fetch() is called."""

    def test_no_clients_at_init(self, fetcher: FieldGroupFetcher) -> None:
        """API and CLI clients are not created during __init__."""
        # cached_property stores in __dict__; it should be empty at init.
        assert "api_client" not in fetcher.__dict__
        assert "cli_client" not in fetcher.__dict__
        assert "collector" not in fetcher.__dict__

    def test_clients_created_on_fetch(self, fetcher: FieldGroupFetcher) -> None:
        """Collector is accessed (and thus created) on first fetch()."""
        mock_collector = MagicMock()
        mock_collector.collect_cluster_info.return_value = MagicMock()

        # Inject a pre-built collector into the cached_property slot
        fetcher.__dict__["collector"] = mock_collector

        fetcher.fetch("cluster")
        mock_collector.collect_cluster_info.assert_called_once()


class TestAPIClientCreation:
    """Tests for lazy API client creation."""

    def test_api_client_returns_none_on_failure(self, mock_config: MagicMock) -> None:
        """api_client returns None when client creation fails."""
        with patch(
            "pynetappfoundry.clients.ontap.api.ONTAPAPIClient.__init__",
            side_effect=Exception("fail"),
        ):
            fetcher = FieldGroupFetcher("test-cluster", "10.0.0.1", mock_config)
            result = fetcher.api_client
            assert result is None

    def test_api_client_created_successfully(self, mock_config: MagicMock) -> None:
        """api_client returns client when creation succeeds."""
        mock_client = MagicMock()
        with patch(
            "pynetappfoundry.clients.ontap.api.ONTAPAPIClient",
            return_value=mock_client,
        ):
            fetcher = FieldGroupFetcher("test-cluster", "10.0.0.1", mock_config)
            result = fetcher.api_client
            assert result is mock_client


class TestCLIClientCreation:
    """Tests for lazy CLI client creation."""

    def test_cli_client_returns_none_on_failure(self, mock_config: MagicMock) -> None:
        """cli_client returns None when credentials are unavailable."""
        mock_config.get_user.side_effect = Exception("No credentials")
        fetcher = FieldGroupFetcher("test-cluster", "10.0.0.1", mock_config)
        result = fetcher.cli_client
        assert result is None

    def test_cli_client_created_successfully(self, mock_config: MagicMock) -> None:
        """cli_client returns client when creation succeeds."""
        mock_client = MagicMock()
        with patch(
            "pynetappfoundry.clients.ontap.cli.ONTAPCLI",
            return_value=mock_client,
        ):
            fetcher = FieldGroupFetcher("test-cluster", "10.0.0.1", mock_config)
            result = fetcher.cli_client
            assert result is mock_client


class TestFieldGroupMapping:
    """Each field group maps to the correct collector method."""

    @pytest.mark.parametrize(
        ("field_group", "method_name"),
        list(_FIELD_GROUP_METHODS.items()),
    )
    def test_fetch_calls_correct_method(
        self,
        field_group: str,
        method_name: str,
        fetcher: FieldGroupFetcher,
    ) -> None:
        """fetch() delegates to the correct collector method."""
        mock_collector = MagicMock()
        expected_result = MagicMock()
        getattr(mock_collector, method_name).return_value = expected_result

        # Inject mock collector into cached_property slot
        fetcher.__dict__["collector"] = mock_collector

        result = fetcher.fetch(field_group)
        getattr(mock_collector, method_name).assert_called_once()
        assert result is expected_result


class TestFetchFailureHandling:
    """Fetch failures return None instead of raising."""

    def test_fetch_returns_none_on_exception(self, fetcher: FieldGroupFetcher) -> None:
        """fetch() returns None when collector method raises."""
        mock_collector = MagicMock()
        mock_collector.collect_cluster_info.side_effect = Exception("API error")

        fetcher.__dict__["collector"] = mock_collector

        result = fetcher.fetch("cluster")
        assert result is None

    def test_fetch_unknown_group_returns_none(self, fetcher: FieldGroupFetcher) -> None:
        """fetch() returns None for unknown field groups."""
        result = fetcher.fetch("nonexistent_field_group")
        assert result is None


class TestCollectorCreation:
    """Tests for lazy collector creation."""

    def test_collector_created_with_clients(self, fetcher: FieldGroupFetcher) -> None:
        """Collector is created with the api_client and cli_client."""
        mock_api = MagicMock()
        mock_cli = MagicMock()

        # Inject mock clients into cached_property slots
        fetcher.__dict__["api_client"] = mock_api
        fetcher.__dict__["cli_client"] = mock_cli

        with patch(
            "pynetappfoundry.cache.collector.MetadataCollector",
        ) as mock_mc_cls:
            _ = fetcher.collector
            mock_mc_cls.assert_called_once_with(
                api_client=mock_api,
                cli_client=mock_cli,
                parallel=False,
            )
