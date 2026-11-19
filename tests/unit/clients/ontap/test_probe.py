"""Tests for the shared ONTAP probe."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.clients.ontap.probe import ClusterProbe, probe_cluster

DETAILS: dict[str, Any] = {"ip": "192.0.2.10"}


def _factory(response: Any) -> MagicMock:
    client = MagicMock()
    client.call_endpoint.return_value = response
    return MagicMock(return_value=client)


def test_name_match() -> None:
    factory = _factory({"name": "c1"})
    config = MagicMock()
    probe = probe_cluster("c1", DETAILS, config, client_factory=factory)
    assert isinstance(probe, ClusterProbe)
    assert probe.cluster_name == "c1"
    assert probe.name_matches is True
    assert probe.client is factory.return_value
    call_endpoint: Any = factory.return_value.call_endpoint
    call_endpoint.assert_called_once_with("/cluster")
    assert factory.call_args.kwargs["config"] is config
    assert factory.call_args.kwargs["cluster"].ip == "192.0.2.10"


def test_name_mismatch() -> None:
    probe = probe_cluster("c1", DETAILS, MagicMock(), client_factory=_factory({"name": "other"}))
    assert probe.cluster_name == "other"
    assert probe.name_matches is False


def test_non_dict_response_has_empty_name() -> None:
    probe = probe_cluster("c1", DETAILS, MagicMock(), client_factory=_factory(None))
    assert probe.cluster_name == ""
    assert probe.name_matches is False


def test_exception_propagates() -> None:
    factory = _factory({})
    factory.return_value.call_endpoint.side_effect = ConnectionError("down")
    with pytest.raises(ConnectionError):
        probe_cluster("c1", DETAILS, MagicMock(), client_factory=factory)


def test_default_factory_is_ontap_client() -> None:
    with patch("pynetappfoundry.clients.ontap.probe.ONTAPAPIClient") as cls:
        cls.return_value.call_endpoint.return_value = {"name": "c1"}
        probe = probe_cluster("c1", DETAILS, MagicMock())
    assert probe.client is cls.return_value
    cls.assert_called_once()
