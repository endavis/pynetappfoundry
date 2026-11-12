"""Tests for pynetappfoundry.data.dii_backend.DiiBackend.

DiiBackend is live-only; no cache DB or network is touched -- all
API clients are mocked.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Iterator
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.data._routing import RoutingDecision
from pynetappfoundry.data.dii_backend import DiiBackend
from pynetappfoundry.models._base import OntapModel

# ---------------------------------------------------------------------------
# Fake DII model & mapping
# ---------------------------------------------------------------------------


class FakeDiiAsset(OntapModel):
    """Synthetic DII model for backend tests."""

    id: int = 0
    name: str = ""
    vendor: str = ""


@pytest.fixture
def fake_dii_mapping() -> Iterator[TypeMapping]:
    """Register a synthetic DII mapping for the duration of one test."""
    mapping = TypeMapping(
        name="FakeDiiAsset",
        model_class=FakeDiiAsset,
        api_endpoint="/assets/storages",
        api_type="dii",
        identifier_field="id",
        records_path="",
        fields=(
            FieldMapping(cache_attr="id", default=0),
            FieldMapping(cache_attr="name"),
            FieldMapping(cache_attr="vendor"),
        ),
    )
    model_registry.register_mapping("FakeDiiAsset", mapping)
    try:
        yield mapping
    finally:
        model_registry._mappings.pop("FakeDiiAsset", None)
        model_registry._mappings_by_class.pop(FakeDiiAsset, None)


@pytest.fixture
def items_mapping(fake_dii_mapping: TypeMapping) -> TypeMapping:
    """The fake mapping with ``records_path="items"`` (same registration)."""
    return dataclasses.replace(fake_dii_mapping, records_path="items")


@pytest.fixture
def mock_config() -> Any:
    """A bare MagicMock standing in for :class:`Config`."""
    return MagicMock(name="Config")


def _make_backend(config: Any) -> DiiBackend:
    return DiiBackend(config)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestDiiBackendQuery:
    """Core query path tests for DiiBackend."""

    def test_live_query_bare_array_response(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Bare-array DII response is parsed into model instances."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("id", "name", "vendor"))

        mock_client = MagicMock()
        mock_client.get_all_pages.return_value = [
            {"id": 1, "name": "stor1", "vendor": "NetApp"},
            {"id": 2, "name": "stor2", "vendor": "NetApp"},
        ]

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            results = backend.query(
                FakeDiiAsset,
                fake_dii_mapping,
                decision,
                cluster="tenant1",
                filters={},
            )

        assert len(results) == 2
        assert results[0].id == 1
        assert results[0].name == "stor1"
        assert results[1].id == 2

    def test_empty_response_returns_empty_list(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Empty list response produces no results."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("id",))

        mock_client = MagicMock()
        mock_client.get_all_pages.return_value = []

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            results = backend.query(
                FakeDiiAsset,
                fake_dii_mapping,
                decision,
                cluster="tenant1",
                filters={},
            )

        assert results == []

    def test_none_response_returns_empty_list(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """None response is handled gracefully."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("id",))

        mock_client = MagicMock()
        mock_client.get_all_pages.return_value = None

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            results = backend.query(
                FakeDiiAsset,
                fake_dii_mapping,
                decision,
                cluster="tenant1",
                filters={},
            )

        assert results == []

    def test_filters_translate_to_query_params(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Dict filters are passed as query_params to get_all_pages."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("id", "name"))

        mock_client = MagicMock()
        mock_client.get_all_pages.return_value = []

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            backend.query(
                FakeDiiAsset,
                fake_dii_mapping,
                decision,
                cluster="tenant1",
                filters={"vendor": "NetApp", "name": "stor1"},
            )

        mock_client.get_all_pages.assert_called_once_with(
            "/assets/storages",
            query_params={"vendor": "NetApp", "name": "stor1"},
        )

    def test_fetched_fields_stamped_on_instances(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Returned instances have _fetched_fields populated."""
        backend = _make_backend(mock_config)
        live_fields = ("id", "name", "vendor")
        decision = RoutingDecision(cache_fields=(), live_fields=live_fields)

        mock_client = MagicMock()
        mock_client.get_all_pages.return_value = [
            {"id": 1, "name": "stor1", "vendor": "NetApp"},
        ]

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            results = backend.query(
                FakeDiiAsset,
                fake_dii_mapping,
                decision,
                cluster="tenant1",
                filters={},
            )

        assert len(results) == 1
        for field in live_fields:
            assert results[0].was_fetched(field)

    def test_records_list_from_envelope_paging(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """get_all_pages returning an envelope's records list is parsed."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("id", "name"))
        mock_client = MagicMock()
        mock_client.get_all_pages.return_value = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            results = backend.query(FakeDiiAsset, fake_dii_mapping, decision, "t", {})

        assert [r.id for r in results] == [1, 2]

    def test_raw_envelope_dict_is_parsed_without_warning(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """The explicit offset/limit path returns a raw envelope; records are parsed."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("id", "name"))
        mock_client = MagicMock()
        mock_client.get_all_pages.return_value = {
            "offset": 0,
            "count": 2,
            "limit": 10,
            "rows": [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}],
        }

        with (
            caplog.at_level("WARNING"),
            patch.object(backend, "_get_api_client", return_value=mock_client),
        ):
            results = backend.query(FakeDiiAsset, fake_dii_mapping, decision, "t", {"limit": 10})

        assert [r.id for r in results] == [1, 2]
        assert "unexpected response type" not in caplog.text

    def test_non_envelope_dict_warns_and_returns_empty(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """A dict that is not an envelope still warns and yields no results."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("id",))
        mock_client = MagicMock()
        mock_client.get_all_pages.return_value = {"results": [{"id": 1}]}

        with (
            caplog.at_level("WARNING"),
            patch.object(backend, "_get_api_client", return_value=mock_client),
        ):
            results = backend.query(FakeDiiAsset, fake_dii_mapping, decision, "t", {})

        assert results == []
        assert "unexpected response type" in caplog.text


def _query_with(mapping: TypeMapping, response: Any, config: Any) -> list[FakeDiiAsset]:
    backend = _make_backend(config)
    decision = RoutingDecision(cache_fields=(), live_fields=("id", "name"))
    mock_client = MagicMock()
    mock_client.get_all_pages.return_value = response
    with patch.object(backend, "_get_api_client", return_value=mock_client):
        return backend.query(FakeDiiAsset, mapping, decision, "t", {})


class TestDiiBackendRecordsPath:
    """A non-empty ``records_path`` is honoured on dict responses (#918)."""

    def test_records_path_dict_parsed(
        self, items_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        with caplog.at_level("WARNING"):
            results = _query_with(
                items_mapping,
                {"items": [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}]},
                mock_config,
            )
        assert [r.id for r in results] == [1, 2]
        assert "unexpected response type" not in caplog.text
        assert "id" in results[0]._fetched_fields

    def test_dotted_records_path(self, fake_dii_mapping: TypeMapping, mock_config: Any) -> None:
        mapping = dataclasses.replace(fake_dii_mapping, records_path="data.items")
        results = _query_with(mapping, {"data": {"items": [{"id": 7, "name": "x"}]}}, mock_config)
        assert [r.id for r in results] == [7]

    def test_missing_path_warns_and_returns_empty(
        self, items_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        with caplog.at_level("WARNING"):
            results = _query_with(items_mapping, {"other": []}, mock_config)
        assert results == []
        assert "items" in caplog.text
        assert "not found" in caplog.text

    def test_non_list_value_warns_and_returns_empty(
        self, items_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        with caplog.at_level("WARNING"):
            results = _query_with(items_mapping, {"items": {"id": 1}}, mock_config)
        assert results == []
        assert "expected list" in caplog.text

    def test_bare_list_wins_over_records_path(
        self, items_mapping: TypeMapping, mock_config: Any
    ) -> None:
        results = _query_with(items_mapping, [{"id": 3, "name": "c"}], mock_config)
        assert [r.id for r in results] == [3]

    def test_records_path_wins_over_envelope(
        self, items_mapping: TypeMapping, mock_config: Any
    ) -> None:
        response = {
            "offset": 0,
            "count": 1,
            "rows": [{"id": 1, "name": "row"}],
            "items": [{"id": 2, "name": "item"}],
        }
        results = _query_with(items_mapping, response, mock_config)
        assert [r.id for r in results] == [2]

    def test_singleton_wraps_dict_as_single_record(
        self, fake_dii_mapping: TypeMapping, mock_config: Any
    ) -> None:
        mapping = dataclasses.replace(fake_dii_mapping, response_shape="singleton")
        results = _query_with(mapping, {"id": 5, "name": "solo"}, mock_config)
        assert [(r.id, r.name) for r in results] == [(5, "solo")]
        assert "id" in results[0]._fetched_fields

    def test_singleton_wins_over_envelope_sniffing(
        self, fake_dii_mapping: TypeMapping, mock_config: Any
    ) -> None:
        mapping = dataclasses.replace(fake_dii_mapping, response_shape="singleton")
        results = _query_with(mapping, {"id": 5, "rows": [{"id": 9}]}, mock_config)
        assert [r.id for r in results] == [5]

    def test_singleton_keeps_list_as_list(
        self, fake_dii_mapping: TypeMapping, mock_config: Any
    ) -> None:
        mapping = dataclasses.replace(fake_dii_mapping, response_shape="singleton")
        results = _query_with(mapping, [{"id": 1}, {"id": 2}], mock_config)
        assert [r.id for r in results] == [1, 2]

    def test_empty_path_still_sniffs_envelope(
        self, fake_dii_mapping: TypeMapping, mock_config: Any
    ) -> None:
        results = _query_with(
            fake_dii_mapping,
            {"offset": 0, "count": 1, "rows": [{"id": 4}]},
            mock_config,
        )
        assert [r.id for r in results] == [4]

    def test_singleton_default_records_path_still_wraps(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Guards branch order: default ``records_path="records"`` must not win."""
        mapping = dataclasses.replace(
            fake_dii_mapping, records_path="records", response_shape="singleton"
        )
        with caplog.at_level("WARNING"):
            results = _query_with(mapping, {"id": 5, "name": "solo"}, mock_config)
        assert [(r.id, r.name) for r in results] == [(5, "solo")]
        assert "unexpected response type" not in caplog.text
        assert "not found" not in caplog.text

    def test_singleton_none_response_is_empty(
        self, fake_dii_mapping: TypeMapping, mock_config: Any
    ) -> None:
        mapping = dataclasses.replace(fake_dii_mapping, response_shape="singleton")
        assert _query_with(mapping, None, mock_config) == []

    def test_real_installcommand_mapping(self, mock_config: Any) -> None:
        from pynetappfoundry.cache.dii.au.installCommand.mapping import (
            DIIAUINSTALLCOMMAND_MAPPING,
        )
        from pynetappfoundry.models.dii.au.installCommand.model import DiiAuInstallcommand

        assert DIIAUINSTALLCOMMAND_MAPPING.response_shape == "singleton"
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("installCommand",))
        client = MagicMock()
        client.get_all_pages.return_value = {"installCommand": "curl x | sh"}
        with (
            patch.object(backend, "_get_api_client", return_value=client),
            pytest.raises(ValueError, match=r"\{platform\}"),
        ):
            backend.query(DiiAuInstallcommand, DIIAUINSTALLCOMMAND_MAPPING, decision, "t", {})

    def test_no_registered_dii_mapping_uses_dot_sentinel(self) -> None:
        from pynetappfoundry.cache.dii.au.installCommand.mapping import (  # noqa: F401
            DIIAUINSTALLCOMMAND_MAPPING,
        )

        dii = [m for m in model_registry.mappings.values() if m.api_type == "dii"]
        assert dii
        assert [m.name for m in dii if m.records_path == "."] == []

    def test_real_onetimetoken_mapping(self, mock_config: Any) -> None:
        from pynetappfoundry.cache.dii.au.oneTimeToken.mapping import DIIAUONETIMETOKEN_MAPPING
        from pynetappfoundry.models.dii.au.oneTimeToken.model import DiiAuOnetimetoken

        assert DIIAUONETIMETOKEN_MAPPING.response_shape == "singleton"
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("token", "installCommand"))
        client = MagicMock()
        client.get_all_pages.return_value = {
            "token": "tok",
            "installCommand": "curl x | sh",
            "imageZipUrl": "https://example/img.zip",
            "additionalInstructionsForManualInstallation": [{"name": "n"}],
        }
        with patch.object(backend, "_get_api_client", return_value=client):
            results = backend.query(DiiAuOnetimetoken, DIIAUONETIMETOKEN_MAPPING, decision, "t", {})
        assert len(results) == 1
        assert results[0].token == "tok"
        assert results[0].installCommand == "curl x | sh"
        assert results[0].imageZipUrl == "https://example/img.zip"
        assert results[0].additionalInstructionsForManualInstallation[0].name == "n"

    def test_real_users_mapping(self, mock_config: Any) -> None:
        from pynetappfoundry.cache.dii.users.mapping import DIIUSERSRESPONSE_MAPPING
        from pynetappfoundry.models.dii.users.model import DiiUsersresponse

        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("id", "name"))
        client = MagicMock()
        client.get_all_pages.return_value = {
            "users": [
                {
                    "id": "u1",
                    "name": "n",
                    "email": "e",
                    "applicationRoles": [{"role": "r", "application": "a"}],
                }
            ]
        }
        with patch.object(backend, "_get_api_client", return_value=client):
            results = backend.query(DiiUsersresponse, DIIUSERSRESPONSE_MAPPING, decision, "t", {})
        assert len(results) == 1
        assert results[0].id == "u1"
        assert results[0].email == "e"
        assert results[0].applicationRoles[0].role == "r"

    def test_real_invites_mapping(self, mock_config: Any) -> None:
        from pynetappfoundry.cache.dii.users.invites.mapping import DIIINVITESRESPONSE_MAPPING
        from pynetappfoundry.models.dii.users.invites.model import DiiInvitesresponse

        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("id", "email"))
        client = MagicMock()
        client.get_all_pages.return_value = {
            "invites": [
                {
                    "id": "i1",
                    "email": "e",
                    "expiration": "2030-01-01T00:00:00Z",
                    "applicationRoles": [{"role": "r", "application": "a"}],
                }
            ]
        }
        with patch.object(backend, "_get_api_client", return_value=client):
            results = backend.query(
                DiiInvitesresponse, DIIINVITESRESPONSE_MAPPING, decision, "t", {}
            )
        assert len(results) == 1
        assert results[0].id == "i1"
        assert results[0].email == "e"


class TestDiiBackendErrors:
    """Error handling tests for DiiBackend."""

    def test_cache_only_decision_raises(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Cache-only routing decision raises NotImplementedError."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("id", "name"), live_fields=())

        with pytest.raises(NotImplementedError, match="cache-only"):
            backend.query(
                FakeDiiAsset,
                fake_dii_mapping,
                decision,
                cluster="tenant1",
                filters={},
            )

    def test_where_expressions_raises(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """where_expressions raises NotImplementedError."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("id",))

        mock_client = MagicMock()
        mock_client.get_all_pages.return_value = []

        with (
            patch.object(backend, "_get_api_client", return_value=mock_client),
            pytest.raises(NotImplementedError, match="where_expressions"),
        ):
            backend.query(
                FakeDiiAsset,
                fake_dii_mapping,
                decision,
                cluster="tenant1",
                filters={},
                where_expressions=("id > 10",),
            )

    def test_no_live_fields_returns_empty(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Decision with no live_fields (and no cache_fields) returns []."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=())

        results = backend.query(
            FakeDiiAsset,
            fake_dii_mapping,
            decision,
            cluster="tenant1",
            filters={},
        )

        assert results == []


class TestDiiBackendClientCaching:
    """Tests for lazy API client construction and caching."""

    def test_api_client_cached_per_cluster(
        self,
        mock_config: Any,
    ) -> None:
        """Repeated calls for the same cluster reuse the same client."""
        backend = _make_backend(mock_config)

        with patch(
            "pynetappfoundry.clients.dii.api.DIIAPIClient",
        ) as mock_cls:
            mock_cls.return_value = MagicMock()
            client1 = backend._get_api_client("tenant1")
            client2 = backend._get_api_client("tenant1")

        assert client1 is client2
        mock_cls.assert_called_once()

    def test_api_client_different_clusters(
        self,
        mock_config: Any,
    ) -> None:
        """Different clusters get different client instances."""
        backend = _make_backend(mock_config)

        with patch(
            "pynetappfoundry.clients.dii.api.DIIAPIClient",
        ) as mock_cls:
            mock_cls.side_effect = [MagicMock(), MagicMock()]
            client1 = backend._get_api_client("tenant1")
            client2 = backend._get_api_client("tenant2")

        assert client1 is not client2
        assert mock_cls.call_count == 2


# ---------------------------------------------------------------------------
# Parent-keyed (placeholder) mappings, #985
# ---------------------------------------------------------------------------


class FakeThing(OntapModel):
    """Parent model for #985 tests."""

    id: int = 0
    name: str = ""


class FakeKid(OntapModel):
    """Child model for #985 tests."""

    id: int = 0
    name: str = ""


class FakeSub(OntapModel):
    """Grandchild model for #985 tests."""

    name: str = ""


_THING = TypeMapping(
    name="FakeThing985",
    model_class=FakeThing,
    api_endpoint="/things",
    api_type="dii",
    records_path="",
    identifier_field="id",
    fields=(FieldMapping(cache_attr="id", default=0), FieldMapping(cache_attr="name")),
)
_KID = TypeMapping(
    name="FakeKid985",
    model_class=FakeKid,
    api_endpoint="/things/{id}/kids",
    api_type="dii",
    records_path="",
    identifier_field="id",
    parent_mapping="FakeThing985",
    parent_id_field="id",
    fields=(FieldMapping(cache_attr="id", default=0), FieldMapping(cache_attr="name")),
)
_SUB = TypeMapping(
    name="FakeSub985",
    model_class=FakeSub,
    api_endpoint="/kids/{id}/subs",
    api_type="dii",
    records_path="",
    identifier_field="name",
    parent_mapping="FakeKid985",
    parent_id_field="id",
    fields=(FieldMapping(cache_attr="name"),),
)
_LONELY = TypeMapping(
    name="FakeLonely985",
    model_class=FakeSub,
    api_endpoint="/lonely/{lid}/things",
    api_type="dii",
    records_path="",
    identifier_field="name",
    fields=(FieldMapping(cache_attr="name"),),
)
_ORPHAN = TypeMapping(
    name="FakeOrphan985",
    model_class=FakeSub,
    api_endpoint="/x/{id}/y",
    api_type="dii",
    records_path="",
    identifier_field="name",
    parent_mapping="DoesNotExist985",
    parent_id_field="id",
    fields=(FieldMapping(cache_attr="name"),),
)
_ALL_985 = (_THING, _KID, _SUB, _LONELY, _ORPHAN)
_LIVE = RoutingDecision(cache_fields=(), live_fields=("id", "name"))


def _fake_client(responses: dict[tuple[str, tuple[tuple[str, Any], ...]], Any]) -> MagicMock:
    """Client whose ``get_all_pages`` answers by ``(template, sorted path_params)``."""
    client = MagicMock()

    def _pages(
        path: str,
        query_params: dict[str, Any] | None = None,
        path_params: dict[str, Any] | None = None,
    ) -> Any:
        key = (path, tuple(sorted((path_params or {}).items())))
        value = responses[key]
        if isinstance(value, Exception):
            raise value
        return value

    client.get_all_pages = MagicMock(side_effect=_pages)
    return client


def _requested(client: MagicMock) -> list[tuple[str, dict[str, Any]]]:
    return [
        (c.args[0], c.kwargs.get("path_params") or {}) for c in client.get_all_pages.call_args_list
    ]


class TestDiiBackendParentKeyed:
    """Placeholder endpoints are fetched per parent or rejected (#985)."""

    def setup_method(self) -> None:
        for m in _ALL_985:
            model_registry.register_mapping(m.name, m)

    def teardown_method(self) -> None:
        for m in _ALL_985:
            model_registry._mappings.pop(m.name, None)
            model_registry._mappings_by_class.pop(m.model_class, None)

    def test_one_request_per_parent(self, mock_config: Any) -> None:
        backend = _make_backend(mock_config)
        client = _fake_client(
            {
                ("/things", ()): [{"id": 1, "name": "t1"}, {"id": 2, "name": "t2"}],
                ("/things/{id}/kids", (("id", "1"),)): [{"id": 10, "name": "a"}],
                ("/things/{id}/kids", (("id", "2"),)): {
                    "offset": 0,
                    "limit": 1000,
                    "count": 1,
                    "rows": [{"id": 20, "name": "b"}],
                },
            }
        )
        with patch.object(backend, "_get_api_client", return_value=client):
            results = backend.query(FakeKid, _KID, _LIVE, "t", {})
        assert [r.name for r in results] == ["a", "b"]
        assert all("id" in getattr(r, "_fetched_fields", {"id"}) for r in results)
        assert _requested(client) == [
            ("/things", {}),
            ("/things/{id}/kids", {"id": "1"}),
            ("/things/{id}/kids", {"id": "2"}),
        ]

    def test_filters_go_to_child_requests_only(self, mock_config: Any) -> None:
        backend = _make_backend(mock_config)
        client = _fake_client(
            {
                ("/things", ()): [{"id": 1, "name": "t1"}],
                ("/things/{id}/kids", (("id", "1"),)): [],
            }
        )
        with patch.object(backend, "_get_api_client", return_value=client):
            backend.query(FakeKid, _KID, _LIVE, "t", {"name": "a"})
        calls = client.get_all_pages.call_args_list
        assert calls[0].kwargs["query_params"] == {}
        assert calls[1].kwargs["query_params"] == {"name": "a"}

    def test_failing_parent_logged_others_returned(
        self, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        import logging

        backend = _make_backend(mock_config)
        client = _fake_client(
            {
                ("/things", ()): [{"id": 1, "name": "t1"}, {"id": 2, "name": "t2"}],
                ("/things/{id}/kids", (("id", "1"),)): RuntimeError("boom"),
                ("/things/{id}/kids", (("id", "2"),)): [{"id": 20, "name": "b"}],
            }
        )
        with (
            patch.object(backend, "_get_api_client", return_value=client),
            caplog.at_level(logging.WARNING),
        ):
            results = backend.query(FakeKid, _KID, _LIVE, "t", {})
        assert [r.name for r in results] == ["b"]
        assert any("CHILD_FETCH_FAILED" in r.message for r in caplog.records)

    def test_two_level_chain(self, mock_config: Any) -> None:
        backend = _make_backend(mock_config)
        client = _fake_client(
            {
                ("/things", ()): [{"id": 1, "name": "t1"}],
                ("/things/{id}/kids", (("id", "1"),)): [{"id": 10, "name": "k"}],
                ("/kids/{id}/subs", (("id", "10"),)): [{"name": "s"}],
            }
        )
        decision = RoutingDecision(cache_fields=(), live_fields=("name",))
        with patch.object(backend, "_get_api_client", return_value=client):
            results = backend.query(FakeSub, _SUB, decision, "t", {})
        assert [r.name for r in results] == ["s"]
        for path, params in _requested(client):
            for key, value in params.items():
                path = path.replace("{" + key + "}", value)
            assert "{" not in path
            assert "}" not in path

    def test_parent_with_zero_id_is_requested(self, mock_config: Any) -> None:
        """An absent DII id parses to 0 and is substituted, not skipped (#976)."""
        backend = _make_backend(mock_config)
        client = _fake_client(
            {
                ("/things", ()): [{"name": "noid"}],
                ("/things/{id}/kids", (("id", "0"),)): [],
            }
        )
        with patch.object(backend, "_get_api_client", return_value=client):
            assert backend.query(FakeKid, _KID, _LIVE, "t", {}) == []
        assert _requested(client)[-1] == ("/things/{id}/kids", {"id": "0"})

    def test_no_parents_no_child_requests(self, mock_config: Any) -> None:
        backend = _make_backend(mock_config)
        client = _fake_client({("/things", ()): []})
        with patch.object(backend, "_get_api_client", return_value=client):
            assert backend.query(FakeKid, _KID, _LIVE, "t", {}) == []
        assert _requested(client) == [("/things", {})]

    def test_placeholder_without_parent_raises_before_client(self, mock_config: Any) -> None:
        backend = _make_backend(mock_config)
        with (
            patch.object(backend, "_get_api_client") as get_client,
            pytest.raises(ValueError, match=r"\{lid\}"),
        ):
            backend.query(FakeSub, _LONELY, _LIVE, "t", {})
        get_client.assert_not_called()

    def test_unregistered_parent_raises_before_request(self, mock_config: Any) -> None:
        backend = _make_backend(mock_config)
        with (
            patch.object(backend, "_get_api_client") as get_client,
            pytest.raises(ValueError, match="not registered"),
        ):
            backend.query(FakeSub, _ORPHAN, _LIVE, "t", {})
        get_client.assert_not_called()

    def test_cycle_raises_before_request(self, mock_config: Any) -> None:
        cyc_a = dataclasses.replace(
            _KID, name="CycA985", api_endpoint="/a/{id}", parent_mapping="CycB985"
        )
        cyc_b = dataclasses.replace(
            _KID, name="CycB985", api_endpoint="/b/{id}", parent_mapping="CycA985"
        )
        for m in (cyc_a, cyc_b):
            model_registry.register_mapping(m.name, m)
        try:
            backend = _make_backend(mock_config)
            with (
                patch.object(backend, "_get_api_client") as get_client,
                pytest.raises(ValueError, match="cycle"),
            ):
                backend.query(FakeThing, cyc_a, _LIVE, "t", {})
            get_client.assert_not_called()
        finally:
            for m in (cyc_a, cyc_b):
                model_registry._mappings.pop(m.name, None)

    def test_real_wired_mapping_uses_template_with_path_params(self, mock_config: Any) -> None:
        from pynetappfoundry.cache.dii.assets.annotations.values.mapping import (
            DIIASSETSANNOTATIONSVALUE_MAPPING,
        )

        child = DIIASSETSANNOTATIONSVALUE_MAPPING
        parent = model_registry.get_mapping("DiiAssetsAnnotation")
        assert parent is not None
        backend = _make_backend(mock_config)
        client = _fake_client(
            {
                (parent.api_endpoint, ()): [{"id": 7, "name": "ann"}],
                ("/assets/annotations/{id}/values", (("id", "7"),)): [],
            }
        )
        decision = RoutingDecision(cache_fields=(), live_fields=("id",))
        with patch.object(backend, "_get_api_client", return_value=client):
            backend.query(child.model_class, child, decision, "t", {})
        assert _requested(client)[-1] == ("/assets/annotations/{id}/values", {"id": "7"})

    def test_registry_placeholder_mappings_without_parent_raise(self, mock_config: Any) -> None:
        import re

        from pynetappfoundry.cache.dii.au.installCommand.mapping import (  # noqa: F401
            DIIAUINSTALLCOMMAND_MAPPING,
        )

        candidates = [
            m
            for m in model_registry.mappings.values()
            if m.api_type == "dii" and "{" in m.api_endpoint and not m.parent_mapping
        ]
        assert candidates
        backend = _make_backend(mock_config)
        with patch.object(backend, "_get_api_client") as get_client:
            for m in candidates:
                name = re.search(r"\{([^}]+)\}", m.api_endpoint)
                assert name is not None
                with pytest.raises(ValueError, match=re.escape("{" + name.group(1) + "}")):
                    backend.query(m.model_class, m, _LIVE, "t", {})
        get_client.assert_not_called()
