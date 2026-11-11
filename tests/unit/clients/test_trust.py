"""Unit tests for trust-on-first-use host identity records."""

from __future__ import annotations

import hashlib
import json
import os
import socket
import ssl
import stat
import threading
from collections.abc import Callable
from pathlib import Path
from unittest.mock import MagicMock, patch

import paramiko
import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.exceptions import MaxRetryError
from urllib3.exceptions import SSLError as Urllib3SSLError
from urllib3.util.ssl_ import assert_fingerprint

from pynetappfoundry.clients.trust import (
    FingerprintPinningAdapter,
    HostIdentityChangedError,
    HostTrustStore,
    KnownHostsStore,
    TlsFingerprintStore,
    TrustOnFirstUsePolicy,
    _atomic_write,
    _lock_for,
)

DER_A = b"certificate-a"
DER_B = b"certificate-b"


# Windows has no POSIX permission bits: chmod only toggles read-only there.
_POSIX_MODES = os.name != "nt"


def _recorded(path: Path, hostname: str, key: paramiko.PKey) -> paramiko.PKey | None:
    """Return the key of *key*'s type recorded for *hostname* in *path*."""
    sub = paramiko.HostKeys(str(path)).lookup(hostname)
    assert sub is not None
    return sub.get(key.get_name())


def _fetcher(der: bytes = DER_A) -> MagicMock:
    return MagicMock(side_effect=lambda host, port: der)


def _run_threads(target: Callable[[int], object], count: int = 16) -> list[BaseException]:
    errors: list[BaseException] = []

    def wrapper(i: int) -> None:
        try:
            target(i)
        except BaseException as exc:
            errors.append(exc)

    threads = [threading.Thread(target=wrapper, args=(i,)) for i in range(count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return errors


class TestKnownHostsStore:
    """SSH host key recording."""

    def test_first_use_records_key_with_private_modes(self, tmp_path: Path) -> None:
        store = KnownHostsStore(tmp_path / ".trust" / "known_hosts")
        key = paramiko.ECDSAKey.generate()
        assert store.record("10.0.0.1", key) is True
        if _POSIX_MODES:
            assert stat.S_IMODE(store.path.stat().st_mode) == 0o600
            assert stat.S_IMODE(store.path.parent.stat().st_mode) == 0o700
        assert _recorded(store.path, "10.0.0.1", key) == key

    def test_later_run_loads_recorded_key(self, tmp_path: Path) -> None:
        store = KnownHostsStore(tmp_path / "known_hosts")
        key = paramiko.ECDSAKey.generate()
        store.record("10.0.0.1", key)
        client = paramiko.SSHClient()
        KnownHostsStore(tmp_path / "known_hosts").load_into(client)
        loaded = client.get_host_keys().lookup("10.0.0.1")
        assert loaded is not None
        assert loaded[key.get_name()] == key

    def test_load_into_without_file_is_noop(self, tmp_path: Path) -> None:
        client = paramiko.SSHClient()
        KnownHostsStore(tmp_path / "missing").load_into(client)
        assert len(client.get_host_keys()) == 0

    def test_matching_key_leaves_file_unchanged(self, tmp_path: Path) -> None:
        store = KnownHostsStore(tmp_path / "known_hosts")
        key = paramiko.ECDSAKey.generate()
        store.record("10.0.0.1", key)
        before = store.path.read_bytes()
        assert store.record("10.0.0.1", key) is False
        assert store.path.read_bytes() == before

    def test_mismatch_raises_and_leaves_file_unchanged(self, tmp_path: Path) -> None:
        store = KnownHostsStore(tmp_path / "known_hosts")
        store.record("10.0.0.1", paramiko.ECDSAKey.generate())
        before = store.path.read_bytes()
        with pytest.raises(HostIdentityChangedError) as exc_info:
            store.record("10.0.0.1", paramiko.ECDSAKey.generate())
        message = str(exc_info.value)
        assert "10.0.0.1" in message
        assert str(store.path) in message
        assert "ssh-keygen -R" in message
        assert store.path.read_bytes() == before

    def test_different_key_type_is_refused(self, tmp_path: Path) -> None:
        store = KnownHostsStore(tmp_path / "known_hosts")
        store.record("10.0.0.1", paramiko.ECDSAKey.generate())
        with pytest.raises(HostIdentityChangedError):
            store.record("10.0.0.1", paramiko.RSAKey.generate(2048))

    def test_non_default_port_stored_bracketed(self, tmp_path: Path) -> None:
        store = KnownHostsStore(tmp_path / "known_hosts")
        key = paramiko.ECDSAKey.generate()
        store.record("[10.0.0.1]:2222", key)
        assert store.path.read_text().startswith("[10.0.0.1]:2222 ")

    def test_existing_content_without_newline_preserved(self, tmp_path: Path) -> None:
        path = tmp_path / "known_hosts"
        first = paramiko.ECDSAKey.generate()
        path.write_text(f"a {first.get_name()} {first.get_base64()}")
        KnownHostsStore(path).record("b", paramiko.ECDSAKey.generate())
        hk = paramiko.HostKeys(str(path))
        assert hk.lookup("a") is not None
        assert hk.lookup("b") is not None

    def test_concurrent_first_connections_keep_all_entries(self, tmp_path: Path) -> None:
        store = KnownHostsStore(tmp_path / "known_hosts")
        keys = [paramiko.ECDSAKey.generate() for _ in range(16)]
        errors = _run_threads(lambda i: store.record(f"host{i}", keys[i]))
        assert errors == []
        for i in range(16):
            assert _recorded(store.path, f"host{i}", keys[i]) == keys[i]


class TestTrustOnFirstUsePolicy:
    """The paramiko missing-host-key policy."""

    def test_records_and_adds_to_client(self, tmp_path: Path) -> None:
        store = KnownHostsStore(tmp_path / "known_hosts")
        client = paramiko.SSHClient()
        key = paramiko.ECDSAKey.generate()
        TrustOnFirstUsePolicy(store).missing_host_key(client, "10.0.0.1", key)
        loaded = client.get_host_keys().lookup("10.0.0.1")
        assert loaded is not None
        assert loaded[key.get_name()] == key
        assert store.path.exists()

    def test_changed_key_is_refused_and_not_added(self, tmp_path: Path) -> None:
        store = KnownHostsStore(tmp_path / "known_hosts")
        store.record("10.0.0.1", paramiko.ECDSAKey.generate())
        client = paramiko.SSHClient()
        with pytest.raises(HostIdentityChangedError):
            TrustOnFirstUsePolicy(store).missing_host_key(
                client, "10.0.0.1", paramiko.ECDSAKey.generate()
            )
        assert client.get_host_keys().lookup("10.0.0.1") is None


class TestTlsFingerprintStore:
    """TLS fingerprint recording."""

    def test_first_use_fetches_once_and_saves_lowercase_hex(self, tmp_path: Path) -> None:
        fetch = _fetcher()
        store = TlsFingerprintStore(tmp_path / ".trust" / "tls.json", fetch)
        expected = hashlib.sha256(DER_A).hexdigest()
        assert store.get_fingerprint("h", 443) == expected
        assert store.get_fingerprint("h", 443) == expected
        fetch.assert_called_once_with("h", 443)
        data = json.loads(store.path.read_text())
        assert data["version"] == 1
        assert data["hosts"]["h:443"]["sha256"] == expected
        assert "first_seen" in data["hosts"]["h:443"]
        if _POSIX_MODES:
            assert stat.S_IMODE(store.path.stat().st_mode) == 0o600

    def test_new_instance_reads_record_without_fetching(self, tmp_path: Path) -> None:
        path = tmp_path / "tls.json"
        TlsFingerprintStore(path, _fetcher()).get_fingerprint("h", 443)
        fetch = _fetcher(DER_B)
        fp = TlsFingerprintStore(path, fetch).get_fingerprint("h", 443)
        assert fp == hashlib.sha256(DER_A).hexdigest()
        fetch.assert_not_called()

    def test_ports_are_separate_records(self, tmp_path: Path) -> None:
        store = TlsFingerprintStore(tmp_path / "tls.json", _fetcher())
        store.get_fingerprint("h", 443)
        store.get_fingerprint("h", 8443)
        assert set(json.loads(store.path.read_text())["hosts"]) == {"h:443", "h:8443"}

    def test_corrupt_file_raises_value_error(self, tmp_path: Path) -> None:
        path = tmp_path / "tls.json"
        path.write_text("{not json")
        with pytest.raises(ValueError, match="Cannot read"):
            TlsFingerprintStore(path, _fetcher()).get_fingerprint("h", 443)

    def test_unexpected_format_raises_value_error(self, tmp_path: Path) -> None:
        path = tmp_path / "tls.json"
        path.write_text("[]")
        with pytest.raises(ValueError, match="Unexpected format"):
            TlsFingerprintStore(path, _fetcher()).get_fingerprint("h", 443)

    def test_concurrent_distinct_hosts_keep_all_entries(self, tmp_path: Path) -> None:
        store = TlsFingerprintStore(tmp_path / "tls.json", _fetcher())
        errors = _run_threads(lambda i: store.get_fingerprint(f"host{i}", 443))
        assert errors == []
        assert len(json.loads(store.path.read_text())["hosts"]) == 16

    def test_concurrent_same_host_fetches_once(self, tmp_path: Path) -> None:
        fetch = _fetcher()
        path = tmp_path / "tls.json"
        stores = [TlsFingerprintStore(path, fetch) for _ in range(16)]
        errors = _run_threads(lambda i: stores[i].get_fingerprint("h", 443))
        assert errors == []
        assert fetch.call_count == 1


class TestFingerprintPinningAdapter:
    """The requests adapter that asserts the pinned fingerprint."""

    def _adapter(self, tmp_path: Path) -> tuple[FingerprintPinningAdapter, TlsFingerprintStore]:
        store = TlsFingerprintStore(tmp_path / "tls.json", _fetcher())
        return FingerprintPinningAdapter(store), store

    def test_sets_assert_fingerprint_for_https_default_port(self, tmp_path: Path) -> None:
        adapter, _ = self._adapter(tmp_path)
        req = requests.Request("GET", "https://cluster.example/api").prepare()
        host_params, tls_params = adapter.build_connection_pool_key_attributes(req, False)
        assert host_params["host"] == "cluster.example"
        assert tls_params["assert_fingerprint"] == hashlib.sha256(DER_A).hexdigest()
        assert tls_params["cert_reqs"] == "CERT_NONE"

    def test_uses_explicit_port(self, tmp_path: Path) -> None:
        adapter, store = self._adapter(tmp_path)
        req = requests.Request("GET", "https://cluster.example:8443/api").prepare()
        adapter.build_connection_pool_key_attributes(req, False)
        assert "cluster.example:8443" in json.loads(store.path.read_text())["hosts"]

    def test_http_requests_are_not_pinned(self, tmp_path: Path) -> None:
        adapter, store = self._adapter(tmp_path)
        req = requests.Request("GET", "http://cluster.example/api").prepare()
        _, tls_params = adapter.build_connection_pool_key_attributes(req, False)
        assert "assert_fingerprint" not in tls_params
        assert not store.path.exists()

    @pytest.mark.parametrize(
        ("failure", "expected"),
        [
            (ConnectionRefusedError("refused"), requests.exceptions.ConnectionError),
            (socket.gaierror("no such host"), requests.exceptions.ConnectionError),
            (ssl.SSLError("handshake failed"), requests.exceptions.ConnectionError),
            (TimeoutError("timed out"), requests.exceptions.ConnectTimeout),
        ],
    )
    def test_capture_failure_maps_to_requests_exception(
        self, tmp_path: Path, failure: OSError, expected: type[requests.exceptions.RequestException]
    ) -> None:
        store = TlsFingerprintStore(tmp_path / "tls.json", MagicMock(side_effect=failure))
        session = requests.Session()
        session.mount("https://", FingerprintPinningAdapter(store))
        # The fetcher raises before any connection is attempted, so no socket is opened.
        with pytest.raises(expected) as exc_info:
            session.get("https://10.255.255.1/api", verify=False)
        assert exc_info.value.__cause__ is failure
        assert exc_info.value.request is not None
        assert not store.path.exists()

    def test_request_exceptions_and_corrupt_records_are_not_remapped(self, tmp_path: Path) -> None:
        adapter = FingerprintPinningAdapter(
            TlsFingerprintStore(
                tmp_path / "tls.json",
                MagicMock(side_effect=requests.exceptions.ProxyError("proxy")),
            )
        )
        req = requests.Request("GET", "https://cluster.example/api").prepare()
        with pytest.raises(requests.exceptions.ProxyError):
            adapter.build_connection_pool_key_attributes(req, False)
        (tmp_path / "bad.json").write_text("{nope")
        corrupt = FingerprintPinningAdapter(TlsFingerprintStore(tmp_path / "bad.json", _fetcher()))
        with pytest.raises(ValueError, match="Cannot read"):
            corrupt.build_connection_pool_key_attributes(req, False)

    def _mismatch_error(self) -> requests.exceptions.SSLError:
        try:
            assert_fingerprint(DER_B, hashlib.sha256(DER_A).hexdigest())
        except Urllib3SSLError as exc:
            return requests.exceptions.SSLError(MaxRetryError(None, "/x", reason=exc))  # type: ignore[arg-type]
        raise AssertionError("urllib3 did not reject the mismatch")

    def test_mismatch_maps_to_identity_error_not_connection_error(self, tmp_path: Path) -> None:
        adapter, store = self._adapter(tmp_path)
        req = requests.Request("GET", "https://cluster.example:8443/api").prepare()
        with (
            patch.object(HTTPAdapter, "send", side_effect=self._mismatch_error()),
            pytest.raises(HostIdentityChangedError) as exc_info,
        ):
            adapter.send(req)
        assert not isinstance(exc_info.value, requests.exceptions.ConnectionError)
        assert "cluster.example:8443" in str(exc_info.value)
        assert str(store.path) in str(exc_info.value)

    def test_other_ssl_errors_pass_through(self, tmp_path: Path) -> None:
        adapter, _ = self._adapter(tmp_path)
        req = requests.Request("GET", "https://cluster.example/api").prepare()
        err = requests.exceptions.SSLError("handshake failure")
        with (
            patch.object(HTTPAdapter, "send", side_effect=err),
            pytest.raises(requests.exceptions.SSLError) as exc_info,
        ):
            adapter.send(req)
        assert exc_info.value is err

    def test_successful_send_returns_response(self, tmp_path: Path) -> None:
        adapter, _ = self._adapter(tmp_path)
        req = requests.Request("GET", "https://cluster.example/api").prepare()
        response = requests.Response()
        with patch.object(HTTPAdapter, "send", return_value=response):
            assert adapter.send(req) is response


class TestHelpers:
    """Locking, atomic writes and the combined store."""

    def test_lock_for_shares_one_lock_per_path(self, tmp_path: Path) -> None:
        assert _lock_for(tmp_path / "f") is _lock_for(tmp_path / "sub" / ".." / "f")
        assert _lock_for(tmp_path / "f") is not _lock_for(tmp_path / "g")

    def test_atomic_write_cleans_temp_on_failure(self, tmp_path: Path) -> None:
        with (
            patch("pynetappfoundry.clients.trust.os.replace", side_effect=OSError("boom")),
            pytest.raises(OSError, match="boom"),
        ):
            _atomic_write(tmp_path / "f", "data")
        assert list(tmp_path.iterdir()) == []

    def test_host_trust_store_layout_creates_nothing(self, tmp_path: Path) -> None:
        store = HostTrustStore(tmp_path / ".trust")
        assert store.ssh.path == tmp_path / ".trust" / "known_hosts"
        assert store.tls.path == tmp_path / ".trust" / "tls_fingerprints.json"
        assert not (tmp_path / ".trust").exists()
