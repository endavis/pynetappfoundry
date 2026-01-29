"""Tests for utils validate command."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cli.commands.utils.validate import _validate_ssh


class TestValidateSSH:
    """Tests for _validate_ssh function."""

    @pytest.fixture
    def mock_config(self) -> MagicMock:
        """Create a mock config."""
        config = MagicMock()
        config.get_user.return_value = ("admin", "password123")
        return config

    def test_validate_ssh_success(self, mock_config: MagicMock) -> None:
        """Test successful SSH connection."""
        details = {"ip": "192.168.1.1"}

        with patch("pynetappfoundry.cli.commands.utils.validate.ONTAPCLI") as mock_cli_class:
            mock_cli = MagicMock()
            mock_cli_class.return_value = mock_cli

            result = _validate_ssh("test-cluster", details, mock_config)

            assert result is True
            mock_cli_class.assert_called_once_with(
                "test-cluster", "192.168.1.1", "admin", "password123"
            )
            mock_cli.connect.assert_called_once()
            mock_cli.run_command.assert_called_once_with("node show")
            mock_cli.disconnect.assert_called_once()

    def test_validate_ssh_no_ip(self, mock_config: MagicMock) -> None:
        """Test SSH validation skipped when no IP configured."""
        details = {}  # No IP

        result = _validate_ssh("test-cluster", details, mock_config)

        assert result is None

    def test_validate_ssh_connect_failure(self, mock_config: MagicMock) -> None:
        """Test SSH connection failure."""
        details = {"ip": "192.168.1.1"}

        with patch("pynetappfoundry.cli.commands.utils.validate.ONTAPCLI") as mock_cli_class:
            mock_cli = MagicMock()
            mock_cli_class.return_value = mock_cli
            mock_cli.connect.side_effect = Exception("Connection refused")

            result = _validate_ssh("test-cluster", details, mock_config)

            assert result is False

    def test_validate_ssh_command_failure(self, mock_config: MagicMock) -> None:
        """Test SSH command execution failure."""
        details = {"ip": "192.168.1.1"}

        with patch("pynetappfoundry.cli.commands.utils.validate.ONTAPCLI") as mock_cli_class:
            mock_cli = MagicMock()
            mock_cli_class.return_value = mock_cli
            mock_cli.run_command.side_effect = Exception("Command failed")

            result = _validate_ssh("test-cluster", details, mock_config)

            assert result is False
