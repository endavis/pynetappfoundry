"""Utility for accessing nested dictionary values via dot notation paths.

This module provides functions for traversing nested dictionaries and lists
using dot notation paths like "cloud.instance_type" or "nodes[0].name".

Example:
    >>> data = {"cloud": {"instance_type": "m5.xlarge"}, "nodes": [{"name": "node-01"}]}
    >>> get_nested_value(data, "cloud.instance_type")
    'm5.xlarge'
    >>> get_nested_value(data, "nodes[0].name")
    'node-01'
"""

from __future__ import annotations

import fnmatch
import re
from collections.abc import Sequence
from typing import Any

# Pattern to match array index access like "nodes[0]"
_ARRAY_INDEX_PATTERN = re.compile(r"^([a-zA-Z_][a-zA-Z0-9_]*)\[(\d+)\]$")

# Pattern to match wildcard array access like "nodes[*]"
_ARRAY_WILDCARD_PATTERN = re.compile(r"^([a-zA-Z_][a-zA-Z0-9_]*)\[\*\]$")

# Pattern to match filter predicate access like nodes["name=vol1"] or nodes['name=vol1']
_ARRAY_FILTER_PATTERN = re.compile(r"""^([a-zA-Z_][a-zA-Z0-9_]*)\[["'](.+?)["']\]$""")

# Default identifier key order tried by get_nested_value_with_identifiers() to
# label each item in a wildcard or filter predicate result. The first key
# present with a non-empty, non-None value wins; items matching none of
# these fall back to their array index.
DEFAULT_IDENTIFIER_KEYS: tuple[str, ...] = ("name", "svm.name", "uuid")


class PathNotFoundError(Exception):
    """Raised when a path cannot be resolved in a nested structure.

    Attributes:
        path: The full path that was being resolved.
        position: The part of the path where the error occurred.
        reason: Why the path resolution failed.
    """

    def __init__(self, path: str, position: str, reason: str) -> None:
        """Initialize PathNotFoundError.

        Args:
            path: The full path that was being resolved.
            position: The part of the path where the error occurred.
            reason: Why the path resolution failed.
        """
        self.path = path
        self.position = position
        self.reason = reason
        super().__init__(f"Path '{path}' not found at '{position}': {reason}")


def _parse_filter_predicate(predicate: str) -> list[tuple[str, str]]:
    """Parse a filter predicate string into field-value pairs.

    Supports OR conditions separated by ``||``.

    Args:
        predicate: Filter string like ``"name=vol1"`` or ``"name=A || name=B"``.

    Returns:
        List of ``(field, value)`` tuples (values are lowercased for comparison).

    Raises:
        ValueError: If any clause is malformed (missing ``=`` or empty field name).
    """
    clauses = predicate.split("||")
    conditions: list[tuple[str, str]] = []
    for clause in clauses:
        clause = clause.strip()
        if "=" not in clause:
            raise ValueError(f"Invalid filter clause (missing '='): {clause!r}")
        field, value = clause.split("=", 1)
        field = field.strip()
        value = value.strip()
        if not field:
            raise ValueError(f"Invalid filter clause (empty field name): {clause!r}")
        conditions.append((field, value.lower()))
    return conditions


def _split_path(path: str) -> list[str]:
    """Split a dot-notation path into segments, ignoring dots inside ``[...]``.

    A plain ``path.split(".")`` would also split on a dot that appears
    inside a filter predicate's bracket (e.g. the dotted field in
    ``nodes["svm.name=svm1"]``). This splits only on dots at bracket
    depth 0, so an entire ``key["predicate"]`` segment -- predicate dots
    included -- stays together as one path segment.

    Args:
        path: Dot-notation path, possibly containing bracketed segments.

    Returns:
        List of path segments, in order.
    """
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for char in path:
        if char == "[":
            depth += 1
            current.append(char)
        elif char == "]":
            depth = max(0, depth - 1)
            current.append(char)
        elif char == "." and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(char)
    parts.append("".join(current))
    return parts


def _matches_filter(item: dict[str, Any], conditions: list[tuple[str, str]]) -> bool:
    """Check whether *item* matches any of the OR *conditions*.

    *field* is resolved as a dotted path inside *item* via
    :func:`_lookup_dotted` (e.g. ``"security.session_security"`` matches
    ``item["security"]["session_security"]``). A field without a dot behaves
    exactly as a plain key lookup, so top-level predicates are unaffected.
    Dotted resolution takes priority over any literal key containing a dot;
    a path that doesn't resolve (missing intermediate key, or an
    intermediate value that isn't a dict) counts as no match, never an
    error.

    Comparison is case-insensitive on the stringified value.  If *expected*
    contains ``*`` or ``?`` glob characters, matching is performed with
    :func:`fnmatch.fnmatchcase` (against the lowercased actual value);
    otherwise an exact ``==`` comparison is used.

    Args:
        item: Dictionary to test.
        conditions: List of ``(field, expected_value_lower)`` pairs (OR logic).

    Returns:
        True if *item* matches at least one condition.
    """
    for field, expected in conditions:
        actual = _lookup_dotted(item, field)
        if actual is not None:
            actual_lower = str(actual).lower()
            if "*" in expected or "?" in expected:
                if fnmatch.fnmatchcase(actual_lower, expected):
                    return True
            elif actual_lower == expected:
                return True
    return False


def get_nested_value(data: dict[str, Any], path: str) -> Any:
    """Retrieve a value from a nested dictionary using dot notation.

    Supports accessing nested dictionaries and lists. Array indices can be
    specified using bracket notation (e.g., "nodes[0].name"). Wildcard syntax
    [*] can be used to access all items in an array. Filter predicates can be
    used to select items matching field values (e.g., ``nodes["name=node-01"]``).
    The field on the left of ``=`` may itself be a dotted path resolved
    inside each item (e.g. ``volumes["svm.name=svm1"]`` matches items where
    ``item["svm"]["name"] == "svm1"``); a missing intermediate key counts as
    no match. Filter values may contain glob patterns (``*`` and ``?``) for
    pattern matching (e.g., ``volumes["name=*Store*"]``).

    Args:
        data: The dictionary to traverse.
        path: Dot-notation path (e.g., "cloud.instance_type", "nodes[0].name",
              "nodes[*].name" for wildcard access,
              ``nodes["name=node-01"].uptime`` for filter predicate access).

    Returns:
        The value at the specified path. For wildcard and filter predicate
        paths, returns a list of values from matching array items.

    Raises:
        PathNotFoundError: If the path cannot be resolved.

    Examples:
        >>> data = {"cloud": {"provider": "AWS", "region": "us-east-1"}}
        >>> get_nested_value(data, "cloud.provider")
        'AWS'

        >>> data = {"nodes": [{"name": "node-01"}, {"name": "node-02"}]}
        >>> get_nested_value(data, "nodes[0].name")
        'node-01'

        >>> data = {"nodes": [{"name": "node-01"}, {"name": "node-02"}]}
        >>> get_nested_value(data, "nodes[*].name")
        ['node-01', 'node-02']

        >>> data = {"vols": [{"name": "v1", "size": 100}, {"name": "v2", "size": 200}]}
        >>> get_nested_value(data, 'vols["name=v1"].size')
        [100]

        >>> get_nested_value(data, 'vols["name=v1 || name=v2"].size')
        [100, 200]

        >>> get_nested_value(data, 'vols["name=v*"].size')
        [100, 200]

        >>> data = {"vols": [{"svm": {"name": "svm1"}, "size": 100}]}
        >>> get_nested_value(data, 'vols["svm.name=svm1"].size')
        [100]
    """
    if not path:
        raise PathNotFoundError(path, "", "empty path")

    parts = _split_path(path)
    current: Any = data
    traversed: list[str] = []

    for i, part in enumerate(parts):
        if not part:
            raise PathNotFoundError(path, ".".join(traversed) or "(root)", "empty path segment")

        # Check for wildcard pattern like "nodes[*]"
        wildcard_match = _ARRAY_WILDCARD_PATTERN.match(part)
        if wildcard_match:
            key = wildcard_match.group(1)

            # First access the key
            if not isinstance(current, dict):
                raise PathNotFoundError(
                    path,
                    ".".join(traversed) or "(root)",
                    f"expected dict, got {type(current).__name__}",
                )
            if key not in current:
                raise PathNotFoundError(
                    path,
                    ".".join([*traversed, key]) if traversed else key,
                    "key not found",
                )

            array = current[key]
            if not isinstance(array, list):
                raise PathNotFoundError(
                    path,
                    ".".join([*traversed, key]) if traversed else key,
                    f"expected list for wildcard access, got {type(array).__name__}",
                )

            # Get remaining path after the wildcard
            remaining_parts = parts[i + 1 :]
            if remaining_parts:
                # Recursively resolve remaining path for each item
                remaining_path = ".".join(remaining_parts)
                results = []
                for idx, item in enumerate(array):
                    if not isinstance(item, dict):
                        raise PathNotFoundError(
                            path,
                            f"{'.'.join([*traversed, key])}[{idx}]"
                            if traversed
                            else f"{key}[{idx}]",
                            f"expected dict for nested access, got {type(item).__name__}",
                        )
                    # Recursively get value using a wrapper dict
                    results.append(get_nested_value({"_": item}, f"_.{remaining_path}"))
                return results
            else:
                # No remaining path, return all items
                return list(array)

        # Check for filter predicate pattern like nodes["name=vol1"]
        filter_match = _ARRAY_FILTER_PATTERN.match(part)
        if filter_match:
            key = filter_match.group(1)
            predicate = filter_match.group(2)

            # First access the key
            if not isinstance(current, dict):
                raise PathNotFoundError(
                    path,
                    ".".join(traversed) or "(root)",
                    f"expected dict, got {type(current).__name__}",
                )
            if key not in current:
                raise PathNotFoundError(
                    path,
                    ".".join([*traversed, key]) if traversed else key,
                    "key not found",
                )

            array = current[key]
            if not isinstance(array, list):
                raise PathNotFoundError(
                    path,
                    ".".join([*traversed, key]) if traversed else key,
                    f"expected list for filter access, got {type(array).__name__}",
                )

            conditions = _parse_filter_predicate(predicate)
            filtered = [
                item
                for item in array
                if isinstance(item, dict) and _matches_filter(item, conditions)
            ]

            # Get remaining path after the filter
            remaining_parts = parts[i + 1 :]
            if remaining_parts:
                remaining_path = ".".join(remaining_parts)
                results = []
                for item in filtered:
                    results.append(get_nested_value({"_": item}, f"_.{remaining_path}"))
                return results
            else:
                return filtered

        # Check for array index pattern like "nodes[0]"
        match = _ARRAY_INDEX_PATTERN.match(part)
        if match:
            key, index_str = match.groups()
            index = int(index_str)

            # First access the key
            if not isinstance(current, dict):
                raise PathNotFoundError(
                    path,
                    ".".join(traversed) or "(root)",
                    f"expected dict, got {type(current).__name__}",
                )
            if key not in current:
                raise PathNotFoundError(
                    path,
                    ".".join([*traversed, key]) if traversed else key,
                    "key not found",
                )

            current = current[key]
            traversed.append(key)

            # Then access the index
            if not isinstance(current, list):
                raise PathNotFoundError(
                    path,
                    ".".join(traversed),
                    f"expected list for index access, got {type(current).__name__}",
                )
            if index < 0 or index >= len(current):
                raise PathNotFoundError(
                    path,
                    f"{'.'.join(traversed)}[{index}]",
                    f"index {index} out of range (list has {len(current)} items)",
                )

            current = current[index]
            # Update traversed to include the index for future error messages
            traversed[-1] = f"{key}[{index}]"
        else:
            # Regular key access
            if not isinstance(current, dict):
                raise PathNotFoundError(
                    path,
                    ".".join(traversed) or "(root)",
                    f"expected dict, got {type(current).__name__}",
                )
            if part not in current:
                raise PathNotFoundError(
                    path,
                    ".".join([*traversed, part]) if traversed else part,
                    "key not found",
                )

            current = current[part]
            traversed.append(part)

    return current


def _has_wildcard_or_filter(parts: Sequence[str]) -> bool:
    """Return True if any path segment is a wildcard or filter predicate access."""
    return any(
        _ARRAY_WILDCARD_PATTERN.match(part) or _ARRAY_FILTER_PATTERN.match(part) for part in parts
    )


def _lookup_dotted(item: dict[str, Any], dotted_key: str) -> Any:
    """Look up a dot-notation key in *item*, returning None if any segment is absent.

    Unlike :func:`get_nested_value`, this never raises -- it is used to probe
    identifier candidates that are expected to be missing on some items.

    Args:
        item: Dictionary to look up the key in.
        dotted_key: Dot-notation key path (e.g. ``"svm.name"``).

    Returns:
        The value at the path, or None if any segment is missing or not a dict.
    """
    current: Any = item
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _resolve_identifier(item: Any, index: int, identifier_keys: Sequence[str]) -> str:
    """Resolve the identifier for a single array item.

    Tries each key in *identifier_keys* in order; the first one present with
    a non-empty, non-None value wins. Falls back to the array index
    (rendered as ``[i]``) when none match or *item* is not a dict.

    Args:
        item: The array item to identify.
        index: The item's position in the array (used for the fallback).
        identifier_keys: Dot-notation key paths tried, in order.

    Returns:
        The resolved identifier string.
    """
    if isinstance(item, dict):
        for key in identifier_keys:
            value = _lookup_dotted(item, key)
            if value is not None and value != "":
                return str(value)
    return f"[{index}]"


def get_nested_value_with_identifiers(
    data: dict[str, Any],
    path: str,
    identifier_keys: Sequence[str] = DEFAULT_IDENTIFIER_KEYS,
) -> list[tuple[str, Any]]:
    """Resolve a wildcard or filter predicate path, labelling each result.

    Mirrors :func:`get_nested_value` for the wildcard (``[*]``) and filter
    predicate (``["field=value"]``) array-access forms, but instead of
    returning a flat list of values, pairs each value with an identifier
    for the array item it came from.

    The identifier is resolved from *identifier_keys*, tried in order (the
    first key present with a non-empty, non-None value wins). Items
    matching none of the keys fall back to their array index, rendered as
    ``[i]``. Nested wildcards/filters compose identifiers with ``/``
    (e.g. ``svm1/vol1``). Duplicate identifiers are kept as separate
    entries -- never merged or overwritten.

    ``get_nested_value()`` is unchanged and is still the right call for
    paths without a wildcard or filter segment.

    Args:
        data: The dictionary to traverse.
        path: Dot-notation path containing at least one wildcard (``[*]``)
            or filter predicate (``["field=value"]``) segment.
        identifier_keys: Dot-notation key paths tried, in order, to label
            each array item. Defaults to :data:`DEFAULT_IDENTIFIER_KEYS`.

    Returns:
        A list of ``(identifier, value)`` tuples, in array order.

    Raises:
        PathNotFoundError: If the path cannot be resolved.
        ValueError: If *path* contains no wildcard or filter segment.

    Examples:
        >>> data = {"nodes": [{"name": "node-01"}, {"name": "node-02"}]}
        >>> get_nested_value_with_identifiers(data, "nodes[*].name")
        [('node-01', 'node-01'), ('node-02', 'node-02')]

        >>> data = {"nodes": [{"serial_number": "SN1"}, {"serial_number": "SN2"}]}
        >>> get_nested_value_with_identifiers(data, "nodes[*].serial_number")
        [('[0]', 'SN1'), ('[1]', 'SN2')]

        >>> data = {"svms": [{"name": "svm1", "vols": [{"name": "vol1", "size": 1}]}]}
        >>> get_nested_value_with_identifiers(data, "svms[*].vols[*].size")
        [('svm1/vol1', 1)]
    """
    if not path:
        raise PathNotFoundError(path, "", "empty path")

    parts = _split_path(path)
    current: Any = data
    traversed: list[str] = []

    for i, part in enumerate(parts):
        if not part:
            raise PathNotFoundError(path, ".".join(traversed) or "(root)", "empty path segment")

        wildcard_match = _ARRAY_WILDCARD_PATTERN.match(part)
        filter_match = None if wildcard_match else _ARRAY_FILTER_PATTERN.match(part)

        if wildcard_match or filter_match:
            match = wildcard_match or filter_match
            assert match is not None
            key = match.group(1)

            if not isinstance(current, dict):
                raise PathNotFoundError(
                    path,
                    ".".join(traversed) or "(root)",
                    f"expected dict, got {type(current).__name__}",
                )
            if key not in current:
                raise PathNotFoundError(
                    path,
                    ".".join([*traversed, key]) if traversed else key,
                    "key not found",
                )

            array = current[key]
            access_label = "wildcard" if wildcard_match else "filter"
            if not isinstance(array, list):
                raise PathNotFoundError(
                    path,
                    ".".join([*traversed, key]) if traversed else key,
                    f"expected list for {access_label} access, got {type(array).__name__}",
                )

            items: list[tuple[int, Any]]
            if wildcard_match:
                items = list(enumerate(array))
            else:
                assert filter_match is not None
                predicate = filter_match.group(2)
                conditions = _parse_filter_predicate(predicate)
                items = [
                    (idx, item)
                    for idx, item in enumerate(array)
                    if isinstance(item, dict) and _matches_filter(item, conditions)
                ]

            remaining_parts = parts[i + 1 :]
            results: list[tuple[str, Any]] = []

            if not remaining_parts:
                for idx, item in items:
                    ident = _resolve_identifier(item, idx, identifier_keys)
                    results.append((ident, item))
                return results

            remaining_path = ".".join(remaining_parts)
            nested_has_wildcard = _has_wildcard_or_filter(remaining_parts)

            for idx, item in items:
                ident = _resolve_identifier(item, idx, identifier_keys)
                if not isinstance(item, dict):
                    raise PathNotFoundError(
                        path,
                        f"{'.'.join([*traversed, key])}[{idx}]" if traversed else f"{key}[{idx}]",
                        f"expected dict for nested access, got {type(item).__name__}",
                    )
                if nested_has_wildcard:
                    nested = get_nested_value_with_identifiers(
                        {"_": item}, f"_.{remaining_path}", identifier_keys
                    )
                    for nested_ident, nested_value in nested:
                        results.append((f"{ident}/{nested_ident}", nested_value))
                else:
                    value = get_nested_value({"_": item}, f"_.{remaining_path}")
                    results.append((ident, value))

            return results

        # Check for array index pattern like "nodes[0]"
        index_match = _ARRAY_INDEX_PATTERN.match(part)
        if index_match:
            key, index_str = index_match.groups()
            index = int(index_str)

            if not isinstance(current, dict):
                raise PathNotFoundError(
                    path,
                    ".".join(traversed) or "(root)",
                    f"expected dict, got {type(current).__name__}",
                )
            if key not in current:
                raise PathNotFoundError(
                    path,
                    ".".join([*traversed, key]) if traversed else key,
                    "key not found",
                )

            current = current[key]
            traversed.append(key)

            if not isinstance(current, list):
                raise PathNotFoundError(
                    path,
                    ".".join(traversed),
                    f"expected list for index access, got {type(current).__name__}",
                )
            if index < 0 or index >= len(current):
                raise PathNotFoundError(
                    path,
                    f"{'.'.join(traversed)}[{index}]",
                    f"index {index} out of range (list has {len(current)} items)",
                )

            current = current[index]
            traversed[-1] = f"{key}[{index}]"
        else:
            # Regular key access
            if not isinstance(current, dict):
                raise PathNotFoundError(
                    path,
                    ".".join(traversed) or "(root)",
                    f"expected dict, got {type(current).__name__}",
                )
            if part not in current:
                raise PathNotFoundError(
                    path,
                    ".".join([*traversed, part]) if traversed else part,
                    "key not found",
                )

            current = current[part]
            traversed.append(part)

    raise ValueError(
        f"Path {path!r} has no wildcard [*] or filter predicate segment; "
        "use get_nested_value() instead."
    )
