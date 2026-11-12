"""Optional CA validation for the ONTAP clients (#982).

Real TLS servers on 127.0.0.1 exercise ``ONTAPAPIClient`` and the python-API path of
``ONTAPCLI``: a CA-signed certificate with a matching IP SAN, one with the wrong SAN, and a
self-signed one.
"""

from __future__ import annotations

import datetime
import ipaddress
import json
import socket
import ssl
import threading
import warnings
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import requests
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID
from urllib3.exceptions import InsecureRequestWarning

from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
from pynetappfoundry.clients.ontap.cli import ONTAPCLI, _open_host_connection
from pynetappfoundry.clients.trust import FingerprintPinningAdapter, HostTrustStore
from pynetappfoundry.core.config import ConfigurationError

CLIENT_TIMEOUT = 10.0
RESPONSE = b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\nConnection: close\r\n\r\n{}"
LOCALHOST = ipaddress.ip_address("127.0.0.1")


@dataclass(frozen=True)
class Tls:
    """A running local HTTPS server."""

    port: int
    der: bytes

    @property
    def url(self) -> str:
        return f"https://127.0.0.1:{self.port}/"

    @property
    def host(self) -> str:
        return f"127.0.0.1:{self.port}"


def _pem(cert: x509.Certificate) -> bytes:
    return cert.public_bytes(serialization.Encoding.PEM)


def _key_pem(key: ec.EllipticCurvePrivateKey) -> bytes:
    return key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )


def _builder(
    subject: x509.Name, issuer: x509.Name, key: ec.EllipticCurvePrivateKey
) -> x509.CertificateBuilder:
    now = datetime.datetime.now(datetime.UTC)
    return (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(minutes=5))
        .not_valid_after(now + datetime.timedelta(days=1))
    )


def _name(common_name: str) -> x509.Name:
    return x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])


def _make_ca(common_name: str) -> tuple[ec.EllipticCurvePrivateKey, x509.Certificate]:
    key = ec.generate_private_key(ec.SECP256R1())
    name = _name(common_name)
    cert = (
        _builder(name, name, key)
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
        .sign(key, hashes.SHA256())
    )
    return key, cert


def _make_leaf(
    ca_key: ec.EllipticCurvePrivateKey,
    ca_cert: x509.Certificate,
    san: x509.GeneralName,
) -> tuple[ec.EllipticCurvePrivateKey, x509.Certificate]:
    key = ec.generate_private_key(ec.SECP256R1())
    cert = (
        _builder(_name("cluster"), ca_cert.subject, key)
        .add_extension(x509.SubjectAlternativeName([san]), critical=False)
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_cert.public_key()),  # type: ignore[arg-type]  # EC key is accepted at runtime
            critical=False,
        )
        .sign(ca_key, hashes.SHA256())
    )
    return key, cert


def _make_self_signed() -> tuple[ec.EllipticCurvePrivateKey, x509.Certificate]:
    key = ec.generate_private_key(ec.SECP256R1())
    name = _name("127.0.0.1")
    cert = (
        _builder(name, name, key)
        .add_extension(x509.SubjectAlternativeName([x509.IPAddress(LOCALHOST)]), critical=False)
        .sign(key, hashes.SHA256())
    )
    return key, cert


@contextmanager
def _serve(directory: Path, name: str, key: Any, cert: x509.Certificate) -> Iterator[Tls]:
    cert_path = directory / f"{name}-cert.pem"
    key_path = directory / f"{name}-key.pem"
    cert_path.write_bytes(_pem(cert))
    key_path.write_bytes(_key_pem(key))
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
                # A client that refuses the certificate must not kill the server thread.
                raw.close()

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    try:
        yield Tls(port=port, der=cert.public_bytes(serialization.Encoding.DER))
    finally:
        stop.set()
        thread.join(timeout=5)
        listener.close()


@dataclass(frozen=True)
class Pki:
    """Servers and bundle files shared by the tests of this module."""

    good: Tls
    mismatch: Tls
    self_signed: Tls
    ca_bundle: Path
    other_ca_bundle: Path


@pytest.fixture(scope="module")
def pki(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Pki]:
    directory = tmp_path_factory.mktemp("pki")
    ca_key, ca_cert = _make_ca("test ca")
    _, other_ca_cert = _make_ca("unrelated ca")
    good_key, good_cert = _make_leaf(ca_key, ca_cert, x509.IPAddress(LOCALHOST))
    bad_key, bad_cert = _make_leaf(ca_key, ca_cert, x509.DNSName("other.example"))
    ss_key, ss_cert = _make_self_signed()
    ca_bundle = directory / "ca.pem"
    ca_bundle.write_bytes(_pem(ca_cert))
    other_bundle = directory / "other-ca.pem"
    other_bundle.write_bytes(_pem(other_ca_cert))
    with (
        _serve(directory, "good", good_key, good_cert) as good,
        _serve(directory, "mismatch", bad_key, bad_cert) as mismatch,
        _serve(directory, "selfsigned", ss_key, ss_cert) as self_signed,
    ):
        yield Pki(good, mismatch, self_signed, ca_bundle, other_bundle)


@pytest.fixture(autouse=True)
def _no_env_ca_bundle(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)
    monkeypatch.delenv("CURL_CA_BUNDLE", raising=False)


@dataclass(frozen=True)
class Built:
    """An ``ONTAPAPIClient`` plus what the test needs to inspect."""

    client: ONTAPAPIClient
    store: HostTrustStore
    fetches: list[tuple[str, int]]


BuildClient = Callable[..., Built]


@pytest.fixture
def build_client(tmp_path: Path) -> Iterator[BuildClient]:
    clients: list[ONTAPAPIClient] = []

    def build(
        cluster_settings: dict[str, Any] | None = None,
        general: dict[str, Any] | None = None,
        der: bytes = b"der",
    ) -> Built:
        schema_dir = tmp_path / "ontap"
        schema_dir.mkdir(exist_ok=True)
        (schema_dir / "all.json").write_text(json.dumps({"basePath": "/api", "paths": {}}))
        fetches: list[tuple[str, int]] = []

        def fetcher(host: str, port: int) -> bytes:
            fetches.append((host, port))
            return der

        store = HostTrustStore(tmp_path / ".trust", fetcher)
        config = MagicMock()
        config.get_user.return_value = ("admin", "secret")
        config.get_schema_location.return_value = schema_dir
        config.get_trust_store.return_value = store
        config.get_ontap_api_settings.return_value = MagicMock(base_api_path="/api", timeout=5.0)
        config.data = {"clusters": {"c1": dict(cluster_settings or {})}}
        config.settings = {"ontapapi": {"general": dict(general or {})}}
        config.config_dir = tmp_path
        cluster = MagicMock()
        cluster.name = "c1"
        cluster.ip = "127.0.0.1"
        client = ONTAPAPIClient(cluster=cluster, config=config)
        clients.append(client)
        return Built(client, store, fetches)

    yield build
    for client in clients:
        client.session.close()


def _get(built: Built, url: str) -> requests.Response:
    return built.client.session.get(url, verify=built.client.verify_ssl, timeout=CLIENT_TIMEOUT)


def _no_fingerprint_record(built: Built) -> None:
    assert not built.store.tls.path.exists()
    assert built.fetches == []


class TestOntapApiClient:
    def test_default_pins_self_signed_server(self, pki: Pki, build_client: BuildClient) -> None:
        built = build_client(der=pki.self_signed.der)
        assert built.client.verify_ssl is False
        assert _get(built, pki.self_signed.url).status_code == 200
        assert built.store.tls.path.exists()

    def test_verify_ssl_true_refuses_self_signed(self, pki: Pki, build_client: BuildClient) -> None:
        built = build_client({"verify_ssl": True})
        assert built.client.verify_ssl is True
        with pytest.raises(requests.exceptions.SSLError):
            _get(built, pki.self_signed.url)
        _no_fingerprint_record(built)

    def test_ca_bundle_accepts_ca_signed_server_without_warning_or_pin(
        self, pki: Pki, build_client: BuildClient
    ) -> None:
        built = build_client({"ca_bundle": str(pki.ca_bundle)})
        assert built.client.verify_ssl == str(pki.ca_bundle)
        with warnings.catch_warnings():
            warnings.simplefilter("error", InsecureRequestWarning)
            response = _get(built, pki.good.url)
        assert response.status_code == 200
        _no_fingerprint_record(built)

    def test_global_ca_bundle_applies(self, pki: Pki, build_client: BuildClient) -> None:
        built = build_client(general={"ca_bundle": str(pki.ca_bundle)})
        assert _get(built, pki.good.url).status_code == 200

    def test_ca_bundle_refuses_self_signed(self, pki: Pki, build_client: BuildClient) -> None:
        built = build_client({"ca_bundle": str(pki.ca_bundle)})
        with pytest.raises(requests.exceptions.SSLError):
            _get(built, pki.self_signed.url)
        _no_fingerprint_record(built)

    def test_wrong_ca_bundle_refuses_server(self, pki: Pki, build_client: BuildClient) -> None:
        built = build_client({"ca_bundle": str(pki.other_ca_bundle)})
        with pytest.raises(requests.exceptions.SSLError):
            _get(built, pki.good.url)
        _no_fingerprint_record(built)

    def test_ca_bundle_refuses_hostname_mismatch(self, pki: Pki, build_client: BuildClient) -> None:
        built = build_client({"ca_bundle": str(pki.ca_bundle)})
        with pytest.raises(requests.exceptions.SSLError):
            _get(built, pki.mismatch.url)
        _no_fingerprint_record(built)

    def test_invalid_bundle_path_raises_naming_cluster(self, build_client: BuildClient) -> None:
        with pytest.raises(ConfigurationError, match=r"clusters\.c1\.ca_bundle"):
            build_client({"ca_bundle": "does-not-exist.pem"})


def _verify_connection(tmp_path: Path, tls: Tls, verify: bool | str) -> requests.Response:
    """Open a connection the way ``run_command_python_api`` does and GET the server."""
    store = HostTrustStore(tmp_path / ".trust", lambda host, port: tls.der)
    conn = _open_host_connection(tls.host, "u", "p", verify=verify)
    with conn:
        session = conn.session
        session.mount(conn.origin, FingerprintPinningAdapter(store.tls))
        response: requests.Response = session.get(tls.url, timeout=CLIENT_TIMEOUT)
    session.close()
    return response


class TestOntapCli:
    def test_run_command_python_api_passes_tls_verify(self) -> None:
        host_connection = MagicMock()
        with (
            patch("paramiko.SSHClient"),
            patch("pynetappfoundry.clients.ontap.cli.HostConnection", host_connection),
            patch("pynetappfoundry.clients.ontap.cli.CLI") as cli_cls,
        ):
            cli_cls.return_value.execute.return_value.http_response.json.return_value = {}
            ONTAPCLI("c", "h", "u", "p", tls_verify="/etc/ca.pem").run_command_python_api("x")
        assert host_connection.call_args.kwargs["verify"] == "/etc/ca.pem"

    def test_default_tls_verify_is_false(self) -> None:
        host_connection = MagicMock()
        with (
            patch("paramiko.SSHClient"),
            patch("pynetappfoundry.clients.ontap.cli.HostConnection", host_connection),
            patch("pynetappfoundry.clients.ontap.cli.CLI") as cli_cls,
        ):
            cli_cls.return_value.execute.return_value.http_response.json.return_value = {}
            ONTAPCLI("c", "h", "u", "p").run_command_python_api("x")
        assert host_connection.call_args.kwargs["verify"] is False

    def test_bundle_accepts_ca_signed_server(self, pki: Pki, tmp_path: Path) -> None:
        response = _verify_connection(tmp_path, pki.good, str(pki.ca_bundle))
        assert response.status_code == 200
        assert not (tmp_path / ".trust").exists()

    def test_bundle_refuses_self_signed_server(self, pki: Pki, tmp_path: Path) -> None:
        with pytest.raises(requests.exceptions.SSLError):
            _verify_connection(tmp_path, pki.self_signed, str(pki.ca_bundle))

    @pytest.mark.parametrize("kind", ["true", "path", "false"])
    def test_open_host_connection_leaves_warning_filters_alone(self, pki: Pki, kind: str) -> None:
        values: dict[str, bool | str] = {"true": True, "path": str(pki.ca_bundle), "false": False}
        verify = values[kind]
        with warnings.catch_warnings():
            before = list(warnings.filters)
            _open_host_connection("h", "u", "p", verify=verify)
            assert warnings.filters == before
