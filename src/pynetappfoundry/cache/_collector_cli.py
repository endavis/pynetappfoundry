"""CLI (SSH) helpers for the metadata collector (#899)."""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING

from pynetappfoundry.cache._collector_base import logger

if TYPE_CHECKING:
    from pynetappfoundry.clients.ontap.cli import ONTAPCLI


def connect_early(cli_client: ONTAPCLI | None, log_prefix: str) -> None:
    """Establish the SSH connection early to reduce latency.

    Failures are logged and swallowed; the CLI call retries the connection.
    """
    if cli_client:
        try:
            logger.debug("%s Establishing early SSH connection", log_prefix)
            cli_client.connect()
            logger.debug("%s Early SSH connection established", log_prefix)
        except Exception as e:
            logger.debug("%s Early SSH connection failed (will retry later): %s", log_prefix, e)


class SshPreconnect:
    """Connect the CLI client's SSH session in a background thread.

    ``start()`` overlaps the connect with API calls; ``wait()`` joins the
    thread so a later CLI call does not race the connect.
    """

    def __init__(self, cli_client: ONTAPCLI | None, log_prefix: str, thread_name: str) -> None:
        self._cli_client = cli_client
        self._log_prefix = log_prefix
        self._thread_name = thread_name
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        """Start the background connect (no-op without a CLI client)."""
        if not self._cli_client:
            return
        logger.debug("%s Starting SSH connection in background", self._log_prefix)
        self._thread = threading.Thread(
            target=connect_early,
            args=(self._cli_client, self._log_prefix),
            name=self._thread_name,
            daemon=True,
        )
        self._thread.start()

    def wait(self, timeout: float | None = None) -> None:
        """Wait for the background connect to finish, if one was started."""
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=timeout)


def run_vm_instance_show(cli_client: ONTAPCLI, log_prefix: str) -> list[str]:
    """Run ``virtual-machine instance show`` and return the raw output."""
    logger.debug("%s CLI command: virtual-machine instance show", log_prefix)
    output = cli_client.run_command("virtual-machine instance show")
    logger.debug("%s CLI response: %d lines", log_prefix, len(output))
    return output
