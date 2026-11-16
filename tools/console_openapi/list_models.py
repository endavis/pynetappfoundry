"""Append a ``RootModel`` list class for every array-response operation (#1032).

``datamodel-codegen`` emits only the item class (``ResponseBody``) for an
operation whose success body is a JSON array of ``$ref`` items. This step reads
the spec, finds each such operation and appends ``ResponseList`` (or
``Response<status>List``) next to the item class, so the whole array body has a
generated model. It runs in ``doit console_models`` after the generator and
before ruff, and fails loudly on any module shape it does not expect.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from tools.console_openapi.client_codegen import (
    _METHODS,
    _REF_PREFIX,
    _response_schema,
)

_ITEM_NAME = re.compile(r"(ResponseBody|Response\d{3}Body)")
_PYDANTIC_IMPORT = re.compile(r"^from pydantic import (.*)$", re.MULTILINE)


class ListModelError(ValueError):
    """A list model cannot be added to the generated tree."""


def array_item_refs(spec: dict[str, Any]) -> list[tuple[str, str]]:
    """Return sorted ``(operationId, component key)`` for each array-of-``$ref`` success body."""
    found: list[tuple[str, str]] = []
    for item in spec.get("paths", {}).values():
        for method, op in item.items():
            if method not in _METHODS or not isinstance(op, dict):
                continue
            _, schema = _response_schema(op.get("responses", {}))
            if not isinstance(schema, dict) or schema.get("type") != "array":
                continue
            items = schema.get("items")
            if isinstance(items, dict) and "$ref" in items:
                ref = str(items["$ref"])
                if not ref.startswith(_REF_PREFIX):
                    raise ListModelError(f"Unsupported $ref {ref!r}")
                found.append((str(op.get("operationId", "")), ref.removeprefix(_REF_PREFIX)))
    return sorted(found)


def list_class_name(item_cls: str) -> str:
    """Return the list class name for an item class, replacing the trailing ``Body``."""
    if not _ITEM_NAME.fullmatch(item_cls):
        raise ListModelError(f"Cannot name a list model for item class {item_cls!r}")
    return item_cls.removesuffix("Body") + "List"


def add_list_models(spec: dict[str, Any], models_root: Path) -> list[Path]:
    """Append the list class to each item module and return the modified files."""
    seen: dict[Path, str] = {}
    changed: list[Path] = []
    for op_id, key in array_item_refs(spec):
        head, _, item_cls = key.rpartition(".")
        package, _, stem = head.partition(".")
        if not package or not stem:
            raise ListModelError(f"Cannot map {key!r} to a generated module")
        file = models_root / package / f"{stem.replace('-', '_')}.py"
        if file in seen:
            raise ListModelError(f"{op_id!r} and {seen[file]!r} both map to {file}")
        seen[file] = op_id
        if not file.is_file():
            raise ListModelError(f"Model module {file} for {key!r} does not exist")
        name = list_class_name(item_cls)
        text = file.read_text(encoding="utf-8")
        if f"class {item_cls}(" not in text:
            raise ListModelError(f"Model module {file} does not define {item_cls}")
        if f"class {name}(" in text:
            raise ListModelError(f"Model module {file} already defines {name}")
        match = _PYDANTIC_IMPORT.search(text)
        if match is None:
            raise ListModelError(f"Model module {file} has no single-line pydantic import")
        names = [n.strip() for n in match.group(1).split(",")]
        if "RootModel" not in names:
            text = (
                text[: match.start()]
                + f"from pydantic import {match.group(1)}, RootModel"
                + text[match.end() :]
            )
        text += f"\n\nclass {name}(RootModel[list[{item_cls}]]):\n    root: list[{item_cls}]\n"
        file.write_text(text, encoding="utf-8")
        changed.append(file)
    return changed
