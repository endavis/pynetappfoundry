"""TOML overlay loader for cache field strategies.

Reads package-default TOML overlay files that define per-field
``cache_strategy`` and ``requires_explicit_fetch`` values, optionally
merges user overrides, and applies the merged configuration to
registered ``TypeMapping`` instances in the model registry.
"""

from __future__ import annotations

import logging
import tomllib
from dataclasses import replace
from pathlib import Path
from typing import Any

from pynetappfoundry.cache._registry import ModelRegistry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping

logger = logging.getLogger(__name__)

_PACKAGE_OVERLAY_ROOT = Path(__file__).parent / "ontap"


def discover_toml_overlays(root: Path) -> dict[str, Path]:
    """Recursively discover TOML overlay files and map class names to paths.

    Each TOML file is expected to contain an ``[endpoint]`` table with a
    ``class_name`` key.  Files missing this key are silently skipped.

    Args:
        root: Directory to search recursively for ``*.toml`` files.

    Returns:
        Mapping of ``class_name`` to the ``Path`` of its overlay file.
    """
    result: dict[str, Path] = {}
    if not root.is_dir():
        return result

    for toml_path in sorted(root.rglob("*.toml")):
        try:
            with toml_path.open("rb") as fh:
                data = tomllib.load(fh)
        except tomllib.TOMLDecodeError:
            logger.warning("Skipping malformed TOML: %s", toml_path)
            continue

        endpoint = data.get("endpoint")
        if not isinstance(endpoint, dict):
            continue
        class_name = endpoint.get("class_name")
        if not class_name:
            continue

        if class_name in result:
            logger.warning(
                "Duplicate class_name %r: %s shadows %s",
                class_name,
                toml_path,
                result[class_name],
            )
        result[class_name] = toml_path

    return result


def load_overlay(path: Path) -> dict[str, Any]:
    """Load and return the contents of a TOML overlay file.

    Args:
        path: Path to the TOML file.

    Returns:
        Parsed TOML data as a dict.

    Raises:
        FileNotFoundError: If *path* does not exist.
        tomllib.TOMLDecodeError: If the file is malformed.
    """
    with path.open("rb") as fh:
        return tomllib.load(fh)


def merge_overlays(
    package: dict[str, Any],
    user: dict[str, Any] | None,
) -> dict[str, dict[str, Any]]:
    """Merge package-default and user-override field configurations.

    Extracts the ``fields`` table from each overlay dict.  User fields
    completely replace the package default at field-level granularity
    (i.e. the entire sub-dict for a field name is replaced, not merged
    key-by-key within a field).

    Args:
        package: Parsed package-default overlay.
        user: Parsed user-override overlay, or ``None``.

    Returns:
        Merged ``{field_name: {config_key: value, ...}}`` dict.
    """
    merged = dict(package.get("fields", {}))
    if user is not None:
        merged.update(user.get("fields", {}))
    return merged


def apply_overlay_to_mapping(
    mapping: TypeMapping,
    fields_config: dict[str, dict[str, Any]],
) -> TypeMapping:
    """Apply overlay field configuration to a ``TypeMapping``.

    For each field in the mapping whose ``cache_attr`` appears in
    *fields_config*, creates a new ``FieldMapping`` with updated
    ``cache_strategy`` and/or ``requires_explicit_fetch`` values.

    Args:
        mapping: The original (frozen) type mapping.
        fields_config: ``{field_name: {"cache_strategy": ..., ...}}`` dict.

    Returns:
        New ``TypeMapping`` with updated field definitions.
    """
    new_fields: list[FieldMapping] = []
    for field in mapping.fields:
        config = fields_config.get(field.cache_attr)
        if config is None:
            new_fields.append(field)
            continue

        replacements: dict[str, Any] = {}
        if "cache_strategy" in config:
            replacements["cache_strategy"] = config["cache_strategy"]
        if "requires_explicit_fetch" in config:
            replacements["requires_explicit_fetch"] = config["requires_explicit_fetch"]

        if replacements:
            new_fields.append(replace(field, **replacements))
        else:
            new_fields.append(field)

    return replace(mapping, fields=tuple(new_fields))


def load_overlays(
    registry: ModelRegistry,
    user_overlay_dir: Path | None = None,
) -> int:
    """Load TOML overlays and apply field strategies to registry mappings.

    Discovers package-default overlays under the built-in ``ontap/``
    tree, optionally discovers user overrides, merges them, and updates
    each matching ``TypeMapping`` in *registry*.

    Args:
        registry: The model registry containing type mappings.
        user_overlay_dir: Optional directory with user-override TOML files
            that mirror the package tree structure.

    Returns:
        Number of mappings updated.
    """
    package_overlays = discover_toml_overlays(_PACKAGE_OVERLAY_ROOT)

    user_overlays: dict[str, Path] = {}
    if user_overlay_dir is not None:
        user_overlays = discover_toml_overlays(user_overlay_dir)

    updated = 0
    for class_name, pkg_path in package_overlays.items():
        mapping = registry.get_mapping(class_name)
        if mapping is None:
            continue

        pkg_data = load_overlay(pkg_path)

        user_data: dict[str, Any] | None = None
        if class_name in user_overlays:
            user_data = load_overlay(user_overlays[class_name])

        fields_config = merge_overlays(pkg_data, user_data)
        new_mapping = apply_overlay_to_mapping(mapping, fields_config)
        registry.register_mapping(class_name, new_mapping)
        updated += 1

    return updated
