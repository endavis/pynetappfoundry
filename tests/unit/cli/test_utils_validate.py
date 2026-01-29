"""Tests for utils validate command."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import paramiko
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

        with patch("pynetappfoundry.cli.commands.utils.validate.paramiko") as mock_paramiko:
            mock_ssh = MagicMock()
            mock_paramiko.SSHClient.return_value = mock_ssh
            mock_paramiko.AutoAddPolicy = paramiko.AutoAddPolicy

            mock_stdout = MagicMock()
            mock_stdout.read.return_value = b"NetApp Release"
            mock_ssh.exec_command.return_value = (MagicMock(), mock_stdout, MagicMock())

            result = _validate_ssh("test-cluster", details, mock_config)

            assert result is True
            mock_ssh.connect.assert_called_once_with(
                "192.168.1.1",
                username="admin",
                password="password123",
                timeout=10,
            )

    def test_validate_ssh_no_ip(self, mock_config: MagicMock) -> None:
        """Test SSH validation skipped when no IP configured."""
        details = {}  # No IP

        result = _validate_ssh("test-cluster", details, mock_config)

        assert result is None

    def test_validate_ssh_auth_failure(self, mock_config: MagicMock) -> None:
        """Test SSH authentication failure."""
        details = {"ip": "192.168.1.1"}

        with patch("pynetappfoundry.cli.commands.utils.validate.paramiko") as mock_paramiko:
            mock_ssh = MagicMock()
            mock_paramiko.SSHClient.return_value = mock_ssh
            mock_paramiko.AutoAddPolicy = paramiko.AutoAddPolicy
            mock_paramiko.AuthenticationException = paramiko.AuthenticationException

            mock_ssh.connect.side_effect = paramiko.AuthenticationException("Auth failed")

            result = _validate_ssh("test-cluster", details, mock_config)

            assert result is False

    def test_validate_ssh_connection_error(self, mock_config: MagicMock) -> None:
        """Test SSH connection error."""
        details = {"ip": "192.168.1.1"}

        with patch("pynetappfoundry.cli.commands.utils.validate.paramiko") as mock_paramiko:
            mock_ssh = MagicMock()
            mock_paramiko.SSHClient.return_value = mock_ssh
            mock_paramiko.AutoAddPolicy = paramiko.AutoAddPolicy
            # Must set ALL exception classes used in except clauses
            mock_paramiko.AuthenticationException = paramiko.AuthenticationException
            mock_paramiko.SSHException = paramiko.SSHException

            mock_ssh.connect.side_effect = paramiko.SSHException("Connection refused")

            result = _validate_ssh("test-cluster", details, mock_config)

            assert result is False

    def test_validate_ssh_timeout(self, mock_config: MagicMock) -> None:
        """Test SSH connection timeout."""
        details = {"ip": "192.168.1.1"}

        with patch("pynetappfoundry.cli.commands.utils.validate.paramiko") as mock_paramiko:
            mock_ssh = MagicMock()
            mock_paramiko.SSHClient.return_value = mock_ssh
            mock_paramiko.AutoAddPolicy = paramiko.AutoAddPolicy
            # Must set ALL exception classes used in except clauses before TimeoutError
            mock_paramiko.AuthenticationException = paramiko.AuthenticationException
            mock_paramiko.SSHException = paramiko.SSHException

            mock_ssh.connect.side_effect = TimeoutError("Connection timed out")

            result = _validate_ssh("test-cluster", details, mock_config)

            assert result is False

    def test_validate_ssh_closes_connection_on_success(self, mock_config: MagicMock) -> None:
        """Test SSH connection is closed after successful validation."""
        details = {"ip": "192.168.1.1"}

        with patch("pynetappfoundry.cli.commands.utils.validate.paramiko") as mock_paramiko:
            mock_ssh = MagicMock()
            mock_paramiko.SSHClient.return_value = mock_ssh
            mock_paramiko.AutoAddPolicy = paramiko.AutoAddPolicy

            mock_stdout = MagicMock()
            mock_stdout.read.return_value = b"NetApp Release"
            mock_ssh.exec_command.return_value = (MagicMock(), mock_stdout, MagicMock())

            _validate_ssh("test-cluster", details, mock_config)

            # Close should be called at least once (in try block and/or finally)
            assert mock_ssh.close.called
