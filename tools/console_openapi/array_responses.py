"""Load the committed list of ``cvo`` operations whose response is an array (#1021).

The docs type every response body as one object, so the builder cannot tell a
list from an object.  ``array_responses.toml`` names the operations whose success
body is a JSON array, with the evidence for each entry.  See that file's header.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

from tools.console_openapi.openapi.builder import _SERVICE_BASE_PATHS, BuildError

ARRAY_RESPONSES_PATH = Path(__file__).resolve().parent / "array_responses.toml"
_EVIDENCE = frozenset({"live", "swagger"})
_KEY = re.compile(r"^(GET|POST|PUT|PATCH|DELETE) (/\S*)$")


def load_array_responses(path: Path = ARRAY_RESPONSES_PATH) -> dict[str, dict[str, str]]:
    """Return ``{service: {"METHOD /path": evidence}}``, validating every entry."""
    with path.open("rb") as f:
        data = tomllib.load(f)
    for service, entries in data.items():
        if service not in _SERVICE_BASE_PATHS or not isinstance(entries, dict):
            raise BuildError(f"{path.name}: unknown service table {service!r}")
        base = _SERVICE_BASE_PATHS[service]
        for key, evidence in entries.items():
            match = _KEY.match(key)
            if match is None:
                raise BuildError(f"{path.name}: [{service}] malformed key {key!r}")
            if not match.group(2).startswith(f"{base}/"):
                raise BuildError(f"{path.name}: [{service}] path of {key!r} is outside {base!r}")
            if evidence not in _EVIDENCE:
                raise BuildError(
                    f"{path.name}: [{service}] {key!r} has evidence {evidence!r}; "
                    f"expected one of {sorted(_EVIDENCE)}"
                )
    return {service: dict(entries) for service, entries in data.items()}


def array_operations(
    data: dict[str, dict[str, str]], services: tuple[str, ...]
) -> frozenset[tuple[str, str]]:
    """Return the ``(METHOD, path)`` pairs of the included services."""
    pairs: set[tuple[str, str]] = set()
    for service in services:
        for key in data.get(service, {}):
            method, _, path = key.partition(" ")
            pairs.add((method, path))
    return frozenset(pairs)
