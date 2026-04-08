"""Tests for pynetappfoundry.data._routing.decide_path."""

from __future__ import annotations

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.data._routing import RoutingDecision, decide_path


class _Sample(BaseModel):
    """Synthetic model for routing tests."""

    name: str = ""
    size: int = 0
    files_scanned: int = 0
    iops: float = 0.0
    is_root: bool = False


@pytest.fixture
def mapping() -> TypeMapping:
    """A synthetic TypeMapping covering all four FieldMapping flavors."""
    return TypeMapping(
        name="Sample",
        model_class=_Sample,
        api_endpoint="/sample?fields=*",
        fields=(
            FieldMapping(cache_attr="name", cache_strategy="cache"),
            FieldMapping(cache_attr="size", cache_strategy="cache"),
            FieldMapping(
                cache_attr="files_scanned",
                cache_strategy="cache",
                requires_explicit_fetch=True,
            ),
            FieldMapping(cache_attr="iops", cache_strategy="realtime"),
            FieldMapping(cache_attr="is_root", cache_strategy="derived"),
        ),
        identifier_field="name",
    )


class TestDecidePathAuto:
    def test_auto_pure_cache(self, mapping: TypeMapping) -> None:
        decision = decide_path(mapping, ["name", "size"], "auto")
        assert decision.cache_fields == ("name", "size")
        assert decision.live_fields == ()
        assert decision.partial is False

    def test_auto_with_realtime_field_explicit(self, mapping: TypeMapping) -> None:
        decision = decide_path(mapping, ["name", "iops"], "auto")
        assert decision.cache_fields == ("name",)
        assert decision.live_fields == ("iops",)
        assert decision.partial is True

    def test_auto_with_realtime_field_not_requested_excluded(self, mapping: TypeMapping) -> None:
        # requested_fields=None: realtime fields must NOT appear at all.
        decision = decide_path(mapping, None, "auto")
        assert "iops" not in decision.cache_fields
        assert "iops" not in decision.live_fields

    def test_auto_with_explicit_fetch_field_not_requested_excluded(
        self, mapping: TypeMapping
    ) -> None:
        decision = decide_path(mapping, None, "auto")
        assert "files_scanned" not in decision.cache_fields
        assert "files_scanned" not in decision.live_fields

    def test_auto_with_explicit_fetch_field_requested(self, mapping: TypeMapping) -> None:
        decision = decide_path(mapping, ["files_scanned"], "auto")
        assert decision.cache_fields == ()
        assert decision.live_fields == ("files_scanned",)


class TestDecidePathCache:
    def test_cache_raises_on_realtime_field(self, mapping: TypeMapping) -> None:
        with pytest.raises(ValueError, match="iops"):
            decide_path(mapping, ["name", "iops"], "cache")

    def test_cache_allows_derived(self, mapping: TypeMapping) -> None:
        decision = decide_path(mapping, ["name", "is_root"], "cache")
        assert decision.cache_fields == ("name", "is_root")
        assert decision.live_fields == ()

    def test_cache_allows_explicit_fetch(self, mapping: TypeMapping) -> None:
        # An explicit-fetch field is still cache_strategy="cache" -- legal.
        decision = decide_path(mapping, ["files_scanned"], "cache")
        assert decision.cache_fields == ("files_scanned",)


class TestDecidePathLive:
    def test_live_raises_on_derived_field(self, mapping: TypeMapping) -> None:
        with pytest.raises(ValueError, match="is_root"):
            decide_path(mapping, ["name", "is_root"], "live")

    def test_live_allows_realtime_and_cache(self, mapping: TypeMapping) -> None:
        decision = decide_path(mapping, ["name", "iops"], "live")
        assert decision.cache_fields == ()
        assert decision.live_fields == ("name", "iops")


class TestDefaultFieldSet:
    def test_default_field_set(self, mapping: TypeMapping) -> None:
        decision = decide_path(mapping, None, "auto")
        # Default = cache (non-explicit-fetch) + derived. No realtime, no
        # explicit-fetch.
        assert "name" in decision.cache_fields
        assert "size" in decision.cache_fields
        assert "is_root" in decision.cache_fields
        assert "files_scanned" not in decision.cache_fields
        assert "iops" not in decision.cache_fields
        assert decision.live_fields == ()


def test_routing_decision_partial_false_when_only_cache() -> None:
    rd = RoutingDecision(cache_fields=("a",), live_fields=())
    assert rd.partial is False


def test_routing_decision_partial_false_when_only_live() -> None:
    rd = RoutingDecision(cache_fields=(), live_fields=("a",))
    assert rd.partial is False
