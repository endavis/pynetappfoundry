"""Tests for the list-model post-processing step (#1032)."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from tools.console_openapi.list_models import (
    ListModelError,
    add_list_models,
    array_item_refs,
    list_class_name,
)
from tools.doit import console_openapi_tasks as tasks

_REF = "#/components/schemas/"
_MODULE = (
    "from __future__ import annotations\n\n"
    "from pydantic import BaseModel\n\n\n"
    "class ResponseBody(BaseModel):\n    a: int | None = None\n"
)


def _spec(
    key: str = "cvo.get_things.ResponseBody", responses: dict[str, Any] | None = None
) -> dict[str, Any]:
    body = responses or {
        "200": {
            "content": {
                "application/json": {"schema": {"type": "array", "items": {"$ref": _REF + key}}}
            }
        }
    }
    return {"paths": {"/things": {"get": {"operationId": "getThings", "responses": body}}}}


def _root(tmp_path: Path, text: str = _MODULE) -> Path:
    (tmp_path / "cvo").mkdir()
    (tmp_path / "cvo" / "get_things.py").write_text(text, encoding="utf-8")
    return tmp_path


def _array(items: dict[str, Any]) -> dict[str, Any]:
    return {"content": {"application/json": {"schema": {"type": "array", "items": items}}}}


def test_array_item_refs_finds_array_of_refs() -> None:
    assert array_item_refs(_spec()) == [("getThings", "cvo.get_things.ResponseBody")]


def test_array_item_refs_ignores_other_shapes() -> None:
    ref = {"$ref": _REF + "cvo.x.ResponseBody"}
    obj = {"200": {"content": {"application/json": {"schema": ref}}}}
    assert array_item_refs(_spec(responses=obj)) == []
    assert array_item_refs(_spec(responses={"200": _array({"type": "string"})})) == []
    assert array_item_refs(_spec(responses={"404": _array(ref)})) == []


def test_array_item_refs_uses_default_without_2xx() -> None:
    spec = _spec(responses={"default": _array({"$ref": _REF + "cvo.x.ResponseBody"})})
    assert array_item_refs(spec) == [("getThings", "cvo.x.ResponseBody")]


def test_array_item_refs_without_paths() -> None:
    assert array_item_refs({"openapi": "3.0.3"}) == []


def test_array_item_refs_rejects_foreign_ref() -> None:
    with pytest.raises(ListModelError, match="Unsupported"):
        array_item_refs(_spec(responses={"200": _array({"$ref": "other.json#/X"})}))


def test_list_class_name() -> None:
    assert list_class_name("ResponseBody") == "ResponseList"
    assert list_class_name("Response200Body") == "Response200List"
    for bad in ("RequestBody", "Foo"):
        with pytest.raises(ListModelError):
            list_class_name(bad)


def test_add_list_models_appends_class(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = _root(tmp_path)
    assert add_list_models(_spec(), root) == [root / "cvo" / "get_things.py"]
    text = (root / "cvo" / "get_things.py").read_text(encoding="utf-8")
    assert "from pydantic import BaseModel, RootModel\n" in text
    name = "_list_models_test_module"
    spec = importlib.util.spec_from_file_location(name, root / "cvo" / "get_things.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, module)
    spec.loader.exec_module(module)
    assert module.ResponseList.model_validate([{"a": 1}, {}]).root[0].a == 1


def test_add_list_models_keeps_existing_root_model_import(tmp_path: Path) -> None:
    root = _root(tmp_path, _MODULE.replace("BaseModel\n", "BaseModel, RootModel\n", 1))
    add_list_models(_spec(), root)
    text = (root / "cvo" / "get_things.py").read_text(encoding="utf-8")
    assert text.count("RootModel,") + text.count(", RootModel") == 1


def test_add_list_models_second_run_raises(tmp_path: Path) -> None:
    root = _root(tmp_path)
    add_list_models(_spec(), root)
    with pytest.raises(ListModelError, match="already defines"):
        add_list_models(_spec(), root)


def test_add_list_models_missing_module(tmp_path: Path) -> None:
    with pytest.raises(ListModelError, match="does not exist"):
        add_list_models(_spec(), tmp_path)


def test_add_list_models_missing_item_class(tmp_path: Path) -> None:
    root = _root(tmp_path, "from pydantic import BaseModel\n")
    with pytest.raises(ListModelError, match="does not define"):
        add_list_models(_spec(), root)


def test_add_list_models_missing_pydantic_import(tmp_path: Path) -> None:
    root = _root(tmp_path, "class ResponseBody(object):\n    pass\n")
    with pytest.raises(ListModelError, match="pydantic import"):
        add_list_models(_spec(), root)


def test_add_list_models_duplicate_module(tmp_path: Path) -> None:
    root = _root(tmp_path)
    spec = _spec()
    responses = spec["paths"]["/things"]["get"]["responses"]
    spec["paths"]["/other"] = {"get": {"operationId": "getOther", "responses": responses}}
    with pytest.raises(ListModelError, match="both map"):
        add_list_models(spec, root)


def test_add_list_models_unmappable_key(tmp_path: Path) -> None:
    with pytest.raises(ListModelError, match="Cannot map"):
        add_list_models(_spec(key="ResponseBody"), tmp_path)


def test_generation_adds_list_models_before_ruff(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import yaml

    spec_file = tmp_path / "spec.yaml"
    spec_file.write_text(yaml.safe_dump(_spec()), encoding="utf-8")
    out = tmp_path / "console"
    monkeypatch.setattr(tasks, "_CONSOLE_SPEC", spec_file)
    monkeypatch.setattr(tasks, "_CONSOLE_MODELS_DIR", out)
    seen: list[bool] = []

    def fake_run(cmd: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        module = out / "cvo" / "get_things.py"
        if "datamodel-codegen" in cmd:
            module.parent.mkdir(parents=True)
            module.write_text(_MODULE, encoding="utf-8")
        elif "ruff" in cmd:
            seen.append("class ResponseList(" in module.read_text(encoding="utf-8"))
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    tasks._generate_console_models()
    assert seen == [True, True]


def test_committed_spec_has_151_array_responses(committed_spec: dict[str, Any]) -> None:
    assert len(array_item_refs(committed_spec)) == 151


def test_every_array_response_has_a_list_model(committed_spec: dict[str, Any]) -> None:
    """The committed tree holds exactly the list classes the spec implies."""
    import importlib
    import pkgutil

    from pydantic import RootModel, ValidationError

    expected: set[tuple[str, str]] = set()
    for _, key in array_item_refs(committed_spec):
        head, _, item_name = key.rpartition(".")
        package, _, stem = head.partition(".")
        module = importlib.import_module(
            f"pynetappfoundry.models.console.{package}.{stem.replace('-', '_')}"
        )
        list_name = list_class_name(item_name)
        list_cls = getattr(module, list_name)
        assert issubclass(list_cls, RootModel)
        parsed = list_cls.model_validate([{}])
        assert type(parsed.root[0]) is getattr(module, item_name)
        with pytest.raises(ValidationError):
            list_cls.model_validate({})
        expected.add((module.__name__, list_name))

    found: set[tuple[str, str]] = set()
    for package_name in ("cvo", "dw"):
        pkg = importlib.import_module(f"pynetappfoundry.models.console.{package_name}")
        for info in pkgutil.iter_modules(pkg.__path__):
            found_module = importlib.import_module(f"{pkg.__name__}.{info.name}")
            for name, obj in vars(found_module).items():
                if (
                    name.endswith("List")
                    and isinstance(obj, type)
                    and issubclass(obj, RootModel)
                    and obj.__module__ == found_module.__name__
                ):
                    found.add((found_module.__name__, name))
    assert found == expected
