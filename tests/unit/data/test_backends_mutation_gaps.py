"""Behavior tests for gaps the mutation run found in ``OntapBackend`` (#1154).

Each test drives real inputs through a method and asserts what a caller or
operator can observe: the URLs requested, the cluster the API client is built
for, the records returned and the log messages written. They use a fake client
that routes by URL instead of patching ``parse_api_response``, so the parsing
arguments reach the real parser.
"""

from __future__ import annotations

import dataclasses
import logging
from collections.abc import Iterator
from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, call, patch
from urllib.parse import parse_qs, urlparse

import pytest
import requests

from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.core.models import PaginationConfig
from pynetappfoundry.data._routing import RoutingDecision
from pynetappfoundry.data.backends import OntapBackend, _log_missing_fields
from pynetappfoundry.models._base import OntapModel
from tests.unit.data._fakes import (
    FakeChildVolume,
    FakeChildWithDottedRef,
    FakeOrphanChild,
    FakeParentModel,
    FakeVolume,
)

BACKENDS_LOGGER = "pynetappfoundry.data.backends"
PREFIX = "OntapBackend<FakeChild>"


class _Thing(OntapModel):
    """Synthetic model for URL-building tests."""

    name: str = ""
    svm_name: str = ""
    uuid: str = ""


def _thing_mapping(endpoint: str, **kwargs: Any) -> TypeMapping:
    return TypeMapping(
        name="Thing",
        model_class=_Thing,
        api_endpoint=endpoint,
        api_type="ontap",
        identifier_field="name",
        fields=(
            FieldMapping(cache_attr="uuid"),
            FieldMapping(cache_attr="name"),
            FieldMapping(cache_attr="svm_name", api_path="svm.name"),
        ),
        **kwargs,
    )


class _Router:
    """A fake API client answering by URL substring; records every request."""

    def __init__(self, routes: list[tuple[str, Any]] | None = None) -> None:
        self.routes = routes or []
        self.urls: list[str] = []
        self.get_all_kwargs: list[dict[str, Any]] = []

    def _lookup(self, url: str, default: Any) -> Any:
        self.urls.append(url)
        for needle, value in self.routes:
            if needle in url:
                if isinstance(value, Exception):
                    raise value
                return value
        return default

    def get_all_records(self, url: str, **kwargs: Any) -> Any:
        self.get_all_kwargs.append(kwargs)
        return self._lookup(url, {"records": []})

    def call_endpoint(self, url: str, **_kwargs: Any) -> Any:
        return self._lookup(url, {})

    def urls_with(self, needle: str) -> list[str]:
        return [u for u in self.urls if needle in u]


_PARENTS = (
    "fake-parents",
    {
        "records": [
            {"name": "p1", "uuid": "p-1"},
            {"name": "p2", "uuid": "p-2"},
            {"name": "p3", "uuid": "p-3"},
        ]
    },
)


_VOL = {"size": 0, "iops": 0.0, "is_root": False, "files_scanned": 0}
_VOL_NO_IOPS = {"size": 0, "is_root": False, "files_scanned": 0}


def _c(uuid: str, metric: float = 0.0) -> dict[str, Any]:
    """A child record carrying every field the child model needs."""
    return {"uuid": uuid, "metric": metric}


def _ns(**kwargs: Any) -> Any:
    """A bare attribute holder standing in for a model."""
    return SimpleNamespace(**kwargs)


def _group(key: tuple[str, ...], *names: str) -> dict[tuple[str, ...], list[_Thing]]:
    return {key: [_Thing(name=n) for n in names]}


def _boom(_record: dict[str, Any]) -> Any:
    raise RuntimeError("bad transform")


def _http_error(status: int) -> requests.HTTPError:
    response = requests.Response()
    response.status_code = status
    return requests.HTTPError(f"status {status}", response=response)


def _backend(client: Any, config: Any) -> tuple[OntapBackend, MagicMock]:
    """Return a backend whose API client is *client*, plus the factory mock."""
    backend = OntapBackend(config)
    factory = MagicMock(return_value=client)
    backend._get_api_client = factory  # type: ignore[method-assign]
    return backend, factory


def _assert_cluster(factory: MagicMock, cluster: str = "c1") -> None:
    assert factory.call_args_list
    assert all(c == call(cluster) for c in factory.call_args_list)


def _messages(
    caplog: pytest.LogCaptureFixture, level: int, logger: str = BACKENDS_LOGGER
) -> list[str]:
    return [r.getMessage() for r in caplog.records if r.name == logger and r.levelno == level]


@pytest.fixture
def singleton_child_mapping(fake_parent_mapping: TypeMapping) -> Iterator[TypeMapping]:
    """A parent-keyed singleton mapping: one record per parent."""
    mapping = TypeMapping(
        name="FakeChild",
        model_class=FakeChildWithDottedRef,
        api_endpoint="/storage/fakes/{volume.uuid}/info?fields=*",
        api_type="ontap",
        parent_mapping="FakeParent",
        parent_id_field="uuid",
        identifier_field="uuid",
        response_shape="singleton",
        fields=(
            FieldMapping(cache_attr="uuid"),
            FieldMapping(cache_attr="metric", cache_strategy="realtime"),
        ),
    )
    yield mapping


# --------------------------------------------------------------------------- #
# _log_missing_fields / _log_child_failure
# --------------------------------------------------------------------------- #


class TestLogHelpers:
    def test_log_missing_fields_names_type_record_and_fields(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        with caplog.at_level(logging.DEBUG, logger=BACKENDS_LOGGER):
            _log_missing_fields({"a": 1}, ["a", "b", "c"], "Thing", "rec-1")
        assert _messages(caplog, logging.DEBUG) == [
            "DataSource Thing[rec-1]: missing fields ['b', 'c']"
        ]

    def test_log_missing_fields_silent_when_nothing_missing(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        with caplog.at_level(logging.DEBUG, logger=BACKENDS_LOGGER):
            _log_missing_fields({"a": 1, "b": 2}, ["a", "b"], "Thing", "rec-1")
        assert _messages(caplog, logging.DEBUG) == []

    def test_log_child_failure_message(
        self, fake_child_mapping: TypeMapping, caplog: pytest.LogCaptureFixture
    ) -> None:
        with caplog.at_level(logging.WARNING, logger=BACKENDS_LOGGER):
            OntapBackend._log_child_failure(PREFIX, fake_child_mapping, "p1", RuntimeError("boom"))
        assert _messages(caplog, logging.WARNING) == [
            f"{PREFIX} CHILD_FETCH_FAILED: FakeChild for parent p1 - RuntimeError: boom"
        ]


# --------------------------------------------------------------------------- #
# small methods
# --------------------------------------------------------------------------- #


class TestSmallMethods:
    def test_init_starts_with_empty_client_caches(self, mock_config: Any) -> None:
        backend = OntapBackend(mock_config)
        assert backend._api_clients == {}
        assert backend._cli_clients == {}

    def test_api_client_unconfigured_cluster_uses_its_name_as_ip(self, mock_config: Any) -> None:
        mock_config.data = {"clusters": {"other": {"ip": "10.0.0.9"}}}
        with patch(
            "pynetappfoundry.clients.ontap.api.ONTAPAPIClient.__init__", return_value=None
        ) as init:
            OntapBackend(mock_config)._get_api_client("cl9")
        assert init.call_args.kwargs["cluster"].ip == "cl9"

    def test_api_client_without_clusters_section_uses_its_name_as_ip(
        self, mock_config: Any
    ) -> None:
        mock_config.data = {}
        with patch(
            "pynetappfoundry.clients.ontap.api.ONTAPAPIClient.__init__", return_value=None
        ) as init:
            OntapBackend(mock_config)._get_api_client("cl9")
        assert init.call_args.kwargs["cluster"].ip == "cl9"

    def test_api_client_gets_the_config_and_is_reused(self, mock_config: Any) -> None:
        mock_config.data = {"clusters": {"cl1": {"ip": "10.0.0.5"}}}
        backend = OntapBackend(mock_config)
        with patch(
            "pynetappfoundry.clients.ontap.api.ONTAPAPIClient.__init__", return_value=None
        ) as init:
            first = backend._get_api_client("cl1")
            second = backend._get_api_client("cl1")
        init.assert_called_once()
        assert init.call_args.kwargs["config"] is mock_config
        assert first is second

    def test_is_cloud_cluster_logs_why_it_defaults_to_false(
        self, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        backend = OntapBackend(mock_config)
        with (
            patch.object(backend, "_resolve_metadata_path", side_effect=ValueError("no table")),
            caplog.at_level(logging.DEBUG, logger=BACKENDS_LOGGER),
        ):
            assert backend._is_cloud_cluster("c1") is False
        assert _messages(caplog, logging.DEBUG) == [
            "OntapBackend: cannot determine is_cloud for c1, defaulting to False"
        ]

    def test_resolve_metadata_path_unregistered_model_names_it(self, mock_config: Any) -> None:
        class _Unregistered(OntapModel):
            pass

        with pytest.raises(
            ValueError, match=r"No cache table registered for model '_Unregistered'"
        ):
            OntapBackend(mock_config)._resolve_metadata_path(_Unregistered)

    def test_filters_force_the_filtered_path_even_with_every_field_live(
        self, fake_volume_mapping: TypeMapping
    ) -> None:
        live = tuple(
            f.cache_attr for f in fake_volume_mapping.fields if f.cache_strategy != "derived"
        )
        decision = RoutingDecision(cache_fields=(), live_fields=live)
        assert OntapBackend._is_full_live_scan(fake_volume_mapping, decision, {}) is True
        assert (
            OntapBackend._is_full_live_scan(fake_volume_mapping, decision, {"name": "v"}) is False
        )

    def test_no_live_fields_is_never_a_full_live_scan(
        self, fake_volume_mapping: TypeMapping
    ) -> None:
        decision = RoutingDecision(cache_fields=("name",), live_fields=())
        assert OntapBackend._is_full_live_scan(fake_volume_mapping, decision, {}) is False

    def test_mark_fetched_tolerates_objects_without_the_field(self) -> None:
        OntapBackend._mark_fetched(_ns(), ("a",))
        holder = _ns(_fetched_fields={"x"})
        OntapBackend._mark_fetched(holder, ("a",))
        assert holder._fetched_fields == {"x", "a"}

    @pytest.mark.parametrize(
        ("endpoint", "expected"),
        [
            ("/a/{x.id}/b/{y.id}/c?filter={z}", ("x.id", "y.id")),
            ("/a/{x.id}?q={y.id}?r=1", ("x.id",)),
            ("/a/{x.id}/b", ("x.id",)),
        ],
    )
    def test_parent_ref_fields_ignore_the_query_string(
        self, endpoint: str, expected: tuple[str, ...]
    ) -> None:
        assert OntapBackend._extract_parent_ref_fields(_thing_mapping(endpoint)) == expected


# --------------------------------------------------------------------------- #
# _build_live_url
# --------------------------------------------------------------------------- #


class TestBuildLiveUrl:
    def test_records_are_returned_by_default(self) -> None:
        url = OntapBackend._build_live_url(_thing_mapping("/things"), {"name": "a"}, ())
        assert parse_qs(urlparse(url).query) == {"name": ["a"]}

    def test_blank_values_in_the_endpoint_survive(self) -> None:
        url = OntapBackend._build_live_url(_thing_mapping("/things?flag=&fields=*"), {}, ())
        assert parse_qs(urlparse(url).query, keep_blank_values=True) == {
            "flag": [""],
            "fields": ["*"],
        }

    def test_fields_use_api_paths_and_fall_back_to_the_attribute(self) -> None:
        url = OntapBackend._build_live_url(
            _thing_mapping("/things"), {}, ("svm_name", "uuid", "not_a_field")
        )
        assert parse_qs(urlparse(url).query) == {"fields": ["svm.name,uuid,not_a_field"]}

    def test_star_fields_in_the_endpoint_are_kept(self) -> None:
        url = OntapBackend._build_live_url(_thing_mapping("/things?fields=*"), {}, ("svm_name",))
        assert parse_qs(urlparse(url).query) == {"fields": ["*"]}


# --------------------------------------------------------------------------- #
# singleton raw fetch and filtered fetch
# --------------------------------------------------------------------------- #


class TestSingletonRaw:
    def test_uses_the_cluster_and_the_given_base_url(self, mock_config: Any) -> None:
        mapping = _thing_mapping("/things", response_shape="singleton")
        router = _Router([("/elsewhere", {"name": "a"})])
        backend, factory = _backend(router, mock_config)
        assert backend._fetch_singleton_raw(mapping, "c1", {}, (), base_url="/elsewhere") == {
            "name": "a"
        }
        _assert_cluster(factory)
        assert router.urls == ["/elsewhere"]

    def test_control_keys_do_not_stop_the_remaining_filters(self, mock_config: Any) -> None:
        mapping = _thing_mapping("/things", response_shape="singleton")
        router = _Router([("/things", {"name": "a"})])
        backend, _ = _backend(router, mock_config)
        filters = {"order_by": "name", "name": "zzz"}
        assert backend._fetch_singleton_raw(mapping, "c1", filters, ()) is None


class TestCountLive:
    def test_envelope_counts_with_the_cluster(self, mock_config: Any) -> None:
        router = _Router([("/things", {"num_records": 7})])
        backend, factory = _backend(router, mock_config)
        assert backend._count_live(_thing_mapping("/things"), "c1", {"name": "a"}) == 7
        _assert_cluster(factory)

    def test_singleton_counts_with_the_cluster(self, mock_config: Any) -> None:
        router = _Router([("/things", {"name": "a"})])
        backend, factory = _backend(router, mock_config)
        mapping = _thing_mapping("/things", response_shape="singleton")
        assert backend._count_live(mapping, "c1", {}) == 1
        _assert_cluster(factory)


class TestFetchLiveFiltered:
    def test_singleton_transform_failure_is_logged_with_the_prefix(
        self, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        mapping = dataclasses.replace(
            _thing_mapping("/things", response_shape="singleton"),
            fields=(FieldMapping(cache_attr="name", transform=_boom),),
        )
        backend, _ = _backend(_Router([("/things", {"name": "a"})]), mock_config)
        with (
            caplog.at_level(logging.ERROR, logger="pynetappfoundry.cache.field_mapping"),
            pytest.raises(RuntimeError, match="bad transform"),
        ):
            backend._fetch_live_filtered(_Thing, mapping, "c1", {}, ())
        errors = _messages(caplog, logging.ERROR, "pynetappfoundry.cache.field_mapping")
        assert errors == [
            "OntapBackend<Thing> TRANSFORM_FAILURE: Thing 'a' - transform error for field 'name'"
        ]

    def test_singleton_uses_the_cluster_and_the_model_class(self, mock_config: Any) -> None:
        mapping = _thing_mapping("/things", response_shape="singleton")
        router = _Router([("/things", {"name": "a", "uuid": "u"})])
        backend, factory = _backend(router, mock_config)
        found = backend._fetch_live_filtered(_Thing, mapping, "c1", {}, ())
        assert [t.name for t in found] == ["a"]
        _assert_cluster(factory)
        assert backend._fetch_live_filtered(FakeVolume, mapping, "c1", {}, ()) == []

    def test_envelope_reads_with_cluster_and_default_url(
        self, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        mapping = _thing_mapping("/things")
        router = _Router([("/things", {"records": [{"name": "a"}, {"name": "b", "uuid": "u"}]})])
        backend, factory = _backend(router, mock_config)
        with caplog.at_level(logging.DEBUG):
            found = backend._fetch_live_filtered(_Thing, mapping, "c1", {"name": "a"}, ("uuid",))
        assert [t.name for t in found] == ["a", "b"]
        _assert_cluster(factory)
        query = parse_qs(urlparse(router.urls[0]).query)
        assert query == {"name": ["a"], "fields": ["uuid"]}
        # the parse call got the mapping, the response and the log prefix
        parse_logs = _messages(caplog, logging.DEBUG, "pynetappfoundry.cache.field_mapping")
        assert "OntapBackend<Thing> API response: 2 things" in parse_logs
        # the missing-field callback reached the parser
        assert "DataSource Thing[b]: missing fields ['svm']" in _messages(caplog, logging.DEBUG)


# --------------------------------------------------------------------------- #
# live child queries
# --------------------------------------------------------------------------- #


class TestChildTargets:
    def test_pinned_multi_placeholder_builds_one_url_and_a_joined_label(self) -> None:
        mapping = _thing_mapping(
            "/a/{svm.uuid}/b/{group.name}/users?fields=*",
            parent_mapping="FakeParent",
            parent_id_fields=("uuid", "name"),
        )
        targets, narrowed = OntapBackend._child_targets(
            mapping, MagicMock(), {"svm.uuid": "s1", "group.name": "g1"}, PREFIX
        )
        assert narrowed is True
        assert targets == [("s1, g1", "/a/s1/b/g1/users?fields=*")]

    def test_pinned_single_placeholder(self, fake_child_mapping: TypeMapping) -> None:
        targets, narrowed = OntapBackend._child_targets(
            fake_child_mapping, MagicMock(), {"volume.uuid": "p-1"}, PREFIX
        )
        assert narrowed is True
        assert targets == [("p-1", "/storage/fakes/p-1/children?fields=*")]

    def test_unpinned_labels_are_parent_names_and_prefix_reaches_the_helpers(
        self, fake_child_mapping: TypeMapping, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router(
            [
                (
                    "fake-parents",
                    {"records": [{"name": "p1", "uuid": "p-1"}, {"name": "nouuid", "uuid": ""}]},
                )
            ]
        )
        with (
            caplog.at_level(logging.WARNING),
            patch(
                "pynetappfoundry.data.backends.fetch_parents",
                wraps=__import__(
                    "pynetappfoundry.cache.fetchers", fromlist=["fetch_parents"]
                ).fetch_parents,
            ) as spy,
        ):
            targets, narrowed = OntapBackend._child_targets(fake_child_mapping, router, {}, PREFIX)
        assert narrowed is False
        assert targets == [("p1", "/storage/fakes/p-1/children?fields=*")]
        args = spy.call_args.args
        assert args[0] is fake_child_mapping
        assert args[1] is router
        assert args[3] == PREFIX
        assert any(
            m.startswith(f"{PREFIX} SKIP_PARENT")
            for m in _messages(caplog, logging.WARNING, "pynetappfoundry.cache.fetchers")
        )

    def test_label_falls_back_to_repr_for_a_parent_without_a_name(
        self, fake_child_mapping: TypeMapping
    ) -> None:
        nameless = _ns(uuid="p-9")
        with (
            patch("pynetappfoundry.data.backends.fetch_parents", return_value=[nameless]),
            patch(
                "pynetappfoundry.data.backends.iter_parent_urls",
                return_value=[(nameless, "/u")],
            ),
        ):
            targets, _ = OntapBackend._child_targets(fake_child_mapping, MagicMock(), {}, PREFIX)
        assert targets == [(repr(nameless), "/u")]


class TestCountLiveChildren:
    def test_envelope_sums_num_records_and_a_missing_count_is_zero(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router(
            [_PARENTS, ("/p-1/", {"num_records": 2}), ("/p-2/", {}), ("/p-3/", {"num_records": 4})]
        )
        backend, factory = _backend(router, mock_config)
        with caplog.at_level(logging.DEBUG, logger=BACKENDS_LOGGER):
            assert backend._count_live(fake_child_mapping, "c1", {}) == 6
        _assert_cluster(factory)
        assert _messages(caplog, logging.WARNING) == []
        assert all("return_records=false" in u for u in router.urls_with("/children"))

    def test_singleton_counts_the_parents_that_have_a_matching_record(
        self,
        singleton_child_mapping: TypeMapping,
        mock_config: Any,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        router = _Router(
            [
                _PARENTS,
                ("/p-1/info", _c("c3")),
                ("/p-2/info", {}),
                ("/p-3/info", _c("c3")),
            ]
        )
        backend, factory = _backend(router, mock_config)
        with caplog.at_level(logging.DEBUG, logger=BACKENDS_LOGGER):
            assert backend._count_live(singleton_child_mapping, "c1", {"uuid": "c3"}) == 2
        _assert_cluster(factory)
        assert _messages(caplog, logging.WARNING) == []
        assert len(router.urls_with("/info")) == 3

    def test_singleton_without_parents_matches_counts_zero(
        self, singleton_child_mapping: TypeMapping, mock_config: Any
    ) -> None:
        router = _Router([_PARENTS, ("/info", {"uuid": "other"})])
        backend, _ = _backend(router, mock_config)
        assert backend._count_live(singleton_child_mapping, "c1", {"uuid": "c3"}) == 0

    def test_unpinned_404_is_a_failure_and_the_next_parent_still_counts(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router([_PARENTS, ("/p-1/", _http_error(404)), ("/p-2/", {"num_records": 3})])
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.WARNING, logger=BACKENDS_LOGGER):
            assert backend._count_live(fake_child_mapping, "c1", {}) == 3
        assert _messages(caplog, logging.WARNING) == [
            f"{PREFIX} CHILD_FETCH_FAILED: FakeChild for parent p1 - HTTPError: status 404"
        ]

    def test_pinned_500_is_a_failure_labelled_with_the_pinned_value(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router([("/p-1/", _http_error(500)), ("/p-2/", {"num_records": 3})])
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.WARNING, logger=BACKENDS_LOGGER):
            assert backend._count_live(fake_child_mapping, "c1", {"volume.uuid": "p-1|p-2"}) == 3
        assert _messages(caplog, logging.WARNING) == [
            f"{PREFIX} CHILD_FETCH_FAILED: FakeChild for parent p-1 - HTTPError: status 500"
        ]

    def test_pinned_404_counts_zero_quietly_and_continues(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router([("/p-1/", _http_error(404)), ("/p-2/", {"num_records": 3})])
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.DEBUG, logger=BACKENDS_LOGGER):
            assert backend._count_live(fake_child_mapping, "c1", {"volume.uuid": "p-1|p-2"}) == 3
        assert _messages(caplog, logging.WARNING) == []
        assert _messages(caplog, logging.DEBUG) == [
            f"{PREFIX} pinned target p-1 answered 404: no records"
        ]

    def test_generic_error_is_logged_and_the_next_parent_counts(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router([_PARENTS, ("/p-1/", RuntimeError("boom")), ("/p-2/", {"num_records": 1})])
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.WARNING, logger=BACKENDS_LOGGER):
            assert backend._count_live(fake_child_mapping, "c1", {}) == 1
        assert _messages(caplog, logging.WARNING) == [
            f"{PREFIX} CHILD_FETCH_FAILED: FakeChild for parent p1 - RuntimeError: boom"
        ]

    def test_unpinned_skip_parent_warning_carries_the_prefix(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router([("fake-parents", {"records": [{"name": "nouuid", "uuid": ""}]})])
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.WARNING):
            assert backend._count_live(fake_child_mapping, "c1", {}) == 0
        skips = [r.getMessage() for r in caplog.records if "SKIP_PARENT" in r.getMessage()]
        assert [m.split(":")[0] for m in skips] == [f"{PREFIX} SKIP_PARENT"]


class TestFetchLiveFilteredChildren:
    _LIVE = ("uuid", "metric")

    def _fetch(
        self,
        backend: OntapBackend,
        mapping: TypeMapping,
        filters: dict[str, Any],
    ) -> list[FakeChildWithDottedRef]:
        return backend._fetch_live_filtered(
            FakeChildWithDottedRef, mapping, "c1", filters, self._LIVE
        )

    def test_zero_max_records_makes_no_request(
        self, fake_child_mapping: TypeMapping, mock_config: Any
    ) -> None:
        router = _Router([_PARENTS])
        backend, factory = _backend(router, mock_config)
        assert self._fetch(backend, fake_child_mapping, {"max_records": 0}) == []
        assert router.urls == []
        factory.assert_not_called()

    def test_max_records_one_returns_one_record(
        self, fake_child_mapping: TypeMapping, mock_config: Any
    ) -> None:
        router = _Router(
            [
                _PARENTS,
                ("/p-1/", {"records": [_c("c1")]}),
                ("/p-2/", {"records": [_c("c2")]}),
            ]
        )
        backend, factory = _backend(router, mock_config)
        found = self._fetch(backend, fake_child_mapping, {"max_records": 1})
        assert [r.uuid for r in found] == ["c1"]
        _assert_cluster(factory)
        assert len(router.urls_with("/children")) == 1

    def test_max_records_is_a_running_total_across_parents(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router(
            [
                _PARENTS,
                ("/p-1/", {"records": [_c("c1"), _c("c2")]}),
                ("/p-2/", {"records": [_c("c3"), _c("c4")]}),
                ("/p-3/", {"records": [_c("c5")]}),
            ]
        )
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.WARNING, logger=BACKENDS_LOGGER):
            found = self._fetch(backend, fake_child_mapping, {"max_records": 3})
        assert [r.uuid for r in found] == ["c1", "c2", "c3"]
        child_urls = router.urls_with("/children")
        assert len(child_urls) == 2
        assert "max_records=3" in child_urls[0]
        assert "max_records=1" in child_urls[1]
        assert "max_records=3" not in child_urls[1]
        kwargs = [
            k for k, u in zip(router.get_all_kwargs, router.urls, strict=True) if "/children" in u
        ]
        assert kwargs == [
            {"pagination_config": PaginationConfig(max_records=3)},
            {"pagination_config": PaginationConfig(max_records=1)},
        ]
        assert _messages(caplog, logging.WARNING) == []

    def test_a_parent_filling_the_limit_stops_the_loop_quietly(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router([_PARENTS, ("/p-1/", {"records": [_c("c1"), _c("c2")]})])
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.WARNING, logger=BACKENDS_LOGGER):
            found = self._fetch(backend, fake_child_mapping, {"max_records": 2})
        assert [r.uuid for r in found] == ["c1", "c2"]
        assert len(router.urls_with("/children")) == 1
        assert _messages(caplog, logging.WARNING) == []

    def test_never_returns_more_than_max_records(
        self, fake_child_mapping: TypeMapping, mock_config: Any
    ) -> None:
        router = _Router([_PARENTS, ("/p-1/", {"records": [_c("c1"), _c("c2"), _c("c3")]})])
        backend, _ = _backend(router, mock_config)
        found = self._fetch(backend, fake_child_mapping, {"max_records": 2})
        assert [r.uuid for r in found] == ["c1", "c2"]

    def test_without_max_records_requests_are_uncapped(
        self, fake_child_mapping: TypeMapping, mock_config: Any
    ) -> None:
        router = _Router(
            [
                _PARENTS,
                ("/p-1/", {"records": [_c("c1")]}),
                ("/p-2/", {"records": [_c("c2")]}),
            ]
        )
        backend, _ = _backend(router, mock_config)
        found = self._fetch(backend, fake_child_mapping, {"uuid": "x"})
        assert sorted(r.uuid for r in found) == ["c1", "c2"]
        child_urls = router.urls_with("/children")
        assert all("max_records" not in u for u in child_urls)
        assert all(
            k == {}
            for k, u in zip(router.get_all_kwargs, router.urls, strict=True)
            if "/children" in u
        )

    def test_parse_gets_the_prefix_and_the_log_callback(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router([_PARENTS, ("/p-1/", {"records": [_c("c1")]})])
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.DEBUG):
            self._fetch(backend, fake_child_mapping, {"uuid": "x"})
        parse_logs = _messages(caplog, logging.DEBUG, "pynetappfoundry.cache.field_mapping")
        assert f"{PREFIX} API response: 1 fakechilds" in parse_logs

    def test_http_error_is_logged_and_the_next_parent_is_still_fetched(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router(
            [_PARENTS, ("/p-1/", _http_error(500)), ("/p-2/", {"records": [_c("c2")]})]
        )
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.WARNING, logger=BACKENDS_LOGGER):
            found = self._fetch(backend, fake_child_mapping, {"uuid": "x"})
        assert [r.uuid for r in found] == ["c2"]
        assert _messages(caplog, logging.WARNING) == [
            f"{PREFIX} CHILD_FETCH_FAILED: FakeChild for parent p1 - HTTPError: status 500"
        ]

    def test_unpinned_404_is_a_failure(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router([_PARENTS, ("/p-1/", _http_error(404))])
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.WARNING, logger=BACKENDS_LOGGER):
            assert self._fetch(backend, fake_child_mapping, {"uuid": "x"}) == []
        assert len(_messages(caplog, logging.WARNING)) == 1

    def test_pinned_404_is_quiet_with_the_target_in_the_debug_line(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router([("/p-1/", _http_error(404)), ("/p-2/", {"records": [_c("c2")]})])
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.DEBUG, logger=BACKENDS_LOGGER):
            found = self._fetch(backend, fake_child_mapping, {"volume.uuid": "p-1|p-2"})
        assert [r.uuid for r in found] == ["c2"]
        assert _messages(caplog, logging.WARNING) == []
        assert [m for m in _messages(caplog, logging.DEBUG) if "pinned target" in m] == [
            f"{PREFIX} pinned target p-1 answered 404: no records"
        ]

    def test_pinned_500_is_logged_with_the_target_label(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router([("/p-1/", _http_error(500))])
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.WARNING, logger=BACKENDS_LOGGER):
            assert self._fetch(backend, fake_child_mapping, {"volume.uuid": "p-1"}) == []
        assert _messages(caplog, logging.WARNING) == [
            f"{PREFIX} CHILD_FETCH_FAILED: FakeChild for parent p-1 - HTTPError: status 500"
        ]

    def test_generic_error_is_logged_with_prefix_label_and_error(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router(
            [_PARENTS, ("/p-1/", RuntimeError("boom")), ("/p-2/", {"records": [_c("c2")]})]
        )
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.WARNING, logger=BACKENDS_LOGGER):
            found = self._fetch(backend, fake_child_mapping, {"uuid": "x"})
        assert [r.uuid for r in found] == ["c2"]
        assert _messages(caplog, logging.WARNING) == [
            f"{PREFIX} CHILD_FETCH_FAILED: FakeChild for parent p1 - RuntimeError: boom"
        ]

    def test_unpinned_skip_parent_warning_carries_the_prefix(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        router = _Router([("fake-parents", {"records": [{"name": "nouuid", "uuid": ""}]})])
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.WARNING):
            assert self._fetch(backend, fake_child_mapping, {}) == []
        skips = [r.getMessage() for r in caplog.records if "SKIP_PARENT" in r.getMessage()]
        assert [m.split(":")[0] for m in skips] == [f"{PREFIX} SKIP_PARENT"]

    def test_singleton_one_record_per_parent(
        self,
        singleton_child_mapping: TypeMapping,
        mock_config: Any,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        router = _Router(
            [
                _PARENTS,
                ("/p-1/info", _c("c1", 1.5)),
                ("/p-2/info", {}),
                ("/p-3/info", _c("c3", 3.5)),
            ]
        )
        backend, factory = _backend(router, mock_config)
        with caplog.at_level(logging.WARNING, logger=BACKENDS_LOGGER):
            found = self._fetch(backend, singleton_child_mapping, {})
        assert [(r.uuid, r.metric) for r in found] == [("c1", 1.5), ("c3", 3.5)]
        _assert_cluster(factory)
        info_urls = router.urls_with("/info")
        assert len(info_urls) == 3
        assert all(parse_qs(urlparse(u).query)["fields"] == ["*"] for u in info_urls)
        assert _messages(caplog, logging.WARNING) == []

    def test_singleton_transform_failure_is_logged_with_the_prefix(
        self,
        singleton_child_mapping: TypeMapping,
        mock_config: Any,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        mapping = dataclasses.replace(
            singleton_child_mapping,
            fields=(FieldMapping(cache_attr="uuid", transform=_boom),),
        )
        router = _Router([_PARENTS, ("/p-1/info", _c("c1")), ("/p-2/info", {})])
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.ERROR):
            assert self._fetch(backend, mapping, {}) == []
        errors = _messages(caplog, logging.ERROR, "pynetappfoundry.cache.field_mapping")
        assert errors == [
            f"{PREFIX} TRANSFORM_FAILURE: FakeChild 'c1' - transform error for field 'uuid'"
        ]

    def test_singleton_max_records_is_a_running_total_and_not_a_filter(
        self,
        singleton_child_mapping: TypeMapping,
        mock_config: Any,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        router = _Router(
            [
                _PARENTS,
                ("/p-1/info", _c("c1")),
                ("/p-2/info", _c("c2")),
                ("/p-3/info", _c("c3")),
            ]
        )
        backend, _ = _backend(router, mock_config)
        with caplog.at_level(logging.WARNING, logger=BACKENDS_LOGGER):
            found = self._fetch(backend, singleton_child_mapping, {"max_records": 2})
        assert [r.uuid for r in found] == ["c1", "c2"]
        assert len(router.urls_with("/info")) == 2
        assert _messages(caplog, logging.WARNING) == []

    def test_singleton_filters_apply_client_side(
        self, singleton_child_mapping: TypeMapping, mock_config: Any
    ) -> None:
        router = _Router(
            [
                _PARENTS,
                ("/p-1/info", _c("c1")),
                ("/p-2/info", _c("c2")),
                ("/p-3/info", _c("c1")),
            ]
        )
        backend, _ = _backend(router, mock_config)
        found = self._fetch(backend, singleton_child_mapping, {"uuid": "c1"})
        assert [r.uuid for r in found] == ["c1", "c1"]


# --------------------------------------------------------------------------- #
# query() dispatch
# --------------------------------------------------------------------------- #


class TestQueryDispatch:
    def test_path_params_error_message(
        self, fake_volume_mapping: TypeMapping, mock_config: Any
    ) -> None:
        with pytest.raises(ValueError) as info:
            OntapBackend(mock_config).query(
                FakeVolume,
                fake_volume_mapping,
                RoutingDecision(cache_fields=("name",), live_fields=()),
                cluster="c1",
                filters={},
                path_params={"x": "1"},
            )
        assert str(info.value) == (
            "OntapBackend does not support path_params; it is only available on DiiBackend"
        )

    def test_cli_mapping_skips_non_cloud_cluster_and_says_so(
        self, fake_volume_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        cli_mapping = TypeMapping(
            name="CliThing",
            model_class=FakeVolume,
            api_endpoint="",
            cli_command="thing show",
            fields=fake_volume_mapping.fields,
        )
        backend = OntapBackend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("name",))
        with (
            patch.object(backend, "_is_cloud_cluster", return_value=False) as is_cloud,
            caplog.at_level(logging.DEBUG, logger=BACKENDS_LOGGER),
        ):
            assert backend.query(FakeVolume, cli_mapping, decision, "c1", {}) == []
        is_cloud.assert_called_once_with("c1")
        assert _messages(caplog, logging.DEBUG) == [
            "OntapBackend: skipping CLI-only CliThing for non-cloud cluster c1"
        ]

    def test_cli_mapping_fetches_with_both_clients_and_wraps_a_single_model(
        self, fake_volume_mapping: TypeMapping, mock_config: Any
    ) -> None:
        cli_mapping = TypeMapping(
            name="CliThing",
            model_class=FakeVolume,
            api_endpoint="",
            cli_command="thing show",
            fields=fake_volume_mapping.fields,
        )
        backend = OntapBackend(mock_config)
        api, cli = MagicMock(name="api"), MagicMock(name="cli")
        api_factory = MagicMock(return_value=api)
        cli_factory = MagicMock(return_value=cli)
        backend._get_api_client = api_factory  # type: ignore[method-assign]
        backend._get_cli_client = cli_factory  # type: ignore[method-assign]
        one = FakeVolume(name="only", uuid="u")
        decision = RoutingDecision(cache_fields=(), live_fields=("name",))
        with (
            patch.object(backend, "_is_cloud_cluster", return_value=True),
            patch("pynetappfoundry.data.backends.fetch", return_value=one) as fetch_mock,
        ):
            results = backend.query(FakeVolume, cli_mapping, decision, "c1", {})
        assert results == [one]
        fetch_mock.assert_called_once_with(
            FakeVolume, cluster="c1", config=mock_config, api_client=api, cli_client=cli
        )
        _assert_cluster(api_factory)
        _assert_cluster(cli_factory)

    def test_full_live_scan_fetches_with_the_cluster_and_config(
        self, fake_volume_mapping: TypeMapping, mock_config: Any
    ) -> None:
        backend = OntapBackend(mock_config)
        api = MagicMock(name="api")
        factory = MagicMock(return_value=api)
        backend._get_api_client = factory  # type: ignore[method-assign]
        live = tuple(
            f.cache_attr for f in fake_volume_mapping.fields if f.cache_strategy != "derived"
        )
        with patch(
            "pynetappfoundry.data.backends.fetch", return_value=[FakeVolume(name="v")]
        ) as fetch_mock:
            backend.query(
                FakeVolume,
                fake_volume_mapping,
                RoutingDecision(cache_fields=(), live_fields=live),
                "c1",
                {},
            )
        fetch_mock.assert_called_once_with(
            FakeVolume, cluster="c1", config=mock_config, api_client=api
        )
        _assert_cluster(factory)

    def test_filtered_live_query_uses_the_cluster(self, mock_config: Any) -> None:
        router = _Router([("/things", {"records": [{"name": "v1", "uuid": "u1"}]})])
        backend, factory = _backend(router, mock_config)
        found = backend.query(
            _Thing,
            _thing_mapping("/things"),
            RoutingDecision(cache_fields=(), live_fields=("name",)),
            "c1",
            {"uuid": "u1"},
        )
        assert [v.name for v in found] == ["v1"]
        _assert_cluster(factory)


# --------------------------------------------------------------------------- #
# partial queries
# --------------------------------------------------------------------------- #


class TestPartialQuery:
    def test_standard_partial_uses_cluster_and_filter_expressions(self, mock_config: Any) -> None:
        mapping = _thing_mapping("/things")
        router = _Router(
            [("/things", {"records": [{"name": "v1", "uuid": "u1", "svm": {"name": "s1"}}]})]
        )
        backend, factory = _backend(router, mock_config)
        db = MagicMock()
        db.query_with_filters.return_value = [_Thing(name="v1", uuid="u1")]
        with (
            patch.object(OntapBackend, "_cache_db", new=db),
            patch.object(backend, "_resolve_metadata_path", return_value="storage.things"),
        ):
            found = backend.query(
                _Thing,
                mapping,
                RoutingDecision(cache_fields=("name", "uuid"), live_fields=("svm_name",)),
                "prod1",
                {"name": "v1"},
            )
        assert [(v.uuid, v.svm_name) for v in found] == [("u1", "s1")]
        db.query_with_filters.assert_called_once_with("prod1", "storage.things", ["name = 'v1'"])
        _assert_cluster(factory, "prod1")

    def test_parent_keyed_partial_uses_cluster_for_the_cache_fallback_and_the_live_fetch(
        self, fake_orphan_child_mapping: TypeMapping, mock_config: Any
    ) -> None:
        router = _Router(
            [
                (
                    "/svm/fakes/p1/orphans",
                    {"records": [{"volume_uuid": "vu1", "transfer_state": "done"}]},
                ),
                ("/svm/fakes/p2/orphans", {"records": []}),
            ]
        )
        backend, factory = _backend(router, mock_config)
        db = MagicMock()
        db.query_with_filters.side_effect = [
            [FakeOrphanChild(volume_uuid="vu1"), FakeOrphanChild(volume_uuid="vu2")],
            [FakeParentModel(uuid="p1", name="n1"), FakeParentModel(uuid="p2", name="n2")],
        ]
        with (
            patch.object(OntapBackend, "_cache_db", new=db),
            patch.object(
                backend,
                "_resolve_metadata_path",
                side_effect=["svm.fake_orphans", "storage.fake_parents"],
            ),
        ):
            found = backend.query(
                FakeOrphanChild,
                fake_orphan_child_mapping,
                RoutingDecision(cache_fields=("volume_uuid",), live_fields=("transfer_state",)),
                "prod1",
                {},
            )
        assert {c.volume_uuid: c.transfer_state for c in found} == {"vu1": "done", "vu2": ""}
        assert db.query_with_filters.call_args_list == [
            call("prod1", "svm.fake_orphans", []),
            call("prod1", "storage.fake_parents", []),
        ]
        _assert_cluster(factory, "prod1")
        urls = router.urls_with("/orphans")
        assert len(urls) == 2
        assert parse_qs(urlparse(urls[0]).query)["volume_uuid"] == ["vu1|vu2"]


class TestResolveParentUuids:
    def test_orphan_warning_message(
        self, fake_child_mapping: TypeMapping, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        backend = OntapBackend(mock_config)
        good = FakeChildWithDottedRef(uuid="c1", volume=FakeChildVolume(uuid="v1"))
        bad = FakeChildWithDottedRef(uuid="c2", volume=FakeChildVolume(uuid=""))
        with caplog.at_level(logging.WARNING, logger=BACKENDS_LOGGER):
            groups = backend._resolve_parent_uuids(
                fake_child_mapping, [good, bad], "c1", ("volume.uuid",)
            )
        assert groups == {("v1",): [good]}
        assert _messages(caplog, logging.WARNING) == [
            "DataSource FakeChild: 1 cached children have no parent ref via "
            "'volume.uuid'; they will pass through unmerged"
        ]

    def test_two_ref_fields_are_joined_in_the_warning(
        self, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        backend = OntapBackend(mock_config)
        mapping = _thing_mapping("/a/{svm.uuid}/b/{group.name}/users")
        good = _ns(svm=_ns(uuid="s1"), group=_ns(name="g1"))
        bad = _ns(svm=_ns(uuid=""), group=_ns(name="g1"))
        with caplog.at_level(logging.WARNING, logger=BACKENDS_LOGGER):
            backend._resolve_parent_uuids(mapping, [good, bad], "c1", ("svm.uuid", "group.name"))
        assert _messages(caplog, logging.WARNING) == [
            "DataSource Thing: 1 cached children have no parent ref via "
            "'svm.uuid, group.name'; they will pass through unmerged"
        ]

    def test_unregistered_parent_warns_and_groups_nothing(
        self, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        backend = OntapBackend(mock_config)
        mapping = _thing_mapping("/a/{svm.uuid}/users", parent_mapping="NoSuchParent")
        child = _ns(svm=None)
        with caplog.at_level(logging.WARNING, logger=BACKENDS_LOGGER):
            groups = backend._resolve_parent_uuids(mapping, [child], "c1", ("svm.uuid",))
        assert groups == {}
        assert _messages(caplog, logging.WARNING) == [
            "DataSource Thing: parent mapping 'NoSuchParent' not found in registry; "
            "cannot resolve parent UUIDs for cache-fallback path"
        ]

    def test_fallback_queries_the_parent_cache_for_the_cluster_and_defaults_to_uuid(
        self, fake_parent_mapping: TypeMapping, mock_config: Any
    ) -> None:
        backend = OntapBackend(mock_config)
        mapping = _thing_mapping("/a/{svm.uuid}/users", parent_mapping="FakeParent")
        assert mapping.effective_parent_id_fields() == ()
        child = _ns(svm=None)
        db = MagicMock()
        db.query_with_filters.return_value = [
            FakeParentModel(uuid="p1", name="n1"),
            FakeParentModel(uuid="", name="n2"),
        ]
        with (
            patch.object(OntapBackend, "_cache_db", new=db),
            patch.object(backend, "_resolve_metadata_path", return_value="storage.fake_parents"),
        ):
            groups = backend._resolve_parent_uuids(mapping, [child], "prod1", ("svm.uuid",))
        assert groups == {("p1",): [child]}
        db.query_with_filters.assert_called_once_with("prod1", "storage.fake_parents", [])


# --------------------------------------------------------------------------- #
# per-parent and per-identifier live fetches
# --------------------------------------------------------------------------- #


class TestFetchLiveByParent:
    @staticmethod
    def _kids(*names: str) -> list[_Thing]:
        return [_Thing(name=n) for n in names]

    def test_urls_fields_chunks_and_skipped_parents(
        self, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        mapping = _thing_mapping(
            "/vols/{vol.uuid}/things?flag=&order=a", batch_size=2, parent_mapping="FakeParent"
        )
        router = _Router(
            [
                ("/vols/v3/", {"records": [{"name": "z", "svm": {"name": "s"}}]}),
                ("/vols/v1/", {"records": [{"name": "a"}]}),
            ]
        )
        backend, factory = _backend(router, mock_config)
        groups: dict[tuple[str, ...], list[_Thing]] = {
            ("v1",): self._kids("a", "b", "c"),
            ("v2",): [_Thing(name="")],
            ("v3",): self._kids("z"),
        }
        with caplog.at_level(logging.DEBUG):
            found = backend._fetch_live_by_parent(
                _Thing, mapping, "c1", groups, "name", ("svm_name", "uuid", "other")
            )
        _assert_cluster(factory)
        assert [t.name for t in found] == ["a", "a", "z"]
        queries = [
            (urlparse(u).path, parse_qs(urlparse(u).query, keep_blank_values=True))
            for u in router.urls
        ]
        fields = {"fields": ["svm.name,uuid,other"], "flag": [""], "order": ["a"]}
        assert queries == [
            ("/vols/v1/things", {**fields, "name": ["a|b"]}),
            ("/vols/v1/things", {**fields, "name": ["c"]}),
            ("/vols/v3/things", {**fields, "name": ["z"]}),
        ]
        parse_logs = _messages(caplog, logging.DEBUG, "pynetappfoundry.cache.field_mapping")
        assert "OntapBackend<Thing> API response: 1 things" in parse_logs
        assert "DataSource Thing[z]: missing fields ['uuid']" in _messages(caplog, logging.DEBUG)

    def test_multi_placeholder_key_fills_every_placeholder(self, mock_config: Any) -> None:
        mapping = _thing_mapping("/a/{svm.uuid}/b/{group.name}/users?fields=*")
        router = _Router([("/a/s1/b/g1/users", {"records": [{"name": "u"}]})])
        backend, _ = _backend(router, mock_config)
        found = backend._fetch_live_by_parent(
            _Thing, mapping, "c1", _group(("s1", "g1"), "u"), "name", ("uuid",)
        )
        assert [t.name for t in found] == ["u"]
        assert parse_qs(urlparse(router.urls[0]).query)["fields"] == ["*"]

    def test_endpoint_without_fields_gets_them_and_star_is_kept_when_present(
        self, mock_config: Any
    ) -> None:
        router = _Router()
        backend, _ = _backend(router, mock_config)
        plain = _thing_mapping("/vols/{vol.uuid}/things")
        backend._fetch_live_by_parent(_Thing, plain, "c1", _group(("v1",), "a"), "name", ("uuid",))
        star = _thing_mapping("/vols/{vol.uuid}/things?fields=*")
        backend._fetch_live_by_parent(_Thing, star, "c1", _group(("v1",), "a"), "name", ("uuid",))
        assert [parse_qs(urlparse(u).query)["fields"] for u in router.urls] == [["uuid"], ["*"]]


class TestFetchLiveByIdentifiers:
    def test_urls_fields_and_chunks(
        self, mock_config: Any, caplog: pytest.LogCaptureFixture
    ) -> None:
        mapping = _thing_mapping("/things?flag=&order=a", batch_size=2)
        router = _Router([("/things", {"records": [{"name": "a", "svm": {"name": "s"}}]})])
        backend, factory = _backend(router, mock_config)
        with caplog.at_level(logging.DEBUG):
            found = backend._fetch_live_by_identifiers(
                _Thing, mapping, "c1", ["a", "b", "c"], "name", ("svm_name", "uuid", "other")
            )
        _assert_cluster(factory)
        assert [t.svm_name for t in found] == ["s", "s"]
        fields = {"fields": ["svm.name,uuid,other"], "flag": [""], "order": ["a"]}
        assert [parse_qs(urlparse(u).query, keep_blank_values=True) for u in router.urls] == [
            {**fields, "name": ["a|b"]},
            {**fields, "name": ["c"]},
        ]
        parse_logs = _messages(caplog, logging.DEBUG, "pynetappfoundry.cache.field_mapping")
        assert "OntapBackend<Thing> API response: 1 things" in parse_logs
        assert "DataSource Thing[a]: missing fields ['uuid']" in _messages(caplog, logging.DEBUG)

    def test_star_fields_are_kept_and_missing_fields_are_added(self, mock_config: Any) -> None:
        router = _Router()
        backend, _ = _backend(router, mock_config)
        backend._fetch_live_by_identifiers(
            _Thing, _thing_mapping("/things?fields=*"), "c1", ["a"], "name", ("uuid",)
        )
        backend._fetch_live_by_identifiers(
            _Thing, _thing_mapping("/things"), "c1", ["a"], "name", ("uuid",)
        )
        assert [parse_qs(urlparse(u).query)["fields"] for u in router.urls] == [["*"], ["uuid"]]
