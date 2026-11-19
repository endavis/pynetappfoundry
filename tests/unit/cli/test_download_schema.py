"""Tests for ``nf config download-schema`` (#1051)."""

from __future__ import annotations

import ast
import importlib
import json
from pathlib import Path
from unittest.mock import patch

import pytest
import requests
from click.testing import CliRunner

from pynetappfoundry.cli.main import nf
from tests.unit.clients.digitaladvisor.helpers import response, session_with

FETCH_SESSION = "pynetappfoundry.clients.digitaladvisor.api.requests.Session"
SCHEMA = {"data": {"__schema": {"types": [{"name": "A"}, {"name": "B"}]}}}


@pytest.fixture
def config_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "cfg").mkdir()
    return tmp_path / "cfg"


def _invoke(*extra: str) -> tuple[int, str]:
    result = CliRunner().invoke(nf, ["--config-dir", "cfg", "config", "download-schema", *extra])
    return result.exit_code, result.output


def _target(config_dir: Path) -> Path:
    return config_dir / "apis" / "digitaladvisor" / "schema.json"


def test_writes_schema_and_creates_directory(config_dir: Path) -> None:
    session = session_with(response(200, SCHEMA))
    with patch(FETCH_SESSION, return_value=session):
        code, output = _invoke()

    assert code == 0
    assert json.loads(_target(config_dir).read_text()) == SCHEMA
    assert "2 types" in output
    call = session.post.call_args
    assert "headers" not in call.kwargs
    assert call.args[0] == "https://gql.aiq.netapp.com/graphql"


def test_overwrites_existing_file(config_dir: Path) -> None:
    _target(config_dir).parent.mkdir(parents=True)
    _target(config_dir).write_text("old")
    with patch(FETCH_SESSION, return_value=session_with(response(200, SCHEMA))):
        code, _ = _invoke("--api", "digitaladvisor")
    assert code == 0
    assert json.loads(_target(config_dir).read_text()) == SCHEMA


def test_uses_graphql_url_from_settings_without_credentials(config_dir: Path) -> None:
    path = config_dir / "apis" / "digitaladvisor" / "digitaladvisorapi.toml"
    path.parent.mkdir(parents=True)
    path.write_text('[general]\ngraphql_url = "https://gql.example.test/graphql"\ntimeout = 9\n')
    session = session_with(response(200, SCHEMA))
    with patch(FETCH_SESSION, return_value=session):
        code, _ = _invoke()
    assert code == 0
    assert session.post.call_args.args[0] == "https://gql.example.test/graphql"
    assert session.post.call_args.kwargs["timeout"] == 9.0


@pytest.mark.parametrize(
    "outcome",
    [
        response(200, None),
        response(200, {"data": {}}),
        response(500, {}),
        requests.ConnectionError("x"),
    ],
)
def test_failures_exit_1_and_write_nothing(
    config_dir: Path, outcome: requests.Response | BaseException
) -> None:
    with patch(FETCH_SESSION, return_value=session_with(outcome)):
        code, output = _invoke()
    assert code == 1
    assert "Schema download failed" in output
    assert not _target(config_dir).exists()


def test_config_help_lists_the_command() -> None:
    result = CliRunner().invoke(nf, ["config", "--help"])
    assert "download-schema" in result.output


def test_command_module_imports_the_client_lazily() -> None:
    """The command imports the client inside its body, not at module level.

    A subprocess check of ``nf --help`` cannot show this: any import of
    ``pynetappfoundry.clients.<x>`` runs ``clients/__init__``, which loads every
    client, so ``nf --help`` already loads the Digital Advisor modules.
    """
    module = importlib.import_module("pynetappfoundry.cli.commands.config.download_schema")

    assert not hasattr(module, "fetch_schema")
    tree = ast.parse(Path(module.__file__ or "").read_text(encoding="utf-8"))
    top_level = [
        n
        for n in tree.body
        if isinstance(n, ast.ImportFrom) and "digitaladvisor" in (n.module or "")
    ]
    assert top_level == []
