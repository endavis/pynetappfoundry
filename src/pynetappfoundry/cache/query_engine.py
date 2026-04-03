"""SQL query engine with json_extract() support for cache DB.

Parses human-readable filter expressions into parameterized SQL
conditions, supporting both scalar columns and nested JSON fields
via SQLite ``json_extract()``.

Filter expression format::

    name = 'vol1'
    autosize.mode != 'grow_shrink'
    size > 1073741824
    autosize.grow_threshold >= 85
    state in ('online', 'mixed')
    state not in ('offline')
    comment = null
    access_time_enabled = true
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, get_args, get_origin

from pydantic import BaseModel

from pynetappfoundry.cache.db_schema import _is_json_column, _unwrap_annotation

# Supported comparison operators
_OPERATORS = frozenset({"=", "!=", "<", ">", "<=", ">=", "in", "not in"})

# Regex for valid JSON sub-paths (prevents injection)
_JSON_PATH_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_.]*$")

# Main filter expression pattern.
# Captures: field_path, operator, value
# Examples:
#   name = 'vol1'
#   autosize.mode != 'grow_shrink'
#   state in ('online', 'mixed')
#   state not in ('offline')
_FILTER_RE = re.compile(
    r"^\s*"
    r"(?P<field>[a-zA-Z_][a-zA-Z0-9_.]*)"  # field path
    r"\s+"
    r"(?P<op>not\s+in|in|!=|<=|>=|<|>|=)"  # operator
    r"\s+"
    r"(?P<value>.+?)"  # value (rest of line)
    r"\s*$",
)

# Pattern for tuple values: ('a', 'b', 'c')
_TUPLE_RE = re.compile(r"^\((.+)\)$")


@dataclass(frozen=True)
class ParsedFilter:
    """A parsed filter expression.

    Attributes:
        field_path: Dot-separated field path (e.g. ``"autosize.mode"``).
        operator: Comparison operator (e.g. ``"="``, ``"!="``, ``"in"``).
        value: The parsed value (string, int, float, bool, None, or list).
    """

    field_path: str
    operator: str
    value: Any


@dataclass(frozen=True)
class SQLCondition:
    """A parameterized SQL condition.

    Attributes:
        clause: SQL WHERE clause fragment (e.g. ``'"name" = ?'``).
        params: Parameter values for the clause.
    """

    clause: str
    params: tuple[Any, ...]


def _parse_value(raw: str) -> Any:
    """Parse a raw value string into a Python object.

    - Quoted strings → strip quotes
    - ``null`` / ``none`` → None
    - ``true`` / ``false`` → bool
    - Numeric → int or float
    - Tuple → list of parsed values

    Args:
        raw: Raw value string from filter expression.

    Returns:
        Parsed Python value.
    """
    stripped = raw.strip()

    # Tuple: ('a', 'b')
    tuple_match = _TUPLE_RE.match(stripped)
    if tuple_match:
        inner = tuple_match.group(1)
        # Split on commas, respecting quoted strings
        items: list[Any] = []
        for item in _split_tuple_items(inner):
            items.append(_parse_value(item.strip()))
        return items

    # Quoted string
    if (stripped.startswith("'") and stripped.endswith("'")) or (
        stripped.startswith('"') and stripped.endswith('"')
    ):
        return stripped[1:-1]

    # Null
    lower = stripped.lower()
    if lower in ("null", "none"):
        return None

    # Boolean
    if lower == "true":
        return True
    if lower == "false":
        return False

    # Integer
    try:
        return int(stripped)
    except ValueError:
        pass

    # Float
    try:
        return float(stripped)
    except ValueError:
        pass

    raise ValueError(f"Cannot parse value: {raw!r}")


def _split_tuple_items(inner: str) -> list[str]:
    """Split comma-separated tuple items, respecting quoted strings.

    Args:
        inner: The content inside parentheses.

    Returns:
        List of individual item strings.
    """
    items: list[str] = []
    current: list[str] = []
    in_quote: str | None = None

    for char in inner:
        if in_quote:
            current.append(char)
            if char == in_quote:
                in_quote = None
        elif char in ("'", '"'):
            in_quote = char
            current.append(char)
        elif char == ",":
            items.append("".join(current))
            current = []
        else:
            current.append(char)

    if current:
        items.append("".join(current))

    return items


def parse_filter(expression: str) -> ParsedFilter:
    """Parse a human-readable filter expression.

    Args:
        expression: Filter string, e.g. ``"name = 'vol1'"``
            or ``"autosize.mode != 'grow_shrink'"``.

    Returns:
        ParsedFilter with field_path, operator, and parsed value.

    Raises:
        ValueError: If the expression cannot be parsed.
    """
    match = _FILTER_RE.match(expression)
    if not match:
        raise ValueError(
            f"Malformed filter expression: {expression!r}. "
            "Expected format: <field> <operator> <value>"
        )

    field_path = match.group("field")
    operator = re.sub(r"\s+", " ", match.group("op")).strip()
    raw_value = match.group("value")

    if operator not in _OPERATORS:
        raise ValueError(f"Unsupported operator: {operator!r}")

    value = _parse_value(raw_value)

    # Validate: in/not in requires a list
    if operator in ("in", "not in") and not isinstance(value, list):
        raise ValueError(
            f"Operator {operator!r} requires a tuple value, e.g. ('a', 'b'), got {raw_value!r}"
        )

    return ParsedFilter(field_path=field_path, operator=operator, value=value)


def parse_filters(expressions: list[str]) -> list[ParsedFilter]:
    """Parse multiple filter expressions.

    Args:
        expressions: List of filter strings.

    Returns:
        List of ParsedFilter instances.

    Raises:
        ValueError: If any expression cannot be parsed.
    """
    return [parse_filter(expr) for expr in expressions]


def resolve_field_path(
    field_path: str,
    model_class: type[BaseModel],
) -> str:
    """Resolve a dotted field path to a SQL column expression.

    For scalar fields like ``"name"``, returns ``'"name"'``.
    For JSON sub-fields like ``"autosize.mode"``, returns
    ``'json_extract("autosize", '$.mode')'``.

    Args:
        field_path: Dot-separated field path.
        model_class: The Pydantic model class to resolve against.

    Returns:
        SQL column expression string.

    Raises:
        ValueError: If the field path is invalid.
    """
    parts = field_path.split(".", 1)
    column = parts[0]

    # Validate column exists in model
    if column not in model_class.model_fields:
        raise ValueError(
            f"Unknown field {column!r} on {model_class.__name__}. "
            f"Available fields: {', '.join(sorted(model_class.model_fields))}"
        )

    field_info = model_class.model_fields[column]
    annotation = field_info.annotation
    is_json = _is_json_column(annotation)

    if len(parts) == 1:
        # No dot-path — must be a scalar column
        if is_json:
            raise ValueError(
                f"Cannot filter on bare JSON column {column!r}. "
                f"Use a sub-field path like '{column}.field_name'."
            )
        return f'"{column}"'

    # Has sub-path — must be a JSON column
    json_path = parts[1]

    if not is_json:
        raise ValueError(
            f"Cannot use dot-path on scalar field {column!r}. Use '{column}' without a sub-path."
        )

    # Check for list[BaseModel] or list[scalar] — not supported in phase 1
    core = _unwrap_annotation(annotation)
    origin = get_origin(core)
    if origin is list:
        args = get_args(core)
        if args and isinstance(args[0], type) and issubclass(args[0], BaseModel):
            raise ValueError(
                f"Cannot filter sub-fields of list[BaseModel] column {column!r}. "
                "Filtering into JSON arrays is not supported."
            )
        raise ValueError(
            f"Cannot filter sub-fields of list column {column!r}. "
            "Filtering into JSON arrays is not supported."
        )

    # Validate json_path
    if not _JSON_PATH_RE.match(json_path):
        raise ValueError(
            f"Invalid JSON sub-path: {json_path!r}. "
            "Only alphanumeric characters, underscores, and dots are allowed."
        )

    return f"""json_extract("{column}", '$.{json_path}')"""


def _is_bool_field(
    field_path: str,
    model_class: type[BaseModel],
) -> bool:
    """Check if a field path resolves to a boolean type.

    For scalar fields, checks the model annotation directly.
    For JSON sub-fields, we cannot introspect the nested model
    statically, so we return False (no coercion needed for JSON
    booleans — SQLite json_extract returns 1/0 natively).

    Args:
        field_path: Dot-separated field path.
        model_class: The Pydantic model class.

    Returns:
        True if the resolved field is a scalar bool column.
    """
    parts = field_path.split(".", 1)
    if len(parts) > 1:
        return False
    column = parts[0]
    if column not in model_class.model_fields:
        return False
    annotation = model_class.model_fields[column].annotation
    core = _unwrap_annotation(annotation)
    return core is bool


def build_sql_condition(
    parsed: ParsedFilter,
    model_class: type[BaseModel],
) -> SQLCondition:
    """Build a parameterized SQL condition from a parsed filter.

    Args:
        parsed: A ParsedFilter instance.
        model_class: The Pydantic model class for field resolution.

    Returns:
        SQLCondition with clause and params.

    Raises:
        ValueError: If the field path is invalid.
    """
    col_expr = resolve_field_path(parsed.field_path, model_class)

    # Handle null
    if parsed.value is None:
        if parsed.operator == "=":
            return SQLCondition(clause=f"{col_expr} IS NULL", params=())
        if parsed.operator == "!=":
            return SQLCondition(clause=f"{col_expr} IS NOT NULL", params=())
        raise ValueError(
            f"Operator {parsed.operator!r} is not valid with null. Use '=' or '!=' for null checks."
        )

    # Handle in / not in
    if parsed.operator in ("in", "not in"):
        values = parsed.value
        placeholders = ", ".join("?" for _ in values)
        keyword = "IN" if parsed.operator == "in" else "NOT IN"
        # Coerce booleans in list if targeting a bool field
        is_bool = _is_bool_field(parsed.field_path, model_class)
        coerced = [
            int(v) if isinstance(v, bool) or (is_bool and isinstance(v, bool)) else v
            for v in values
        ]
        return SQLCondition(
            clause=f"{col_expr} {keyword} ({placeholders})",
            params=tuple(coerced),
        )

    # Handle boolean coercion for scalar bool columns
    value = parsed.value
    if isinstance(value, bool) and _is_bool_field(parsed.field_path, model_class):
        value = int(value)

    op_map = {
        "=": "=",
        "!=": "!=",
        "<": "<",
        ">": ">",
        "<=": "<=",
        ">=": ">=",
    }
    sql_op = op_map[parsed.operator]

    return SQLCondition(
        clause=f"{col_expr} {sql_op} ?",
        params=(value,),
    )


def build_where_clause(
    filters: list[ParsedFilter],
    model_class: type[BaseModel],
    *,
    cluster_name: str | None = None,
) -> tuple[str, list[Any]]:
    """Build a complete WHERE clause from multiple parsed filters.

    Args:
        filters: List of ParsedFilter instances.
        model_class: The Pydantic model class for field resolution.
        cluster_name: If provided, prepend a ``cluster_name = ?`` condition.

    Returns:
        Tuple of (where_clause_string, params_list).
        The where_clause_string includes the ``WHERE`` keyword.
        If no conditions, returns ``("", [])``.

    Raises:
        ValueError: If any field path is invalid.
    """
    conditions: list[str] = []
    params: list[Any] = []

    if cluster_name is not None:
        conditions.append('"cluster_name" = ?')
        params.append(cluster_name)

    for parsed in filters:
        cond = build_sql_condition(parsed, model_class)
        conditions.append(cond.clause)
        params.extend(cond.params)

    if not conditions:
        return ("", [])

    return ("WHERE " + " AND ".join(conditions), params)
