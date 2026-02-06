"""Unit tests for ONTAP CLI client."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.clients.ontap.cli import (
    ONTAPCLI,
    CLICommandError,
    CLITimeoutError,
    _parse_separator_output,
)

if TYPE_CHECKING:
    pass


class TestCLITimeoutError:
    """Tests for CLITimeoutError exception."""

    def test_inherits_from_cli_command_error(self) -> None:
        """CLITimeoutError should inherit from CLICommandError."""
        error = CLITimeoutError("Test timeout", timeout=30.0)
        assert isinstance(error, CLICommandError)

    def test_stores_timeout_value(self) -> None:
        """CLITimeoutError should store the timeout value."""
        error = CLITimeoutError("Test timeout", timeout=45.5)
        assert error.timeout == 45.5
        assert error.message == "Test timeout"

    def test_can_be_caught_as_cli_command_error(self) -> None:
        """CLITimeoutError can be caught as CLICommandError."""
        with pytest.raises(CLICommandError):
            raise CLITimeoutError("Timeout occurred", timeout=60.0)


class TestONTAPCLILogPrefix:
    """Tests for ONTAPCLI log prefix functionality."""

    def test_log_prefix_format(self) -> None:
        """ONTAPCLI should have log_prefix in [name:ssh] format."""
        with patch("paramiko.SSHClient"):
            cli = ONTAPCLI(
                name="cluster1",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
            )
            assert cli.log_prefix == "[cluster1:ssh]"

    def test_log_prefix_with_special_characters(self) -> None:
        """ONTAPCLI should handle cluster names with special characters."""
        with patch("paramiko.SSHClient"):
            cli = ONTAPCLI(
                name="cluster-prod-01",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
            )
            assert cli.log_prefix == "[cluster-prod-01:ssh]"

    def test_log_prefix_empty_name(self) -> None:
        """ONTAPCLI should handle empty cluster name."""
        with patch("paramiko.SSHClient"):
            cli = ONTAPCLI(
                name="",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
            )
            assert cli.log_prefix == "[:ssh]"


class TestONTAPCLIConnect:
    """Tests for ONTAPCLI connect functionality."""

    def test_connect_lock_exists(self) -> None:
        """ONTAPCLI should have a connect lock for thread safety."""
        with patch("paramiko.SSHClient"):
            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
            )
            assert hasattr(cli, "_connect_lock")
            import threading

            assert isinstance(cli._connect_lock, type(threading.Lock()))

    def test_connect_is_thread_safe(self) -> None:
        """Multiple threads calling connect should only create one connection."""
        import threading
        import time
        from typing import Any

        with patch("paramiko.SSHClient") as mock_ssh_class:
            mock_ssh = MagicMock()
            mock_ssh_class.return_value = mock_ssh
            # First call: no transport, second+ calls: active transport
            mock_transport = MagicMock()
            mock_transport.is_active.return_value = True
            # Start with no transport, then return the mock after connect
            transport_state: dict[str, Any] = {"transport": None}

            def get_transport_side_effect() -> MagicMock | None:
                if transport_state["transport"] is None:
                    # Simulate connection delay
                    time.sleep(0.05)
                    transport_state["transport"] = mock_transport
                    return None
                return transport_state["transport"]

            mock_ssh.get_transport.side_effect = get_transport_side_effect

            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
            )

            # Reset to track actual connect calls
            mock_ssh.connect.reset_mock()
            transport_state["transport"] = None

            # Launch multiple threads that all try to connect
            threads = []
            for _ in range(5):
                t = threading.Thread(target=cli.connect)
                threads.append(t)

            for t in threads:
                t.start()
            for t in threads:
                t.join()

            # Only one connect call should have been made due to locking
            assert mock_ssh.connect.call_count == 1


class TestONTAPCLITimeout:
    """Tests for ONTAPCLI timeout functionality."""

    def test_default_timeout(self) -> None:
        """ONTAPCLI should have a default timeout of 10 seconds."""
        with patch("paramiko.SSHClient"):
            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
            )
            assert cli.timeout == 10.0

    def test_custom_timeout_in_init(self) -> None:
        """ONTAPCLI should accept custom timeout in __init__."""
        with patch("paramiko.SSHClient"):
            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
                timeout=120.0,
            )
            assert cli.timeout == 120.0

    def test_zero_timeout_is_valid(self) -> None:
        """Zero timeout should be accepted (though not practical)."""
        with patch("paramiko.SSHClient"):
            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
                timeout=0,
            )
            assert cli.timeout == 0

    def test_run_command_uses_instance_timeout(self) -> None:
        """run_command should use the instance timeout by default."""
        with patch("paramiko.SSHClient") as mock_ssh_class:
            mock_ssh = MagicMock()
            mock_ssh_class.return_value = mock_ssh
            mock_transport = MagicMock()
            mock_channel = MagicMock()
            mock_ssh.get_transport.return_value = mock_transport
            mock_transport.open_session.return_value = mock_channel
            mock_transport.is_active.return_value = True
            # First recv_ready returns True with data, second returns True with EOF
            mock_channel.recv_ready.side_effect = [True, True]
            mock_channel.recv.side_effect = [b"output\n", b""]

            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
                timeout=90.0,
            )

            cli.run_command("test command")

            mock_channel.settimeout.assert_called_once_with(90.0)

    def test_run_command_timeout_override(self) -> None:
        """run_command should allow timeout override per-call."""
        with patch("paramiko.SSHClient") as mock_ssh_class:
            mock_ssh = MagicMock()
            mock_ssh_class.return_value = mock_ssh
            mock_transport = MagicMock()
            mock_channel = MagicMock()
            mock_ssh.get_transport.return_value = mock_transport
            mock_transport.open_session.return_value = mock_channel
            mock_transport.is_active.return_value = True
            mock_channel.recv_ready.side_effect = [True, True]
            mock_channel.recv.side_effect = [b"output\n", b""]

            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
                timeout=60.0,
            )

            cli.run_command("test command", timeout=30.0)

            mock_channel.settimeout.assert_called_once_with(30.0)

    def test_timeout_raises_cli_timeout_error(self) -> None:
        """run_command should raise CLITimeoutError when elapsed time exceeds timeout."""
        with (
            patch("paramiko.SSHClient") as mock_ssh_class,
            patch("pynetappfoundry.clients.ontap.cli.time.monotonic") as mock_time,
        ):
            mock_ssh = MagicMock()
            mock_ssh_class.return_value = mock_ssh
            mock_transport = MagicMock()
            mock_channel = MagicMock()
            mock_ssh.get_transport.return_value = mock_transport
            mock_transport.open_session.return_value = mock_channel
            mock_transport.is_active.return_value = True
            # No data ready, command not finished
            mock_channel.recv_ready.return_value = False
            mock_channel.exit_status_ready.return_value = False
            # Simulate time passing: start at 0, then jump past timeout
            mock_time.side_effect = [0.0, 6.0]

            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
                timeout=5.0,
            )

            with pytest.raises(CLITimeoutError) as exc_info:
                cli.run_command("slow command")

            assert exc_info.value.timeout == 5.0
            assert "slow command" in str(exc_info.value)
            assert "5.0 seconds" in str(exc_info.value)
            mock_channel.close.assert_called()

    def test_timeout_error_includes_command_name(self) -> None:
        """CLITimeoutError message should include the command name."""
        with (
            patch("paramiko.SSHClient") as mock_ssh_class,
            patch("pynetappfoundry.clients.ontap.cli.time.monotonic") as mock_time,
        ):
            mock_ssh = MagicMock()
            mock_ssh_class.return_value = mock_ssh
            mock_transport = MagicMock()
            mock_channel = MagicMock()
            mock_ssh.get_transport.return_value = mock_transport
            mock_transport.open_session.return_value = mock_channel
            mock_transport.is_active.return_value = True
            mock_channel.recv_ready.return_value = False
            mock_channel.exit_status_ready.return_value = False
            # Simulate time passing past timeout
            mock_time.side_effect = [0.0, 11.0]

            cli = ONTAPCLI(
                name="test-cluster",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
                timeout=10.0,
            )

            with pytest.raises(CLITimeoutError) as exc_info:
                cli.run_command("virtual-machine instance show")

            assert "virtual-machine instance show" in str(exc_info.value)

    def test_channel_closed_on_timeout(self) -> None:
        """Channel should be closed when timeout occurs."""
        with (
            patch("paramiko.SSHClient") as mock_ssh_class,
            patch("pynetappfoundry.clients.ontap.cli.time.monotonic") as mock_time,
        ):
            mock_ssh = MagicMock()
            mock_ssh_class.return_value = mock_ssh
            mock_transport = MagicMock()
            mock_channel = MagicMock()
            mock_ssh.get_transport.return_value = mock_transport
            mock_transport.open_session.return_value = mock_channel
            mock_transport.is_active.return_value = True
            mock_channel.recv_ready.return_value = False
            mock_channel.exit_status_ready.return_value = False
            # Simulate time passing past timeout (default is 10s)
            mock_time.side_effect = [0.0, 11.0]

            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
            )

            with pytest.raises(CLITimeoutError):
                cli.run_command("test")

            # Channel should be closed (called in finally block)
            assert mock_channel.close.call_count >= 1


class TestONTAPCLIRunCommand:
    """Tests for ONTAPCLI.run_command method."""

    def test_successful_command_returns_output(self) -> None:
        """run_command should return parsed output lines."""
        with patch("paramiko.SSHClient") as mock_ssh_class:
            mock_ssh = MagicMock()
            mock_ssh_class.return_value = mock_ssh
            mock_transport = MagicMock()
            mock_channel = MagicMock()
            mock_ssh.get_transport.return_value = mock_transport
            mock_transport.open_session.return_value = mock_channel
            mock_transport.is_active.return_value = True
            # recv_ready returns True for both reads
            mock_channel.recv_ready.side_effect = [True, True]
            # Return output then empty to signal end
            mock_channel.recv.side_effect = [b"Node: node1\nStatus: up\n", b""]

            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
            )

            result = cli.run_command("system node show")

            assert "Node: node1" in result
            assert "Status: up" in result

    def test_error_in_output_raises_cli_command_error(self) -> None:
        """run_command should raise CLICommandError if output contains Error:."""
        with patch("paramiko.SSHClient") as mock_ssh_class:
            mock_ssh = MagicMock()
            mock_ssh_class.return_value = mock_ssh
            mock_transport = MagicMock()
            mock_channel = MagicMock()
            mock_ssh.get_transport.return_value = mock_transport
            mock_transport.open_session.return_value = mock_channel
            mock_transport.is_active.return_value = True
            mock_channel.recv_ready.side_effect = [True, True]
            mock_channel.recv.side_effect = [b"Error: command not found\n", b""]

            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
            )

            with pytest.raises(CLICommandError) as exc_info:
                cli.run_command("invalid command")

            assert "Error:" in str(exc_info.value)

    def test_no_transport_raises_error(self) -> None:
        """run_command should raise CLICommandError if transport is unavailable."""
        with patch("paramiko.SSHClient") as mock_ssh_class:
            mock_ssh = MagicMock()
            mock_ssh_class.return_value = mock_ssh
            mock_ssh.get_transport.return_value = None

            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
            )

            with pytest.raises(CLICommandError) as exc_info:
                cli.run_command("test")

            assert "transport not available" in str(exc_info.value)

    def test_skips_login_messages(self) -> None:
        """run_command should skip login-related messages."""
        with patch("paramiko.SSHClient") as mock_ssh_class:
            mock_ssh = MagicMock()
            mock_ssh_class.return_value = mock_ssh
            mock_transport = MagicMock()
            mock_channel = MagicMock()
            mock_ssh.get_transport.return_value = mock_transport
            mock_transport.open_session.return_value = mock_channel
            mock_transport.is_active.return_value = True
            mock_channel.recv_ready.side_effect = [True, True]
            mock_channel.recv.side_effect = [
                b"Last login time: 2024-01-01\nNode: node1\nStatus: up\n",
                b"",
            ]

            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
            )

            result = cli.run_command("system node show")

            assert "Last login time" not in " ".join(result)
            assert "Node: node1" in result


class TestParseSeparatorOutput:
    """Tests for the _parse_separator_output helper function."""

    def test_empty_input(self) -> None:
        """Empty list returns empty data and descriptions."""
        data, descriptions = _parse_separator_output([])
        assert data == []
        assert descriptions == {}

    def test_headers_only(self) -> None:
        """Single header line with no description/data returns empty."""
        data, descriptions = _parse_separator_output(["node,aggr,status"])
        assert data == []
        assert descriptions == {}

    def test_headers_and_descriptions_only(self) -> None:
        """Headers + descriptions but no data returns empty data with descriptions."""
        lines = [
            "node,aggr,status",
            "Node Name,Aggregate,Status",
        ]
        data, descriptions = _parse_separator_output(lines)
        assert data == []
        assert descriptions == {
            "node": "Node Name",
            "aggr": "Aggregate",
            "status": "Status",
        }

    def test_simple_data(self) -> None:
        """Standard unquoted rows parse correctly."""
        lines = [
            "node,aggr,status",
            "Node Name,Aggregate,Status",
            "node1,aggr0,online",
            "node2,aggr1,offline",
        ]
        data, descriptions = _parse_separator_output(lines)
        assert len(data) == 2
        assert data[0] == {"node": "node1", "aggr": "aggr0", "status": "online"}
        assert data[1] == {"node": "node2", "aggr": "aggr1", "status": "offline"}
        assert descriptions == {
            "node": "Node Name",
            "aggr": "Aggregate",
            "status": "Status",
        }

    def test_quoted_value_with_comma(self) -> None:
        """Quoted value containing a comma is kept intact."""
        lines = [
            "node,raidstatus,state",
            "Node Name,RAID Status,State",
            'node1,"raid0, normal",online',
        ]
        data, _ = _parse_separator_output(lines)
        assert len(data) == 1
        assert data[0]["raidstatus"] == "raid0, normal"
        assert data[0]["node"] == "node1"
        assert data[0]["state"] == "online"

    def test_multiline_quoted_value(self) -> None:
        """Value spanning multiple input lines is reassembled by csv.reader.

        When run_command splits SSH output by lines, a quoted value like
        ``"raid0\\nnormal"`` arrives as two separate strings. csv.reader
        reassembles them into a single field (joining without newline).
        """
        lines = [
            "node,raidstatus,state",
            "Node Name,RAID Status,State",
            'node1,"raid0',
            'normal",online',
        ]
        data, _ = _parse_separator_output(lines)
        assert len(data) == 1
        assert data[0]["raidstatus"] == "raid0normal"
        assert data[0]["state"] == "online"

    def test_trailing_comma_in_headers(self) -> None:
        """Trailing comma produces empty header that is filtered out."""
        lines = [
            "node,aggr,",
            "Node Name,Aggregate,",
            "node1,aggr0,",
        ]
        data, _ = _parse_separator_output(lines)
        assert "" not in data[0]
        assert data[0] == {"node": "node1", "aggr": "aggr0"}

    def test_empty_field_values(self) -> None:
        """Empty fields between commas are preserved as empty strings."""
        lines = [
            "node,aggr,status",
            "Node Name,Aggregate,Status",
            "node1,,online",
        ]
        data, _ = _parse_separator_output(lines)
        assert data[0]["aggr"] == ""

    def test_backward_compat_unquoted(self) -> None:
        """Unquoted values produce identical results to old str.split behavior."""
        lines = [
            "node,aggr,status",
            "Node Name,Aggregate,Status",
            "node1,aggr0,online",
        ]
        data, descriptions = _parse_separator_output(lines)

        # Simulate old str.split behavior
        headers = lines[0].split(",")
        old_desc = dict(zip(headers, lines[1].split(","), strict=False))
        old_data = dict(zip(headers, lines[2].split(","), strict=False))

        assert data[0] == old_data
        assert descriptions == old_desc


class TestSeparatorParserMethod:
    """Tests for ONTAPCLI.run_a_show_command_and_parse_seperator."""

    def test_delegates_to_helper(self) -> None:
        """Method returns correct data and command includes set -showseparator."""
        with patch("paramiko.SSHClient") as mock_ssh_class:
            mock_ssh = MagicMock()
            mock_ssh_class.return_value = mock_ssh
            mock_transport = MagicMock()
            mock_channel = MagicMock()
            mock_ssh.get_transport.return_value = mock_transport
            mock_transport.open_session.return_value = mock_channel
            mock_transport.is_active.return_value = True
            mock_channel.recv_ready.side_effect = [True, True]
            mock_channel.recv.side_effect = [
                b"node,aggr,status\nNode Name,Aggregate,Status\nnode1,aggr0,online\n",
                b"",
            ]

            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
            )

            data, _ = cli.run_a_show_command_and_parse_seperator("aggr show")

            assert len(data) == 1
            assert data[0]["node"] == "node1"

            # Verify command includes separator config
            executed_cmd = mock_channel.exec_command.call_args[0][0]
            assert 'set -showseparator ","' in executed_cmd
            assert "aggr show" in executed_cmd

    def test_empty_output_returns_empty(self) -> None:
        """Empty output from run_command returns empty data and descriptions."""
        with patch("paramiko.SSHClient") as mock_ssh_class:
            mock_ssh = MagicMock()
            mock_ssh_class.return_value = mock_ssh
            mock_transport = MagicMock()
            mock_channel = MagicMock()
            mock_ssh.get_transport.return_value = mock_transport
            mock_transport.open_session.return_value = mock_channel
            mock_transport.is_active.return_value = True
            # Command produces no output lines
            mock_channel.recv_ready.side_effect = [True, True]
            mock_channel.recv.side_effect = [b"\n", b""]

            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
            )

            data, desc = cli.run_a_show_command_and_parse_seperator("aggr show")

            assert data == []
            assert desc == {}

    def test_quoted_commas_end_to_end(self) -> None:
        """Quoted values with commas are parsed without corruption end-to-end."""
        with patch("paramiko.SSHClient") as mock_ssh_class:
            mock_ssh = MagicMock()
            mock_ssh_class.return_value = mock_ssh
            mock_transport = MagicMock()
            mock_channel = MagicMock()
            mock_ssh.get_transport.return_value = mock_transport
            mock_transport.open_session.return_value = mock_channel
            mock_transport.is_active.return_value = True
            mock_channel.recv_ready.side_effect = [True, True]
            mock_channel.recv.side_effect = [
                b"node,raidstatus,state\n"
                b"Node Name,RAID Status,State\n"
                b'node1,"raid0, normal",online\n',
                b"",
            ]

            cli = ONTAPCLI(
                name="test",
                host_or_ip="192.168.1.1",
                username="admin",
                password="password",
            )

            data, _ = cli.run_a_show_command_and_parse_seperator("aggr show")

            assert len(data) == 1
            assert data[0]["raidstatus"] == "raid0, normal"
            assert data[0]["state"] == "online"
