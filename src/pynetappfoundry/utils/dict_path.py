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
from typing import Any

# Pattern to match array index access like "nodes[0]"
_ARRAY_INDEX_PATTERN = re.compile(r"^([a-zA-Z_][a-zA-Z0-9_]*)\[(\d+)\]$")

# Pattern to match wildcard array access like "nodes[*]"
_ARRAY_WILDCARD_PATTERN = re.compile(r"^([a-zA-Z_][a-zA-Z0-9_]*)\[\*\]$")

# Pattern to match filter predicate access like nodes["name=vol1"] or nodes['name=vol1']
_ARRAY_FILTER_PATTERN = re.compile(r"""^([a-zA-Z_][a-zA-Z0-9_]*)\[["'](.+?)["']\]$""")


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


def _matches_filter(item: dict[str, Any], conditions: list[tuple[str, str]]) -> bool:
    """Check whether *item* matches any of the OR *conditions*.

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
        actual = item.get(field)
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
    Filter values may contain glob patterns (``*`` and ``?``) for pattern
    matching (e.g., ``volumes["name=*Store*"]``).

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
    """
    if not path:
        raise PathNotFoundError(path, "", "empty path")

    parts = path.split(".")
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
