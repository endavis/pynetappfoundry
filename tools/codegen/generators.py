"""Code generators for cache models, mappings, and TOML overlays.

Produces Python source code and TOML configuration files from
:class:`~tools.codegen.adapters.ParsedEndpoint` data.  Generated output
follows the project's URL-tree convention (ADR-0007).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    import tomli as tomllib  # type: ignore[no-redef]

import tomli_w

from tools.codegen.adapters import ParsedEndpoint, ParsedField


def _path_to_module_parts(api_path: str) -> list[str]:
    """Convert an API path to Python module path parts.

    ``"/storage/volumes"`` → ``["storage", "volumes"]``
    ``"/network/ip/interfaces"`` → ``["network", "ip", "interfaces"]``

    Strips path parameters and converts hyphens to underscores.

    Args:
        api_path: API endpoint path.

    Returns:
        List of Python module name segments.
    """
    segments = api_path.strip("/").split("/")
    result = []
    for seg in segments:
        if "{" in seg:
            continue
        result.append(seg.replace("-", "_"))
    return result


def _path_to_class_name(api_path: str) -> str:
    """Convert an API path to a PascalCase class name.

    ``"/storage/volumes"`` → ``"StorageVolume"``
    ``"/network/ip/interfaces"`` → ``"NetworkIpInterface"``

    Uses singular form by stripping trailing ``s`` from the last segment.

    Args:
        api_path: API endpoint path.

    Returns:
        PascalCase class name string.
    """
    parts = _path_to_module_parts(api_path)
    words = []
    for i, part in enumerate(parts):
        # Singularize only the last segment
        if i == len(parts) - 1:
            part = _singularize(part)
        # Convert underscores to PascalCase
        for word in part.split("_"):
            words.append(word.capitalize())
    return "".join(words)


def _singularize(name: str) -> str:
    """Naive singularization of a plural resource name.

    Handles common patterns: ``policies`` → ``policy``,
    ``interfaces`` → ``interface``, ``volumes`` → ``volume``.

    Args:
        name: Plural resource name.

    Returns:
        Singular form.
    """
    if name.endswith("ies"):
        return name[:-3] + "y"
    if name.endswith("ses") or name.endswith("xes") or name.endswith("zes"):
        return name[:-2]
    if name.endswith("s") and not name.endswith("ss"):
        return name[:-1]
    return name


def _field_to_cache_attr(field: ParsedField) -> str:
    """Convert a ParsedField's api_path to a flat cache attribute name.

    ``"svm.name"`` → ``"svm_name"``
    ``"autosize.mode"`` → ``"autosize_mode"``
    ``"nas.export_policy.name"`` → ``"nas_export_policy_name"``

    Args:
        field: Parsed field.

    Returns:
        Flat Python attribute name.
    """
    return field.api_path.replace(".", "_").replace("-", "_")


def _python_type_annotation(field: ParsedField) -> str:
    """Get the Python type annotation string for a field.

    Args:
        field: Parsed field.

    Returns:
        Type annotation string.
    """
    if field.is_uuid:
        return "OntapUUID"
    if field.is_list:
        return field.python_type
    return field.python_type


def _python_default_repr(field: ParsedField) -> str:
    """Get the Python default value representation for a field.

    Args:
        field: Parsed field.

    Returns:
        Default value as Python source code.
    """
    if field.is_list:
        return "Field(default_factory=list)"
    default = field.default
    if isinstance(default, str):
        return f'"{default}"'
    if isinstance(default, bool):
        return "True" if default else "False"
    return repr(default)


def _select_leaf_fields(fields: list[ParsedField]) -> list[ParsedField]:
    """Select only leaf (non-object) fields for model generation.

    Object fields are flattened — we include their children, not the
    parent. For array-of-objects, we include the array field itself
    (typed as ``list[dict[str, Any]]``).

    Args:
        fields: All parsed fields including nested objects.

    Returns:
        List of leaf fields suitable for model attributes.
    """
    leaves = []
    for f in fields:
        if f.is_object and not f.is_list:
            # Skip pure object containers — their children are already
            # in the list as separate flat fields
            continue
        leaves.append(f)
    return leaves


def generate_model(endpoint: ParsedEndpoint, api_type: str = "ontap") -> str:
    """Generate a Pydantic model class for an endpoint.

    Produces a flat ``CacheModel`` subclass following ADR-0007 naming.

    Args:
        endpoint: Parsed endpoint with fields.
        api_type: API type for import path context.

    Returns:
        Python source code for the model module.
    """
    class_name = _path_to_class_name(endpoint.path)
    doc = f"{class_name} — {endpoint.path}."
    leaves = _select_leaf_fields(endpoint.fields)

    needs_field_import = any(f.is_list for f in leaves)
    needs_any_import = any(f.is_list and f.is_object for f in leaves)
    needs_uuid_import = any(f.is_uuid for f in leaves)

    lines = [
        f'"""{doc}"""',
        "",
        "from __future__ import annotations",
        "",
    ]

    # Conditional imports
    if needs_any_import:
        lines.append("from typing import Any")
        lines.append("")

    pydantic_imports = ["Field"] if needs_field_import else []
    if not pydantic_imports:
        # No pydantic imports needed beyond CacheModel
        pass

    base_imports = ["CacheModel"]
    if needs_uuid_import:
        base_imports.append("OntapUUID")

    if pydantic_imports:
        lines.append(f"from pydantic import {', '.join(sorted(pydantic_imports))}")
        lines.append("")

    lines.append(f"from pynetappfoundry.cache._base import {', '.join(sorted(base_imports))}")
    lines.append("")
    lines.append("")
    lines.append(f"class {class_name}(CacheModel):")
    lines.append(f'    """{class_name} information."""')
    lines.append("")

    if not leaves:
        lines.append("    pass")
    else:
        for field in leaves:
            attr = _field_to_cache_attr(field)
            type_ann = _python_type_annotation(field)
            default_repr = _python_default_repr(field)
            lines.append(f"    {attr}: {type_ann} = {default_repr}")

    lines.append("")
    return "\n".join(lines)


def generate_mapping(
    endpoint: ParsedEndpoint,
    api_type: str = "ontap",
) -> str:
    """Generate a TypeMapping/FieldMapping module for an endpoint.

    Produces a ``mapping.py`` file with the mapping constant and
    registry registration call.

    Args:
        endpoint: Parsed endpoint with fields.
        api_type: API type tag.

    Returns:
        Python source code for the mapping module.
    """
    class_name = _path_to_class_name(endpoint.path)
    module_parts = _path_to_module_parts(endpoint.path)
    mapping_name = f"{class_name.upper()}_MAPPING"
    leaves = _select_leaf_fields(endpoint.fields)

    # Build the import path for the model
    model_import = f"pynetappfoundry.cache.{'.'.join(module_parts)}.model"

    lines = [
        f'"""{class_name} type mapping — {endpoint.path}."""',
        "",
        "from __future__ import annotations",
        "",
        "from pynetappfoundry.cache._registry import model_registry",
        "from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping",
        f"from {model_import} import {class_name}",
        "",
        "",
        f"{mapping_name} = TypeMapping(",
        f'    name="{class_name}",',
        f"    model_class={class_name},",
        f'    api_endpoint="{endpoint.path}?fields=*',
    ]

    # Add expensive fields to the endpoint query
    expensive = [f for f in leaves if f.requires_explicit_fetch]
    if expensive:
        # Group by top-level prefix
        top_level = sorted({f.api_path.split(".")[0] for f in expensive})
        lines[-1] += "," + ",".join(top_level)

    lines[-1] += '",'

    lines.append(f'    api_type="{api_type}",')

    if endpoint.records_path != "records":
        lines.append(f'    records_path="{endpoint.records_path}",')

    if endpoint.has_parent:
        # Derive parent mapping name from parent path
        parent_class = _path_to_class_name(endpoint.parent_path)
        lines.append(f'    parent_mapping="{parent_class}",')
        lines.append('    parent_id_field="uuid",')

    lines.append("    fields=(")

    for field in leaves:
        attr = _field_to_cache_attr(field)
        default_repr = _python_default_repr(field)

        field_args = [f'        cache_attr="{attr}"']
        field_args.append(f'        api_path="{field.api_path}"')

        if field.default != "":
            field_args.append(f"        default={default_repr}")

        if field.requires_explicit_fetch:
            field_args.append("        requires_explicit_fetch=True")

        lines.append("        FieldMapping(")
        for arg in field_args:
            lines.append(f"    {arg},")
        lines.append("        ),")

    lines.append("    ),")
    lines.append(")")
    lines.append("")
    lines.append(f'model_registry.register_mapping("{class_name}", {mapping_name})')
    lines.append("")

    return "\n".join(lines)


def generate_init(endpoint: ParsedEndpoint) -> str:
    """Generate an ``__init__.py`` for an endpoint's package.

    Args:
        endpoint: Parsed endpoint.

    Returns:
        Python source code for ``__init__.py``.
    """
    class_name = _path_to_class_name(endpoint.path)
    module_parts = _path_to_module_parts(endpoint.path)

    lines = [
        f'"""{class_name} cache model — /{"/".join(module_parts)}."""',
        "",
        f"from pynetappfoundry.cache.{'.'.join(module_parts)}.model import {class_name}",
        "",
        f'__all__ = ["{class_name}"]',
        "",
    ]
    return "\n".join(lines)


def generate_toml_overlay(
    endpoint: ParsedEndpoint,
    existing_path: Path | None = None,
) -> str:
    """Generate or update a TOML overlay for an endpoint.

    If ``existing_path`` points to an existing TOML file, user edits
    are preserved — new fields get defaults, removed fields get a
    warning comment.

    Args:
        endpoint: Parsed endpoint with fields.
        existing_path: Path to existing overlay file, or None.

    Returns:
        TOML content as a string.
    """
    class_name = _path_to_class_name(endpoint.path)
    leaves = _select_leaf_fields(endpoint.fields)

    # Load existing overlay if present
    existing: dict[str, Any] = {}
    if existing_path and existing_path.exists():
        with open(existing_path, "rb") as f:
            existing = tomllib.load(f)

    existing_fields = existing.get("fields", {})

    # Build new overlay
    overlay: dict[str, Any] = {
        "endpoint": {
            "path": endpoint.path,
            "schema": endpoint.schema_name,
            "class_name": class_name,
        },
        "fields": {},
    }

    for field in leaves:
        attr = _field_to_cache_attr(field)
        if attr in existing_fields:
            # Preserve user edits
            overlay["fields"][attr] = existing_fields[attr]
        else:
            entry: dict[str, Any] = {"cache_strategy": "cache"}
            if field.requires_explicit_fetch:
                entry["requires_explicit_fetch"] = True
            overlay["fields"][attr] = entry

    # Warn about removed fields
    removed = set(existing_fields) - {_field_to_cache_attr(f) for f in leaves}
    if removed:
        overlay["_removed_fields"] = sorted(removed)

    return tomli_w.dumps(overlay)


def write_endpoint_files(
    endpoint: ParsedEndpoint,
    output_dir: Path,
    api_type: str = "ontap",
    overlay_dir: Path | None = None,
) -> list[Path]:
    """Write all generated files for an endpoint.

    Creates the directory tree under ``output_dir`` following ADR-0007's
    URL-tree convention, then writes ``model.py``, ``mapping.py``,
    ``__init__.py``, and optionally a TOML overlay.

    Args:
        endpoint: Parsed endpoint with fields.
        output_dir: Root output directory (e.g. ``src/pynetappfoundry/cache/``).
        api_type: API type tag.
        overlay_dir: Directory for TOML overlay files.  If None, overlays
            are written next to the model files.

    Returns:
        List of paths to all files written.
    """
    module_parts = _path_to_module_parts(endpoint.path)
    pkg_dir = output_dir
    for part in module_parts:
        pkg_dir = pkg_dir / part

    pkg_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    # Also ensure intermediate __init__.py files exist
    _ensure_init_files(output_dir, module_parts)

    # model.py
    model_path = pkg_dir / "model.py"
    model_path.write_text(generate_model(endpoint, api_type))
    written.append(model_path)

    # mapping.py
    mapping_path = pkg_dir / "mapping.py"
    mapping_path.write_text(generate_mapping(endpoint, api_type))
    written.append(mapping_path)

    # __init__.py for the leaf package
    init_path = pkg_dir / "__init__.py"
    init_path.write_text(generate_init(endpoint))
    written.append(init_path)

    # TOML overlay
    toml_dir = overlay_dir or pkg_dir
    toml_dir.mkdir(parents=True, exist_ok=True)
    toml_path = toml_dir / f"{module_parts[-1]}.toml"
    existing = toml_path if toml_path.exists() else None
    toml_path.write_text(generate_toml_overlay(endpoint, existing))
    written.append(toml_path)

    return written


def _ensure_init_files(base_dir: Path, parts: list[str]) -> None:
    """Ensure ``__init__.py`` exists at every intermediate directory.

    Args:
        base_dir: Root directory.
        parts: Module path segments.
    """
    current = base_dir
    for part in parts[:-1]:  # Skip the leaf — it gets a full __init__.py
        current = current / part
        current.mkdir(parents=True, exist_ok=True)
        init_file = current / "__init__.py"
        if not init_file.exists():
            pkg_name = part.replace("_", " ").title()
            init_file.write_text(f'"""{pkg_name} cache models."""\n')
