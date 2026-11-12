"""InsecureRequestWarning is scoped, not suppressed process-wide (#983).

Pinned connections count as verified to urllib3, so the ONTAP client needs no suppression, and
netapp_ontap's own ``urllib3.disable_warnings`` call is contained to ``HostConnection``
construction.
"""

from __future__ import annotations

import datetime
import socket
import ssl
import subprocess
import sys
import textwrap
import threading
import warnings
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

import pytest
import requests
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID
from netapp_ontap import HostConnection
from urllib3.exceptions import InsecureRequestWarning

from pynetappfoundry.clients.ontap.cli import ONTAPCLI, _open_host_connection
from pynetappfoundry.clients.trust import FingerprintPinningAdapter, TlsFingerprintStore

CLIENT_TIMEOUT = 10.0
RESPONSE = b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\nConnection: close\r\n\r\n{}"


@dataclass(frozen=True)
class TlsServer:
    """A local HTTPS server with a self-signed certificate."""

    url: str
    der: bytes


def _self_signed(directory: Path) -> tuple[Path, Path, bytes]:
    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "127.0.0.1")])
    now = datetime.datetime.now(datetime.UTC)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(minutes=5))
        .not_valid_after(now + datetime.timedelta(days=1))
        .sign(key, hashes.SHA256())
    )
    cert_path = directory / "cert.pem"
    key_path = directory / "key.pem"
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    return cert_path, key_path, cert.public_bytes(serialization.Encoding.DER)


@pytest.fixture(scope="module")
def tls_server(tmp_path_factory: pytest.TempPathFactory) -> Iterator[TlsServer]:
    cert_path, key_path, der = _self_signed(tmp_path_factory.mktemp("tls"))
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_path, key_path)

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    listener.listen(5)
    listener.settimeout(0.2)
    port = listener.getsockname()[1]
    stop = threading.Event()

    def serve() -> None:
        while not stop.is_set():
            try:
                raw, _ = listener.accept()
            except TimeoutError:
                continue
            except OSError:
                return
            raw.settimeout(CLIENT_TIMEOUT)
            try:
                with context.wrap_socket(raw, server_side=True) as tls:
                    tls.recv(65536)
                    tls.sendall(RESPONSE)
            except (OSError, ssl.SSLError):
                # A client that drops mid-handshake must not kill the server thread.
                raw.close()

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    try:
        yield TlsServer(url=f"https://127.0.0.1:{port}/", der=der)
    finally:
        stop.set()
        thread.join(timeout=5)
        listener.close()


def _pinned_session(tmp_path: Path, der: bytes) -> requests.Session:
    store = TlsFingerprintStore(tmp_path / "tls.json", lambda host, port: der)
    session = requests.Session()
    session.mount("https://", FingerprintPinningAdapter(store))
    return session


def _unverified_get_warns(url: str) -> bool:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with requests.Session() as session:
            session.get(url, verify=False, timeout=CLIENT_TIMEOUT)
    return any(issubclass(w.category, InsecureRequestWarning) for w in caught)


def _run_python(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-c", code], check=True, capture_output=True, text=True)


def test_importing_api_leaves_warning_filters_alone() -> None:
    """Criterion 1: importing the client adds no InsecureRequestWarning filter."""
    code = textwrap.dedent(
        """
        import warnings
        import requests, urllib3, netapp_ontap  # their first import adds filters of its own
        before = list(warnings.filters)
        import pynetappfoundry.clients.ontap.api
        assert warnings.filters == before, "importing api changed warnings.filters"
        bad = [f for f in warnings.filters if f[2] is urllib3.exceptions.InsecureRequestWarning]
        assert not bad, bad
        print("ok")
        """
    )
    assert _run_python(code).stdout.strip() == "ok"


def test_pinned_request_does_not_warn(tls_server: TlsServer, tmp_path: Path) -> None:
    """Criterion 2 (#52): a pinned request raises no InsecureRequestWarning."""
    session = _pinned_session(tmp_path, tls_server.der)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        response = session.get(tls_server.url, verify=False, timeout=CLIENT_TIMEOUT)
    session.close()
    assert response.status_code == 200
    assert not [w for w in caught if issubclass(w.category, InsecureRequestWarning)]


def test_unverified_request_outside_the_client_warns(tls_server: TlsServer) -> None:
    """Criterion 3: importing the ONTAP client does not silence unverified requests."""
    import pynetappfoundry.clients.ontap.api  # noqa: F401  # the import itself is under test

    assert _unverified_get_warns(tls_server.url)


def test_open_host_connection_drops_netapp_ontap_filter() -> None:
    """The filter netapp_ontap adds on construction does not outlive the helper."""
    with warnings.catch_warnings():
        before = list(warnings.filters)
        _open_host_connection("h", "u", "p")
        assert warnings.filters == before


def test_direct_host_connection_does_add_the_filter() -> None:
    """Control: without the helper the filter is added, so the test above can fail."""
    with warnings.catch_warnings():
        before = list(warnings.filters)
        HostConnection("h", username="u", password="p", verify=False)
        assert warnings.filters != before
        assert any(f[2] is InsecureRequestWarning for f in warnings.filters)


def test_unverified_request_still_warns_after_python_api_call(tls_server: TlsServer) -> None:
    """A CLI python-API command leaves later unverified requests able to warn."""
    with (
        patch("paramiko.SSHClient"),
        patch("pynetappfoundry.clients.ontap.cli.CLI") as cli_cls,
    ):
        cli_cls.return_value.execute.return_value.http_response.json.return_value = {}
        ONTAPCLI("c", "127.0.0.1", "u", "p").run_command_python_api("volume show")
    assert _unverified_get_warns(tls_server.url)
