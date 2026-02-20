"""Tests for cache.overlay_loader module."""

from __future__ import annotations

import tomllib

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import ModelRegistry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.overlay_loader import (
    apply_overlay_to_mapping,
    discover_toml_overlays,
    load_overlay,
    load_overlays,
    merge_overlays,
)


class _DummyModel(BaseModel):
    name: str = ""
    size: int = 0
    state: str = ""


def _make_mapping(
    *,
    name: str = "DummyModel",
    fields: tuple[FieldMapping, ...] | None = None,
) -> TypeMapping:
    if fields is None:
        fields = (
            FieldMapping(cache_attr="name", api_path="name"),
            FieldMapping(cache_attr="size", api_path="size"),
            FieldMapping(
                cache_attr="state",
                api_path="state",
                cache_strategy="cache",
                requires_explicit_fetch=True,
            ),
        )
    return TypeMapping(
        name=name,
        model_class=_DummyModel,
        api_endpoint="/test",
        fields=fields,
    )


def _write_toml(path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


class TestDiscoverTomlOverlays:
    """Tests for discover_toml_overlays."""

    def test_discovers_overlays_in_tree(self, tmp_path):
        _write_toml(
            tmp_path / "storage" / "volumes" / "volumes.toml",
            '[endpoint]\nclass_name = "OntapVolume"\n\n[fields.name]\ncache_strategy = "cache"\n',
        )
        _write_toml(
            tmp_path / "cluster" / "nodes" / "nodes.toml",
            '[endpoint]\nclass_name = "OntapNodeResponse"\n\n'
            '[fields.state]\ncache_strategy = "realtime"\n',
        )
        result = discover_toml_overlays(tmp_path)
        assert result == {
            "OntapVolume": tmp_path / "storage" / "volumes" / "volumes.toml",
            "OntapNodeResponse": tmp_path / "cluster" / "nodes" / "nodes.toml",
        }

    def test_skips_toml_without_class_name(self, tmp_path):
        _write_toml(
            tmp_path / "no_endpoint.toml",
            '[fields.name]\ncache_strategy = "cache"\n',
        )
        _write_toml(
            tmp_path / "empty_endpoint.toml",
            '[endpoint]\npath = "/test"\n',
        )
        result = discover_toml_overlays(tmp_path)
        assert result == {}

    def test_returns_empty_for_empty_dir(self, tmp_path):
        result = discover_toml_overlays(tmp_path)
        assert result == {}

    def test_returns_empty_for_nonexistent_dir(self, tmp_path):
        result = discover_toml_overlays(tmp_path / "nonexistent")
        assert result == {}

    def test_warns_on_duplicate_class_name(self, tmp_path, caplog):
        _write_toml(
            tmp_path / "a" / "first.toml",
            '[endpoint]\nclass_name = "Dup"\n\n[fields.x]\ncache_strategy = "cache"\n',
        )
        _write_toml(
            tmp_path / "b" / "second.toml",
            '[endpoint]\nclass_name = "Dup"\n\n[fields.x]\ncache_strategy = "realtime"\n',
        )
        with caplog.at_level("WARNING"):
            result = discover_toml_overlays(tmp_path)
        assert "Dup" in result
        assert "Duplicate class_name" in caplog.text

    def test_skips_malformed_toml(self, tmp_path, caplog):
        bad = tmp_path / "bad.toml"
        bad.write_text("this is not valid toml {{{}}")
        with caplog.at_level("WARNING"):
            result = discover_toml_overlays(tmp_path)
        assert result == {}
        assert "malformed TOML" in caplog.text


class TestLoadOverlay:
    """Tests for load_overlay."""

    def test_loads_valid_toml(self, tmp_path):
        p = tmp_path / "test.toml"
        p.write_text('[endpoint]\nclass_name = "Foo"\n\n[fields.bar]\ncache_strategy = "cache"\n')
        data = load_overlay(p)
        assert data["endpoint"]["class_name"] == "Foo"
        assert data["fields"]["bar"]["cache_strategy"] == "cache"

    def test_raises_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_overlay(tmp_path / "missing.toml")

    def test_raises_toml_decode_error(self, tmp_path):
        p = tmp_path / "bad.toml"
        p.write_text("not valid toml {{{")
        with pytest.raises(tomllib.TOMLDecodeError):
            load_overlay(p)


class TestMergeOverlays:
    """Tests for merge_overlays."""

    def test_package_only(self):
        pkg = {
            "fields": {"name": {"cache_strategy": "cache"}, "size": {"cache_strategy": "realtime"}}
        }
        result = merge_overlays(pkg, None)
        assert result == {
            "name": {"cache_strategy": "cache"},
            "size": {"cache_strategy": "realtime"},
        }

    def test_user_replaces_field(self):
        pkg = {"fields": {"name": {"cache_strategy": "cache"}, "size": {"cache_strategy": "cache"}}}
        user = {"fields": {"name": {"cache_strategy": "realtime", "requires_explicit_fetch": True}}}
        result = merge_overlays(pkg, user)
        assert result["name"] == {"cache_strategy": "realtime", "requires_explicit_fetch": True}
        assert result["size"] == {"cache_strategy": "cache"}

    def test_fields_not_in_user_inherit_package(self):
        pkg = {"fields": {"a": {"cache_strategy": "cache"}, "b": {"cache_strategy": "derived"}}}
        user = {"fields": {"a": {"cache_strategy": "realtime"}}}
        result = merge_overlays(pkg, user)
        assert result["b"] == {"cache_strategy": "derived"}

    def test_none_user_overlay(self):
        pkg = {"fields": {"x": {"cache_strategy": "cache"}}}
        result = merge_overlays(pkg, None)
        assert result == {"x": {"cache_strategy": "cache"}}

    def test_empty_package_fields(self):
        result = merge_overlays({}, None)
        assert result == {}


class TestApplyOverlayToMapping:
    """Tests for apply_overlay_to_mapping."""

    def test_updates_cache_strategy(self):
        mapping = _make_mapping()
        config = {"name": {"cache_strategy": "realtime"}}
        result = apply_overlay_to_mapping(mapping, config)
        name_field = next(f for f in result.fields if f.cache_attr == "name")
        assert name_field.cache_strategy == "realtime"

    def test_updates_requires_explicit_fetch(self):
        mapping = _make_mapping()
        config = {"size": {"requires_explicit_fetch": True}}
        result = apply_overlay_to_mapping(mapping, config)
        size_field = next(f for f in result.fields if f.cache_attr == "size")
        assert size_field.requires_explicit_fetch is True

    def test_unmatched_fields_unchanged(self):
        mapping = _make_mapping()
        config = {"name": {"cache_strategy": "realtime"}}
        result = apply_overlay_to_mapping(mapping, config)
        size_field = next(f for f in result.fields if f.cache_attr == "size")
        assert size_field.cache_strategy == "cache"
        assert size_field.requires_explicit_fetch is False

    def test_extra_overlay_fields_ignored(self):
        mapping = _make_mapping()
        config = {"nonexistent_field": {"cache_strategy": "realtime"}}
        result = apply_overlay_to_mapping(mapping, config)
        assert len(result.fields) == len(mapping.fields)

    def test_original_not_mutated(self):
        mapping = _make_mapping()
        original_fields = mapping.fields
        config = {"name": {"cache_strategy": "realtime"}}
        apply_overlay_to_mapping(mapping, config)
        assert mapping.fields is original_fields
        name_field = next(f for f in mapping.fields if f.cache_attr == "name")
        assert name_field.cache_strategy == "cache"

    def test_empty_config_returns_equivalent_mapping(self):
        mapping = _make_mapping()
        result = apply_overlay_to_mapping(mapping, {})
        assert result.fields == mapping.fields


class TestLoadOverlays:
    """Integration tests for load_overlays."""

    def test_applies_package_defaults(self, tmp_path):
        registry = ModelRegistry()
        mapping = _make_mapping()
        registry.register_mapping("DummyModel", mapping)

        _write_toml(
            tmp_path / "test.toml",
            '[endpoint]\nclass_name = "DummyModel"\n\n[fields.name]\ncache_strategy = "realtime"\n',
        )

        import pynetappfoundry.cache.overlay_loader as loader

        original_root = loader._PACKAGE_OVERLAY_ROOT
        try:
            loader._PACKAGE_OVERLAY_ROOT = tmp_path
            count = load_overlays(registry)
        finally:
            loader._PACKAGE_OVERLAY_ROOT = original_root

        assert count == 1
        updated = registry.get_mapping("DummyModel")
        assert updated is not None
        name_field = next(f for f in updated.fields if f.cache_attr == "name")
        assert name_field.cache_strategy == "realtime"

    def test_user_override_wins(self, tmp_path):
        registry = ModelRegistry()
        mapping = _make_mapping()
        registry.register_mapping("DummyModel", mapping)

        pkg_dir = tmp_path / "pkg"
        user_dir = tmp_path / "user"

        _write_toml(
            pkg_dir / "test.toml",
            '[endpoint]\nclass_name = "DummyModel"\n\n[fields.name]\ncache_strategy = "cache"\n',
        )
        _write_toml(
            user_dir / "test.toml",
            '[endpoint]\nclass_name = "DummyModel"\n\n[fields.name]\ncache_strategy = "realtime"\n',
        )

        import pynetappfoundry.cache.overlay_loader as loader

        original_root = loader._PACKAGE_OVERLAY_ROOT
        try:
            loader._PACKAGE_OVERLAY_ROOT = pkg_dir
            count = load_overlays(registry, user_overlay_dir=user_dir)
        finally:
            loader._PACKAGE_OVERLAY_ROOT = original_root

        assert count == 1
        updated = registry.get_mapping("DummyModel")
        assert updated is not None
        name_field = next(f for f in updated.fields if f.cache_attr == "name")
        assert name_field.cache_strategy == "realtime"

    def test_missing_overlay_keeps_original(self, tmp_path):
        registry = ModelRegistry()
        mapping = _make_mapping()
        registry.register_mapping("DummyModel", mapping)

        import pynetappfoundry.cache.overlay_loader as loader

        original_root = loader._PACKAGE_OVERLAY_ROOT
        try:
            loader._PACKAGE_OVERLAY_ROOT = tmp_path  # empty dir
            count = load_overlays(registry)
        finally:
            loader._PACKAGE_OVERLAY_ROOT = original_root

        assert count == 0
        assert registry.get_mapping("DummyModel") is mapping

    def test_returns_correct_count(self, tmp_path):
        registry = ModelRegistry()
        for name in ("Alpha", "Beta", "Gamma"):
            m = _make_mapping(name=name)
            registry.register_mapping(name, m)

        for name in ("Alpha", "Beta"):
            _write_toml(
                tmp_path / f"{name.lower()}.toml",
                f'[endpoint]\nclass_name = "{name}"\n\n'
                f'[fields.name]\ncache_strategy = "realtime"\n',
            )

        import pynetappfoundry.cache.overlay_loader as loader

        original_root = loader._PACKAGE_OVERLAY_ROOT
        try:
            loader._PACKAGE_OVERLAY_ROOT = tmp_path
            count = load_overlays(registry)
        finally:
            loader._PACKAGE_OVERLAY_ROOT = original_root

        assert count == 2

    def test_nonexistent_user_dir_no_error(self, tmp_path):
        registry = ModelRegistry()
        mapping = _make_mapping()
        registry.register_mapping("DummyModel", mapping)

        _write_toml(
            tmp_path / "test.toml",
            '[endpoint]\nclass_name = "DummyModel"\n\n[fields.name]\ncache_strategy = "cache"\n',
        )

        import pynetappfoundry.cache.overlay_loader as loader

        original_root = loader._PACKAGE_OVERLAY_ROOT
        try:
            loader._PACKAGE_OVERLAY_ROOT = tmp_path
            count = load_overlays(registry, user_overlay_dir=tmp_path / "nonexistent")
        finally:
            loader._PACKAGE_OVERLAY_ROOT = original_root

        assert count == 1
