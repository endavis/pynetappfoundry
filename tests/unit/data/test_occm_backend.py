"""Unit tests for OccmBackend (Console agent). No network: the client is patched."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cache.occm.onprem_working_environments.mapping import (
    EXPLICIT_FETCH_FIELDS,
)
from pynetappfoundry.cache.occm.onprem_working_environments.mapping import (
    OCCMONPREMWORKINGENVIRONMENT_MAPPING as MAPPING,
)
from pynetappfoundry.clients.console.generated import ConsoleAgentOps
from pynetappfoundry.data._routing import RoutingDecision
from pynetappfoundry.data.occm_backend import _OPS, OccmBackend
from pynetappfoundry.data.source import _BACKENDS
from pynetappfoundry.models.console.cvo.get_onprem_working_environments import (
    OnPremClusterProperties,
    ResponseBody,
)

_CLIENT_PATH = "pynetappfoundry.clients.console.agent.ConsoleAgentClient"
_LIVE = RoutingDecision(cache_fields=(), live_fields=("name", "publicId"))


def _config(connectors: dict[str, Any] | None = None) -> MagicMock:
    config = MagicMock()
    config.data = {"connectors": connectors} if connectors is not None else {}
    return config


def _env(public_id: str, **kwargs: Any) -> ResponseBody:
    return ResponseBody(publicId=public_id, name=f"n-{public_id}", **kwargs)


@pytest.fixture
def client_cls() -> Iterator[MagicMock]:
    with patch(_CLIENT_PATH) as cls:
        cls.return_value.ops.list_onprem_working_environments.return_value = []
        yield cls


def _op(client_cls: MagicMock) -> MagicMock:
    op: MagicMock = client_cls.return_value.ops.list_onprem_working_environments
    return op


def test_registered_backend() -> None:
    assert _BACKENDS["occm"] is OccmBackend
    assert OccmBackend.live_only is False
    assert OccmBackend.is_live_only(MAPPING) is False
    assert MAPPING.api_type == "occm"


def test_connector_with_agent_id(client_cls: MagicMock) -> None:
    backend = OccmBackend(_config({"c1": {"agent_id": "agent-1"}}))
    backend.query(ResponseBody, MAPPING, _LIVE, "c1", {})
    assert client_cls.call_args.args[1] == "agent-1"


def test_unknown_name_is_agent_id(client_cls: MagicMock) -> None:
    backend = OccmBackend(_config({"c1": {"agent_id": "agent-1"}}))
    backend.query(ResponseBody, MAPPING, _LIVE, "raw-agent", {})
    assert client_cls.call_args.args[1] == "raw-agent"


@pytest.mark.parametrize("entry", [{}, {"agent_id": ""}, {"agent_id": "  "}, "text"])
def test_connector_without_agent_id(client_cls: MagicMock, entry: Any) -> None:
    backend = OccmBackend(_config({"c1": entry}))
    with pytest.raises(ValueError, match=r"connectors\.c1"):
        backend.query(ResponseBody, MAPPING, _LIVE, "c1", {})
    client_cls.assert_not_called()


def test_client_cached_per_agent(client_cls: MagicMock) -> None:
    backend = OccmBackend(_config())
    backend.query(ResponseBody, MAPPING, _LIVE, "a1", {})
    backend.query(ResponseBody, MAPPING, _LIVE, "a1", {})
    backend.query(ResponseBody, MAPPING, _LIVE, "a2", {})
    assert client_cls.call_count == 2


def test_default_query_has_no_fields(client_cls: MagicMock) -> None:
    items = [_env("p1"), _env("p2")]
    _op(client_cls).return_value = items
    result = OccmBackend(_config()).query(ResponseBody, MAPPING, _LIVE, "a1", {})
    assert result == items
    _op(client_cls).assert_called_once_with()


def test_fields_csv_for_explicit_fields(client_cls: MagicMock) -> None:
    decision = RoutingDecision(cache_fields=(), live_fields=("svms", "name", "status"))
    OccmBackend(_config()).query(ResponseBody, MAPPING, decision, "a1", {})
    _op(client_cls).assert_called_once_with(fields="status,svms")


def test_dotted_filter_adds_fields_and_filters(client_cls: MagicMock) -> None:
    match = _env("p1", ontapClusterProperties=OnPremClusterProperties(clusterUuid="u1"))
    other = _env("p2", ontapClusterProperties=OnPremClusterProperties(clusterUuid="u2"))
    _op(client_cls).return_value = [match, other]
    result = OccmBackend(_config()).query(
        ResponseBody, MAPPING, _LIVE, "a1", {"ontapClusterProperties.clusterUuid": "u1"}
    )
    assert result == [match]
    _op(client_cls).assert_called_once_with(fields="ontapClusterProperties")


def test_tenant_filter_in_memory_only(client_cls: MagicMock) -> None:
    keep = _env("p1", tenantId="t1")
    drop = _env("p2", tenantId="t2")
    _op(client_cls).return_value = [keep, drop]
    result = OccmBackend(_config()).query(ResponseBody, MAPPING, _LIVE, "a1", {"tenantId": "t1"})
    assert result == [keep]
    assert "tenant_id" not in _op(client_cls).call_args.kwargs


def test_missing_path_excludes_item(client_cls: MagicMock) -> None:
    _op(client_cls).return_value = [_env("p1")]
    result = OccmBackend(_config()).query(
        ResponseBody, MAPPING, _LIVE, "a1", {"ontapClusterProperties.clusterUuid": "u1"}
    )
    assert result == []


def test_cache_only_decision_reads_cache(client_cls: MagicMock, tmp_path: Path) -> None:
    from pynetappfoundry.cache.occm_db import OccmCacheDB

    decision = RoutingDecision(cache_fields=("name",), live_fields=())
    with (
        OccmCacheDB(db_path=tmp_path / "occm_cache.db") as db,
        patch.object(OccmBackend, "_cache_db", db),
    ):
        assert OccmBackend(_config()).query(ResponseBody, MAPPING, decision, "a1", {}) == []
    client_cls.assert_not_called()


def test_where_expressions_rejected(client_cls: MagicMock) -> None:
    with pytest.raises(NotImplementedError, match="where_expressions"):
        OccmBackend(_config()).query(
            ResponseBody, MAPPING, _LIVE, "a1", {}, where_expressions=("name = 'x'",)
        )


def test_path_params_rejected(client_cls: MagicMock) -> None:
    with pytest.raises(ValueError, match="path_params"):
        OccmBackend(_config()).query(ResponseBody, MAPPING, _LIVE, "a1", {}, path_params={"x": "y"})


def test_no_live_fields_returns_empty(client_cls: MagicMock) -> None:
    decision = RoutingDecision(cache_fields=(), live_fields=())
    assert OccmBackend(_config()).query(ResponseBody, MAPPING, decision, "a1", {}) == []
    client_cls.assert_not_called()


def test_endpoint_without_op_builds_no_client(client_cls: MagicMock) -> None:
    mapping = MAPPING.__class__(
        name="Other",
        model_class=ResponseBody,
        api_endpoint="/occm/api/other",
        api_type="occm",
        fields=MAPPING.fields,
    )
    with pytest.raises(NotImplementedError, match="/occm/api/other"):
        OccmBackend(_config()).query(ResponseBody, mapping, _LIVE, "a1", {})
    client_cls.assert_not_called()


def test_wrong_item_class_raises(client_cls: MagicMock) -> None:
    _op(client_cls).return_value = [{"publicId": "p1"}]
    with pytest.raises(TypeError, match="expected ResponseBody"):
        OccmBackend(_config()).query(ResponseBody, MAPPING, _LIVE, "a1", {})


def test_every_ops_entry_exists_on_agent_ops() -> None:
    from pynetappfoundry.cache._registry import model_registry

    model_registry.get_mapping_by_model_class(ResponseBody)
    for name in _OPS.values():
        assert callable(getattr(ConsoleAgentOps, name))
    assert MAPPING.api_endpoint in _OPS


def test_mapping_matches_model_and_measured_fields() -> None:
    assert [f.cache_attr for f in MAPPING.fields] == list(ResponseBody.model_fields)
    assert set(MAPPING.explicit_fetch_fields()) == set(EXPLICIT_FETCH_FIELDS)
    assert len(EXPLICIT_FETCH_FIELDS) == 15
