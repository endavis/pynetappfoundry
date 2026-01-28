"""A module to run commands through the ONTAP CLI."""

from __future__ import annotations

import json
import logging
from typing import Any

import paramiko
from netapp_ontap import HostConnection
from netapp_ontap.resources import CLI

CMD_KEYS: dict[str, str] = {
    "volume show": "Volume Name",
    "vol show": "Volume Name",
}


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


class ONTAPCLI:
    """Class to run commands through the ONTAP CLI."""

    def __init__(
        self,
        name: str,
        host_or_ip: str,
        username: str,
        password: str,
    ) -> None:
        """Initialize the ONTAP CLI client.

        Args:
            name: Name of the host.
            host_or_ip: IP address or hostname to connect to.
            username: SSH username.
            password: SSH password.
        """
        self.name = name
        self.host = host_or_ip
        self.username = username
        self.password = password

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

    def connect(self) -> None:
        """Connect to the server via SSH."""
        transport = self.ssh.get_transport()
        if not transport or not transport.is_active():
            logging.debug("Connect: creating connection")
            if self.pkey:
                self.ssh.connect(self.host, username=self.username, pkey=self.pkey)
            else:
                self.ssh.connect(self.host, username=self.username, password=self.password)
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
            logging.info(f"{cmd} returned no output")
            return [], {}

        headers = output[0].split(",")
        if "" in headers:
            headers.remove("")
        del output[0]

        descriptions = output[0].split(",")
        if "" in descriptions:
            descriptions.remove("")
        descriptions_dict = dict(zip(headers, descriptions, strict=False))
        del output[0]

        data: list[dict[str, str]] = []
        for line in output:
            tdata = line.split(",")
            datadict = dict(zip(headers, tdata, strict=False))
            datadict.pop("", None)

            data.append(datadict)

        return data, descriptions_dict

    def run_command(
        self,
        cmd: str,
        arguments: str = "",
        respondto: str = " {y|n}:",
        response: str = "y\n",
    ) -> list[str]:
        """Run a command through the CLI and return the output.

        Args:
            cmd: The command to run.
            arguments: Arguments to the command.
            respondto: Prompt pattern to respond to.
            response: Response string to send.

        Returns:
            List of output lines.

        Raises:
            CLICommandError: If the command returns an error.
        """
        output: list[str] = []

        self.connect()
        logging.info(f"host {self.name}:{self.host} - running '{cmd}'")

        stdin, stdout, _stderr = self.cli.exec_command(f"{cmd} {arguments}")

        # Read raw bytes and decode with error handling for non-UTF-8 characters
        raw_output = stdout.read()
        decoded_output = raw_output.decode("utf-8", errors="replace")

        for line in decoded_output.splitlines():
            line = line.rstrip()
            logging.info(line)
            if not line or line == "\x07":
                continue

            if any(line_to_skip in line for line_to_skip in self.lines_to_skip):
                continue

            if "Error:" in line:
                raise CLICommandError(line)

            if respondto in line:
                logging.info(f"found {respondto} and sending {response}")
                stdin.write(response)
                stdin.flush()
            else:
                output.append(line)

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
                logging.error(f"bad line: {line}")
                continue

            key = key.strip()
            value = value.strip()

            if not primary_key:
                logging.info(f"setting primary_key to {key}")
                primary_key = key
            if not first_key:
                logging.info(f"setting first_key to {key}")
                first_key = key

            if primary_key == first_key and key == primary_key:
                logging.info(f"primary == first, setting current object to {value}")
                current_object = value
                if current_object not in data:
                    data[current_object] = {}
                continue

            if key == primary_key:
                logging.info(
                    f"primary_key != first_key, found primary key,"
                    f" setting current object to {value}"
                )
                current_object = value
                if temp_data:
                    logging.info("have temp_data")
                    data[current_object] = temp_data
                    temp_data = {}

            if key == first_key:
                logging.info(
                    "primary_key != first_key, found first key, "
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
            f'{self.name} - running "{command}" with arguments'
            f" {kwargs} and privilege: {privilege_level}"
        )
        with HostConnection(
            self.host, username=self.username, password=self.password, verify=False
        ):
            response = CLI().execute(command, privilege_level=privilege_level, **kwargs)
            print(json.dumps(response.http_response.json(), indent=4))
