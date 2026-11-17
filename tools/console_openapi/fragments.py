"""Hand-written spec fragments merged into the built Console spec (#1078).

The Console ``/agents-mgmt`` endpoints are not in the NetAppDocs sources, so the
builder cannot parse them. Each file under ``fragments/`` is a partial OpenAPI
document (``x-namespace``, ``paths`` and ``components.schemas``) taken from live
evidence. ``merge_fragments`` adds them to a built spec and records what came
from which fragment in ``info.x-fragments``; ``strip_fragments`` removes exactly
those entries again, so the committed spec can be re-merged offline without
fetching the docs repo (``doit console_openapi_fragments``).
"""

from __future__ import annotations

import copy
from collections.abc import Collection
from pathlib import Path
from typing import Any

import yaml

from tools.console_openapi.openapi.builder import BuildError

FRAGMENTS_DIR = Path(__file__).resolve().parent / "fragments"
_HTTP_METHODS = frozenset({"get", "put", "post", "delete", "options", "head", "patch", "trace"})
_EVIDENCE = "live"
_INFO_KEY = "x-fragments"


class FragmentError(BuildError):
    """A spec fragment is malformed or conflicts with the built spec."""


def load_fragments(directory: Path = FRAGMENTS_DIR) -> list[tuple[str, dict[str, Any]]]:
    """Return ``(file name, document)`` for each ``*.yaml`` fragment, sorted by name."""
    fragments: list[tuple[str, dict[str, Any]]] = []
    for path in sorted(directory.glob("*.yaml")):
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise FragmentError(f"{path.name}: a fragment must be a YAML mapping")
        fragments.append((path.name, data))
    return fragments


def _check_operations(name: str, path: str, item: object) -> None:
    """Require every operation of a fragment path to carry ``x-evidence: live``."""
    if not isinstance(item, dict):
        raise FragmentError(f"{name}: path {path!r} must be a mapping")
    for method, op in item.items():
        if method not in _HTTP_METHODS:
            continue
        evidence = op.get("x-evidence") if isinstance(op, dict) else None
        if evidence != _EVIDENCE:
            raise FragmentError(
                f"{name}: {method.upper()} {path} needs 'x-evidence: {_EVIDENCE}', "
                f"found {evidence!r}"
            )


def merge_fragments(
    spec: dict[str, Any], fragments: Collection[tuple[str, dict[str, Any]]]
) -> None:
    """Merge ``fragments`` into ``spec`` in place and record them in ``info.x-fragments``.

    Raises:
        FragmentError: If a fragment has no ``x-namespace``, redefines an existing
            path or schema, defines a schema outside its namespace, or has an
            operation whose ``x-evidence`` is missing or not ``live``.
    """
    if not fragments:
        return
    paths: dict[str, Any] = spec["paths"]
    schemas: dict[str, Any] = spec["components"]["schemas"]
    recorded: dict[str, Any] = spec["info"].setdefault(_INFO_KEY, {})
    for name, fragment in fragments:
        namespace = fragment.get("x-namespace")
        if not isinstance(namespace, str) or not namespace:
            raise FragmentError(f"{name}: missing 'x-namespace'")
        new_paths = fragment.get("paths") or {}
        new_schemas = (fragment.get("components") or {}).get("schemas") or {}
        for path, item in new_paths.items():
            if path in paths:
                raise FragmentError(f"{name}: path {path!r} already exists in the spec")
            _check_operations(name, path, item)
        for key in new_schemas:
            if not key.startswith(f"{namespace}."):
                raise FragmentError(
                    f"{name}: schema {key!r} is outside the namespace {namespace!r}"
                )
            if key in schemas:
                raise FragmentError(f"{name}: schema {key!r} already exists in the spec")
        for path, item in new_paths.items():
            paths[path] = copy.deepcopy(item)
        for key, schema in new_schemas.items():
            schemas[key] = copy.deepcopy(schema)
        recorded[name] = {"paths": list(new_paths), "schemas": list(new_schemas)}


def strip_fragments(spec: dict[str, Any]) -> None:
    """Remove every path and schema listed in ``info.x-fragments``, then the record itself."""
    recorded = spec["info"].pop(_INFO_KEY, None) or {}
    for entry in recorded.values():
        for path in entry.get("paths", []):
            spec["paths"].pop(path, None)
        for key in entry.get("schemas", []):
            spec["components"]["schemas"].pop(key, None)
