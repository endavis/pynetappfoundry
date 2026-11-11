"""Unit tests for the ONTAP API client's host identity pinning."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
from pynetappfoundry.clients.trust import FingerprintPinningAdapter, HostTrustStore


def test_api_client_mounts_pinning_adapter(tmp_path: Path) -> None:
    schema_dir = tmp_path / "ontap"
    schema_dir.mkdir()
    (schema_dir / "all.json").write_text(json.dumps({"basePath": "/api", "paths": {}}))
    store = HostTrustStore(tmp_path / ".trust", lambda host, port: b"der")
    config = MagicMock()
    config.get_user.return_value = ("admin", "secret")
    config.get_schema_location.return_value = schema_dir
    config.get_trust_store.return_value = store
    config.get_ontap_api_settings.return_value = MagicMock(base_api_path="/api", timeout=5.0)
    cluster = MagicMock()
    cluster.name = "c1"
    cluster.ip = "10.0.0.1"

    client = ONTAPAPIClient(cluster=cluster, config=config)

    adapter = client.session.get_adapter("https://10.0.0.1")
    assert isinstance(adapter, FingerprintPinningAdapter)
    assert client.verify_ssl is False
