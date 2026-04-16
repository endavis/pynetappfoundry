"""Code generators for cache models, mappings, and TOML overlays.

Produces Python source code and TOML configuration files from
:class:`~tools.codegen.adapters.ParsedEndpoint` data.  Generated output
follows the project's URL-tree convention (ADR-0007).

Models are generated with **nested sub-model classes** that mirror the
ONTAP API structure (ADR-0011).  For example, ``ip.address`` in the API
becomes ``iface.ip.address`` on the Pydantic model, not
``iface.ip_address``.
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
    *,
    shared_schemas: frozenset[str] | set[str] = frozenset(),
) -> str:
    """Derive a PascalCase class name for an API endpoint.

    Uses ``{ApiType}{SchemaName}`` when a schema ``$ref`` name is
    available AND the schema is unique to this endpoint.  Falls back to
    ``{ApiType}{UrlPathDerived}`` for inline schemas OR when the schema
    is shared across multiple endpoints (to avoid registry collisions).

    Examples (with ``api_type="ontap"``):

    * ``schema_name="volume"`` → ``"OntapVolume"``
    * ``schema_name="svm"`` → ``"OntapSvm"``
    * ``schema_name="cloud_target"`` → ``"OntapCloudTarget"``
    * ``schema_name=""`` (inline), path ``"/cluster"`` → ``"OntapCluster"``
    * ``schema_name=""`` (inline), path ``"/cluster/licensing/licenses"``
      → ``"OntapClusterLicensingLicense"``

    DII example (schema ``Count`` shared across 7 endpoints):

    * ``schema_name="Count"``, path ``"/assets/storages/count"``,
      ``shared_schemas={"Count"}`` → ``"DiiAssetsStoragesCount"``
      (URL-path-derived; the schema-derived ``DiiCount`` would collide
      with six other endpoints).

    Args:
        api_path: API endpoint path.
        schema_name: Schema ``$ref`` name (e.g. ``"volume"``).
            Empty string for inline schemas.
        api_type: API type prefix (e.g. ``"ontap"``, ``"aiqum"``).
        shared_schemas: Set of schema names that appear on more than
            one endpoint across the full spec.  When ``schema_name`` is
            in this set, the URL-path fallback is used instead of the
            schema-derived name to produce distinct class names per
            endpoint.  Default is empty (legacy schema-name behavior).

    Returns:
        PascalCase class name string.
    """
    if api_path in _CLASS_NAME_OVERRIDES:
        return _CLASS_NAME_OVERRIDES[api_path]

    prefix = api_type.capitalize()

    if schema_name and schema_name not in shared_schemas:
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
        "copy",
        # Pydantic v2 reserved attributes
        "model_config",
        "model_fields",
        "model_computed_fields",
        "model_extra",
        "model_fields_set",
        "model_post_init",
        "model_validate",
        "model_dump",
        "model_json_schema",
        "metadata",
        "config",
    }
)


def _safe_attr_name(name: str) -> str:
    """Append underscore to Python reserved words.

    ``"class"`` → ``"class_"``
    ``"type"`` → ``"type_"``
    """
    return f"{name}_" if name in _PYTHON_KEYWORDS else name


def _field_to_cache_attr(field: ParsedField) -> str:
    """Convert a ParsedField's api_path to a dot-path cache attribute.

    For nested models the ``cache_attr`` is the same as ``api_path``:
    ``"svm.name"`` → ``"svm.name"``
    ``"nas.export_policy.name"`` → ``"nas.export_policy.name"``

    Python reserved words at any level get an underscore suffix.

    Args:
        field: Parsed field.

    Returns:
        Dot-path cache attribute name.
    """
    parts = field.api_path.replace("-", "_").split(".")
    safe_parts = [_safe_attr_name(p) for p in parts]
    return ".".join(safe_parts)


def _sub_model_name(parent_class: str, field: ParsedField) -> str:
    """Build a sub-model class name for a nested object field.

    Convention: ``{ParentClassName}{FieldNamePascalized}``.

    ``OntapVolume`` + ``svm`` → ``OntapVolumeSvm``
    ``OntapIpInterface`` + ``ip`` → ``OntapIpInterfaceIp``

    For array-of-objects: singularize the field name.
    ``OntapSnapshotPolicy`` + ``copies`` → ``OntapSnapshotPolicyCopy``

    Args:
        parent_class: Parent model class name.
        field: The nested object field.

    Returns:
        Sub-model class name.
    """
    name = field.name.replace("-", "_")
    if field.is_list:
        name = _singularize(name)
    # PascalCase the field name
    pascal = "".join(w.capitalize() for w in name.split("_"))
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
        cls = sub_model_map[field.api_path]
        if field.is_list:
            return f"list[{cls}]"
        return cls
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


# ---------------------------------------------------------------------------
# Nested model generation helpers
# ---------------------------------------------------------------------------


def _collect_all_leaves(fields: list[ParsedField]) -> list[ParsedField]:
    """Recursively collect all leaf fields from a field tree.

    Walks the tree depth-first and returns every non-object scalar field
    and every array-of-objects field.  Pure object containers are skipped
    but their children are included.

    Args:
        fields: Top-level field tree.

    Returns:
        Flat list of all leaf fields with full ``api_path``.
    """
    result: list[ParsedField] = []
    for f in fields:
        if f.is_object and not f.is_list:
            # Recurse into sub-fields
            result.extend(_collect_all_leaves(f.sub_fields))
        else:
            result.append(f)
    return result


def _generate_nested_sub_models(
    parent_class: str,
    fields: list[ParsedField],
    sub_model_map: dict[str, str],
    lines: list[str],
    *,
    _seen_sub_names: dict[str, int] | None = None,
) -> None:
    """Recursively generate nested sub-model classes (deepest-first).

    Modifies *lines* in place with class definitions and populates
    *sub_model_map* with ``{api_path: ClassName}`` entries for every
    generated sub-model.

    Args:
        parent_class: Name of the parent class.
        fields: Fields at the current nesting level.
        sub_model_map: Accumulator for api_path → class name.
        lines: Accumulator for source code lines.
        _seen_sub_names: Deduplication tracker for class names.
    """
    if _seen_sub_names is None:
        _seen_sub_names = {}

    for field in fields:
        if field.is_object and not field.is_list and field.sub_fields:
            # Nested object — generate a sub-model class
            sub_cls = _sub_model_name(parent_class, field)
            if sub_cls in _seen_sub_names:
                _seen_sub_names[sub_cls] += 1
                sub_cls = f"{sub_cls}{_seen_sub_names[sub_cls]}"
            else:
                _seen_sub_names[sub_cls] = 1
            sub_model_map[field.api_path] = sub_cls

            # Recurse first (deepest-first ordering)
            _generate_nested_sub_models(
                sub_cls,
                field.sub_fields,
                sub_model_map,
                lines,
                _seen_sub_names=_seen_sub_names,
            )

            # Now emit this sub-model class
            lines.append("")
            lines.append(f"class {sub_cls}(OntapModel):")
            lines.append(f'    """{sub_cls} sub-model for {field.name}."""')
            lines.append("")

            has_fields = False
            for sf in field.sub_fields:
                attr = _safe_attr_name(sf.name.replace("-", "_"))
                if sf.is_object and not sf.is_list and sf.api_path in sub_model_map:
                    # Nested object field — typed as sub-model with default_factory
                    nested_cls = sub_model_map[sf.api_path]
                    lines.append(f"    {attr}: {nested_cls} = Field(default_factory={nested_cls})")
                    has_fields = True
                elif sf.is_list and sf.is_object and sf.api_path in sub_model_map:
                    # Array-of-objects with typed sub-model
                    nested_cls = sub_model_map[sf.api_path]
                    lines.append(f"    {attr}: list[{nested_cls}] = Field(default_factory=list)")
                    has_fields = True
                elif sf.is_object and not sf.is_list:
                    # Object without sub-fields (shouldn't happen but be safe)
                    continue
                else:
                    # Scalar or simple list
                    type_ann = _python_type_annotation(sf, sub_model_map)
                    default_repr = _python_default_repr(sf)
                    lines.append(f"    {attr}: {type_ann} = {default_repr}")
                    has_fields = True

            if not has_fields:
                lines.append("    pass")
            lines.append("")

        elif field.is_list and field.is_object and _has_typed_sub_fields(field):
            # Array-of-objects — generate a sub-model for array items
            sub_cls = _sub_model_name(parent_class, field)
            if sub_cls in _seen_sub_names:
                _seen_sub_names[sub_cls] += 1
                sub_cls = f"{sub_cls}{_seen_sub_names[sub_cls]}"
            else:
                _seen_sub_names[sub_cls] = 1
            sub_model_map[field.api_path] = sub_cls

            # Recurse into sub-fields for deeper nesting
            _generate_nested_sub_models(
                sub_cls,
                field.sub_fields,
                sub_model_map,
                lines,
                _seen_sub_names=_seen_sub_names,
            )

            # Emit the sub-model class
            lines.append("")
            lines.append(f"class {sub_cls}(OntapModel):")
            lines.append(f'    """{sub_cls} sub-model for {field.name}."""')
            lines.append("")

            has_fields = False
            for sf in field.sub_fields:
                if sf.is_object and not sf.is_list and sf.api_path in sub_model_map:
                    nested_cls = sub_model_map[sf.api_path]
                    attr = _safe_attr_name(sf.name.replace("-", "_"))
                    lines.append(f"    {attr}: {nested_cls} = Field(default_factory={nested_cls})")
                    has_fields = True
                elif sf.is_list and sf.is_object and sf.api_path in sub_model_map:
                    # Array-of-objects with typed sub-model
                    nested_cls = sub_model_map[sf.api_path]
                    attr = _safe_attr_name(sf.name.replace("-", "_"))
                    lines.append(f"    {attr}: list[{nested_cls}] = Field(default_factory=list)")
                    has_fields = True
                elif sf.is_object and not sf.is_list:
                    continue
                else:
                    leaf = sf.api_path.rsplit(".", 1)[-1]
                    attr = _safe_attr_name(leaf.replace("-", "_"))
                    type_ann = _python_type_annotation(sf, sub_model_map)
                    default_repr = _python_default_repr(sf)
                    lines.append(f"    {attr}: {type_ann} = {default_repr}")
                    has_fields = True

            if not has_fields:
                lines.append("    pass")
            lines.append("")


def _needs_field_import(
    fields: list[ParsedField],
    sub_model_map: dict[str, str],
) -> bool:
    """Check if any field requires ``from pydantic import Field``."""
    for f in fields:
        if f.is_list:
            return True
        if f.is_object and not f.is_list and f.api_path in sub_model_map:
            return True
        if f.is_object and f.sub_fields and _needs_field_import(f.sub_fields, sub_model_map):
            return True
    return False


def _needs_any_import(fields: list[ParsedField], sub_model_map: dict[str, str]) -> bool:
    """Check if ``from typing import Any`` is needed."""
    for f in fields:
        if f.is_list and f.is_object and f.api_path not in sub_model_map:
            return True
        if f.sub_fields and _needs_any_import(f.sub_fields, sub_model_map):
            return True
    return False


def _needs_uuid_import(fields: list[ParsedField]) -> bool:
    """Check if any field uses ``OntapUUID``."""
    for f in fields:
        if f.is_uuid:
            return True
        if f.sub_fields and _needs_uuid_import(f.sub_fields):
            return True
    return False


def _collect_all_attrs(fields: list[ParsedField], sub_model_map: dict[str, str]) -> list[str]:
    """Collect all attribute names recursively for noqa detection."""
    attrs: list[str] = []
    for f in fields:
        if f.is_object and not f.is_list:
            attr = _safe_attr_name(f.name.replace("-", "_"))
            attrs.append(attr)
            attrs.extend(_collect_all_attrs(f.sub_fields, sub_model_map))
        else:
            attr = _field_to_cache_attr(f)
            # For top-level fields, the attr is just the field name
            leaf = f.api_path.rsplit(".", 1)[-1] if "." in f.api_path else f.api_path
            attrs.append(_safe_attr_name(leaf.replace("-", "_")))
    return attrs


def generate_model(
    endpoint: ParsedEndpoint,
    api_type: str = "ontap",
    *,
    shared_schemas: frozenset[str] | set[str] = frozenset(),
) -> str:
    """Generate a Pydantic model class for an endpoint.

    Produces nested ``OntapModel`` subclasses mirroring the API structure
    (ADR-0011).  Object fields become typed sub-model attributes with
    ``Field(default_factory=SubModelClass)`` for safe chained access.

    Args:
        endpoint: Parsed endpoint with fields (tree structure).
        api_type: API type for import path context.
        shared_schemas: Set of schema names referenced by >1 endpoint
            in the current spec.  Passed through to
            :func:`_path_to_class_name` so the class name is
            URL-path-derived for shared schemas (avoids registry
            collisions across endpoints that share a schema).

    Returns:
        Python source code for the model module.
    """
    class_name = _path_to_class_name(
        endpoint.path, endpoint.schema_name, api_type, shared_schemas=shared_schemas
    )
    doc = f"{class_name} information."

    # Build sub-model map by walking the field tree
    sub_model_map: dict[str, str] = {}  # api_path → sub-model class name
    sub_model_lines: list[str] = []
    _generate_nested_sub_models(
        class_name,
        endpoint.fields,
        sub_model_map,
        sub_model_lines,
    )

    needs_field = _needs_field_import(endpoint.fields, sub_model_map)
    needs_any = _needs_any_import(endpoint.fields, sub_model_map)
    needs_uuid = _needs_uuid_import(endpoint.fields)

    lines = [
        f'"""{doc}"""',
        "",
        "from __future__ import annotations",
        "",
    ]

    # Conditional imports
    if needs_any:
        lines.append("from typing import Any")
        lines.append("")

    pydantic_imports = ["Field"] if needs_field else []

    base_imports = ["OntapModel"]
    if needs_uuid:
        base_imports.append("OntapUUID")

    if pydantic_imports:
        lines.append(f"from pydantic import {', '.join(sorted(pydantic_imports))}")
        lines.append("")

    lines.append(f"from pynetappfoundry.models._base import {', '.join(sorted(base_imports))}")
    lines.append("")

    # Add sub-model class definitions (already generated deepest-first)
    lines.extend(sub_model_lines)

    # Generate the parent class
    lines.append("")
    lines.append(f"class {class_name}(OntapModel):")
    lines.append(f'    """{class_name} information."""')
    lines.append("")

    if not endpoint.fields:
        lines.append("    pass")
    else:
        parent_seen: set[str] = set()
        for field in endpoint.fields:
            attr = _safe_attr_name(field.name.replace("-", "_"))
            if attr in parent_seen:
                continue
            parent_seen.add(attr)

            if field.is_object and not field.is_list and field.api_path in sub_model_map:
                # Nested object → typed sub-model with default_factory
                nested_cls = sub_model_map[field.api_path]
                lines.append(f"    {attr}: {nested_cls} = Field(default_factory={nested_cls})")
            elif field.is_list and field.is_object and field.api_path in sub_model_map:
                # Array-of-objects with typed sub-model
                nested_cls = sub_model_map[field.api_path]
                lines.append(f"    {attr}: list[{nested_cls}] = Field(default_factory=list)")
            elif field.is_object and not field.is_list:
                # Object without sub-model (no sub_fields) — skip
                continue
            else:
                # Scalar or simple list
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
    all_attrs = _collect_all_attrs(endpoint.fields, sub_model_map)
    if any(c.isupper() for attr in all_attrs for c in attr):
        noqa_codes.append("N815")
    if noqa_codes:
        result = f"# ruff: noqa: {', '.join(noqa_codes)}\n" + result
    return result


def _load_toml_field_overrides(
    existing_toml_path: Path | None,
) -> dict[str, dict[str, Any]]:
    """Load per-field overrides from a sibling ``<name>.toml`` overlay.

    Used by :func:`generate_mapping` to mirror any ``cache_strategy`` or
    ``requires_explicit_fetch`` values that the user (or a prior
    hand-edit) has set in the TOML into the emitted Python source.  The
    runtime overlay loader (``cache/overlay_loader.py``) already treats
    the TOML as authoritative; mirroring into Python keeps the two in
    sync for readability and round-trip stability.

    A missing path or malformed TOML returns an empty mapping — callers
    fall back to dataclass defaults.  This mirrors the silent-fallback
    behavior of :func:`generate_toml_overlay`.

    Args:
        existing_toml_path: Path to the sibling TOML overlay, or
            ``None`` if no overlay exists on disk.

    Returns:
        ``{cache_attr: {config_key: value}}`` extracted from the
        ``[fields.*]`` tables.  Empty when no TOML, no ``fields`` table,
        or the TOML can't be parsed.
    """
    if existing_toml_path is None or not existing_toml_path.exists():
        return {}
    try:
        with open(existing_toml_path, "rb") as f:
            data = tomllib.load(f)
    except (tomllib.TOMLDecodeError, OSError):
        # Malformed TOML or filesystem error: fall back to defaults.
        return {}
    fields_table = data.get("fields")
    if not isinstance(fields_table, dict):
        return {}
    return {k: v for k, v in fields_table.items() if isinstance(v, dict)}


# ``parent_id_field`` defaults by API.  ONTAP identifies parents by
# ``uuid``; DII by ``id`` (integer primary key).  Future APIs extend
# this dispatch.
_PARENT_ID_FIELD_BY_API: dict[str, str] = {
    "ontap": "uuid",
    "aiqum": "uuid",
    "dii": "id",
    "occm": "id",
}


def generate_mapping(
    endpoint: ParsedEndpoint,
    api_type: str = "ontap",
    schema_lookup: dict[str, str] | None = None,
    existing_toml_path: Path | None = None,
    *,
    shared_schemas: frozenset[str] | set[str] = frozenset(),
    identifier_map: dict[str, str] | None = None,
) -> str:
    """Generate a TypeMapping/FieldMapping module for an endpoint.

    Produces a ``mapping.py`` file with the mapping constant and
    registry registration call.  ``cache_attr`` values use dot-path
    notation matching the ``api_path`` (e.g. ``"svm.name"``).

    Array-of-objects fields with typed sub-models get transform functions
    that construct sub-model instances using ``get_nested_value()``.

    When ``existing_toml_path`` points at a sibling ``<name>.toml``
    overlay, per-field ``cache_strategy`` and ``requires_explicit_fetch``
    values are mirrored from the overlay into the emitted Python
    ``FieldMapping(...)`` calls.  The TOML remains the authoritative
    runtime source; the Python-level mirror only exists so that the file
    is self-describing and so regeneration is a byte-identical round
    trip against the on-disk output.

    Args:
        endpoint: Parsed endpoint with fields (tree structure).
        api_type: API type tag.
        schema_lookup: Optional mapping of API path → schema name for
            resolving parent class names.
        existing_toml_path: Optional path to an existing sibling TOML
            overlay.  When present, per-field ``cache_strategy`` and
            ``requires_explicit_fetch`` values are mirrored into the
            emitted Python.  Missing or malformed overlays fall back
            silently to dataclass defaults.
        shared_schemas: Set of schema names referenced by >1 endpoint
            in the current spec.  Passed through to
            :func:`_path_to_class_name` so the class name is
            URL-path-derived for shared schemas (avoids registry
            collisions across endpoints that share a schema).
        identifier_map: Optional mapping of API path → identifier_field
            name (e.g. ``{"/network/fc/fabrics": "name"}``).  Used to
            look up the parent endpoint's actual identifier when emitting
            ``parent_id_field``.  Falls back to the API-default dispatch
            table when the parent path is absent from the map.

    Returns:
        Python source code for the mapping module.
    """
    class_name = _path_to_class_name(
        endpoint.path, endpoint.schema_name, api_type, shared_schemas=shared_schemas
    )
    module_parts = _path_to_module_parts(endpoint.path)
    mapping_name = f"{class_name.upper()}_MAPPING"

    # Collect all leaf fields from the tree
    leaves = _collect_all_leaves(endpoint.fields)

    # Load the sibling TOML overlay (if any) so we can mirror user-set
    # cache_strategy / requires_explicit_fetch into the emitted Python.
    toml_field_overrides = _load_toml_field_overrides(existing_toml_path)

    # Identify sub-model fields for array-of-objects transforms
    # Build the same sub_model_map as generate_model to get consistent names
    sub_model_map: dict[str, str] = {}
    _temp_lines: list[str] = []
    _generate_nested_sub_models(
        class_name,
        endpoint.fields,
        sub_model_map,
        _temp_lines,
    )

    # Only array-of-objects sub-models need transforms in the mapping
    array_sub_models: dict[str, str] = {}
    for field in leaves:
        if field.is_list and field.is_object and field.api_path in sub_model_map:
            array_sub_models[field.api_path] = sub_model_map[field.api_path]

    # Build the import path for the model (models live in models.ontap/)
    model_import = f"pynetappfoundry.models.{api_type}.{'.'.join(module_parts)}.model"

    # Build model imports (parent class + any array sub-model classes)
    model_classes = [class_name, *sorted(array_sub_models.values())]

    docstring = f'"""{class_name} type mapping."""'
    lines = [
        docstring,
        "",
        "from __future__ import annotations",
        "",
    ]

    if array_sub_models:
        lines.append("from typing import Any")
        lines.append("")

    lines.extend(
        [
            "from pynetappfoundry.cache._registry import model_registry",
            "from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping",
        ]
    )

    # Split long model import across multiple lines.  Emitted before the
    # ``utils.dict_path`` import so the resulting order matches ruff's
    # isort convention (alphabetical: ``cache.*``, ``models.*``,
    # ``utils.*``) — this keeps codegen output in sync with the on-disk
    # files and lets round-trip regeneration stay byte-identical.
    model_import_line = f"from {model_import} import {', '.join(model_classes)}"
    if len(model_import_line) > 100:
        lines.append(f"from {model_import} import (")
        for cls in model_classes:
            lines.append(f"    {cls},")
        lines.append(")")
    else:
        lines.append(model_import_line)

    # Add get_nested_value import if we have nested transforms
    has_nested_transforms = any("." in ap for ap in array_sub_models)
    if has_nested_transforms:
        lines.append("from pynetappfoundry.utils.dict_path import get_nested_value")

    # Generate transform functions for array sub-model fields
    if array_sub_models:
        for field in leaves:
            if field.api_path not in array_sub_models:
                continue
            sub_cls = array_sub_models[field.api_path]
            # Use the leaf field name for the transform function name
            func_name = f"_transform_{field.api_path.replace('.', '_')}"
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

            # Use get_nested_value for nested paths, record.get() for top-level
            if "." in field.api_path:
                lines.append("    try:")
                lines.append(f'        items = get_nested_value(record, "{field.api_path}")')
                lines.append("    except Exception:")
                lines.append("        items = []")
                ret_line = f"    return [{sub_cls}(**item) for item in items]"
            else:
                ret_line = (
                    f'    return [{sub_cls}(**item) for item in record.get("{field.api_path}", [])]'
                )
            if len(ret_line) > 100:
                lines.append("    return [")
                lines.append(f"        {sub_cls}(**item)")
                if "." in field.api_path:
                    lines.append("        for item in items")
                else:
                    lines.append(f'        for item in record.get("{field.api_path}", [])')
                lines.append("    ]")
            else:
                lines.append(ret_line)

    # Separate the TypeMapping from the preceding block.  PEP 8 calls for
    # two blank lines before a top-level class/function, but a single
    # blank line is conventional when the preceding block is only
    # imports.  We detect which by whether transform helpers were
    # emitted.
    lines.append("")
    if array_sub_models:
        lines.append("")
    lines.append(f"{mapping_name} = TypeMapping(")
    lines.append(f'    name="{class_name}",')
    lines.append(f"    model_class={class_name},")
    # ``?fields=*`` is an ONTAP REST convention (fetches every field by
    # default); DII, AIQUM, and OCCM do not honor it.  Emitting it for
    # non-ONTAP endpoints returns HTTP 400 or silently mangles the
    # response, so we gate on api_type.
    api_endpoint = f"{endpoint.path}?fields=*" if api_type == "ontap" else endpoint.path
    lines.append(f'    api_endpoint="{api_endpoint}",')

    lines.append(f'    api_type="{api_type}",')

    if endpoint.identifier_field is not None:
        lines.append(f'    identifier_field="{endpoint.identifier_field}",')

    if endpoint.records_path != "records":
        lines.append(f'    records_path="{endpoint.records_path}",')

    # Only emit ``parent_mapping`` when the parent path's module tree
    # actually generates a registered mapping whose class name matches
    # the computed parent_class — otherwise ``parent_mapping`` would
    # point to a name that no mapping in the registry claims (tracked
    # by ``tests/unit/cache/test_mapping_parent_validation.py``).
    # ONTAP parents resolve because every `/foo/{id}` item endpoint has
    # a sibling `/foo` collection that registers under the same class
    # name the parent_class algorithm derives.  DII often lacks the
    # collection (e.g. `/assets/disks/{id}/...` exists but
    # `/assets/disks` does not), so the parent link would dangle.
    parent_resolvable = False
    parent_class = ""
    if endpoint.has_parent and schema_lookup:
        parent_module_parts = tuple(_path_to_module_parts(endpoint.parent_path))
        parent_schema = schema_lookup.get(endpoint.parent_path, "")
        parent_class = _path_to_class_name(
            endpoint.parent_path,
            parent_schema,
            api_type,
            shared_schemas=shared_schemas,
        )
        for candidate_path, candidate_schema in schema_lookup.items():
            if tuple(_path_to_module_parts(candidate_path)) != parent_module_parts:
                continue
            candidate_class = _path_to_class_name(
                candidate_path,
                candidate_schema,
                api_type,
                shared_schemas=shared_schemas,
            )
            if candidate_class == parent_class:
                parent_resolvable = True
                break
    if parent_resolvable:
        lines.append(f'    parent_mapping="{parent_class}",')
        # Look up the parent endpoint's actual ``identifier_field`` from
        # the pre-built map.  This correctly handles parents that use
        # non-default identifiers (e.g. ``"name"`` instead of ``"uuid"``).
        # Fall back to the API-default dispatch table when the parent
        # path is absent from the map (legacy behavior).
        parent_id_field = (identifier_map or {}).get(
            endpoint.parent_path
        ) or _PARENT_ID_FIELD_BY_API.get(api_type, "uuid")
        lines.append(f'    parent_id_field="{parent_id_field}",')

    lines.append("    fields=(")

    seen_attrs: set[str] = set()
    for field in leaves:
        cache_attr = _field_to_cache_attr(field)
        if cache_attr in seen_attrs:
            continue
        seen_attrs.add(cache_attr)
        default_repr = _python_default_repr(field, for_mapping=True)

        # Mirror the sibling TOML's per-field config (if any).  TOML is
        # authoritative at runtime; this only keeps the emitted Python
        # in sync for readability and round-trip stability.
        toml_field_cfg = toml_field_overrides.get(cache_attr, {})
        toml_cache_strategy = toml_field_cfg.get("cache_strategy")
        toml_requires_explicit_fetch = bool(toml_field_cfg.get("requires_explicit_fetch", False))
        # Emit ``requires_explicit_fetch`` when the parser flagged it OR
        # when the sibling TOML declares it.  This keeps the Python and
        # TOML in sync on regen even if the TOML has hand-edited the
        # flag for a field the parser didn't detect as expensive.
        emit_explicit_fetch = field.requires_explicit_fetch or toml_requires_explicit_fetch

        field_args = [f'        cache_attr="{cache_attr}"']

        # Ordering matches the on-disk ONTAP mappings:
        # cache_attr, api_path, transform, cache_strategy, default,
        # requires_explicit_fetch.  When api_path equals cache_attr it's
        # omitted (FieldMapping.__post_init__ fills it in).
        if field.api_path in array_sub_models:
            func_name = f"_transform_{field.api_path.replace('.', '_')}"
            if field.api_path != cache_attr:
                field_args.append(f'        api_path="{field.api_path}"')
            field_args.append(f"        transform={func_name}")
        elif field.api_path != cache_attr:
            field_args.append(f'        api_path="{field.api_path}"')

        if isinstance(toml_cache_strategy, str) and toml_cache_strategy != "cache":
            field_args.append(f'        cache_strategy="{toml_cache_strategy}"')

        if field.default != "" or field.is_list:
            field_args.append(f"        default={default_repr}")

        if emit_explicit_fetch:
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

    # Emit a file-level noqa header for rules likely to remain after
    # ``ruff format`` wraps what it can.  ``E501`` covers pre-format
    # lines >100 chars (post-format ``ruff check --fix`` strips the
    # directive when redundant).  ``N802`` is needed when any generated
    # ``_transform_*`` helper has a mixedCase suffix derived from a
    # camelCase API field (DII's ``applicationRoles`` ->
    # ``_transform_applicationRoles``).  ONTAP's snake_case API fields
    # never trigger N802, so ONTAP output is unchanged.
    noqa_codes: list[str] = []
    if any(len(line) > 100 for line in lines):
        noqa_codes.append("E501")
    if any(any(c.isupper() for c in ap.replace(".", "_")) for ap in array_sub_models):
        noqa_codes.append("N802")
    if noqa_codes:
        result = f"# ruff: noqa: {', '.join(noqa_codes)}\n" + result
    return result


def generate_init(
    endpoint: ParsedEndpoint,
    api_type: str = "ontap",
    *,
    shared_schemas: frozenset[str] | set[str] = frozenset(),
) -> str:
    """Generate an ``__init__.py`` for an endpoint's package.

    Args:
        endpoint: Parsed endpoint.
        api_type: API type prefix for class naming.
        shared_schemas: Set of schema names referenced by >1 endpoint.
            Passed through to :func:`_path_to_class_name` for
            consistent class naming across generated files.

    Returns:
        Python source code for ``__init__.py``.
    """
    class_name = _path_to_class_name(
        endpoint.path, endpoint.schema_name, api_type, shared_schemas=shared_schemas
    )
    module_parts = _path_to_module_parts(endpoint.path)

    docstring = f'"""{class_name} model."""'
    module_path = f"pynetappfoundry.models.{api_type}.{'.'.join(module_parts)}.model"
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
    *,
    shared_schemas: frozenset[str] | set[str] = frozenset(),
) -> str:
    """Generate or update a TOML overlay for an endpoint.

    If ``existing_path`` points to an existing TOML file, user edits
    are preserved — new fields get defaults, removed fields get a
    warning comment.  Field keys use dot-path notation (e.g.
    ``"svm.name"``) matching the nested model structure.

    Args:
        endpoint: Parsed endpoint with fields (tree structure).
        existing_path: Path to existing overlay file, or None.
        api_type: API type prefix for class naming.
        shared_schemas: Set of schema names referenced by >1 endpoint.
            Passed through to :func:`_path_to_class_name` for
            consistent class naming across generated files.

    Returns:
        TOML content as a string.
    """
    class_name = _path_to_class_name(
        endpoint.path, endpoint.schema_name, api_type, shared_schemas=shared_schemas
    )
    leaves = _collect_all_leaves(endpoint.fields)

    # Load existing overlay if present
    existing: dict[str, Any] = {}
    if existing_path and existing_path.exists():
        with open(existing_path, "rb") as f:
            existing = tomllib.load(f)

    existing_fields = existing.get("fields", {})

    # Build a migration map from old flat keys to new dot-path keys
    # so we can preserve user edits from the old format
    flat_to_dot: dict[str, str] = {}
    for field in leaves:
        dot_key = _field_to_cache_attr(field)
        flat_key = field.api_path.replace(".", "_").replace("-", "_")
        if flat_key != dot_key:
            flat_to_dot[flat_key] = dot_key

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
        # Use dot-path as the TOML key
        dot_key = _field_to_cache_attr(field)
        # Also check the old flat key for migration
        flat_key = field.api_path.replace(".", "_").replace("-", "_")

        if dot_key in existing_fields:
            # Preserve user edits (already using new format)
            overlay["fields"][dot_key] = existing_fields[dot_key]
        elif flat_key in existing_fields:
            # Migrate from old flat key format
            overlay["fields"][dot_key] = existing_fields[flat_key]
        else:
            entry: dict[str, Any] = {"cache_strategy": "cache"}
            if field.requires_explicit_fetch:
                entry["requires_explicit_fetch"] = True
            overlay["fields"][dot_key] = entry

    # Warn about removed fields (check both dot and flat keys)
    current_keys = set()
    for field in leaves:
        current_keys.add(_field_to_cache_attr(field))
        current_keys.add(field.api_path.replace(".", "_").replace("-", "_"))
    removed = set(existing_fields) - current_keys
    if removed:
        overlay["_removed_fields"] = sorted(removed)

    return tomli_w.dumps(overlay)


def write_endpoint_files(
    endpoint: ParsedEndpoint,
    output_dir: Path,
    api_type: str = "ontap",
    overlay_dir: Path | None = None,
    schema_lookup: dict[str, str] | None = None,
    models_dir: Path | None = None,
    *,
    shared_schemas: frozenset[str] | set[str] = frozenset(),
    identifier_map: dict[str, str] | None = None,
) -> list[Path]:
    """Write all generated files for an endpoint.

    Creates the directory tree following ADR-0007's URL-tree convention.
    Model files (``model.py``, ``__init__.py``) are written under
    ``models_dir`` (defaults to ``output_dir/../models/``).  Mapping and
    TOML overlay files are written under ``output_dir`` (``cache/``).

    Args:
        endpoint: Parsed endpoint with fields.
        output_dir: Root output directory for cache files
            (e.g. ``src/pynetappfoundry/cache/``).
        api_type: API type tag.
        overlay_dir: Directory for TOML overlay files.  If None, overlays
            are written next to the mapping files.
        schema_lookup: Mapping of API path -> schema name for resolving
            parent class names in mappings.
        models_dir: Root output directory for model files
            (e.g. ``src/pynetappfoundry/models/``).  Defaults to
            ``output_dir/../models/``.
        shared_schemas: Set of schema names referenced by >1 endpoint
            in the current spec.  Threaded through the model, mapping,
            init, and TOML generators so class names stay consistent.
        identifier_map: Optional mapping of API path → identifier_field
            name.  Threaded through to :func:`generate_mapping` for
            resolving the parent's ``parent_id_field``.

    Returns:
        List of paths to all files written.
    """
    module_parts = _path_to_module_parts(endpoint.path)

    # Model files go into models/<api_type>/...
    if models_dir is None:
        models_dir = output_dir.parent / "models"
    model_pkg_dir = models_dir / api_type
    for part in module_parts:
        model_pkg_dir = model_pkg_dir / part
    model_pkg_dir.mkdir(parents=True, exist_ok=True)

    # Cache files (mapping, TOML) go into cache/<api_type>/...
    cache_pkg_dir = output_dir / api_type
    for part in module_parts:
        cache_pkg_dir = cache_pkg_dir / part
    cache_pkg_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []

    # Ensure intermediate __init__.py files exist in both trees
    _ensure_init_files(models_dir / api_type, module_parts, pkg_type="models")
    _ensure_init_files(output_dir / api_type, module_parts, pkg_type="cache")

    # Resolve the sibling TOML path up-front so ``generate_mapping``
    # can read any existing overlay before it's regenerated.  The TOML
    # is authoritative for ``cache_strategy`` / ``requires_explicit_fetch``
    # at runtime; mirroring it into the emitted Python keeps the file
    # self-describing and regeneration byte-identical (round-trip
    # invariant — see ADR-0008).
    toml_dir = overlay_dir or cache_pkg_dir
    toml_dir.mkdir(parents=True, exist_ok=True)
    toml_path = toml_dir / f"{module_parts[-1]}.toml"
    existing_toml = toml_path if toml_path.exists() else None

    # model.py (in models/)
    model_path = model_pkg_dir / "model.py"
    model_path.write_text(generate_model(endpoint, api_type, shared_schemas=shared_schemas))
    written.append(model_path)

    # __init__.py for the leaf model package (in models/)
    init_path = model_pkg_dir / "__init__.py"
    init_path.write_text(generate_init(endpoint, api_type, shared_schemas=shared_schemas))
    written.append(init_path)

    # mapping.py (in cache/) — reads the current on-disk TOML if any
    mapping_path = cache_pkg_dir / "mapping.py"
    mapping_path.write_text(
        generate_mapping(
            endpoint,
            api_type,
            schema_lookup,
            existing_toml_path=existing_toml,
            shared_schemas=shared_schemas,
            identifier_map=identifier_map,
        )
    )
    written.append(mapping_path)

    # TOML overlay (in cache/ or overlay_dir) — regenerated after mapping
    toml_path.write_text(
        generate_toml_overlay(endpoint, existing_toml, api_type, shared_schemas=shared_schemas)
    )
    written.append(toml_path)

    return written


def _ensure_init_files(base_dir: Path, parts: list[str], pkg_type: str = "cache") -> None:
    """Ensure ``__init__.py`` exists at every intermediate directory.

    Also seeds ``base_dir/__init__.py`` (the api-type package root) and,
    for the cache side, the leaf package directory.  The model side's
    leaf is overwritten immediately after by :func:`generate_init`; for
    cache leaves we need a placeholder so ``pkgutil.walk_packages`` can
    discover ``mapping.py`` modules on a freshly generated tree.

    Args:
        base_dir: Root directory.
        parts: Module path segments.
        pkg_type: Type label for the docstring (``"cache"`` or ``"models"``).
    """
    base_dir.mkdir(parents=True, exist_ok=True)
    base_init = base_dir / "__init__.py"
    if not base_init.exists():
        base_name = base_dir.name.replace("_", " ").title()
        base_init.write_text(f'"""{base_name} {pkg_type} models."""\n')

    current = base_dir
    for part in parts:
        current = current / part
        current.mkdir(parents=True, exist_ok=True)
        init_file = current / "__init__.py"
        if not init_file.exists():
            pkg_name = part.replace("_", " ").title()
            init_file.write_text(f'"""{pkg_name} {pkg_type} models."""\n')
