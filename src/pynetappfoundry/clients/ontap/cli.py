"""A module to run commands through the ONTAP CLI."""

from __future__ import annotations

import csv
import json
import logging
import threading
import time
from typing import Any

import paramiko
from netapp_ontap import HostConnection
from netapp_ontap.resources import CLI

CMD_KEYS: dict[str, str] = {
    "volume show": "Volume Name",
    "vol show": "Volume Name",
}


def _parse_separator_output(
    lines: list[str],
) -> tuple[list[dict[str, str]], dict[str, str]]:
    """Parse comma-separated CLI output using CSV reader.

    Uses ``csv.reader`` to correctly handle quoted values that contain
    commas or span multiple lines (RFC 4180).

    Args:
        lines: Raw output lines from ``run_command``.

    Returns:
        Tuple of (data rows as list of dicts, descriptions dict).
    """
    if not lines:
        return [], {}

    reader = csv.reader(iter(lines))

    try:
        raw_headers = next(reader)
    except StopIteration:
        return [], {}

    headers = [h for h in raw_headers if h]

    try:
        raw_descriptions = next(reader)
    except StopIteration:
        return [], {}

    descriptions = [d for d in raw_descriptions if d]
    descriptions_dict = dict(zip(headers, descriptions, strict=False))

    data: list[dict[str, str]] = []
    for row in reader:
        datadict = dict(zip(headers, row, strict=False))
        datadict.pop("", None)
        data.append(datadict)

    return data, descriptions_dict


class CLICommandError(Exception):
    """Exception raised for CLI command errors.

    Attributes:
        message: The error message.
    """

    def __init__(self, message: str) -> None:
        """Initialize the exception.

        Args:
            message: The error message.
        """
        self.message = message
        super().__init__(self.message)


class CLITimeoutError(CLICommandError):
    """Exception raised when a CLI command times out.

    Attributes:
        message: The error message.
        timeout: The timeout value that was exceeded.
    """

    def __init__(self, message: str, timeout: float) -> None:
        """Initialize the exception.

        Args:
            message: The error message.
            timeout: The timeout value in seconds.
        """
        self.timeout = timeout
        super().__init__(message)


class ONTAPCLI:
    """Class to run commands through the ONTAP CLI."""

    # Default timeout for CLI commands in seconds
    DEFAULT_TIMEOUT: float = 10.0

    def __init__(
        self,
        name: str,
        host_or_ip: str,
        username: str,
        password: str,
        timeout: float | None = None,
    ) -> None:
        """Initialize the ONTAP CLI client.

        Args:
            name: Name of the host.
            host_or_ip: IP address or hostname to connect to.
            username: SSH username.
            password: SSH password.
            timeout: Default timeout for commands in seconds. Defaults to 10s.
        """
        self.name = name
        self.host = host_or_ip
        self.username = username
        self.password = password
        self.timeout = timeout if timeout is not None else self.DEFAULT_TIMEOUT

        self.ssh: paramiko.SSHClient = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.cli = self.ssh

        self.lines_to_skip = [
            "Unsuccessful login attempts since last login",
            "Last login time:",
            "Your privilege has changed since last login.",
            "This is your first recorded login.",
        ]

        self.pkey: paramiko.RSAKey | None = None
        self.log_prefix = f"[{name}:ssh]"
        self._connect_lock = threading.Lock()

    def connect(self) -> None:
        """Connect to the server via SSH.

        Thread-safe: uses a lock to prevent race conditions when multiple
        threads attempt to connect simultaneously.
        """
        with self._connect_lock:
            transport = self.ssh.get_transport()
            if not transport or not transport.is_active():
                logging.debug(f"{self.log_prefix} Connect: creating connection")
                if self.pkey:
                    self.ssh.connect(
                        self.host,
                        username=self.username,
                        pkey=self.pkey,
                        timeout=self.timeout,
                    )
                else:
                    self.ssh.connect(
                        self.host,
                        username=self.username,
                        password=self.password,
                        timeout=self.timeout,
                    )
                transport = self.ssh.get_transport()
                if transport:
                    transport.set_keepalive(5)

    def run_command_and_parse(
        self,
        cmd: str,
        arguments: str = "",
        respondto: str = " {y|n}:",
        response: str = "y\n",
    ) -> dict[str, dict[str, str]]:
        """Run and parse a command.

        Args:
            cmd: The command to run.
            arguments: Arguments to the command.
            respondto: Prompt pattern to respond to.
            response: Response string to send.

        Returns:
            Parsed command output as dictionary.
        """
        output = self.run_command(cmd, arguments, respondto, response)

        primary_key: str | None = None
        if cmd in CMD_KEYS:
            primary_key = CMD_KEYS[cmd]

        return self.parse_generic_output(output, primary_key=primary_key)

    def run_a_show_command_and_parse_seperator(
        self,
        cmd: str,
        arguments: str = "",
        respondto: str = " {y|n}:",
        response: str = "y\n",
    ) -> tuple[list[dict[str, str]], dict[str, str]]:
        """Parse a show command with separators.

        Args:
            cmd: The command to run.
            arguments: Arguments to the command.
            respondto: Prompt pattern to respond to.
            response: Response string to send.

        Returns:
            Tuple of (data list, descriptions dict).
        """
        cmd = f'set d -confirmations off;set -showallfields true;set -showseparator ",";{cmd}'

        output = self.run_command(cmd, arguments, respondto, response)

        if not output:
            logging.info(f"{self.log_prefix} {cmd} returned no output")
            return [], {}

        return _parse_separator_output(output)

    def run_command(
        self,
        cmd: str,
        arguments: str = "",
        respondto: str = " {y|n}:",
        response: str = "y\n",
        timeout: float | None = None,
    ) -> list[str]:
        """Run a command through the CLI and return the output.

        Args:
            cmd: The command to run.
            arguments: Arguments to the command.
            respondto: Prompt pattern to respond to.
            response: Response string to send.
            timeout: Command timeout in seconds. Uses instance default if not specified.

        Returns:
            List of output lines.

        Raises:
            CLICommandError: If the command returns an error.
            CLITimeoutError: If the command times out.
        """
        output: list[str] = []
        effective_timeout = timeout if timeout is not None else self.timeout

        self.connect()
        logging.info(f"{self.log_prefix} running '{cmd}'")

        full_command = f"{cmd} {arguments}"

        # Get transport and open a channel with timeout
        transport = self.ssh.get_transport()
        if not transport:
            raise CLICommandError("SSH transport not available")

        channel = transport.open_session()
        channel.settimeout(effective_timeout)

        try:
            channel.exec_command(full_command)

            # Read output with application-level timeout tracking
            # Use recv_ready() instead of select() because select doesn't work
            # reliably with paramiko channels (may return ready when no data available)
            raw_output = b""
            start_time = time.monotonic()

            while True:
                # Check total elapsed time
                elapsed = time.monotonic() - start_time
                if elapsed >= effective_timeout:
                    channel.close()
                    raise CLITimeoutError(
                        f"Command '{cmd}' timed out after {effective_timeout} seconds",
                        timeout=effective_timeout,
                    )

                # Check if data is available to read (non-blocking)
                if channel.recv_ready():
                    chunk = channel.recv(4096)
                    if not chunk:
                        break
                    raw_output += chunk
                elif channel.exit_status_ready():
                    # Command completed, drain any remaining output
                    while channel.recv_ready():
                        chunk = channel.recv(4096)
                        if chunk:
                            raw_output += chunk
                        else:
                            break
                    break
                else:
                    # No data ready and command not finished, wait briefly
                    time.sleep(0.1)

            decoded_output = raw_output.decode("utf-8", errors="replace")

            for line in decoded_output.splitlines():
                line = line.rstrip()
                logging.info(f"{self.log_prefix} {line}")
                if not line or line == "\x07":
                    continue

                if any(line_to_skip in line for line_to_skip in self.lines_to_skip):
                    continue

                if "Error:" in line:
                    raise CLICommandError(line)

                if respondto in line:
                    logging.info(f"{self.log_prefix} found {respondto} and sending {response}")
                    channel.send(response.encode())
                else:
                    output.append(line)

        finally:
            channel.close()

        return output

    def disconnect(self) -> None:
        """Disconnect the SSH session."""
        self.ssh.close()

    def parse_generic_output(
        self,
        output: list[str],
        primary_key: str | None = None,
    ) -> dict[str, dict[str, str]]:
        """Parse generic output from a CLI command.

        Args:
            output: The output lines from the command.
            primary_key: The primary key field for the command.

        Returns:
            Parsed data as nested dictionary.
        """
        data: dict[str, dict[str, str]] = {}
        current_object: str | None = None
        first_key: str | None = None
        temp_data: dict[str, str] = {}

        for line in output:
            line = line.strip()

            if not line:
                continue
            if ":" not in line:
                continue
            if any(line_to_skip in line for line_to_skip in self.lines_to_skip):
                continue

            try:
                slist = line.split(":")
                key = slist[0]
                value = ":".join(slist[1:])
            except ValueError:
                logging.error(f"{self.log_prefix} bad line: {line}")
                continue

            key = key.strip()
            value = value.strip()

            if not primary_key:
                logging.info(f"{self.log_prefix} setting primary_key to {key}")
                primary_key = key
            if not first_key:
                logging.info(f"{self.log_prefix} setting first_key to {key}")
                first_key = key

            if primary_key == first_key and key == primary_key:
                logging.info(
                    f"{self.log_prefix} primary == first, setting current object to {value}"
                )
                current_object = value
                if current_object not in data:
                    data[current_object] = {}
                continue

            if key == primary_key:
                logging.info(
                    f"{self.log_prefix} primary_key != first_key, found primary key,"
                    f" setting current object to {value}"
                )
                current_object = value
                if temp_data:
                    logging.info(f"{self.log_prefix} have temp_data")
                    data[current_object] = temp_data
                    temp_data = {}

            if key == first_key:
                logging.info(
                    f"{self.log_prefix} primary_key != first_key, found first key, "
                    "setting current_object to None, updating temp_data"
                )
                current_object = None
                temp_data = {}
                temp_data[key] = value

            if current_object:
                data[current_object][key] = value
            else:
                temp_data[key] = value

        return data

    def run_command_python_api(
        self,
        command: str,
        privilege_level: str = "admin",
        **kwargs: Any,
    ) -> None:
        """Run a command through the Python API.

        Note: The fields that are returned must be specified in the fields argument.

        Args:
            command: The CLI command to run.
            privilege_level: Privilege level for the command.
            **kwargs: Additional arguments for the CLI execute call.
        """
        logging.info(
            f'{self.log_prefix} running "{command}" with arguments'
            f" {kwargs} and privilege: {privilege_level}"
        )
        with HostConnection(
            self.host, username=self.username, password=self.password, verify=False
        ):
            response = CLI().execute(command, privilege_level=privilege_level, **kwargs)
            print(json.dumps(response.http_response.json(), indent=4))
