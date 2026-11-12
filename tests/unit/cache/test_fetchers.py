"""Tests for the generic ``fetch()`` dispatcher (issue #541, ADR-0013 §2)."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.fetchers import (
    fetch,
    normalize_cli_key,
    parse_vm_instance_output,
)
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.cluster.mapping import ONTAPCLUSTER_MAPPING
from pynetappfoundry.cache.ontap.cluster.nodes.mapping import ONTAPNODERESPONSE_MAPPING
from pynetappfoundry.cache.ontap.storage.volumes.mapping import ONTAPVOLUME_MAPPING
from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata
from pynetappfoundry.models.ontap.cluster.model import OntapCluster
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse
from pynetappfoundry.models.ontap.cluster.traits.model import ClusterTraits
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume

# ---------------------------------------------------------------------------
# TypeMapping / registry plumbing
# ---------------------------------------------------------------------------


class TestResponseShapeMetadata:
    """TypeMapping.response_shape default + ONTAPCLUSTER_MAPPING singleton flag."""

    def test_default_response_shape_envelope(self) -> None:
        """Unflagged TypeMappings default to ``"envelope"``."""

        class _M(BaseModel):
            name: str = ""

        tm = TypeMapping(name="X", model_class=_M, api_endpoint="/x")
        assert tm.response_shape == "envelope"

    def test_cluster_mapping_marked_singleton(self) -> None:
        """``ONTAPCLUSTER_MAPPING.response_shape`` is ``"singleton"``."""
        assert ONTAPCLUSTER_MAPPING.response_shape == "singleton"

    def test_nodes_mapping_envelope(self) -> None:
        """The nodes mapping uses the default envelope shape."""
        assert ONTAPNODERESPONSE_MAPPING.response_shape == "envelope"


class TestRegistryReverseLookup:
    """ModelRegistry.get_mapping_by_model_class()."""

    def test_lookup_by_model_class_returns_mapping(self) -> None:
        """Class-keyed lookup returns the registered mapping."""
        # The registered mapping is the overlay-applied copy of the module constant.
        mapping = model_registry.get_mapping_by_model_class(OntapCluster)
        assert mapping is model_registry.get_mapping("OntapCluster")
        assert mapping is not None
        assert mapping.name == ONTAPCLUSTER_MAPPING.name
        assert mapping.model_class is ONTAPCLUSTER_MAPPING.model_class

    def test_lookup_unregistered_class_returns_none(self) -> None:
        """Unregistered classes return ``None``."""

        class _Unregistered(BaseModel):
            pass

        assert model_registry.get_mapping_by_model_class(_Unregistered) is None


# ---------------------------------------------------------------------------
# Singleton fetch path (OntapCluster)
# ---------------------------------------------------------------------------


def _make_api_client(
    *,
    call_endpoint_response: Any = None,
    get_all_records_response: Any = None,
) -> MagicMock:
    """Build a mock ONTAP API client with the two methods fetch() may invoke."""
    client = MagicMock()
    client.call_endpoint = MagicMock(return_value=call_endpoint_response)
    client.get_all_records = MagicMock(return_value=get_all_records_response)
    return client


_CLUSTER_RESPONSE: dict[str, Any] = {
    "name": "cluster1",
    "uuid": "00000000-0000-0000-0000-000000000001",
    "version": {"full": "9.14.1", "generation": 9, "major": 14, "minor": 1},
}

_NODE_UUID_1 = "11111111-1111-1111-1111-111111111111"
_NODE_UUID_2 = "22222222-2222-2222-2222-222222222222"

_NODES_RESPONSE: dict[str, Any] = {
    "records": [
        {"name": "node1", "uuid": _NODE_UUID_1},
        {"name": "node2", "uuid": _NODE_UUID_2},
    ],
    "num_records": 2,
}

_SINGLE_NODE_RESPONSE: dict[str, Any] = {
    "records": [{"name": "node1", "uuid": _NODE_UUID_1}],
    "num_records": 1,
}


class TestFetchSingleton:
    """fetch() singleton path for OntapCluster (response_shape='singleton')."""

    def test_calls_call_endpoint_not_get_all_records(self) -> None:
        """Singleton path uses call_endpoint, never get_all_records."""
        client = _make_api_client(call_endpoint_response=_CLUSTER_RESPONSE)
        # Supply results_cache so the compute_is_ha hook short-circuits.
        result = fetch(
            OntapCluster,
            cluster="c1",
            config=None,
            api_client=client,
            results_cache={"OntapNodeResponse": []},
        )
        assert isinstance(result, OntapCluster)
        assert result.name == "cluster1"
        assert client.call_endpoint.call_count == 1
        assert client.get_all_records.call_count == 0

    def test_singleton_uses_correct_url(self) -> None:
        """The URL passed to call_endpoint is ONTAPCLUSTER_MAPPING.build_collection_url()."""
        client = _make_api_client(call_endpoint_response=_CLUSTER_RESPONSE)
        fetch(
            OntapCluster,
            cluster="c1",
            config=None,
            api_client=client,
            results_cache={"OntapNodeResponse": []},
        )
        called_url = client.call_endpoint.call_args[0][0]
        assert called_url == ONTAPCLUSTER_MAPPING.build_collection_url()

    def test_singleton_runs_compute_is_ha_with_two_nodes(self) -> None:
        """compute_is_ha runs on the singleton result and sets is_ha=True for HA."""
        client = _make_api_client(call_endpoint_response=_CLUSTER_RESPONSE)
        node_a = OntapNodeResponse(name="a")
        node_b = OntapNodeResponse(name="b")
        result = fetch(
            ClusterTraits,
            cluster="c1",
            config=None,
            api_client=client,
            results_cache={"OntapNodeResponse": [node_a, node_b]},
        )
        assert isinstance(result, ClusterTraits)
        assert result.is_ha is True

    def test_singleton_runs_compute_is_ha_with_single_node(self) -> None:
        """is_ha=False when a single node is in the results cache."""
        client = _make_api_client(call_endpoint_response=_CLUSTER_RESPONSE)
        result = fetch(
            ClusterTraits,
            cluster="c1",
            config=None,
            api_client=client,
            results_cache={"OntapNodeResponse": [OntapNodeResponse(name="solo")]},
        )
        assert isinstance(result, ClusterTraits)
        assert result.is_ha is False

    def test_singleton_with_results_cache_does_not_fan_out(self) -> None:
        """Supplying results_cache prevents the recursive nodes fetch."""
        client = _make_api_client(call_endpoint_response=_CLUSTER_RESPONSE)
        # Pre-populated cache → no extra get_all_records call.
        fetch(
            OntapCluster,
            cluster="c1",
            config=None,
            api_client=client,
            results_cache={"OntapNodeResponse": []},
        )
        assert client.get_all_records.call_count == 0

    def test_singleton_without_results_cache_fans_out_to_nodes(self) -> None:
        """No results_cache → fetch() recursively fetches nodes for compute_is_ha."""
        client = MagicMock()
        client.call_endpoint = MagicMock(return_value=_CLUSTER_RESPONSE)
        client.get_all_records = MagicMock(return_value=_NODES_RESPONSE)

        result = fetch(
            ClusterTraits,
            cluster="c1",
            config=None,
            api_client=client,
        )
        assert isinstance(result, ClusterTraits)
        # Two nodes → is_ha=True
        assert result.is_ha is True
        # Recursive call must have happened.
        assert client.get_all_records.call_count >= 1
        urls = [c.args[0] for c in client.get_all_records.call_args_list]
        assert any("/cluster/nodes" in u for u in urls)

    def test_singleton_fan_out_single_node_sets_is_ha_false(self) -> None:
        """Recursive nodes fetch with one node yields is_ha=False."""
        client = MagicMock()
        client.call_endpoint = MagicMock(return_value=_CLUSTER_RESPONSE)
        client.get_all_records = MagicMock(return_value=_SINGLE_NODE_RESPONSE)
        result = fetch(
            ClusterTraits,
            cluster="c1",
            config=None,
            api_client=client,
        )
        assert isinstance(result, ClusterTraits)
        assert result.is_ha is False

    def test_singleton_empty_response_returns_default_instance(self) -> None:
        """A None/empty singleton response yields a default model instance."""
        client = _make_api_client(call_endpoint_response=None)
        result = fetch(
            OntapCluster,
            cluster="c1",
            config=None,
            api_client=client,
            results_cache={"OntapNodeResponse": []},
        )
        assert isinstance(result, OntapCluster)


# ---------------------------------------------------------------------------
# Envelope fetch path (OntapNodeResponse, OntapVolume)
# ---------------------------------------------------------------------------


class TestFetchEnvelope:
    """fetch() envelope path uses get_all_records + parse_api_response."""

    def test_envelope_returns_list(self) -> None:
        """Envelope path returns a list of parsed instances."""
        client = _make_api_client(get_all_records_response=_NODES_RESPONSE)
        result = fetch(
            OntapNodeResponse,
            cluster="c1",
            config=None,
            api_client=client,
        )
        assert isinstance(result, list)
        assert len(result) == 2
        assert client.get_all_records.call_count == 1
        assert client.call_endpoint.call_count == 0

    def test_envelope_uses_correct_url(self) -> None:
        """Envelope path passes the collection URL to get_all_records."""
        client = _make_api_client(get_all_records_response=_NODES_RESPONSE)
        fetch(
            OntapNodeResponse,
            cluster="c1",
            config=None,
            api_client=client,
        )
        called_url = client.get_all_records.call_args[0][0]
        assert called_url == ONTAPNODERESPONSE_MAPPING.build_collection_url()

    def test_envelope_volume_with_realtime_subfields(self) -> None:
        """Volume fetch with inline realtime sub-fields parses successfully."""
        volume_response: dict[str, Any] = {
            "records": [
                {
                    "name": "vol1",
                    "uuid": "vol-uuid-1",
                    "svm": {"name": "svm1", "uuid": "svm-uuid-1"},
                    "size": 1024,
                },
            ],
            "num_records": 1,
        }
        client = _make_api_client(get_all_records_response=volume_response)
        result = fetch(
            OntapVolume,
            cluster="c1",
            config=None,
            api_client=client,
        )
        assert isinstance(result, list)
        assert len(result) == 1
        assert client.get_all_records.call_count == 1
        # Sanity: the URL is the volumes collection URL.
        called_url = client.get_all_records.call_args[0][0]
        assert called_url == ONTAPVOLUME_MAPPING.build_collection_url()


# ---------------------------------------------------------------------------
# Generic FieldMapping.depends_on fan-out (issue #547)
# ---------------------------------------------------------------------------


class _DepA(BaseModel):
    name: str = ""


class _DepB(BaseModel):
    name: str = ""


class _HasDeps(BaseModel):
    name: str = ""
    computed: int = 0


def _hook_two_deps(instance: _HasDeps, results: dict[str, Any]) -> _HasDeps:
    total = len(results.get("_DepA", [])) + len(results.get("_DepB", []))
    return instance.model_copy(update={"computed": total})


_DEP_A_MAPPING = TypeMapping(
    name="_DepA",
    model_class=_DepA,
    api_endpoint="/deps/a?fields=*",
    fields=(FieldMapping(cache_attr="name"),),
)

_DEP_B_MAPPING = TypeMapping(
    name="_DepB",
    model_class=_DepB,
    api_endpoint="/deps/b?fields=*",
    fields=(FieldMapping(cache_attr="name"),),
)

_HAS_DEPS_MAPPING = TypeMapping(
    name="_HasDeps",
    model_class=_HasDeps,
    api_endpoint="/owner?fields=*",
    response_shape="singleton",
    fields=(
        FieldMapping(cache_attr="name"),
        FieldMapping(
            cache_attr="computed",
            cache_strategy="derived",
            default=0,
            post_collection=_hook_two_deps,
            depends_on=(_DepA, _DepB),
        ),
    ),
)


class TestFetchDependsOn:
    """Generic FieldMapping.depends_on fan-out tests."""

    def setup_method(self) -> None:
        model_registry.register_mapping("_DepA", _DEP_A_MAPPING)
        model_registry.register_mapping("_DepB", _DEP_B_MAPPING)
        model_registry.register_mapping("_HasDeps", _HAS_DEPS_MAPPING)

    def teardown_method(self) -> None:
        for name, cls in (("_DepA", _DepA), ("_DepB", _DepB), ("_HasDeps", _HasDeps)):
            model_registry._mappings.pop(name, None)
            model_registry._mappings_by_class.pop(cls, None)

    def test_hook_with_two_dependencies_triggers_two_fetches(self) -> None:
        """Both dependencies fanned out when absent from results_cache."""
        responses = {
            "/owner?fields=*": {"name": "owner1"},
            "/deps/a?fields=*": {"records": [{"name": "a1"}, {"name": "a2"}]},
            "/deps/b?fields=*": {"records": [{"name": "b1"}]},
        }
        client = MagicMock()
        client.call_endpoint = MagicMock(side_effect=lambda url, **kw: responses.get(url))
        client.get_all_records = MagicMock(
            side_effect=lambda url, **kw: responses.get(url, {"records": []})
        )
        result = fetch(_HasDeps, cluster="c1", config=None, api_client=client)
        assert isinstance(result, _HasDeps)
        assert result.computed == 3  # 2 _DepA + 1 _DepB
        assert client.get_all_records.call_count == 2

    def test_deps_in_results_cache_prevent_refetch(self) -> None:
        """Pre-populated results_cache short-circuits the generic fan-out."""
        responses = {"/owner?fields=*": {"name": "owner1"}}
        client = MagicMock()
        client.call_endpoint = MagicMock(side_effect=lambda url, **kw: responses.get(url))
        client.get_all_records = MagicMock(return_value={"records": []})
        result = fetch(
            _HasDeps,
            cluster="c1",
            config=None,
            api_client=client,
            results_cache={
                "_DepA": [_DepA(name="a1")],
                "_DepB": [_DepB(name="b1"), _DepB(name="b2")],
            },
        )
        assert isinstance(result, _HasDeps)
        assert result.computed == 3
        # No dependency fetches should have fired.
        assert client.get_all_records.call_count == 0


# ---------------------------------------------------------------------------
# Parameterized fetch path (synthetic mapping)
# ---------------------------------------------------------------------------


class _ParentParam(BaseModel):
    name: str = ""
    uuid: str = ""


class _ChildParam(BaseModel):
    name: str = ""


_PARENT_PARAM_MAPPING = TypeMapping(
    name="ParentParam",
    model_class=_ParentParam,
    api_endpoint="/parents?fields=*",
    fields=(
        FieldMapping(cache_attr="name"),
        FieldMapping(cache_attr="uuid"),
    ),
)


_CHILD_PARAM_MAPPING = TypeMapping(
    name="ChildParam",
    model_class=_ChildParam,
    api_endpoint="/parents/{parent.uuid}/children?fields=*",
    fields=(FieldMapping(cache_attr="name"),),
    parent_mapping="ParentParam",
    parent_id_field="uuid",
)


class TestFetchParameterized:
    """fetch() parameterized path iterates parents and concatenates children."""

    def setup_method(self) -> None:
        model_registry.register_mapping("ParentParam", _PARENT_PARAM_MAPPING)
        model_registry.register_mapping("ChildParam", _CHILD_PARAM_MAPPING)

    def teardown_method(self) -> None:
        model_registry._mappings.pop("ParentParam", None)
        model_registry._mappings.pop("ChildParam", None)
        model_registry._mappings_by_class.pop(_ParentParam, None)
        model_registry._mappings_by_class.pop(_ChildParam, None)

    def test_parameterized_iterates_parents(self) -> None:
        """fetch() iterates parents from results_cache and aggregates children."""
        parents = [
            _ParentParam(name="p1", uuid="uuid-1"),
            _ParentParam(name="p2", uuid="uuid-2"),
        ]
        responses = {
            "/parents/uuid-1/children?fields=*": {"records": [{"name": "c1"}, {"name": "c2"}]},
            "/parents/uuid-2/children?fields=*": {"records": [{"name": "c3"}]},
        }

        client = MagicMock()
        client.get_all_records = MagicMock(side_effect=lambda url, **kw: responses[url])

        result = fetch(
            _ChildParam,
            cluster="c1",
            config=None,
            api_client=client,
            # Parents are keyed by parent mapping name in results_cache.
            results_cache={"ParentParam": parents},
        )
        assert isinstance(result, list)
        assert [c.name for c in result] == ["c1", "c2", "c3"]
        assert client.get_all_records.call_count == 2


class _MultiParent(BaseModel):
    svm: _ParentParam = _ParentParam()
    name: str = ""


_MULTI_CHILD_MAPPING = TypeMapping(
    name="MultiChild",
    model_class=_ChildParam,
    api_endpoint="/groups/{svm.uuid}/{group.name}/users?fields=*",
    fields=(FieldMapping(cache_attr="name"),),
    parent_mapping="MultiParent",
    parent_id_fields=("svm.uuid", "name"),
)


class TestFetchParameterizedMultiPlaceholder:
    """A two-field child fills both placeholders; a missing value skips the parent."""

    def test_fills_both_placeholders(self) -> None:
        from pynetappfoundry.cache.fetchers import _fetch_parameterized

        parents = [_MultiParent(svm=_ParentParam(uuid="s1"), name="g1")]
        client = MagicMock()
        client.get_all_records = MagicMock(return_value={"records": [{"name": "u1"}]})
        result = _fetch_parameterized(_MULTI_CHILD_MAPPING, parents, client, "[t]")
        assert [c.name for c in result] == ["u1"]  # type: ignore[attr-defined]
        client.get_all_records.assert_called_once_with("/groups/s1/g1/users?fields=*", method="GET")

    def test_missing_second_value_skips_parent(self, caplog: pytest.LogCaptureFixture) -> None:
        import logging

        from pynetappfoundry.cache.fetchers import _fetch_parameterized

        parents = [_MultiParent(svm=_ParentParam(uuid="s1"), name="")]
        client = MagicMock()
        with caplog.at_level(logging.WARNING):
            result = _fetch_parameterized(_MULTI_CHILD_MAPPING, parents, client, "[t]")
        assert result == []
        client.get_all_records.assert_not_called()
        assert any("SKIP_PARENT" in r.message and "'name'" in r.message for r in caplog.records)

    def test_no_parent_fields_raises(self) -> None:
        from pynetappfoundry.cache.fetchers import _fetch_parameterized

        mapping = TypeMapping(
            name="NoFields",
            model_class=_ChildParam,
            api_endpoint="/a/{x}/b",
            parent_mapping="P",
        )
        with pytest.raises(ValueError, match="parent_id_field must be set"):
            _fetch_parameterized(mapping, [], MagicMock(), "[t]")


class _IntIdParent(BaseModel):
    id: int | str | None = None
    name: str = ""


_INT_ID_CHILD_MAPPING = TypeMapping(
    name="IntIdChild",
    model_class=_ChildParam,
    api_endpoint="/parents/{parent.id}/children?fields=*",
    fields=(FieldMapping(cache_attr="name"),),
    parent_mapping="IntIdParent",
    parent_id_field="id",
)

_INT_ID_MULTI_MAPPING = TypeMapping(
    name="IntIdMulti",
    model_class=_ChildParam,
    api_endpoint="/volumes/{volume.id}/qtrees/{qtree.id}/metrics",
    fields=(FieldMapping(cache_attr="name"),),
    parent_mapping="IntIdParent",
    parent_id_fields=("name", "id"),
)


class TestParentIdZero:
    """A falsy but valid parent identifier (0) is substituted, not skipped (#976)."""

    def _run(
        self, mapping: TypeMapping, parent: _IntIdParent, caplog: pytest.LogCaptureFixture
    ) -> tuple[MagicMock, list[object], list[str]]:
        import logging

        from pynetappfoundry.cache.fetchers import _fetch_parameterized

        client = MagicMock()
        client.get_all_records = MagicMock(return_value={"records": [{"name": "c"}]})
        with caplog.at_level(logging.WARNING):
            result = _fetch_parameterized(mapping, [parent], client, "[t]")
        skips = [r.message for r in caplog.records if "SKIP_PARENT" in r.message]
        return client, list(result), skips

    def test_int_zero_is_substituted(self, caplog: pytest.LogCaptureFixture) -> None:
        client, result, skips = self._run(_INT_ID_CHILD_MAPPING, _IntIdParent(id=0), caplog)
        client.get_all_records.assert_called_once_with("/parents/0/children?fields=*", method="GET")
        assert len(result) == 1
        assert skips == []

    def test_none_is_skipped(self, caplog: pytest.LogCaptureFixture) -> None:
        client, result, skips = self._run(_INT_ID_CHILD_MAPPING, _IntIdParent(id=None), caplog)
        client.get_all_records.assert_not_called()
        assert result == []
        assert len(skips) == 1

    def test_empty_string_is_skipped(self, caplog: pytest.LogCaptureFixture) -> None:
        client, result, skips = self._run(_INT_ID_CHILD_MAPPING, _IntIdParent(id=""), caplog)
        client.get_all_records.assert_not_called()
        assert result == []
        assert len(skips) == 1

    def test_multi_placeholder_with_zero_field_is_filled(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        client, result, skips = self._run(
            _INT_ID_MULTI_MAPPING, _IntIdParent(id=0, name="vol1"), caplog
        )
        client.get_all_records.assert_called_once_with(
            "/volumes/vol1/qtrees/0/metrics", method="GET"
        )
        assert len(result) == 1
        assert skips == []


class _GrandParent(BaseModel):
    name: str = ""
    id: str = ""


class _MidParent(BaseModel):
    name: str = ""
    uuid: str = ""


class _Leaf(BaseModel):
    name: str = ""


class _OrphanLeaf(BaseModel):
    name: str = ""


class _CycleA(BaseModel):
    id: str = ""


class _CycleB(BaseModel):
    uuid: str = ""


class _SingletonLeaf(BaseModel):
    enabled: bool = False


_GP_MAPPING = TypeMapping(
    name="GP975",
    model_class=_GrandParent,
    api_endpoint="/gps?fields=*",
    fields=(FieldMapping(cache_attr="name"), FieldMapping(cache_attr="id")),
)
_MID_MAPPING = TypeMapping(
    name="Mid975",
    model_class=_MidParent,
    api_endpoint="/gps/{gp.id}/mids?fields=*",
    fields=(FieldMapping(cache_attr="name"), FieldMapping(cache_attr="uuid")),
    parent_mapping="GP975",
    parent_id_field="id",
)
_LEAF_MAPPING = TypeMapping(
    name="Leaf975",
    model_class=_Leaf,
    api_endpoint="/mids/{mid.uuid}/leaves?fields=*",
    fields=(FieldMapping(cache_attr="name"),),
    parent_mapping="Mid975",
    parent_id_field="uuid",
)
_SINGLETON_LEAF_MAPPING = TypeMapping(
    name="SLeaf975",
    model_class=_SingletonLeaf,
    api_endpoint="/mids/{mid.uuid}/setting",
    fields=(FieldMapping(cache_attr="enabled"),),
    parent_mapping="Mid975",
    parent_id_field="uuid",
    response_shape="singleton",
)
_ORPHAN_MAPPING = TypeMapping(
    name="Orphan975",
    model_class=_OrphanLeaf,
    api_endpoint="/x/{y.id}/z",
    fields=(FieldMapping(cache_attr="name"),),
    parent_mapping="NoSuchParent975",
    parent_id_field="id",
)
_CYCLE_A = TypeMapping(
    name="CycleA975",
    model_class=_CycleA,
    api_endpoint="/a/{b.id}",
    fields=(FieldMapping(cache_attr="id"),),
    parent_mapping="CycleB975",
    parent_id_field="id",
)
_CYCLE_B = TypeMapping(
    name="CycleB975",
    model_class=_CycleB,
    api_endpoint="/b/{a.id}",
    fields=(FieldMapping(cache_attr="uuid"),),
    parent_mapping="CycleA975",
    parent_id_field="uuid",
)

_ALL_975 = (
    _GP_MAPPING,
    _MID_MAPPING,
    _LEAF_MAPPING,
    _SINGLETON_LEAF_MAPPING,
    _ORPHAN_MAPPING,
    _CYCLE_A,
    _CYCLE_B,
)


class TestFetchParentsOnDemand:
    """A child fetch fetches its missing parents, recursively (#975)."""

    def setup_method(self) -> None:
        for m in _ALL_975:
            model_registry.register_mapping(m.name, m)

    def teardown_method(self) -> None:
        for m in _ALL_975:
            model_registry._mappings.pop(m.name, None)
            model_registry._mappings_by_class.pop(m.model_class, None)

    @staticmethod
    def _client(responses: dict[str, Any]) -> MagicMock:
        client = MagicMock()
        client.get_all_records = MagicMock(side_effect=lambda url, **kw: responses[url])
        return client

    def test_fetches_parents_then_children(self) -> None:
        client = self._client(
            {
                "/mids/u1/leaves?fields=*": {"records": [{"name": "a"}, {"name": "b"}]},
                "/mids/u2/leaves?fields=*": {"records": [{"name": "c"}]},
            }
        )
        cache: dict[str, Any] = {
            "Mid975": [_MidParent(name="m1", uuid="u1"), _MidParent(name="m2", uuid="u2")]
        }
        result = fetch(_Leaf, cluster="c", config=None, api_client=client, results_cache=cache)
        assert isinstance(result, list)
        assert [r.name for r in result] == ["a", "b", "c"]

    def test_missing_parents_are_fetched_and_cached(self) -> None:
        client = self._client(
            {
                "/gps?fields=*": {"records": [{"name": "g", "id": "g1"}]},
                "/gps/g1/mids?fields=*": {"records": [{"name": "m1", "uuid": "u1"}]},
                "/mids/u1/leaves?fields=*": {"records": [{"name": "a"}]},
            }
        )
        cache: dict[str, Any] = {}
        result = fetch(_Leaf, cluster="c", config=None, api_client=client, results_cache=cache)
        assert isinstance(result, list)
        assert [r.name for r in result] == ["a"]
        assert [m.uuid for m in cache["Mid975"]] == ["u1"]
        assert [g.id for g in cache["GP975"]] == ["g1"]
        urls = [c.args[0] for c in client.get_all_records.call_args_list]
        assert urls == ["/gps?fields=*", "/gps/g1/mids?fields=*", "/mids/u1/leaves?fields=*"]
        assert not any("{" in u or "}" in u for u in urls)

    def test_cached_parents_not_refetched(self) -> None:
        client = self._client({"/mids/u1/leaves?fields=*": {"records": [{"name": "a"}]}})
        cache: dict[str, Any] = {"Mid975": [_MidParent(uuid="u1")]}
        fetch(_Leaf, cluster="c", config=None, api_client=client, results_cache=cache)
        fetch(_Leaf, cluster="c", config=None, api_client=client, results_cache=cache)
        assert client.get_all_records.call_count == 2  # leaves only, no parent request

    def test_empty_cached_parents_mean_no_request(self) -> None:
        client = self._client({})
        result = fetch(
            _Leaf, cluster="c", config=None, api_client=client, results_cache={"Mid975": []}
        )
        assert result == []
        client.get_all_records.assert_not_called()

    def test_unregistered_parent_raises_before_request(self) -> None:
        from pynetappfoundry.cache.fetchers import fetch_parents

        client = MagicMock()
        with pytest.raises(ValueError, match="not registered"):
            fetch_parents(_ORPHAN_MAPPING, client, {})
        client.get_all_records.assert_not_called()

    def test_cycle_raises_before_request(self) -> None:
        from pynetappfoundry.cache.fetchers import fetch_parents

        client = MagicMock()
        with pytest.raises(ValueError, match="cycle"):
            fetch_parents(_CYCLE_A, client, {})
        client.get_all_records.assert_not_called()

    def test_singleton_child_one_call_per_parent(self) -> None:
        client = MagicMock()
        client.call_endpoint = MagicMock(return_value={"enabled": True})
        cache: dict[str, Any] = {"Mid975": [_MidParent(uuid="u1"), _MidParent(uuid="u2")]}
        result = fetch(
            _SingletonLeaf, cluster="c", config=None, api_client=client, results_cache=cache
        )
        assert isinstance(result, list)
        assert len(result) == 2
        assert [c.args[0] for c in client.call_endpoint.call_args_list] == [
            "/mids/u1/setting",
            "/mids/u2/setting",
        ]

    def test_iter_parent_urls_warns_on_skip(self, caplog: pytest.LogCaptureFixture) -> None:
        import logging

        from pynetappfoundry.cache.fetchers import iter_parent_urls

        parents = [_MidParent(uuid="u1"), _MidParent(name="bad", uuid="")]
        with caplog.at_level(logging.WARNING):
            pairs = list(iter_parent_urls(_LEAF_MAPPING, parents, "[t]"))
        assert [url for _, url in pairs] == ["/mids/u1/leaves?fields=*"]
        assert any("SKIP_PARENT" in r.message for r in caplog.records)


# ---------------------------------------------------------------------------
# CLI parsing helpers (extracted from collector, issue #532)
# ---------------------------------------------------------------------------


class TestNormalizeCliKey:
    """normalize_cli_key() converts CLI keys to snake_case."""

    def test_spaces_to_underscores(self) -> None:
        assert normalize_cli_key("Instance ID") == "instance_id"

    def test_hyphens_to_underscores(self) -> None:
        assert normalize_cli_key("cpu-platform") == "cpu_platform"

    def test_strips_special_chars(self) -> None:
        assert normalize_cli_key("Region (AWS)") == "region_aws"

    def test_lowercase(self) -> None:
        assert normalize_cli_key("Node") == "node"


class TestParseVmInstanceOutput:
    """parse_vm_instance_output() parses CLI key-value lines into records."""

    def test_two_nodes(self) -> None:
        output = [
            "Node: node-01",
            "Instance ID: i-abc",
            "Provider: AWS",
            "",
            "Node: node-02",
            "Instance ID: i-def",
            "Provider: AWS",
        ]
        records = parse_vm_instance_output(output)
        assert len(records) == 2
        assert records[0]["node"] == "node-01"
        assert records[0]["instance_id"] == "i-abc"
        assert records[1]["node"] == "node-02"
        assert records[1]["instance_id"] == "i-def"

    def test_single_node(self) -> None:
        output = [
            "Node: solo",
            "Region: us-east-1",
        ]
        records = parse_vm_instance_output(output)
        assert len(records) == 1
        assert records[0]["node"] == "solo"
        assert records[0]["region"] == "us-east-1"

    def test_empty_output(self) -> None:
        assert parse_vm_instance_output([]) == []

    def test_no_node_field_creates_single_entry(self) -> None:
        output = ["Region: us-east-1", "Provider: AWS"]
        records = parse_vm_instance_output(output)
        assert len(records) == 1
        assert records[0]["node"] == ""

    def test_skips_blank_and_no_colon_lines(self) -> None:
        output = [
            "Node: n1",
            "",
            "---separator---",
            "Region: eu-west-1",
        ]
        records = parse_vm_instance_output(output)
        assert len(records) == 1
        assert records[0]["region"] == "eu-west-1"


# ---------------------------------------------------------------------------
# CLI dispatch (issue #532)
# ---------------------------------------------------------------------------


class _CliModel(BaseModel):
    name: str = ""


_CLI_MAPPING = TypeMapping(
    name="CliMapping",
    model_class=_CliModel,
    api_endpoint="/never",
    cli_command="something show",
    fields=(FieldMapping(cache_attr="name", cli_field="name"),),
)


class TestFetchCliDispatch:
    """CLI dispatch via _fetch_cli (#532)."""

    def setup_method(self) -> None:
        model_registry.register_mapping("CliMapping", _CLI_MAPPING)

    def teardown_method(self) -> None:
        model_registry._mappings.pop("CliMapping", None)
        model_registry._mappings_by_class.pop(_CliModel, None)

    def test_cli_without_client_raises_value_error(self) -> None:
        """fetch() with cli_command but no cli_client raises ValueError."""
        client = MagicMock()
        with pytest.raises(ValueError, match="requires cli_client"):
            fetch(
                _CliModel,
                cluster="c1",
                config=None,
                api_client=client,
            )

    def test_cli_dispatch_parses_output(self) -> None:
        """fetch() dispatches to CLI path and returns parsed instances."""
        api_client = MagicMock()
        cli_client = MagicMock()
        cli_client.run_command.return_value = [
            "Node: n1",
            "Name: alpha",
            "",
            "Node: n2",
            "Name: beta",
        ]
        result = fetch(
            _CliModel,
            cluster="c1",
            config=None,
            api_client=api_client,
            cli_client=cli_client,
        )
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].name == "alpha"
        assert result[1].name == "beta"
        cli_client.run_command.assert_called_once_with("something show")
        # API client should not be called for CLI-only mappings.
        api_client.call_endpoint.assert_not_called()
        api_client.get_all_records.assert_not_called()


class TestFetchCloudMetadataViaFetch:
    """Integration test: fetch(CloudMetadata) with a mock CLI client."""

    def test_cloud_metadata_fetch_returns_instances(self) -> None:
        """fetch(CloudMetadata, ...) returns CloudMetadata with link fields."""
        api_client = MagicMock()
        cli_client = MagicMock()
        cli_client.run_command.return_value = [
            "Node: cvo-node-01",
            "Instance ID: i-0123456789abcdef0",
            "Account ID: 123456789012",
            "Provider: AWS",
            "Region: us-east-1",
        ]
        result = fetch(
            CloudMetadata,
            cluster="c1",
            config=None,
            api_client=api_client,
            cli_client=cli_client,
        )
        assert isinstance(result, list)
        assert len(result) == 1
        cm = result[0]
        assert isinstance(cm, CloudMetadata)
        assert cm.node == "cvo-node-01"
        assert cm.instance_id == "i-0123456789abcdef0"
        assert cm.provider == "AWS"
        # instance_link should be populated by the post_collection hook.
        assert "i-0123456789abcdef0" in cm.instance_link


# ---------------------------------------------------------------------------
# Side-effect check: fetch() never persists to the cache substrate
# ---------------------------------------------------------------------------


class TestFetchDoesNotPersist:
    """fetch() must never write to the cache DB layer (ADR-0013 §4)."""

    def test_no_db_set_calls_singleton(self) -> None:
        """Singleton fetch path does not invoke ClusterMetadataDB.set()."""
        client = _make_api_client(call_endpoint_response=_CLUSTER_RESPONSE)
        with patch("pynetappfoundry.cache.db.ClusterMetadataDB.set", autospec=True) as mock_set:
            fetch(
                OntapCluster,
                cluster="c1",
                config=None,
                api_client=client,
                results_cache={"OntapNodeResponse": []},
            )
            assert mock_set.call_count == 0

    def test_no_db_set_calls_envelope(self) -> None:
        """Envelope fetch path does not invoke ClusterMetadataDB.set()."""
        client = _make_api_client(get_all_records_response=_NODES_RESPONSE)
        with patch("pynetappfoundry.cache.db.ClusterMetadataDB.set", autospec=True) as mock_set:
            fetch(
                OntapNodeResponse,
                cluster="c1",
                config=None,
                api_client=client,
            )
            assert mock_set.call_count == 0


# ---------------------------------------------------------------------------
# Unregistered model class
# ---------------------------------------------------------------------------


class _NeverRegistered(BaseModel):
    pass


class TestFetchUnregistered:
    def test_unregistered_class_raises_value_error(self) -> None:
        """Calling fetch() on an unregistered model class raises ValueError."""
        client = MagicMock()
        with pytest.raises(ValueError, match="no TypeMapping registered"):
            fetch(
                _NeverRegistered,
                cluster="c1",
                config=None,
                api_client=client,
            )


# ---------------------------------------------------------------------------
# computed mappings: ClusterTraits (#967, ADR-0024)
# ---------------------------------------------------------------------------


class TestFetchComputed:
    """``fetch(ClusterTraits)`` builds the model from nodes without a traits endpoint."""

    @staticmethod
    def _client(nodes: list[dict[str, Any]]) -> MagicMock:
        client = MagicMock()
        client.get_all_records = MagicMock(return_value={"records": nodes})
        return client

    def test_two_nodes_from_results_cache_is_ha_without_api_call(self) -> None:
        client = self._client([])
        cache = {"OntapNodeResponse": [OntapNodeResponse(name="n1"), OntapNodeResponse(name="n2")]}
        result = fetch(
            ClusterTraits, cluster="c", config=None, api_client=client, results_cache=cache
        )
        assert isinstance(result, ClusterTraits)
        assert result.is_ha is True
        assert result.is_cloud is False
        client.get_all_records.assert_not_called()
        client.call_endpoint.assert_not_called()

    def test_without_cache_fetches_nodes_once(self) -> None:
        client = self._client([{"name": "n1"}, {"name": "n2"}])
        result = fetch(ClusterTraits, cluster="c", config=None, api_client=client)
        assert isinstance(result, ClusterTraits)
        assert result.is_ha is True
        assert client.get_all_records.call_count == 1
        assert "/cluster/nodes" in client.get_all_records.call_args.args[0]

    @pytest.mark.parametrize(
        ("model", "serial"),
        [("CDvM200", ""), ("", "9092014567"), ("", "9092013001")],
    )
    def test_cvo_nodes_are_cloud(self, model: str, serial: str) -> None:
        node = OntapNodeResponse(name="n", model_=model, serial_number=serial)
        result = fetch(
            ClusterTraits,
            cluster="c",
            config=None,
            api_client=MagicMock(),
            results_cache={"OntapNodeResponse": [node]},
        )
        assert isinstance(result, ClusterTraits)
        assert result.is_cloud is True
        assert result.is_ha is False

    def test_onprem_node_is_not_cloud(self) -> None:
        node = OntapNodeResponse(name="n", model_="FAS8200", serial_number="721000")
        result = fetch(
            ClusterTraits,
            cluster="c",
            config=None,
            api_client=MagicMock(),
            results_cache={"OntapNodeResponse": [node]},
        )
        assert isinstance(result, ClusterTraits)
        assert result.is_cloud is False


class TestClusterTraitsRegistration:
    """The mapping is registered and indexed under the class name."""

    def test_get_mapping_by_name_and_class(self) -> None:
        by_name = model_registry.get_mapping("ClusterTraits")
        by_class = model_registry.get_mapping_by_model_class(ClusterTraits)
        assert by_name is not None
        assert by_name is by_class
        assert by_name.is_computed is True
        assert by_name.api_endpoint == ""

    def test_index_entry_has_no_overlay(self) -> None:
        from pynetappfoundry.cache._mapping_index import MAPPING_INDEX

        module, model_module, qualname, overlay = MAPPING_INDEX["ClusterTraits"]
        assert module == "pynetappfoundry.cache.ontap.cluster.traits.mapping"
        assert (model_module, qualname) == (ClusterTraits.__module__, "ClusterTraits")
        assert overlay is None

    def test_moved_names_import_from_traits_mapping(self) -> None:
        """The hooks and CVO helpers live in ``traits.mapping`` (#967 Part B)."""
        from pynetappfoundry.cache.ontap.cluster.traits import mapping as traits_mapping

        for name in (
            "compute_is_ha",
            "compute_is_cloud",
            "_is_cloud_node",
            "_CLOUD_MODEL_PREFIXES",
            "_CLOUD_SERIAL_PREFIXES",
        ):
            assert hasattr(traits_mapping, name)
