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

import re
from typing import Any

# Pattern to match array index access like "nodes[0]"
_ARRAY_INDEX_PATTERN = re.compile(r"^([a-zA-Z_][a-zA-Z0-9_]*)\[(\d+)\]$")


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


def get_nested_value(data: dict[str, Any], path: str) -> Any:
    """Retrieve a value from a nested dictionary using dot notation.

    Supports accessing nested dictionaries and lists. Array indices can be
    specified using bracket notation (e.g., "nodes[0].name").

    Args:
        data: The dictionary to traverse.
        path: Dot-notation path (e.g., "cloud.instance_type", "nodes[0].name").

    Returns:
        The value at the specified path.

    Raises:
        PathNotFoundError: If the path cannot be resolved.

    Examples:
        >>> data = {"cloud": {"provider": "AWS", "region": "us-east-1"}}
        >>> get_nested_value(data, "cloud.provider")
        'AWS'

        >>> data = {"nodes": [{"name": "node-01"}, {"name": "node-02"}]}
        >>> get_nested_value(data, "nodes[0].name")
        'node-01'
    """
    if not path:
        raise PathNotFoundError(path, "", "empty path")

    parts = path.split(".")
    current: Any = data
    traversed: list[str] = []

    for part in parts:
        if not part:
            raise PathNotFoundError(path, ".".join(traversed) or "(root)", "empty path segment")

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
