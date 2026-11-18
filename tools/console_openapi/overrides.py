"""Hand-written retypings of schemas the docs describe wrongly (#1095).

The NetAppDocs sources type some fields differently from what live agents return
(a tag map documented as a prose anchor, a cron field documented as strings but
sent as integers). ``overrides.yaml`` replaces those schemas or properties after
the fragments are merged. Every override names its ``evidence`` (``live`` for a
shape measured against a real agent, ``inferred`` for a same-shaped schema in
another module that was not measured) and a ``reason``.

Each override is recorded in the node it changes as
``x-override: {evidence, reason, original}``. ``strip_overrides`` puts the
originals back, so the committed spec can be re-processed offline
(``doit console_openapi_fragments``). The record is an extension key and does not
change the generated models.
"""

from __future__ import annotations

import builtins
import copy
from collections.abc import Collection
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from tools.console_openapi.openapi.builder import BuildError

OVERRIDES_PATH = Path(__file__).resolve().parent / "overrides.yaml"
EVIDENCE_VALUES = frozenset({"live", "inferred"})
_NODE_KEY = "x-override"
_FRAGMENTS_KEY = "x-fragments"
_ENTRY_KEYS = frozenset({"schemas", "properties", "replace", "evidence", "reason"})
#: What a schema override keeps from the node it replaces.
_KEPT_SCHEMA_KEYS = ("x-source-file", "x-source-anchor", "title", "description")


class OverrideError(BuildError):
    """An override file is malformed or names something the spec does not have."""


@dataclass(frozen=True)
class Override:
    """One retyping of a schema, or of one property of a schema."""

    schema: str
    property: str | None
    replace: dict[str, Any]
    evidence: str
    reason: str

    @builtins.property
    def target(self) -> str:
        """The target as written in error messages."""
        return self.schema if self.property is None else f"{self.schema}.{self.property}"


def _string_list(entry: dict[str, Any], key: str, where: str, *, required: bool) -> list[str]:
    value = entry.get(key)
    if value is None and not required:
        return []
    if not isinstance(value, list) or not value or not all(isinstance(v, str) and v for v in value):
        raise OverrideError(f"{where}: {key!r} must be a non-empty list of names")
    return list(value)


def load_overrides(path: Path = OVERRIDES_PATH) -> list[Override]:
    """Read ``path`` and return its overrides, one per ``schemas x properties`` pair.

    Raises:
        OverrideError: On an unknown key, an evidence value other than ``live`` or
            ``inferred``, an empty reason, an empty or non-mapping ``replace``, or
            a target listed twice.
    """
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    entries = data.get("overrides") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        raise OverrideError(f"{path.name}: expected a mapping with an 'overrides' list")
    loaded: list[Override] = []
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        where = f"{path.name}: overrides[{index}]"
        if not isinstance(entry, dict):
            raise OverrideError(f"{where}: must be a mapping")
        unknown = sorted(set(entry) - _ENTRY_KEYS)
        if unknown:
            raise OverrideError(f"{where}: unknown key(s) {unknown}")
        evidence = entry.get("evidence")
        if evidence not in EVIDENCE_VALUES:
            raise OverrideError(
                f"{where}: 'evidence' must be one of {sorted(EVIDENCE_VALUES)}, found {evidence!r}"
            )
        reason = entry.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            raise OverrideError(f"{where}: 'reason' must be a non-empty string")
        replace = entry.get("replace")
        if not isinstance(replace, dict) or not replace:
            raise OverrideError(f"{where}: 'replace' must be a non-empty mapping")
        schemas = _string_list(entry, "schemas", where, required=True)
        properties: list[str | None] = [
            *_string_list(entry, "properties", where, required=False)
        ] or [None]
        for schema in schemas:
            for prop in properties:
                override = Override(schema, prop, copy.deepcopy(replace), evidence, reason.strip())
                if override.target in seen:
                    raise OverrideError(f"{where}: {override.target!r} is overridden twice")
                seen.add(override.target)
                loaded.append(override)
    return loaded


def _record(override: Override, original: dict[str, Any]) -> dict[str, Any]:
    return {
        "evidence": override.evidence,
        "reason": override.reason,
        "original": copy.deepcopy(original),
    }


def apply_overrides(spec: dict[str, Any], overrides: Collection[Override]) -> None:
    """Apply ``overrides`` to ``spec`` in place and record each in an ``x-override`` node.

    A property override keeps the property's ``description`` unless ``replace``
    supplies one. A schema override keeps ``x-source-*``, ``title`` and
    ``description`` and replaces the rest.

    Raises:
        OverrideError: If a schema or property does not exist, a target comes from a
            fragment, or a target already carries ``x-override``.
    """
    schemas: dict[str, Any] = spec["components"]["schemas"]
    fragment_schemas = {
        key
        for entry in (spec["info"].get(_FRAGMENTS_KEY) or {}).values()
        for key in entry.get("schemas", [])
    }
    for override in overrides:
        target = schemas.get(override.schema)
        if target is None:
            raise OverrideError(f"{override.target}: no such schema in the spec")
        if override.schema in fragment_schemas:
            raise OverrideError(f"{override.target}: schema comes from a fragment, edit that")
        if override.property is None:
            if _NODE_KEY in target:
                raise OverrideError(f"{override.target}: already overridden")
            new_schema = {k: target[k] for k in _KEPT_SCHEMA_KEYS if k in target}
            new_schema.update(copy.deepcopy(override.replace))
            new_schema[_NODE_KEY] = _record(override, target)
            schemas[override.schema] = new_schema
            continue
        properties: dict[str, Any] = target.get("properties") or {}
        original = properties.get(override.property)
        if original is None:
            raise OverrideError(f"{override.target}: no such property in the schema")
        if _NODE_KEY in original:
            raise OverrideError(f"{override.target}: already overridden")
        new_property = copy.deepcopy(override.replace)
        if "description" in original and "description" not in new_property:
            new_property["description"] = original["description"]
        new_property[_NODE_KEY] = _record(override, original)
        properties[override.property] = new_property


def strip_overrides(spec: dict[str, Any]) -> None:
    """Restore every node that carries ``x-override`` to its recorded original."""
    schemas: dict[str, Any] = spec["components"]["schemas"]
    for key, schema in list(schemas.items()):
        if _NODE_KEY in schema:
            schemas[key] = copy.deepcopy(schema[_NODE_KEY]["original"])
            continue
        properties = schema.get("properties")
        if not isinstance(properties, dict):
            continue
        for name, prop in list(properties.items()):
            if isinstance(prop, dict) and _NODE_KEY in prop:
                properties[name] = copy.deepcopy(prop[_NODE_KEY]["original"])
