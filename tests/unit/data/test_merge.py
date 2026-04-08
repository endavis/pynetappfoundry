"""Tests for pynetappfoundry.data._merge.merge_models."""

from __future__ import annotations

import pytest

from pynetappfoundry.data._merge import merge_models
from pynetappfoundry.models._base import OntapModel


class _Vol(OntapModel):
    name: str = ""
    size: int = 0
    iops: float = 0.0


class _OtherModel(OntapModel):
    name: str = ""


class TestMergeModels:
    def test_merge_disjoint_field_sets(self) -> None:
        cached = _Vol(name="vol1", size=100)
        cached._fetched_fields.update({"name", "size"})
        live = _Vol(iops=42.5)
        live._fetched_fields.add("iops")

        merged = merge_models(cached, live)
        assert merged.name == "vol1"
        assert merged.size == 100
        assert merged.iops == 42.5
        assert merged._fetched_fields == {"name", "size", "iops"}

    def test_merge_overlapping_fields_live_wins(self) -> None:
        cached = _Vol(name="vol1", size=100)
        cached._fetched_fields.update({"name", "size"})
        live = _Vol(name="vol1-live", size=999)
        live._fetched_fields.update({"name", "size"})

        merged = merge_models(cached, live)
        assert merged.name == "vol1-live"
        assert merged.size == 999

    def test_merge_preserves_model_class(self) -> None:
        cached = _Vol(name="a")
        live = _Vol(name="b")
        merged = merge_models(cached, live)
        assert type(merged) is _Vol

    def test_merge_unions_fetched_fields(self) -> None:
        cached = _Vol()
        cached._fetched_fields.update({"a", "b"})
        live = _Vol()
        live._fetched_fields.update({"b", "c"})
        merged = merge_models(cached, live)
        assert merged._fetched_fields == {"a", "b", "c"}

    def test_merge_different_classes_raises(self) -> None:
        a = _Vol(name="x")
        b = _OtherModel(name="x")
        with pytest.raises(TypeError, match="different classes"):
            merge_models(a, b)  # type: ignore[arg-type]
