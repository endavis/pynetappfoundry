"""Path-placeholder helpers shared by the DII and AIQUM backends.

A mapping's ``api_endpoint`` may carry ``{name}`` path placeholders.  These
helpers find them and validate and percent-encode caller-supplied
``path_params`` values (#990, #1054).  Pure functions, no I/O.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

if TYPE_CHECKING:
    from pynetappfoundry.cache.field_mapping import TypeMapping


def placeholders(mapping: TypeMapping) -> list[str]:
    """Return the ``{name}`` path placeholders of ``mapping.api_endpoint``, in order."""
    return re.findall(r"\{([^}]+)\}", mapping.api_endpoint.split("?", 1)[0])


def caller_path_params(
    mapping: TypeMapping, placeholders: list[str], path_params: dict[str, Any]
) -> dict[str, str]:
    """Validate and percent-encode caller-supplied *path_params* (#990).

    Raises :class:`ValueError` for an unknown key, a missing placeholder, or a
    value that is empty, ``.`` or ``..``.  Every value is ``str()``-ed and
    quoted with no safe characters, so the requested path never gains a ``{``,
    ``}``, ``/``, ``?`` or ``#`` from a value.
    """
    valid = ", ".join("{" + p + "}" for p in placeholders) or "(none)"
    unknown = [key for key in path_params if key not in placeholders]
    if unknown:
        msg = (
            f"{mapping.name}: unknown path_params key(s) {', '.join(repr(k) for k in unknown)}; "
            f"valid placeholder(s) for {mapping.api_endpoint}: {valid}"
        )
        raise ValueError(msg)
    missing = [p for p in placeholders if p not in path_params]
    if missing:
        names = ", ".join("{" + p + "}" for p in missing)
        msg = (
            f"{mapping.name}: path_params is missing value(s) for {names} in {mapping.api_endpoint}"
        )
        raise ValueError(msg)
    encoded: dict[str, str] = {}
    for key, value in path_params.items():
        text = str(value)
        if text in ("", ".", ".."):
            msg = f"{mapping.name}: path_params value for {{{key}}} must not be {text!r}"
            raise ValueError(msg)
        encoded[key] = quote(text, safe="")
    return encoded
