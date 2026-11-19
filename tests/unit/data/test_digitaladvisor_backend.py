"""Unit tests for DigitalAdvisorBackend. No network: the session is a fake (placeholders only)."""

from __future__ import annotations

import re
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.clients.digitaladvisor.api import (
    DigitalAdvisorAPIClient,
    RateLimiter,
    ensure_read_only,
)
from pynetappfoundry.clients.digitaladvisor.auth import (
    DigitalAdvisorQueryError,
    StaticTokenProvider,
)
from pynetappfoundry.core.models import DigitalAdvisorAPISettings
from pynetappfoundry.data._routing import RoutingDecision
from pynetappfoundry.data.digitaladvisor_backend import (
    _SPECS,
    PERSONAL_DATA_FIELDS,
    DigitalAdvisorBackend,
    build_document,
    selection_set,
)
from pynetappfoundry.data.source import _BACKENDS, DataSource
from pynetappfoundry.models.digitaladvisor import (
    DigitalAdvisorCluster,
    DigitalAdvisorSystem,
    DigitalAdvisorVolume,
)
from pynetappfoundry.models.digitaladvisor.system import DigitalAdvisorSite
from tests.unit.clients.digitaladvisor.helpers import gql, response, session_with

_MODELS: dict[str, type[BaseModel]] = {
    "clusters": DigitalAdvisorCluster,
    "systems": DigitalAdvisorSystem,
    "volumes": DigitalAdvisorVolume,
}


def _client(session: MagicMock) -> DigitalAdvisorAPIClient:
    return DigitalAdvisorAPIClient(
        settings=DigitalAdvisorAPISettings(personal_access_token="placeholder"),  # type: ignore[arg-type]  # str is coerced to SecretStr
        token_provider=StaticTokenProvider("placeholder"),
        session=session,
        rate_limiter=RateLimiter(sleep=lambda s: None),
        sleep=lambda s: None,
    )


@contextmanager
def _source(*outcomes: Any) -> Iterator[tuple[DataSource, MagicMock]]:
    session = session_with(*outcomes)
    with patch.object(DigitalAdvisorBackend, "_get_api_client", return_value=_client(session)):
        yield DataSource(MagicMock()), session


def _sent(session: MagicMock, index: int = 0) -> dict[str, Any]:
    body: dict[str, Any] = session.post.call_args_list[index].kwargs["json"]
    return body


def test_registered_and_live_only() -> None:
    assert _BACKENDS["digitaladvisor"] is DigitalAdvisorBackend
    assert DigitalAdvisorBackend.live_only is True
    for name in ("DigitalAdvisorCluster", "DigitalAdvisorSystem", "DigitalAdvisorVolume"):
        mapping = model_registry.get_mapping(name)
        assert mapping is not None
        assert mapping.api_type == "digitaladvisor"


def test_cache_source_rejected_and_auto_goes_live() -> None:
    with _source(gql({"systems": {"cursor": "c", "systems": []}})) as (ds, session):
        with pytest.raises(ValueError, match="cache"):
            list(ds.query(DigitalAdvisorSystem, cluster="x", source="cache"))
        assert session.post.call_count == 0
        assert list(ds.query(DigitalAdvisorSystem, cluster="x", source="auto")) == []
        assert session.post.call_count == 1


def test_systems_defaults_and_overrides() -> None:
    empty = gql({"systems": {"cursor": "c", "systems": []}})
    with _source(empty, empty) as (ds, session):
        list(ds.query(DigitalAdvisorSystem, cluster="x"))
        list(
            ds.query(DigitalAdvisorSystem, cluster="x").filter(
                systemStates=["ACTIVE", "INACTIVE"], includeAllStates=True, clusterId="c1"
            )
        )
    first, second = _sent(session, 0), _sent(session, 1)
    assert first["variables"] == {
        "productTypes": ["FILER"],
        "systemStates": ["ACTIVE"],
        "includeAllStates": False,
        "includeStorageGridNodes": False,
        "pageSize": 100,
    }
    for decl in (
        "$productTypes: [ProductType!]!",
        "$systemStates: [SystemState!]!",
        "$includeAllStates: Boolean!",
        "$includeStorageGridNodes: Boolean!",
    ):
        assert decl in first["query"]
    assert "$clusterId" not in first["query"]
    assert second["variables"]["systemStates"] == ["ACTIVE", "INACTIVE"]
    assert second["variables"]["includeAllStates"] is True
    assert second["variables"]["clusterId"] == "c1"
    assert "$clusterId: String" in second["query"]
    assert "clusterId: $clusterId" in second["query"]


def test_total_count_only_on_systems_and_volumes() -> None:
    docs = {
        key: build_document(spec, selection_set(_MODELS[key]), []) for key, spec in _SPECS.items()
    }
    assert "totalCount" in docs["systems"].split("cursor")[0]
    assert "totalCount" in docs["volumes"].split("cursor")[0]
    assert "totalCount" not in docs["clusters"].split("cursor")[0]


def test_generated_documents_are_read_only() -> None:
    for key, spec in _SPECS.items():
        ensure_read_only(build_document(spec, selection_set(_MODELS[key]), list(spec.optional)))


def test_documents_never_select_personal_data() -> None:
    for key, spec in _SPECS.items():
        document = build_document(spec, selection_set(_MODELS[key]), list(spec.optional))
        assert not set(re.findall(r"\w+", document)) & PERSONAL_DATA_FIELDS


def test_selection_set_refuses_personal_data() -> None:
    from pynetappfoundry.models._base import OntapModel

    class _Bad(OntapModel):
        contactPerson: str | None = None  # noqa: N815  # a GraphQL field name

    with pytest.raises(ValueError, match="personal data"):
        selection_set(_Bad)


def test_selection_set_refuses_personal_data_in_nested_model() -> None:
    from pynetappfoundry.models._base import OntapModel

    class _Address(OntapModel):
        postalCode: str | None = None  # noqa: N815  # a GraphQL field name

    class _Outer(OntapModel):
        id: str | None = None
        site: _Address | None = None

    with pytest.raises(ValueError, match="postalCode"):
        selection_set(_Outer)


def test_selection_set_nests_models() -> None:
    selection = selection_set(DigitalAdvisorSite)
    assert selection == "id cmatId name countryCode city state"
    assert "site { id cmatId" in selection_set(DigitalAdvisorSystem)


def test_argument_allowlists_disjoint_from_model_fields() -> None:
    for key, spec in _SPECS.items():
        names = set(spec.required) | set(spec.optional)
        assert not names & set(_MODELS[key].model_fields), key


def test_two_pages_systems() -> None:
    page1 = gql(
        {
            "systems": {
                "totalCount": 3,
                "cursor": "c1",
                "systems": [{"serialNumber": "SN-1"}, {"serialNumber": "SN-2"}],
            }
        }
    )
    page2 = gql(
        {"systems": {"totalCount": 3, "cursor": "c2", "systems": [{"serialNumber": "SN-3"}]}}
    )
    with _source(page1, page2) as (ds, session):
        found = list(ds.query(DigitalAdvisorSystem, cluster="x"))
    assert [s.serialNumber for s in found] == ["SN-1", "SN-2", "SN-3"]
    assert "after" not in _sent(session, 0)["variables"]
    assert _sent(session, 1)["variables"]["after"] == "c1"


def test_clusters_stop_on_empty_page() -> None:
    page1 = gql({"clusters": {"cursor": "c1", "clusters": [{"id": "c-1", "name": "n-1"}]}})
    page2 = gql({"clusters": {"cursor": "c2", "clusters": []}})
    with _source(page1, page2) as (ds, session):
        found = list(ds.query(DigitalAdvisorCluster, cluster="x"))
    assert [c.id for c in found] == [
        "c-1",
    ]
    assert session.post.call_count == 2
    assert "totalCount" not in _sent(session, 0)["query"].split("cursor")[0]


def test_in_memory_filter_on_nested_path() -> None:
    body = gql(
        {
            "systems": {
                "cursor": "",
                "systems": [
                    {"serialNumber": "SN-1", "site": {"city": "Placeholder City"}},
                    {"serialNumber": "SN-2", "site": {"city": "Other City"}},
                    {"serialNumber": "SN-3"},
                ],
            }
        }
    )
    with _source(body) as (ds, session):
        found = list(
            ds.query(DigitalAdvisorSystem, cluster="x").filter({"site.city": "Placeholder City"})
        )
    assert [s.serialNumber for s in found] == ["SN-1"]
    assert "site {" in _sent(session)["query"]


def test_get_by_id_filters_in_memory() -> None:
    body = {"volumes": {"cursor": "", "volumes": [{"id": "vol-1"}, {"id": "vol-2"}]}}
    with _source(gql(body), gql(body)) as (ds, _session):
        hit = ds.get(DigitalAdvisorVolume, cluster="x", id="vol-1")
        miss = ds.get(DigitalAdvisorVolume, cluster="x", id="vol-9")
    assert hit is not None
    assert hit.id == "vol-1"
    assert miss is None


def test_unknown_filter_raises_before_request() -> None:
    with _source() as (ds, session):
        with pytest.raises(ValueError, match="unknown filter 'clustrId'"):
            list(ds.query(DigitalAdvisorSystem, cluster="x").filter(clustrId="c1"))
        assert session.post.call_count == 0


def test_fields_narrow_selection() -> None:
    body = gql({"systems": {"cursor": "", "systems": [{"hostName": "h1", "serialNumber": "SN-1"}]}})
    with _source(body) as (ds, session):
        found = list(ds.query(DigitalAdvisorSystem, cluster="x").fields("hostName"))
    query = _sent(session)["query"]
    assert "systems { serialNumber hostName }" in query
    assert "site" not in query
    assert found[0].was_fetched("hostName")
    assert found[0]._fetched_fields == {"hostName"}


def test_fields_plus_in_memory_filter_key_are_selected() -> None:
    body = gql({"systems": {"cursor": "", "systems": []}})
    with _source(body) as (ds, session):
        list(
            ds.query(DigitalAdvisorSystem, cluster="x")
            .fields("hostName")
            .filter({"site.city": "Placeholder City"})
        )
    assert "systems { serialNumber hostName site { " in _sent(session)["query"]


def test_unsupported_options() -> None:
    backend = DigitalAdvisorBackend(MagicMock())
    mapping = model_registry.get_mapping("DigitalAdvisorSystem")
    assert mapping is not None
    live = RoutingDecision(cache_fields=(), live_fields=("serialNumber",))
    with pytest.raises(NotImplementedError):
        backend.query(DigitalAdvisorSystem, mapping, live, "x", {}, where_expressions=("a > 1",))
    with pytest.raises(ValueError, match="path_params"):
        backend.query(DigitalAdvisorSystem, mapping, live, "x", {}, path_params={"a": 1})
    cache_only = RoutingDecision(cache_fields=("serialNumber",), live_fields=())
    with pytest.raises(NotImplementedError):
        backend.query(DigitalAdvisorSystem, mapping, cache_only, "x", {})
    none = RoutingDecision(cache_fields=(), live_fields=())
    assert backend.query(DigitalAdvisorSystem, mapping, none, "x", {}) == []
    assert DigitalAdvisorBackend.supports_where_expressions is False
    assert DigitalAdvisorBackend.supports_path_params is False
    assert DigitalAdvisorBackend.supports_parent_filters is False


def test_where_raises_at_chain_time() -> None:
    with _source() as (ds, _session), pytest.raises(ValueError):
        ds.query(DigitalAdvisorSystem, cluster="x").where("ageInYears > 3")


def test_client_error_propagates() -> None:
    with (
        _source(response(400, {"errors": [{"message": "bad"}]})) as (ds, _session),
        pytest.raises(DigitalAdvisorQueryError),
    ):
        list(ds.query(DigitalAdvisorVolume, cluster="x"))


def test_api_client_is_lazy_and_cached() -> None:
    backend = DigitalAdvisorBackend(MagicMock())
    with patch("pynetappfoundry.clients.digitaladvisor.api.DigitalAdvisorAPIClient") as cls:
        first = backend._get_api_client()
        second = backend._get_api_client()
    assert first is second
    cls.assert_called_once()
