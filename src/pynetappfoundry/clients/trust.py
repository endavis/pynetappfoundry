"""Trust-on-first-use records for ONTAP SSH host keys and TLS certificates.

The first connection to a host records its identity. Later connections must present
the same identity, otherwise :class:`HostIdentityChangedError` is raised before any
credentials are sent. Records live in a trust directory (``<config_dir>/.trust``):

- ``known_hosts``: SSH host keys in OpenSSH format, so ``ssh-keygen -R`` works on it.
- ``tls_fingerprints.json``: SHA-256 certificate fingerprints keyed ``host:port``.

See ADR-0025 and ``docs/usage/basics.md`` ("Host identity").
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import logging
import os
import socket
import ssl
import tempfile
import threading
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import paramiko
import requests
from requests.adapters import HTTPAdapter

logger = logging.getLogger(__name__)

TRUST_DIR_NAME = ".trust"
KNOWN_HOSTS_NAME = "known_hosts"
TLS_FINGERPRINTS_NAME = "tls_fingerprints.json"
_FINGERPRINT_MISMATCH_TEXT = "Fingerprints did not match"
_CAPTURE_TIMEOUT_SECONDS = 10.0

TlsFetcher = Callable[[str, int], bytes]


class HostIdentityChangedError(Exception):
    """A host presented an identity that differs from the one recorded earlier.

    Deliberately not a ``requests.ConnectionError`` so retry logic does not retry it.

    Attributes:
        host: The host (``host`` or ``host:port``) whose identity differs.
        record_path: The file holding the recorded identity.
        reset_hint: The command or step that clears the recorded identity.
    """

    def __init__(self, host: str, record_path: Path, reset_hint: str, detail: str = "") -> None:
        """Initialize the error.

        Args:
            host: The host whose identity differs from the recorded one.
            record_path: The file holding the recorded identity.
            reset_hint: How to clear the recorded identity once the change is verified.
            detail: Optional extra detail (for example the expected and received values).
        """
        self.host = host
        self.record_path = record_path
        self.reset_hint = reset_hint
        self.detail = detail
        message = (
            f"The identity presented by {host} differs from the one recorded in "
            f"{record_path}. The connection was refused before credentials were sent."
        )
        if detail:
            message += f" {detail}"
        message += f" If the change is expected, reset the record with: {reset_hint}"
        super().__init__(message)


_registry_lock = threading.Lock()
_path_locks: dict[str, threading.Lock] = {}


def _lock_for(path: Path) -> threading.Lock:
    """Return the one lock shared by every writer of *path* in this process."""
    key = str(path.resolve())
    with _registry_lock:
        lock = _path_locks.get(key)
        if lock is None:
            lock = threading.Lock()
            _path_locks[key] = lock
        return lock


def _atomic_write(path: Path, data: str) -> None:
    """Write *data* to *path* via a temp file, fsync and ``os.replace``.

    The directory is created with mode 0o700 and the file has mode 0o600.
    """
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)
    with contextlib.suppress(OSError):
        parent.chmod(0o700)
    fd, tmp_name = tempfile.mkstemp(dir=parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp_name, 0o600)
        os.replace(tmp_name, path)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(tmp_name)
        raise


class KnownHostsStore:
    """SSH host keys recorded on first use, in OpenSSH ``known_hosts`` format."""

    def __init__(self, path: Path) -> None:
        """Initialize the store.

        Args:
            path: The ``known_hosts`` file. Created on the first recorded key.
        """
        self.path = path

    def load_into(self, client: paramiko.SSHClient) -> None:
        """Load the recorded keys into *client*'s host keys, if the file exists."""
        if self.path.exists():
            client.load_host_keys(str(self.path))

    def record(self, hostname: str, key: paramiko.PKey) -> bool:
        """Record *key* for *hostname*, or confirm it matches the recorded one.

        Args:
            hostname: Host name as paramiko passes it (``[host]:port`` for a
                non-default port).
            key: The host key presented by the server.

        Returns:
            True if the key was newly recorded, False if it was already recorded.

        Raises:
            HostIdentityChangedError: A different key is recorded for the host.
        """
        with _lock_for(self.path):
            existing_text = self.path.read_text(encoding="utf-8") if self.path.exists() else ""
            known = paramiko.HostKeys()
            if self.path.exists():
                known.load(str(self.path))
            recorded = known.lookup(hostname)
            if recorded is not None:
                if recorded.get(key.get_name()) == key:
                    return False
                raise HostIdentityChangedError(
                    hostname,
                    self.path,
                    f"ssh-keygen -R {hostname} -f {self.path}",
                    detail=f"The presented {key.get_name()} key does not match the recorded key.",
                )
            if existing_text and not existing_text.endswith("\n"):
                existing_text += "\n"
            line = f"{hostname} {key.get_name()} {key.get_base64()}\n"
            _atomic_write(self.path, existing_text + line)
            logger.info("Recorded SSH host key for %s in %s", hostname, self.path)
            return True


class TrustOnFirstUsePolicy(paramiko.MissingHostKeyPolicy):
    """Record an unknown SSH host key on first use and reject a changed one."""

    def __init__(self, store: KnownHostsStore) -> None:
        """Initialize the policy.

        Args:
            store: The store that holds the recorded keys.
        """
        self._store = store

    def missing_host_key(
        self, client: paramiko.SSHClient, hostname: str, key: paramiko.PKey
    ) -> None:
        """Record *key* for *hostname* and add it to *client*'s in-memory host keys."""
        self._store.record(hostname, key)
        client.get_host_keys().add(hostname, key.get_name(), key)


def _fetch_peer_certificate_der(host: str, port: int) -> bytes:
    """Return the DER certificate a TLS server presents, without validating it.

    Makes one unauthenticated handshake and sends no application data.
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with (
        socket.create_connection((host, port), timeout=_CAPTURE_TIMEOUT_SECONDS) as sock,
        context.wrap_socket(sock, server_hostname=host) as tls,
    ):
        der = tls.getpeercert(binary_form=True)
    if not der:
        raise ssl.SSLError(f"{host}:{port} presented no certificate")
    return der


class TlsFingerprintStore:
    """SHA-256 certificate fingerprints recorded on first use, keyed ``host:port``."""

    def __init__(self, path: Path, fetcher: TlsFetcher | None = None) -> None:
        """Initialize the store.

        Args:
            path: The JSON file. Created on the first recorded fingerprint.
            fetcher: Returns the DER certificate a host presents. Injected so tests
                never open a socket. Defaults to one unauthenticated TLS handshake.
        """
        self.path = path
        self._fetcher: TlsFetcher = fetcher or _fetch_peer_certificate_der
        self._cache: dict[str, str] = {}

    def _read(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"version": 1, "hosts": {}}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Cannot read TLS fingerprint records in {self.path}: {exc}") from exc
        if not isinstance(data, dict) or not isinstance(data.get("hosts"), dict):
            raise ValueError(f"Unexpected format in TLS fingerprint records: {self.path}")
        return data

    def get_fingerprint(self, host: str, port: int = 443) -> str:
        """Return the recorded fingerprint for *host*:*port*, recording it on first use.

        Args:
            host: Host name or address.
            port: TLS port.

        Returns:
            The lowercase SHA-256 hex digest of the certificate.
        """
        key = f"{host}:{port}"
        cached = self._cache.get(key)
        if cached is not None:
            return cached
        with _lock_for(self.path):
            data = self._read()
            entry = data["hosts"].get(key)
            if entry is None:
                fingerprint = hashlib.sha256(self._fetcher(host, port)).hexdigest()
                data["hosts"][key] = {
                    "sha256": fingerprint,
                    "first_seen": datetime.now(UTC).isoformat(),
                }
                _atomic_write(self.path, json.dumps(data, indent=2, sort_keys=True) + "\n")
                logger.info("Recorded TLS fingerprint for %s in %s", key, self.path)
            else:
                fingerprint = str(entry["sha256"]).lower()
        self._cache[key] = fingerprint
        return fingerprint


class FingerprintPinningAdapter(HTTPAdapter):
    """HTTPS adapter that requires the pinned certificate fingerprint for each host.

    Certificate chain validation stays off (ONTAP clusters commonly use self-signed
    certificates); urllib3 compares the fingerprint at connect time, before the
    request and its credentials are written.
    """

    def __init__(self, store: TlsFingerprintStore, **kwargs: Any) -> None:
        """Initialize the adapter.

        Args:
            store: The store that supplies the pinned fingerprints.
            **kwargs: Passed to ``HTTPAdapter`` (pool sizes, ``max_retries``).
        """
        self._store = store
        super().__init__(**kwargs)

    def build_connection_pool_key_attributes(
        self, request: requests.PreparedRequest, verify: Any, cert: Any = None
    ) -> tuple[Any, Any]:
        """Add ``assert_fingerprint`` to the TLS settings of https requests.

        Returns ``Any`` pairs because the requests stubs type the pool settings as a
        closed TypedDict that has no ``assert_fingerprint`` key, which urllib3 accepts.
        """
        host_params, stub_tls_params = super().build_connection_pool_key_attributes(
            request, verify, cert
        )
        tls_params: dict[str, Any] = dict(stub_tls_params)
        if host_params["scheme"] == "https":
            host = host_params["host"]
            port = host_params["port"] or 443
            try:
                tls_params["assert_fingerprint"] = self._store.get_fingerprint(host, port)
            except requests.exceptions.RequestException:
                raise
            except TimeoutError as exc:
                raise requests.exceptions.ConnectTimeout(
                    f"Timed out reading the TLS certificate of {host}:{port}: {exc}",
                    request=request,
                ) from exc
            except OSError as exc:
                raise requests.exceptions.ConnectionError(
                    f"Could not read the TLS certificate of {host}:{port}: {exc}",
                    request=request,
                ) from exc
        return host_params, tls_params

    def send(
        self, request: requests.PreparedRequest, *args: Any, **kwargs: Any
    ) -> requests.Response:
        """Send *request*, mapping a fingerprint mismatch to ``HostIdentityChangedError``."""
        try:
            return super().send(request, *args, **kwargs)
        except requests.exceptions.SSLError as exc:
            if _FINGERPRINT_MISMATCH_TEXT not in str(exc):
                raise
            parts = urlsplit(request.url or "")
            host = parts.hostname or ""
            port = parts.port or 443
            raise HostIdentityChangedError(
                f"{host}:{port}",
                self._store.path,
                f'remove the "{host}:{port}" entry from {self._store.path}',
                detail="The presented TLS certificate does not match the recorded fingerprint.",
            ) from exc


class HostTrustStore:
    """The SSH and TLS trust records under one trust directory."""

    def __init__(self, directory: Path, tls_fetcher: TlsFetcher | None = None) -> None:
        """Initialize the store. Nothing is created on disk until a record is written.

        Args:
            directory: The trust directory (``<config_dir>/.trust``).
            tls_fetcher: Optional certificate fetcher for the TLS store (tests).
        """
        self.directory = directory
        self.ssh = KnownHostsStore(directory / KNOWN_HOSTS_NAME)
        self.tls = TlsFingerprintStore(directory / TLS_FINGERPRINTS_NAME, tls_fetcher)
