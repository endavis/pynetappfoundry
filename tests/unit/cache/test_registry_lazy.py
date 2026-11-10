"""Tests for the lazy, index-backed ModelRegistry (#903).

Must not import ``tools`` (#873); the codegen side is covered in
``tests/unit/codegen/test_mapping_index.py``.
"""

from __future__ import annotations

import importlib
import importlib.util
import json
import logging
import pkgutil
import subprocess
import sys
import textwrap
import types
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from pynetappfoundry.cache import _registry, overlay_loader
from pynetappfoundry.cache._mapping_index import MAPPING_INDEX
from pynetappfoundry.cache._registry import MappingIndexEntry, ModelRegistry, model_registry
from pynetappfoundry.cache.field_mapping import TypeMapping

_FAKE_MAPPING_SRC = textwrap.dedent(
    """
    import sys

    from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
    from {model_module} import {model_name}

    MAPPING = TypeMapping(
        name="{name}",
        model_class={model_name},
        api_endpoint="/fake",
        fields=(FieldMapping(cache_attr="size", api_path="size", cache_strategy="realtime"),),
    )
    holder = sys.modules["lazy_test_holder"]
    holder.imports.append(__name__)
    holder.registry.register_mapping("{name}", MAPPING)
    """
)
_FAKE_MODEL_SRC = textwrap.dedent(
    """
    from pydantic import BaseModel

    class {model_name}(BaseModel):
        size: int = 0
    """
)
_FAKE_OVERLAY = '[endpoint]\nclass_name = "LazyFake"\n\n[fields.size]\ncache_strategy = "cache"\n'


def _write_pkg(root: Path, package: str, name: str, model_name: str) -> None:
    """Write ``<package>/a/{model,mapping}.py`` registering *name*."""
    for sub in (root / package, root / package / "a"):
        sub.mkdir(parents=True, exist_ok=True)
        (sub / "__init__.py").write_text("", encoding="utf-8")
    model_module = f"{package}.a.model"
    (root / package / "a" / "model.py").write_text(
        _FAKE_MODEL_SRC.format(model_name=model_name), encoding="utf-8"
    )
    (root / package / "a" / "mapping.py").write_text(
        _FAKE_MAPPING_SRC.format(model_module=model_module, model_name=model_name, name=name),
        encoding="utf-8",
    )


@pytest.fixture
def holder(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Iterator[types.SimpleNamespace]:
    """Importable temp dir plus the ``lazy_test_holder`` module fake mappings register on."""
    ns = types.SimpleNamespace(registry=None, imports=[], root=tmp_path)
    monkeypatch.setitem(sys.modules, "lazy_test_holder", ns)
    monkeypatch.syspath_prepend(str(tmp_path))
    # Misses must not walk (and import) the real mapping packages.
    monkeypatch.setattr(_registry, "_FALLBACK_PACKAGES", ())
    importlib.invalidate_caches()
    yield ns
    for mod in [m for m in sys.modules if m.startswith(("lazyfake", "lazystale"))]:
        del sys.modules[mod]


@pytest.fixture
def fake_overlay_root(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    root = tmp_path / "overlays"
    (root / "fake").mkdir(parents=True)
    (root / "fake" / "fake.toml").write_text(_FAKE_OVERLAY, encoding="utf-8")
    (root / "dii" / "fake").mkdir(parents=True)
    (root / "dii" / "fake" / "fake.toml").write_text(_FAKE_OVERLAY, encoding="utf-8")
    monkeypatch.setattr(overlay_loader, "_PACKAGE_OVERLAY_ROOT", root)
    return root


def _indexed_registry(
    holder: types.SimpleNamespace, overlay: str | None = "fake/fake.toml"
) -> ModelRegistry:
    _write_pkg(holder.root, "lazyfake", "LazyFake", "LazyFakeModel")
    entry = MappingIndexEntry("lazyfake.a.mapping", "lazyfake.a.model", "LazyFakeModel", overlay)
    registry = ModelRegistry({"LazyFake": entry})
    holder.registry = registry
    return registry


def _strategies(mapping: TypeMapping) -> list[tuple[str, str, bool]]:
    return [(f.cache_attr, f.cache_strategy, f.requires_explicit_fetch) for f in mapping.fields]


class TestLazyMechanics:
    def test_no_import_before_lookup(
        self, holder: types.SimpleNamespace, fake_overlay_root: Path
    ) -> None:
        registry = _indexed_registry(holder)
        assert holder.imports == []
        assert "lazyfake.a.mapping" not in sys.modules
        assert registry._mappings == {}

    def test_get_mapping_imports_and_applies_overlay(
        self, holder: types.SimpleNamespace, fake_overlay_root: Path
    ) -> None:
        registry = _indexed_registry(holder)
        mapping = registry.get_mapping("LazyFake")
        assert mapping is not None
        assert holder.imports == ["lazyfake.a.mapping"]
        # The module declared "realtime"; the overlay says "cache".
        assert mapping.fields[0].cache_strategy == "cache"

    def test_dii_overlay_applied_on_lookup(
        self, holder: types.SimpleNamespace, fake_overlay_root: Path
    ) -> None:
        registry = _indexed_registry(holder, overlay="dii/fake/fake.toml")
        mapping = registry.get_mapping("LazyFake")
        assert mapping is not None
        # The module declared "realtime"; the DII overlay says "cache".
        assert mapping.fields[0].cache_strategy == "cache"

    def test_overlay_applied_once(
        self,
        holder: types.SimpleNamespace,
        fake_overlay_root: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        calls: list[str] = []
        real = overlay_loader.apply_package_overlay

        def counting(mapping: TypeMapping, rel_path: str) -> TypeMapping:
            calls.append(rel_path)
            return real(mapping, rel_path)

        monkeypatch.setattr(overlay_loader, "apply_package_overlay", counting)
        registry = _indexed_registry(holder)
        first = registry.get_mapping("LazyFake")
        assert first is not None
        # Re-registering (as load_overlays does) must not apply the overlay again.
        registry.register_mapping("LazyFake", first)
        registry.get_mapping("LazyFake")
        assert calls == ["fake/fake.toml"]

    def test_lookup_by_class_alone_triggers_load(
        self, holder: types.SimpleNamespace, fake_overlay_root: Path
    ) -> None:
        registry = _indexed_registry(holder)
        model_module = importlib.import_module("lazyfake.a.model")
        assert holder.imports == []
        mapping = registry.get_mapping_by_model_class(model_module.LazyFakeModel)
        assert mapping is not None
        assert mapping.name == "LazyFake"
        assert holder.imports == ["lazyfake.a.mapping"]

    def test_unknown_name_is_none_and_imports_nothing(
        self, holder: types.SimpleNamespace, fake_overlay_root: Path
    ) -> None:
        registry = _indexed_registry(holder)
        assert registry.get_mapping("Nope") is None
        assert holder.imports == []

    def test_mappings_loads_everything(
        self, holder: types.SimpleNamespace, fake_overlay_root: Path
    ) -> None:
        registry = _indexed_registry(holder)
        assert set(registry.mappings) == {"LazyFake"}
        assert holder.imports == ["lazyfake.a.mapping"]

    def test_unindexed_overlay_none_leaves_mapping_unchanged(
        self, holder: types.SimpleNamespace, fake_overlay_root: Path
    ) -> None:
        registry = _indexed_registry(holder, overlay=None)
        mapping = registry.get_mapping("LazyFake")
        assert mapping is not None
        assert mapping.fields[0].cache_strategy == "realtime"


class TestStaleIndexFallback:
    @pytest.fixture
    def walk_counter(self, monkeypatch: pytest.MonkeyPatch) -> list[int]:
        calls: list[int] = []
        real = pkgutil.walk_packages

        def counting(*args: Any, **kwargs: Any) -> Any:
            # pkgutil recurses through its own module global; count only the top-level walks.
            if kwargs.get("prefix") in ("lazystale.", "lazyfake."):
                calls.append(1)
            return real(*args, **kwargs)

        monkeypatch.setattr(_registry.pkgutil, "walk_packages", counting)
        return calls

    @pytest.fixture
    def stale(
        self, holder: types.SimpleNamespace, monkeypatch: pytest.MonkeyPatch
    ) -> ModelRegistry:
        """An empty index while ``lazystale.a.mapping`` exists on the walk path."""
        _write_pkg(holder.root, "lazystale", "LazyStale", "LazyStaleModel")
        monkeypatch.setattr(_registry, "_FALLBACK_PACKAGES", ("lazystale",))
        registry = ModelRegistry({})
        holder.registry = registry
        return registry

    def test_get_mapping_miss_finds_it_and_warns(
        self,
        stale: ModelRegistry,
        walk_counter: list[int],
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        with caplog.at_level(logging.WARNING, logger=_registry.logger.name):
            mapping = stale.get_mapping("LazyStale")
        assert mapping is not None
        assert (
            "mapping index is stale: lazystale.a.mapping is not indexed; run doit mapping_index"
            in caplog.text
        )

    def test_get_mapping_by_model_class_miss_finds_it(
        self, stale: ModelRegistry, walk_counter: list[int]
    ) -> None:
        model = importlib.import_module("lazystale.a.model").LazyStaleModel
        mapping = stale.get_mapping_by_model_class(model)
        assert mapping is not None
        assert mapping.name == "LazyStale"

    def test_mappings_includes_unindexed(self, stale: ModelRegistry) -> None:
        assert "LazyStale" in stale.mappings

    def test_walk_runs_once(self, stale: ModelRegistry, walk_counter: list[int]) -> None:
        stale.get_mapping("LazyStale")
        stale.get_mapping("Other")
        _ = stale.mappings
        stale.get_mapping_by_model_class(types.SimpleNamespace)  # type: ignore[arg-type]
        assert len(walk_counter) == 1

    def test_unknown_name_still_none_after_one_walk(
        self, stale: ModelRegistry, walk_counter: list[int]
    ) -> None:
        assert stale.get_mapping("Nope") is None
        assert stale.get_mapping("Nope") is None
        assert len(walk_counter) == 1

    def test_miss_does_not_import_indexed_modules(
        self,
        holder: types.SimpleNamespace,
        fake_overlay_root: Path,
        monkeypatch: pytest.MonkeyPatch,
        walk_counter: list[int],
    ) -> None:
        registry = _indexed_registry(holder)
        monkeypatch.setattr(_registry, "_FALLBACK_PACKAGES", ("lazyfake",))
        assert registry.get_mapping("NoSuchName") is None
        assert len(walk_counter) == 1
        assert "lazyfake.a.mapping" not in sys.modules
        assert holder.imports == []

    def test_unindexed_found_while_indexed_stay_unimported(
        self,
        holder: types.SimpleNamespace,
        fake_overlay_root: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        registry = _indexed_registry(holder)
        _write_pkg(holder.root, "lazystale", "LazyStale", "LazyStaleModel")
        monkeypatch.setattr(_registry, "_FALLBACK_PACKAGES", ("lazyfake", "lazystale"))
        mapping = registry.get_mapping("LazyStale")
        assert mapping is not None
        assert holder.imports == ["lazystale.a.mapping"]
        assert "lazyfake.a.mapping" not in sys.modules

    def test_mappings_still_complete_with_indexed_and_unindexed(
        self,
        holder: types.SimpleNamespace,
        fake_overlay_root: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        registry = _indexed_registry(holder)
        _write_pkg(holder.root, "lazystale", "LazyStale", "LazyStaleModel")
        monkeypatch.setattr(_registry, "_FALLBACK_PACKAGES", ("lazyfake", "lazystale"))
        assert set(registry.mappings) == {"LazyFake", "LazyStale"}

    def test_indexed_hit_does_not_walk(
        self,
        holder: types.SimpleNamespace,
        fake_overlay_root: Path,
        walk_counter: list[int],
    ) -> None:
        registry = _indexed_registry(holder)
        assert registry.get_mapping("LazyFake") is not None
        model = importlib.import_module("lazyfake.a.model").LazyFakeModel
        assert registry.get_mapping_by_model_class(model) is not None
        assert walk_counter == []

    def test_bare_registry_never_walks(
        self, walk_counter: list[int], monkeypatch: pytest.MonkeyPatch
    ) -> None:
        registry = ModelRegistry()
        assert registry.get_mapping("Nope") is None
        assert registry.get_mapping_by_model_class(types.SimpleNamespace) is None  # type: ignore[arg-type]
        assert registry.mappings == {}
        assert walk_counter == []

    def test_stale_overlay_path_rediscovers_and_applies(
        self,
        holder: types.SimpleNamespace,
        fake_overlay_root: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        registry = _indexed_registry(holder, overlay="moved/gone.toml")
        with caplog.at_level(logging.WARNING, logger=_registry.logger.name):
            mapping = registry.get_mapping("LazyFake")
        assert mapping is not None
        assert mapping.fields[0].cache_strategy == "cache"
        assert "mapping index is stale" in caplog.text

    def test_stale_dii_overlay_rediscovers(
        self,
        holder: types.SimpleNamespace,
        fake_overlay_root: Path,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        registry = _indexed_registry(holder, overlay="dii/moved/gone.toml")
        with caplog.at_level(logging.WARNING, logger=_registry.logger.name):
            mapping = registry.get_mapping("LazyFake")
        assert mapping is not None
        assert mapping.fields[0].cache_strategy == "cache"
        assert "mapping index is stale" in caplog.text


def _walk_mapping_modules() -> set[str]:
    found: set[str] = set()
    for pkg_name in ("pynetappfoundry.cache.ontap", "pynetappfoundry.cache.dii"):
        pkg = importlib.import_module(pkg_name)
        for info in pkgutil.walk_packages(pkg.__path__, prefix=f"{pkg_name}."):
            if info.name.endswith(".mapping"):
                found.add(info.name)
    return found


def _record_module(module_name: str, monkeypatch: pytest.MonkeyPatch) -> tuple[str, TypeMapping]:
    """Execute a mapping module afresh and return the single raw registration."""
    spec = importlib.util.find_spec(module_name)
    assert spec is not None
    assert spec.origin is not None
    calls: list[tuple[str, TypeMapping]] = []
    monkeypatch.setattr(model_registry, "register_mapping", lambda n, m: calls.append((n, m)))
    probe = importlib.util.spec_from_file_location(f"_lazy_probe.{module_name}", spec.origin)
    assert probe is not None
    assert probe.loader is not None
    module = importlib.util.module_from_spec(probe)
    sys.modules[probe.name] = module
    try:
        probe.loader.exec_module(module)
    finally:
        sys.modules.pop(probe.name, None)
        monkeypatch.undo()
    assert len(calls) == 1, module_name
    return calls[0]


class TestCommittedIndex:
    def test_index_matches_package_walk(self) -> None:
        indexed = {entry[0] for entry in MAPPING_INDEX.values()}
        walked = _walk_mapping_modules()
        assert indexed == walked, (
            "mapping index is stale; run `doit mapping_index`. "
            f"unindexed={sorted(walked - indexed)} removed={sorted(indexed - walked)}"
        )
        assert len(indexed) == len(MAPPING_INDEX)

    def test_index_matches_registered_names_and_classes(self) -> None:
        for name, (module_name, model_module, qualname, _overlay) in MAPPING_INDEX.items():
            importlib.import_module(module_name)
            mapping = model_registry._mappings.get(name)
            assert mapping is not None, f"{module_name} did not register {name!r}"
            cls = mapping.model_class
            assert (cls.__module__, cls.__qualname__) == (model_module, qualname), (
                f"{name}: run `doit mapping_index`"
            )

    def test_index_overlays_match_discovery(self) -> None:
        discovered = overlay_loader.discover_toml_overlays(overlay_loader._PACKAGE_OVERLAY_ROOT)
        root = overlay_loader._PACKAGE_OVERLAY_ROOT
        for name, (_m, _mm, _q, overlay) in MAPPING_INDEX.items():
            expected = discovered[name].relative_to(root).as_posix() if name in discovered else None
            assert overlay == expected, f"{name}: run `doit mapping_index`"

    def test_dii_overlays_indexed(self) -> None:
        root = overlay_loader._PACKAGE_OVERLAY_ROOT
        dii = {
            n: e for n, e in MAPPING_INDEX.items() if e[0].startswith("pynetappfoundry.cache.dii.")
        }
        assert dii
        for name, (_m, _mm, _q, overlay) in dii.items():
            assert overlay is not None, name
            assert overlay.startswith("dii/"), name
            assert (root / overlay).is_file(), name
        for name, (module_name, _mm, _q, overlay) in MAPPING_INDEX.items():
            if module_name.startswith("pynetappfoundry.cache.ontap.") and overlay is not None:
                assert overlay.startswith("ontap/"), name
        assert MAPPING_INDEX["DiiQuery"][3] == "dii/queries/queries.toml"

    def test_dii_overlay_applied_by_singleton(self, monkeypatch: pytest.MonkeyPatch) -> None:
        module_name = MAPPING_INDEX["DiiQuery"][0]
        _name, raw = _record_module(module_name, monkeypatch)
        expected = overlay_loader.apply_package_overlay(raw, "dii/queries/queries.toml")
        actual = model_registry.get_mapping("DiiQuery")
        assert actual is not None
        assert _strategies(actual) == _strategies(expected)

    def test_lazy_equals_eager(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """The lazy singleton gives what the old walk plus ``load_overlays`` gave."""
        reference = ModelRegistry()
        for module_name, *_ in MAPPING_INDEX.values():
            name, raw = _record_module(module_name, monkeypatch)
            reference.register_mapping(name, raw)
        overlay_loader.load_overlays(reference)

        lazy = model_registry.mappings
        assert set(lazy) == set(reference.mappings)
        for name, expected in reference.mappings.items():
            actual = lazy[name]
            assert actual.model_class is expected.model_class
            assert actual.api_endpoint == expected.api_endpoint
            assert _strategies(actual) == _strategies(expected), name
            by_class = model_registry.get_mapping_by_model_class(expected.model_class)
            assert by_class is not None
            assert by_class.name == actual.name
            assert model_registry.get_mapping(name) == actual


def _run_python(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-c", code], check=True, capture_output=True, text=True)


class TestStartup:
    def test_cluster_info_maps_to_cluster(self) -> None:
        out = _run_python(
            "from pynetappfoundry.cache import model_registry\n"
            "from pynetappfoundry.models.ontap.cluster.model import ClusterInfo\n"
            "print(model_registry.get_mapping_by_model_class(ClusterInfo).name)\n"
        )
        assert out.stdout.strip() == "Cluster"

    def test_cli_import_is_lazy(self) -> None:
        code = textwrap.dedent(
            """
            import json, sys
            try:
                from pynetappfoundry.cli import nf
                nf(['--help'])
            except SystemExit as exc:
                code = exc.code
            from pynetappfoundry.cache._mapping_index import MAPPING_INDEX
            loaded = [m for m in sys.modules if m.endswith('.mapping')]
            print(json.dumps({
                "code": code or 0,
                "jsonschema": 'jsonschema' in sys.modules or 'rfc3987_syntax' in sys.modules,
                "loaded": len([m for m in loaded if m in {e[0] for e in MAPPING_INDEX.values()}]),
                "dii": [m for m in loaded if m.startswith('pynetappfoundry.cache.dii.')],
                "total": len(MAPPING_INDEX),
            }))
            """
        )
        result = _run_python(code)
        data = json.loads(result.stdout.strip().splitlines()[-1])
        assert data["code"] == 0
        assert data["jsonschema"] is False
        assert data["dii"] == []
        assert data["loaded"] < data["total"] * 0.10
