"""Characterization tests for ``_fetch_live_groups`` (#965).

``test_query.py`` always patches ``_fetch_live_groups`` out, so the nesting
it does with dotted registry paths is pinned here.
"""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock, patch

from pynetappfoundry.cache.db_schema import _ensure_registry
from pynetappfoundry.cli.commands.cache.query import _fetch_live_groups


class _Result:
    """Fake query result exposing ``model_dump``."""

    def __init__(self, dump: dict[str, Any]) -> None:
        self._dump = dump

    def model_dump(self) -> dict[str, Any]:
        return self._dump


def _run(
    groups: set[str],
    results: dict[str, list[_Result]],
) -> dict[str, Any]:
    """Run ``_fetch_live_groups`` with a fake DataSource keyed by model name."""
    ds = MagicMock()
    ds.query.side_effect = lambda model_class, **_kw: iter(results.get(model_class.__name__, []))
    with (
        patch("pynetappfoundry.cli.commands.cache.query.DataSource", return_value=ds),
        patch(
            "pynetappfoundry.cli.commands.cache.query.model_registry.get_mapping",
            return_value=object(),
        ),
    ):
        data = _fetch_live_groups(MagicMock(), "c1", groups)
    data.pop("cached_at")
    return data


def test_storage_group_nests_under_relative_paths() -> None:
    result = _run(
        {"storage"},
        {
            "OntapVolume": [_Result({"name": "vol1"}), _Result({"name": "vol2"})],
            "OntapAggregate": [_Result({"name": "aggr1"})],
        },
    )

    storage_paths = [p[len("storage.") :] for p in _ensure_registry() if p.startswith("storage.")]
    expected_storage: dict[str, Any] = {p: [] for p in storage_paths}
    expected_storage["volumes"] = [{"name": "vol1"}, {"name": "vol2"}]
    expected_storage["aggregates"] = [{"name": "aggr1"}]
    assert json.dumps(result) == json.dumps({"cluster_name": "c1", "storage": expected_storage})
    assert result["storage"]["volumes"] == [{"name": "vol1"}, {"name": "vol2"}]
    assert next(iter(result["storage"])) == "aggregates"


def test_network_container_replaces_children() -> None:
    """``network`` follows its children in the registry and overwrites them."""
    result = _run(
        {"network"},
        {
            "OntapDns": [_Result({"servers": ["10.0.0.1"]})],
            "NetworkInfo": [_Result({"dns": [], "ipspaces": []})],
        },
    )

    assert json.dumps(result) == json.dumps(
        {"cluster_name": "c1", "network": {"dns": [], "ipspaces": []}}
    )


def test_network_children_nest_when_container_has_no_result() -> None:
    result = _run({"network"}, {"OntapDns": [_Result({"servers": ["10.0.0.1"]})]})

    # NetworkInfo is a singleton with no results -> {} replaces the children.
    assert result["network"] == {}


def test_list_spec_without_results_is_empty_list() -> None:
    result = _run({"cloud"}, {})

    assert result["cloud"] == []


def test_singleton_spec_without_results_is_empty_dict() -> None:
    result = _run({"cluster"}, {})

    assert result["cluster"] == {}


def test_unknown_group_skipped() -> None:
    result = _run({"nonexistent"}, {})

    assert result == {"cluster_name": "c1"}
