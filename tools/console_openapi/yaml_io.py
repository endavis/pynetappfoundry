"""YAML load and dump for spec-sized documents (#1148).

The Console spec is 6 MB. The pure-Python SafeLoader parses it in about 6 s; CSafeLoader (libyaml)
takes about 1.2 s and is equally safe, so ``load_yaml`` uses it when PyYAML has it and falls back
to SafeLoader otherwise.

``dump_yaml`` deliberately stays on the pure-Python SafeDumper. CSafeDumper wraps long
double-quoted scalars with non-ASCII text differently, so a spec written with it could fail the
drift guards, which compare the committed file to ``yaml.safe_dump`` output.
"""

from __future__ import annotations

from typing import Any, TextIO

import yaml


def load_yaml(stream: str | TextIO) -> Any:  # noqa: ANN401  # YAML documents are untyped
    """Parse YAML text or an open text file with a safe loader (CSafeLoader when available)."""
    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
    return yaml.load(stream, Loader=loader)  # nosec B506  # both loaders are safe


def dump_yaml(data: Any) -> str:  # noqa: ANN401  # YAML documents are untyped
    """Serialize ``data`` with ``yaml.safe_dump(data, sort_keys=False)`` (see module docstring)."""
    result: str = yaml.safe_dump(data, sort_keys=False)
    return result
