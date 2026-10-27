"""Guard against CLI commands reading ONTAP through the netapp_ontap SDK.

CLI commands read ONTAP data through ``ClusterEntry.ontap``, ``QuerySet`` or
``DataSource`` (ADR-0012). The events commands were the last to import the SDK
directly (#741); this keeps the import from coming back.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import pynetappfoundry.cli.commands

COMMANDS_DIR = Path(pynetappfoundry.cli.commands.__file__).parent


def _netapp_ontap_imports(path: Path) -> list[str]:
    """Return 'file:line' for each import of netapp_ontap in *path*."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    hits: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            modules = [node.module]
        else:
            continue
        if any(m == "netapp_ontap" or m.startswith("netapp_ontap.") for m in modules):
            hits.append(f"{path.relative_to(COMMANDS_DIR)}:{node.lineno}")
    return hits


def test_commands_dir_has_python_files() -> None:
    """Test that the scan below has files to look at."""
    assert any(COMMANDS_DIR.rglob("*.py"))


def test_cli_commands_do_not_import_netapp_ontap() -> None:
    """Test that no CLI command imports the netapp_ontap SDK."""
    hits = [
        hit for path in sorted(COMMANDS_DIR.rglob("*.py")) for hit in _netapp_ontap_imports(path)
    ]

    assert hits == []


def test_detects_netapp_ontap_imports(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that the scan catches both import forms and ignores look-alikes."""
    monkeypatch.setattr(f"{__name__}.COMMANDS_DIR", tmp_path)
    sample = tmp_path / "sample.py"
    sample.write_text(
        "import netapp_ontap.error\n"
        "from netapp_ontap.resources import EmsEvent\n"
        "import netapp_ontap_extra\n"
        "from . import netapp_ontap\n"
        '"""netapp_ontap in a docstring"""\n',
        encoding="utf-8",
    )

    assert _netapp_ontap_imports(sample) == ["sample.py:1", "sample.py:2"]
