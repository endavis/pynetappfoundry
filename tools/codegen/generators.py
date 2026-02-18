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


_CLASS_NAME_OVERRIDES: dict[str, str] = {}
"""Manual overrides for class names keyed by API path.

Use this as an escape hatch for names the algorithm can't handle.
Example: ``{"/some/weird/path": "OntapBetterName"}``.
"""


def _schema_to_pascal(name: str) -> str:
    """Convert a snake_case schema name to PascalCase.

    ``"cloud_target"`` → ``"CloudTarget"``
    ``"ip_interface"`` → ``"IpInterface"``
    ``"svm"`` → ``"Svm"``

    Args:
        name: Schema name (typically snake_case).

    Returns:
        PascalCase string.
    """
    return "".join(w.capitalize() for w in name.split("_"))


def _path_to_class_name(
    api_path: str,
    schema_name: str = "",
    api_type: str = "ontap",
) -> str:
    """Derive a PascalCase class name for an API endpoint.

    Uses ``{ApiType}{SchemaName}`` when a schema ``$ref`` name is
    available.  Falls back to ``{ApiType}{UrlPathDerived}`` for inline
    schemas (with redundant-segment deduplication).

    Examples (with ``api_type="ontap"``):

    * ``schema_name="volume"`` → ``"OntapVolume"``
    * ``schema_name="svm"`` → ``"OntapSvm"``
    * ``schema_name="cloud_target"`` → ``"OntapCloudTarget"``
    * ``schema_name=""`` (inline), path ``"/cluster"`` → ``"OntapCluster"``
    * ``schema_name=""`` (inline), path ``"/cluster/licensing/licenses"``
      → ``"OntapClusterLicensingLicense"``

    Args:
        api_path: API endpoint path.
        schema_name: Schema ``$ref`` name (e.g. ``"volume"``).
            Empty string for inline schemas.
        api_type: API type prefix (e.g. ``"ontap"``, ``"aiqum"``).

    Returns:
        PascalCase class name string.
    """
    if api_path in _CLASS_NAME_OVERRIDES:
        return _CLASS_NAME_OVERRIDES[api_path]

    prefix = api_type.capitalize()

    if schema_name:
        return f"{prefix}{_schema_to_pascal(schema_name)}"

    # Fallback: derive from the URL path
    parts = _path_to_module_parts(api_path)
    if parts:
        parts[-1] = _singularize(parts[-1])

    # Remove redundant segments
    deduped: list[str] = []
    for i, part in enumerate(parts):
        if part in parts[i + 1 :]:
            continue
        deduped.append(part)

    words = []
    for part in deduped:
        for word in part.split("_"):
            words.append(word.capitalize())
    return f"{prefix}{''.join(words)}"


_SINGULAR_EXCEPTIONS: dict[str, str] = {
    "dns": "dns",
    "licenses": "license",
    "chassis": "chassis",
    "flexcaches": "flexcache",
    "status": "status",
    "alias": "alias",
    "bus": "bus",
    "metrocluster": "metrocluster",
    "nfs": "nfs",
    "cifs": "cifs",
    "s3": "s3",
    "iscsi": "iscsi",
    "nvme": "nvme",
    "fpolicy": "fpolicy",
}


def _singularize(name: str) -> str:
    """Singularize a plural resource name.

    Checks an exception dictionary first, then applies common English
    pluralization rules.

    Args:
        name: Plural resource name.

    Returns:
        Singular form.
    """
    if name in _SINGULAR_EXCEPTIONS:
        return _SINGULAR_EXCEPTIONS[name]
    if name.endswith("ies"):
        return name[:-3] + "y"
    if name.endswith("ses") or name.endswith("xes") or name.endswith("zes"):
        return name[:-2]
    if name.endswith("s") and not name.endswith("ss"):
        return name[:-1]
    return name


_PYTHON_KEYWORDS: frozenset[str] = frozenset(
    {
        "False",
        "None",
        "True",
        "and",
        "as",
        "assert",
        "async",
        "await",
        "break",
        "class",
        "continue",
        "def",
        "del",
        "elif",
        "else",
        "except",
        "finally",
        "for",
        "from",
        "global",
        "if",
        "import",
        "in",
        "is",
        "lambda",
        "nonlocal",
        "not",
        "or",
        "pass",
        "raise",
        "return",
        "try",
        "while",
        "with",
        "yield",
        "type",
        # Pydantic BaseModel reserved attributes
        "schema",
        "model",
    }
)


def _safe_attr_name(name: str) -> str:
    """Append underscore to Python reserved words.

    ``"class"`` → ``"class_"``
    ``"type"`` → ``"type_"``
    """
    return f"{name}_" if name in _PYTHON_KEYWORDS else name


def _field_to_cache_attr(field: ParsedField) -> str:
    """Convert a ParsedField's api_path to a flat cache attribute name.

    ``"svm.name"`` → ``"svm_name"``
    ``"autosize.mode"`` → ``"autosize_mode"``
    ``"nas.export_policy.name"`` → ``"nas_export_policy_name"``
    ``"class"`` → ``"class_"``

    Args:
        field: Parsed field.

    Returns:
        Flat Python attribute name.
    """
    attr = field.api_path.replace(".", "_").replace("-", "_")
    return _safe_attr_name(attr)


def _sub_model_name(parent_class: str, field: ParsedField) -> str:
    """Build a sub-model class name for an array-of-objects field.

    Convention: ``{ParentClassName}{FieldNameSingularized}``.

    ``StorageSnapshotPolicy`` + ``copies`` → ``StorageSnapshotPolicyCopy``

    Args:
        parent_class: Parent model class name.
        field: The array-of-objects field.

    Returns:
        Sub-model class name.
    """
    singular = _singularize(field.name)
    # PascalCase the singular field name
    pascal = "".join(w.capitalize() for w in singular.split("_"))
    return f"{parent_class}{pascal}"


def _has_typed_sub_fields(field: ParsedField) -> bool:
    """Check if a field should get a typed sub-model.

    True when the field is an array of objects with at least one
    non-object sub-field (i.e. actual leaf data to model).
    """
    if not (field.is_list and field.is_object and field.sub_fields):
        return False
    return any(not (sf.is_object and not sf.is_list) for sf in field.sub_fields)


def _python_type_annotation(field: ParsedField, sub_model_map: dict[str, str] | None = None) -> str:
    """Get the Python type annotation string for a field.

    Args:
        field: Parsed field.
        sub_model_map: Optional mapping from field api_path to sub-model class name.

    Returns:
        Type annotation string.
    """
    if field.is_uuid:
        return "OntapUUID"
    if sub_model_map and field.api_path in sub_model_map:
        return f"list[{sub_model_map[field.api_path]}]"
    if field.is_list:
        return field.python_type
    return field.python_type


def _python_default_repr(field: ParsedField, *, for_mapping: bool = False) -> str:
    """Get the Python default value representation for a field.

    Args:
        field: Parsed field.
        for_mapping: If True, emit plain ``[]`` for list fields instead of
            ``Field(default_factory=list)``.  FieldMapping defaults are plain
            values, not Pydantic Field descriptors.

    Returns:
        Default value as Python source code.
    """
    if field.is_list:
        return "[]" if for_mapping else "Field(default_factory=list)"
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
    Array-of-objects fields with sub-fields get typed sub-model classes
    defined before the parent class.

    Args:
        endpoint: Parsed endpoint with fields.
        api_type: API type for import path context.

    Returns:
        Python source code for the model module.
    """
    class_name = _path_to_class_name(endpoint.path, endpoint.schema_name, api_type)
    doc = f"{class_name} information."
    leaves = _select_leaf_fields(endpoint.fields)

    # Identify fields that get typed sub-models
    sub_model_map: dict[str, str] = {}  # field api_path -> sub-model class name
    sub_model_fields: list[tuple[str, ParsedField]] = []  # (sub_class_name, field)
    _seen_sub_names: dict[str, int] = {}
    for field in leaves:
        if _has_typed_sub_fields(field):
            sub_cls = _sub_model_name(class_name, field)
            # Deduplicate sub-model class names
            if sub_cls in _seen_sub_names:
                _seen_sub_names[sub_cls] += 1
                sub_cls = f"{sub_cls}{_seen_sub_names[sub_cls]}"
            else:
                _seen_sub_names[sub_cls] = 1
            sub_model_map[field.api_path] = sub_cls
            sub_model_fields.append((sub_cls, field))

    needs_field_import = any(f.is_list for f in leaves)
    # Only need Any import if there are list-of-object fields WITHOUT sub-models
    needs_any_import = any(
        f.is_list and f.is_object and f.api_path not in sub_model_map for f in leaves
    )
    needs_uuid_import = any(f.is_uuid for f in leaves)

    # Check sub-model fields for UUID needs and Any needs
    for _sub_cls, sf in sub_model_fields:
        sub_leaves = _select_leaf_fields(sf.sub_fields)
        if any(ssf.is_uuid for ssf in sub_leaves):
            needs_uuid_import = True
        # Sub-model may have list[dict[str, Any]] fields that need Any import
        if any(ssf.is_list and ssf.is_object for ssf in sub_leaves):
            needs_any_import = True
        # Sub-model may have list fields needing Field import
        if any(ssf.is_list for ssf in sub_leaves):
            needs_field_import = True

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

    base_imports = ["CacheModel"]
    if needs_uuid_import:
        base_imports.append("OntapUUID")

    if pydantic_imports:
        lines.append(f"from pydantic import {', '.join(sorted(pydantic_imports))}")
        lines.append("")

    lines.append(f"from pynetappfoundry.cache._base import {', '.join(sorted(base_imports))}")
    lines.append("")

    # Generate sub-model classes before the parent
    for sub_cls, field in sub_model_fields:
        lines.append("")
        lines.append(f"class {sub_cls}(CacheModel):")
        lines.append(f'    """{sub_cls} sub-model for {field.name}."""')
        lines.append("")
        sub_leaves = _select_leaf_fields(field.sub_fields)
        if not sub_leaves:
            lines.append("    pass")
        else:
            seen_attrs: set[str] = set()
            for sf in sub_leaves:
                attr = _safe_attr_name(sf.api_path.replace(".", "_").replace("-", "_"))
                # Deduplicate: if attr already seen, skip
                if attr in seen_attrs:
                    continue
                seen_attrs.add(attr)
                type_ann = _python_type_annotation(sf)
                default_repr = _python_default_repr(sf)
                lines.append(f"    {attr}: {type_ann} = {default_repr}")
        lines.append("")

    lines.append("")
    lines.append(f"class {class_name}(CacheModel):")
    lines.append(f'    """{class_name} information."""')
    lines.append("")

    if not leaves:
        lines.append("    pass")
    else:
        parent_seen: set[str] = set()
        for field in leaves:
            attr = _field_to_cache_attr(field)
            if attr in parent_seen:
                continue  # skip duplicate flattened names
            parent_seen.add(attr)
            type_ann = _python_type_annotation(field, sub_model_map)
            default_repr = _python_default_repr(field)
            lines.append(f"    {attr}: {type_ann} = {default_repr}")

    lines.append("")
    result = "\n".join(lines)
    # Add noqa directives for generated code that can't conform to lint rules
    noqa_codes: list[str] = []
    if any(len(line) > 100 for line in lines):
        noqa_codes.append("E501")
    # Detect mixed-case field names from the API (e.g., isDnsTTLEnabled)
    all_attrs = [_field_to_cache_attr(f) for f in leaves] if leaves else []
    if any(c.isupper() for attr in all_attrs for c in attr):
        noqa_codes.append("N815")
    if noqa_codes:
        result = f"# ruff: noqa: {', '.join(noqa_codes)}\n" + result
    return result


def generate_mapping(
    endpoint: ParsedEndpoint,
    api_type: str = "ontap",
    schema_lookup: dict[str, str] | None = None,
) -> str:
    """Generate a TypeMapping/FieldMapping module for an endpoint.

    Produces a ``mapping.py`` file with the mapping constant and
    registry registration call.  Array-of-objects fields with typed
    sub-models get transform functions that construct sub-model instances.

    Args:
        endpoint: Parsed endpoint with fields.
        api_type: API type tag.
        schema_lookup: Optional mapping of API path → schema name for
            resolving parent class names.

    Returns:
        Python source code for the mapping module.
    """
    class_name = _path_to_class_name(endpoint.path, endpoint.schema_name, api_type)
    module_parts = _path_to_module_parts(endpoint.path)
    mapping_name = f"{class_name.upper()}_MAPPING"
    leaves = _select_leaf_fields(endpoint.fields)

    # Identify sub-model fields (must mirror dedup logic from generate_model)
    sub_model_map: dict[str, str] = {}
    _seen_sub_names: dict[str, int] = {}
    for field in leaves:
        if _has_typed_sub_fields(field):
            sub_cls = _sub_model_name(class_name, field)
            if sub_cls in _seen_sub_names:
                _seen_sub_names[sub_cls] += 1
                sub_cls = f"{sub_cls}{_seen_sub_names[sub_cls]}"
            else:
                _seen_sub_names[sub_cls] = 1
            sub_model_map[field.api_path] = sub_cls

    # Build the import path for the model
    model_import = f"pynetappfoundry.cache.{api_type}.{'.'.join(module_parts)}.model"

    # Build model imports (parent class + any sub-model classes)
    model_classes = [class_name, *sorted(sub_model_map.values())]

    docstring = f'"""{class_name} type mapping."""'
    lines = [
        docstring,
        "",
        "from __future__ import annotations",
        "",
    ]

    if sub_model_map:
        lines.append("from typing import Any")
        lines.append("")

    lines.extend(
        [
            "from pynetappfoundry.cache._registry import model_registry",
            "from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping",
        ]
    )
    # Split long model import across multiple lines
    model_import_line = f"from {model_import} import {', '.join(model_classes)}"
    if len(model_import_line) > 100:
        lines.append(f"from {model_import} import (")
        for cls in model_classes:
            lines.append(f"    {cls},")
        lines.append(")")
    else:
        lines.append(model_import_line)

    # Generate transform functions for sub-model fields
    if sub_model_map:
        for field in leaves:
            if field.api_path not in sub_model_map:
                continue
            sub_cls = sub_model_map[field.api_path]
            func_name = f"_transform_{_field_to_cache_attr(field)}"
            lines.append("")
            lines.append("")
            sig = f"def {func_name}(record: dict[str, Any]) -> list[{sub_cls}]:"
            if len(sig) > 100:
                lines.append(f"def {func_name}(")
                lines.append("    record: dict[str, Any],")
                lines.append(f") -> list[{sub_cls}]:")
            else:
                lines.append(sig)
            lines.append(f'    """Transform {field.api_path} into {sub_cls} list."""')
            ret_line = (
                f'    return [{sub_cls}(**item) for item in record.get("{field.api_path}", [])]'
            )
            if len(ret_line) > 100:
                lines.append("    return [")
                lines.append(f"        {sub_cls}(**item)")
                lines.append(f'        for item in record.get("{field.api_path}", [])')
                lines.append("    ]")
            else:
                lines.append(ret_line)

    lines.append("")
    lines.append("")
    lines.append(f"{mapping_name} = TypeMapping(")
    lines.append(f'    name="{class_name}",')
    lines.append(f"    model_class={class_name},")
    lines.append(f'    api_endpoint="{endpoint.path}?fields=*')

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
        parent_schema = (schema_lookup or {}).get(endpoint.parent_path, "")
        parent_class = _path_to_class_name(endpoint.parent_path, parent_schema, api_type)
        lines.append(f'    parent_mapping="{parent_class}",')
        lines.append('    parent_id_field="uuid",')

    lines.append("    fields=(")

    seen_attrs: set[str] = set()
    for field in leaves:
        attr = _field_to_cache_attr(field)
        if attr in seen_attrs:
            continue
        seen_attrs.add(attr)
        default_repr = _python_default_repr(field, for_mapping=True)

        field_args = [f'        cache_attr="{attr}"']

        if field.api_path in sub_model_map:
            # Sub-model field: use transform instead of api_path
            func_name = f"_transform_{attr}"
            field_args.append(f"        transform={func_name}")
        else:
            field_args.append(f'        api_path="{field.api_path}"')

        if field.default != "" or field.is_list:
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

    result = "\n".join(lines)
    if any(len(line) > 100 for line in lines):
        result = "# ruff: noqa: E501\n" + result
    return result


def generate_init(endpoint: ParsedEndpoint, api_type: str = "ontap") -> str:
    """Generate an ``__init__.py`` for an endpoint's package.

    Args:
        endpoint: Parsed endpoint.
        api_type: API type prefix for class naming.

    Returns:
        Python source code for ``__init__.py``.
    """
    class_name = _path_to_class_name(endpoint.path, endpoint.schema_name, api_type)
    module_parts = _path_to_module_parts(endpoint.path)

    docstring = f'"""{class_name} cache model."""'
    module_path = f"pynetappfoundry.cache.{api_type}.{'.'.join(module_parts)}.model"
    import_line = f"from {module_path} import {class_name}"
    if len(import_line) > 100:
        paren_first_line = f"from {module_path} import ("
        noqa = "  # noqa: E501" if len(paren_first_line) > 100 else ""
        import_line = f"{paren_first_line}{noqa}\n    {class_name},\n)"

    lines = [docstring, "", import_line, "", f'__all__ = ["{class_name}"]', ""]
    return "\n".join(lines)


def generate_toml_overlay(
    endpoint: ParsedEndpoint,
    existing_path: Path | None = None,
    api_type: str = "ontap",
) -> str:
    """Generate or update a TOML overlay for an endpoint.

    If ``existing_path`` points to an existing TOML file, user edits
    are preserved — new fields get defaults, removed fields get a
    warning comment.

    Args:
        endpoint: Parsed endpoint with fields.
        existing_path: Path to existing overlay file, or None.
        api_type: API type prefix for class naming.

    Returns:
        TOML content as a string.
    """
    class_name = _path_to_class_name(endpoint.path, endpoint.schema_name, api_type)
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
    schema_lookup: dict[str, str] | None = None,
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
        schema_lookup: Mapping of API path → schema name for resolving
            parent class names in mappings.

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
    mapping_path.write_text(generate_mapping(endpoint, api_type, schema_lookup))
    written.append(mapping_path)

    # __init__.py for the leaf package
    init_path = pkg_dir / "__init__.py"
    init_path.write_text(generate_init(endpoint, api_type))
    written.append(init_path)

    # TOML overlay
    toml_dir = overlay_dir or pkg_dir
    toml_dir.mkdir(parents=True, exist_ok=True)
    toml_path = toml_dir / f"{module_parts[-1]}.toml"
    existing = toml_path if toml_path.exists() else None
    toml_path.write_text(generate_toml_overlay(endpoint, existing, api_type))
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
