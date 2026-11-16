"""Tests for pynetappfoundry.data._per_parent.fetch_per_parent."""

from __future__ import annotations

import logging
from collections.abc import Iterator, Sequence
from typing import Any

import pytest

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.data._per_parent import fetch_per_parent
from pynetappfoundry.data._routing import RoutingDecision
from pynetappfoundry.models._base import OntapModel


class PerParentParent(OntapModel):
    """Synthetic parent model."""

    key: str | None = None
    name: str = ""


class PerParentChild(OntapModel):
    """Synthetic child model."""

    key: str = ""


def _mapping(**overrides: Any) -> TypeMapping:
    kwargs: dict[str, Any] = {
        "name": "PerParentChild",
        "model_class": PerParentChild,
        "api_endpoint": "/parents/{key}/children",
        "api_type": "aiqum",
        "identifier_field": "key",
        "fields": (FieldMapping(cache_attr="key"),),
        "parent_mapping": "PerParentParent",
        "parent_id_field": "key",
    }
    kwargs.update(overrides)
    return TypeMapping(**kwargs)


@pytest.fixture
def parent_registered() -> Iterator[None]:
    m = TypeMapping(
        name="PerParentParent",
        model_class=PerParentParent,
        api_endpoint="/parents",
        api_type="aiqum",
        identifier_field="key",
        fields=(FieldMapping(cache_attr="key"), FieldMapping(cache_attr="name")),
    )
    model_registry.register_mapping("PerParentParent", m)
    try:
        yield
    finally:
        model_registry._mappings.pop("PerParentParent", None)
        model_registry._mappings_by_class.pop(PerParentParent, None)


def _run(
    parents: Sequence[PerParentParent],
    calls: list[dict[str, str]],
    *,
    mapping: TypeMapping | None = None,
    placeholders: list[str] | None = None,
    encode: bool = False,
    max_parents: int | None = None,
    fail_on: str | None = None,
) -> list[Any]:
    def query_parents(_pm: TypeMapping, _decision: RoutingDecision) -> Sequence[PerParentParent]:
        return parents

    def fetch_child(path_params: dict[str, str]) -> list[Any]:
        calls.append(path_params)
        if path_params["key"] == fail_on:
            raise RuntimeError("boom")
        return [{"key": path_params["key"]}, {"key": path_params["key"] + "-2"}]

    return fetch_per_parent(
        mapping or _mapping(),
        placeholders if placeholders is not None else ["key"],
        query_parents=query_parents,
        fetch_child=fetch_child,
        log_prefix="Test",
        encode=encode,
        max_parents=max_parents,
    )


@pytest.mark.usefixtures("parent_registered")
class TestFetchPerParent:
    def test_ordered_concatenation(self) -> None:
        calls: list[dict[str, str]] = []
        out = _run([PerParentParent(key="a"), PerParentParent(key="b")], calls)
        assert calls == [{"key": "a"}, {"key": "b"}]
        assert [r["key"] for r in out] == ["a", "a-2", "b", "b-2"]

    def test_encode_off_passes_raw_value(self) -> None:
        calls: list[dict[str, str]] = []
        _run([PerParentParent(key="a,b")], calls)
        assert calls == [{"key": "a,b"}]

    def test_encode_on_percent_encodes(self) -> None:
        calls: list[dict[str, str]] = []
        _run([PerParentParent(key="a,b/c")], calls, encode=True)
        assert calls == [{"key": "a%2Cb%2Fc"}]

    def test_encode_failure_skips_parent(self, caplog: pytest.LogCaptureFixture) -> None:
        calls: list[dict[str, str]] = []
        with caplog.at_level(logging.WARNING):
            out = _run([PerParentParent(key=".."), PerParentParent(key="ok")], calls, encode=True)
        assert calls == [{"key": "ok"}]
        assert len(out) == 2
        assert "CHILD_FETCH_FAILED" in caplog.text

    def test_no_cap_by_default(self) -> None:
        calls: list[dict[str, str]] = []
        _run([PerParentParent(key=str(i)) for i in range(30)], calls)
        assert len(calls) == 30

    def test_cap_exceeded_raises_before_any_call(self) -> None:
        calls: list[dict[str, str]] = []
        with pytest.raises(ValueError, match="max_parent_requests=1"):
            _run([PerParentParent(key="a"), PerParentParent(key="b")], calls, max_parents=1)
        assert calls == []

    def test_cap_counts_usable_parents_only(self) -> None:
        calls: list[dict[str, str]] = []
        _run([PerParentParent(key="a"), PerParentParent()], calls, max_parents=1)
        assert calls == [{"key": "a"}]

    def test_zero_cap_unlimited(self) -> None:
        calls: list[dict[str, str]] = []
        _run([PerParentParent(key="a"), PerParentParent(key="b")], calls, max_parents=0)
        assert len(calls) == 2

    def test_child_failure_logged_and_skipped(self, caplog: pytest.LogCaptureFixture) -> None:
        calls: list[dict[str, str]] = []
        with caplog.at_level(logging.WARNING):
            out = _run(
                [PerParentParent(key="bad", name="p-bad"), PerParentParent(key="ok")],
                calls,
                fail_on="bad",
            )
        assert [r["key"] for r in out] == ["ok", "ok-2"]
        assert "Test CHILD_FETCH_FAILED: PerParentChild for parent p-bad - RuntimeError: boom" in (
            caplog.text
        )

    def test_id_count_mismatch_raises_before_any_call(self) -> None:
        calls: list[dict[str, str]] = []
        with pytest.raises(ValueError, match="parent id field"):
            _run([PerParentParent(key="a")], calls, placeholders=["key", "other"])
        assert calls == []

    def test_unregistered_parent_raises(self) -> None:
        calls: list[dict[str, str]] = []
        with pytest.raises(ValueError, match="not registered"):
            _run([], calls, mapping=_mapping(parent_mapping="Missing"))
        assert calls == []
