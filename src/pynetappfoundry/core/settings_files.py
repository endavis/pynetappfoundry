"""Locate and update root settings files (``<name>api.toml``, ``users.toml``, ...).

These helpers belong to the runtime layer so that both the CLI and the API clients
can use them. A client that rotates a token writes it back through
:func:`write_toml_values`; the CLI's ``set-credential --setting`` uses the same
functions to pick and update the target file.
"""

from __future__ import annotations

import contextlib
import os
import tempfile
import tomllib
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import tomlkit

from pynetappfoundry.core.config import SCOPE_MARKER, ConfigurationError

# Root API settings file stem -> its directory name under ``<config>/apis/``.
API_DIRS = {
    "ontapapi": "ontap",
    "aiqumapi": "aiqum",
    "diiapi": "dii",
    "consoleapi": "console",
    "digitaladvisorapi": "digitaladvisor",
}


def is_data_file(path: Path) -> bool:
    """Return True when a TOML file is a data file (``[settings] type = "data"``)."""
    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
    except Exception:  # unreadable TOML files are not data files
        return False
    settings = data.get("settings", {})
    return isinstance(settings, dict) and settings.get("type") == "data"


def find_setting_file(config_path: Path, stem: str, scope: str | None) -> Path:
    """Pick the settings file a ``--setting`` target is written to.

    The loader reads every non-data ``*.toml`` file by stem, so the writer uses the
    same rule. A root target skips scope directories; a scope target looks only
    under ``<config>/<scope>/``. With no match, the conventional path is returned
    (not created yet): ``<config>/apis/<name>/<stem>.toml`` for a root API settings
    file, otherwise ``<base>/<stem>.toml``.

    Raises:
        ConfigurationError: If more than one file carries the stem.
    """
    base = config_path if scope is None else config_path / scope
    scope_dirs = {
        d.name for d in config_path.iterdir() if d.is_dir() and (d / SCOPE_MARKER).is_file()
    }
    matches: list[Path] = []
    for toml_file in sorted(base.rglob("*.toml")) if base.is_dir() else []:
        if scope is None and toml_file.relative_to(config_path).parts[0] in scope_dirs:
            continue
        if toml_file.stem == stem and not is_data_file(toml_file):
            matches.append(toml_file)
    if len(matches) > 1:
        raise ConfigurationError(
            f"More than one file provides {stem}.toml settings: "
            f"{', '.join(str(m) for m in matches)}."
        )
    if matches:
        return matches[0]
    if scope is None and stem in API_DIRS:
        return config_path / "apis" / API_DIRS[stem] / f"{stem}.toml"
    return base / f"{stem}.toml"


def atomic_write_text(path: Path, text: str) -> None:
    """Write ``text`` to ``path`` atomically, keeping an existing file's mode.

    The text goes to a temporary file in the same directory, is flushed to disk
    and then moved over ``path`` with ``os.replace``, so a reader never sees a
    half-written file. The temporary file has a ``.tmp`` suffix, so a leftover
    never matches the loader's ``*.toml`` search. Missing parent directories are
    created.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = path.stat().st_mode & 0o777 if path.exists() else None
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        if mode is not None:
            tmp_path.chmod(mode)
        os.replace(tmp_path, path)
    except BaseException:
        with contextlib.suppress(OSError):
            tmp_path.unlink()
        raise


def write_toml_values(
    path: Path, tables: Sequence[str], values: Mapping[str, str]
) -> dict[str, Any]:
    """Set ``values`` in the table at ``tables`` of a TOML file, keeping its formatting.

    The file is parsed with tomlkit, so comments and unrelated keys survive. A
    missing file starts as an empty document; missing tables are created (the
    intermediate ones as super tables); missing parent directories are created.
    The write is atomic (see :func:`atomic_write_text`).

    Args:
        path: The TOML file.
        tables: Table path, outermost first.
        values: Keys and values to set in the leaf table.

    Returns:
        A plain copy of the leaf table after the update.
    """
    doc = tomlkit.parse(path.read_text(encoding="utf-8")) if path.exists() else tomlkit.document()
    node: Any = doc
    for index, name in enumerate(tables):
        if name not in node:
            is_last = index == len(tables) - 1
            node[name] = tomlkit.table(is_super_table=not is_last)
        node = node[name]
    for key, value in values.items():
        node[key] = value
    atomic_write_text(path, tomlkit.dumps(doc))
    leaf: dict[str, Any] = dict(node.unwrap())
    return leaf
