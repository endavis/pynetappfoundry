"""Tests for the mapping-index generator and ``doit mapping_index`` (#903)."""

from __future__ import annotations

import shutil
import textwrap
from pathlib import Path
from typing import Any

import pytest

from tools.codegen import mapping_index
from tools.codegen.mapping_index import build_index, check_index, render_index
from tools.doit import codegen as doit_codegen

_REPO = Path(__file__).resolve().parents[3]
_CACHE_ROOT = _REPO / "src" / "pynetappfoundry" / "cache"

_MAPPING_TEMPLATE = textwrap.dedent(
    """
    from pydantic import BaseModel

    from pynetappfoundry.cache._registry import model_registry
    from pynetappfoundry.cache.field_mapping import TypeMapping


    class {cls}(BaseModel):
        pass


    {registrations}
    """
)


def _write_mapping(root: Path, rel: str, cls: str, names: list[str]) -> None:
    path = root / rel / "mapping.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    registrations = "\n".join(
        f'model_registry.register_mapping("{n}", TypeMapping(name="{n}", model_class={cls}, '
        'api_endpoint="/x"))'
        for n in names
    )
    path.write_text(_MAPPING_TEMPLATE.format(cls=cls, registrations=registrations), "utf-8")


class TestBuildIndex:
    def test_committed_index_is_current(self) -> None:
        diff = check_index(_CACHE_ROOT)
        assert diff is None, f"run `doit mapping_index`:\n{diff}"

    def test_committed_file_equals_regenerated(self) -> None:
        committed = (_CACHE_ROOT / "_mapping_index.py").read_text(encoding="utf-8")
        assert render_index(build_index(_CACHE_ROOT)) == committed

    def test_output_is_deterministic(self) -> None:
        assert render_index(build_index(_CACHE_ROOT)) == render_index(build_index(_CACHE_ROOT))

    def test_builds_rows_from_fake_tree(self, tmp_path: Path) -> None:
        _write_mapping(tmp_path, "ontap/a", "ModelA", ["A"])
        _write_mapping(tmp_path, "dii/b", "ModelB", ["B"])
        index = build_index(tmp_path)
        assert list(index) == ["A", "B"]
        assert index["A"][0] == "pynetappfoundry.cache.ontap.a.mapping"
        assert index["A"][2] == "ModelA"
        assert index["A"][3] is None

    def test_duplicate_name_raises(self, tmp_path: Path) -> None:
        _write_mapping(tmp_path, "ontap/a", "ModelA", ["Same"])
        _write_mapping(tmp_path, "ontap/b", "ModelB", ["Same"])
        with pytest.raises(ValueError, match="Duplicate mapping name"):
            build_index(tmp_path)

    def test_duplicate_model_class_raises(self, tmp_path: Path) -> None:
        _write_mapping(tmp_path, "ontap/a", "ModelA", ["A"])
        # A second module whose model class has the same module-qualified identity.
        shared = tmp_path / "ontap" / "b" / "mapping.py"
        shared.parent.mkdir(parents=True)
        shared.write_text(
            textwrap.dedent(
                """
                from pynetappfoundry.cache._registry import model_registry
                from pynetappfoundry.cache.field_mapping import TypeMapping
                from pynetappfoundry.models.ontap.cluster.model import ClusterInfo

                model_registry.register_mapping(
                    "B1", TypeMapping(name="B1", model_class=ClusterInfo, api_endpoint="/x")
                )
                """
            ),
            "utf-8",
        )
        other = tmp_path / "ontap" / "c" / "mapping.py"
        other.parent.mkdir(parents=True)
        other.write_text(shared.read_text("utf-8").replace("B1", "C1"), "utf-8")
        with pytest.raises(ValueError, match="Duplicate model class"):
            build_index(tmp_path)

    def test_missing_registration_raises(self, tmp_path: Path) -> None:
        _write_mapping(tmp_path, "ontap/a", "ModelA", [])
        with pytest.raises(ValueError, match="exactly once, found 0"):
            build_index(tmp_path)

    def test_several_registrations_raises(self, tmp_path: Path) -> None:
        _write_mapping(tmp_path, "ontap/a", "ModelA", ["A1", "A2"])
        with pytest.raises(ValueError, match="exactly once, found 2"):
            build_index(tmp_path)

    def test_does_not_register_on_singleton(self, tmp_path: Path) -> None:
        from pynetappfoundry.cache._registry import model_registry

        _write_mapping(tmp_path, "ontap/a", "ModelA", ["IndexProbeOnly"])
        build_index(tmp_path)
        assert "IndexProbeOnly" not in model_registry._mappings
        assert "register_mapping" not in vars(model_registry)


class TestCheck:
    def test_passes_on_committed_index(self) -> None:
        assert check_index(_CACHE_ROOT) is None

    def test_fails_on_modified_copy(self, tmp_path: Path) -> None:
        copy = tmp_path / "_mapping_index.py"
        shutil.copy(_CACHE_ROOT / "_mapping_index.py", copy)
        copy.write_text(copy.read_text("utf-8").replace('"Cluster"', '"ClusterX"', 1), "utf-8")
        diff = check_index(_CACHE_ROOT, index_path=copy)
        assert diff is not None
        assert "ClusterX" in diff

    def test_doit_check_flag_passes_and_writes_nothing(self) -> None:
        before = (_CACHE_ROOT / "_mapping_index.py").read_bytes()
        task = doit_codegen.task_mapping_index()
        action = task["actions"][0]
        # The doit task resolves paths against the repository root.
        import os

        cwd = Path.cwd()
        os.chdir(_REPO)
        try:
            assert action(check=True) is None
        finally:
            os.chdir(cwd)
        assert (_CACHE_ROOT / "_mapping_index.py").read_bytes() == before

    def test_doit_check_flag_fails_on_drift(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        def stale(*_a: Any, **_k: Any) -> str:
            return "--- committed\n+++ regenerated\n"

        monkeypatch.setattr(mapping_index, "check_index", stale)
        action = doit_codegen.task_mapping_index()["actions"][0]
        assert action(check=True) is False
        assert "doit mapping_index" in capsys.readouterr().err
