"""Tests for utils validate command."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cli.commands.utils.validate import (
    _validate_cluster,
    _validate_ssh,
)

MODULE = "pynetappfoundry.cli.commands.utils.validate"


@pytest.fixture
def mock_config() -> MagicMock:
    """Create a mock Config object."""
    config = MagicMock()
    config.get_user.return_value = ("admin", "password123")
    config.get_ontap_api_settings.return_value = MagicMock(
        base_api_path="/api",
        timeout=30.0,
    )
    config.get_schema_location.return_value = MagicMock()
    return config


@pytest.fixture
def sample_details() -> dict[str, Any]:
    """Sample cluster connection details."""
    return {"ip": "10.0.0.1", "bu": "Platform", "env": "Prod"}


class TestValidateCluster:
    """Tests for _validate_cluster."""

    @patch(f"{MODULE}.QuerySet")
    @patch(f"{MODULE}.ONTAPAPIClient")
    def test_validate_cluster_success(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test successful cluster validation returns counts and True."""
        mock_client = mock_client_cls.return_value
        mock_client.call_endpoint.return_value = {"name": "cluster1"}

        # First QuerySet call (nodes) returns 2, second (volumes) returns 5
        mock_qs_cls.return_value.count.side_effect = [2, 5]

        node_count, vol_count, success = _validate_cluster("cluster1", sample_details, mock_config)

        assert node_count == 2
        assert vol_count == 5
        assert success is True

    @patch(f"{MODULE}.print_warning")
    @patch(f"{MODULE}.QuerySet")
    @patch(f"{MODULE}.ONTAPAPIClient")
    def test_validate_cluster_name_mismatch(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_print_warning: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test warning when config name differs from actual cluster name."""
        mock_client = mock_client_cls.return_value
        mock_client.call_endpoint.return_value = {"name": "actual-cluster"}
        mock_qs_cls.return_value.count.side_effect = [1, 3]

        _node_count, _vol_count, success = _validate_cluster(
            "configured-name", sample_details, mock_config
        )

        assert success is True
        mock_print_warning.assert_called_once()
        warning_msg = mock_print_warning.call_args[0][0]
        assert "configured-name" in warning_msg
        assert "actual-cluster" in warning_msg

    @patch(f"{MODULE}.print_error")
    @patch(f"{MODULE}.ONTAPAPIClient")
    def test_validate_cluster_failure(
        self,
        mock_client_cls: MagicMock,
        mock_print_error: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test connection error returns zeros and False."""
        mock_client_cls.side_effect = Exception("Connection refused")

        node_count, vol_count, success = _validate_cluster("cluster1", sample_details, mock_config)

        assert node_count == 0
        assert vol_count == 0
        assert success is False
        mock_print_error.assert_called_once()

    @patch(f"{MODULE}.print_warning")
    @patch(f"{MODULE}.QuerySet")
    @patch(f"{MODULE}.ONTAPAPIClient")
    def test_validate_cluster_name_match_no_warning(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_print_warning: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test no warning when config name matches cluster name."""
        mock_client = mock_client_cls.return_value
        mock_client.call_endpoint.return_value = {"name": "cluster1"}
        mock_qs_cls.return_value.count.side_effect = [2, 10]

        _validate_cluster("cluster1", sample_details, mock_config)

        mock_print_warning.assert_not_called()

    @patch(f"{MODULE}.QuerySet")
    @patch(f"{MODULE}.ONTAPAPIClient")
    def test_validate_cluster_non_dict_response(
        self,
        mock_client_cls: MagicMock,
        mock_qs_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test cluster name extraction handles non-dict response."""
        mock_client = mock_client_cls.return_value
        mock_client.call_endpoint.return_value = None
        mock_qs_cls.return_value.count.side_effect = [1, 1]

        _node_count, _vol_count, success = _validate_cluster(
            "cluster1", sample_details, mock_config
        )

        # Non-dict response yields empty cluster_name, which won't match
        assert success is True


class TestValidateSSH:
    """Tests for _validate_ssh."""

    @patch(f"{MODULE}.ONTAPCLI")
    def test_validate_ssh_success(
        self,
        mock_cli_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test successful SSH connection returns True."""
        result = _validate_ssh("cluster1", sample_details, mock_config)

        assert result is True
        mock_cli_cls.return_value.connect.assert_called_once()
        mock_cli_cls.return_value.run_command.assert_called_once_with("node show")
        mock_cli_cls.return_value.disconnect.assert_called_once()

    @patch(f"{MODULE}.ONTAPCLI")
    def test_validate_ssh_failure(
        self,
        mock_cli_cls: MagicMock,
        mock_config: MagicMock,
        sample_details: dict[str, Any],
    ) -> None:
        """Test SSH connection failure returns False."""
        mock_cli_cls.return_value.connect.side_effect = Exception("SSH timeout")

        result = _validate_ssh("cluster1", sample_details, mock_config)

        assert result is False

    def test_validate_ssh_skipped(
        self,
        mock_config: MagicMock,
    ) -> None:
        """Test SSH is skipped when no IP configured."""
        details: dict[str, Any] = {"bu": "Platform", "env": "Prod"}

        result = _validate_ssh("cluster1", details, mock_config)

        assert result is None
