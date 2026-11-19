"""Tests for ``nf doctor`` (#1113). No test makes a network call."""

from __future__ import annotations

import json
import socket
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import requests
from click.testing import CliRunner, Result

from pynetappfoundry.cli.main import nf
from pynetappfoundry.core.config_checks import CheckResult, CheckSection, CheckStatus

CIPHERTEXT = "SOPS[placeholder-ciphertext]"
SENTINEL = "SENTINEL-plaintext-value"
DATA = '[settings]\ntype = "data"\n\n'
LIVE = "pynetappfoundry.doctor.live.run_live_checks"
INSTALLED = "pynetappfoundry.utils.sops.is_sops_installed"
DECRYPT = "pynetappfoundry.utils.sops.decrypt_value"

VALID = {
    "inv.toml": DATA
    + '[clusters.c1]\nip = "192.0.2.1"\nenv = "Prod"\n\n'
    + '[clusters.c2]\nip = "192.0.2.2"\nenv = "Dev"\n',
    "users.toml": '[clusters]\nuser = "u"\nenc = "placeholder"\n',
    "ontapapi.toml": '[general]\nbase_api_path = "/api"\n',
    "Org1/scope.toml": "",
    "Org1/inv.toml": DATA + '[clusters.o1]\nip = "192.0.2.9"\n',
}


@pytest.fixture(autouse=True)
def _isolate(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("SOPS_AGE_KEY", raising=False)
    monkeypatch.setenv("SOPS_AGE_KEY_FILE", str(tmp_path / "age-keys.txt"))


def _write(tmp_path: Path, files: dict[str, str]) -> None:
    for rel, content in files.items():
        path = tmp_path / "cfg" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


def _run(*args: str) -> Result:
    return CliRunner().invoke(nf, ["-c", "cfg", "doctor", *args])


def _ok_live(titles: list[str] | None = None) -> MagicMock:
    sections = [
        CheckSection(t, (CheckResult(f"live.{t}", CheckStatus.OK, f"{t} row"),))
        for t in titles or ["ONTAP"]
    ]
    return MagicMock(return_value=sections)


def test_all_ok_exits_zero_with_summary(tmp_path: Path) -> None:
    _write(tmp_path, VALID)
    with patch(LIVE, _ok_live()):
        result = _run()

    assert result.exit_code == 0, result.output
    assert "Summary:" in result.output
    assert "0 error" in result.output
    assert "ONTAP row" in result.output


def test_static_error_exits_one_with_hint(tmp_path: Path) -> None:
    _write(tmp_path, {**VALID, "inv.toml": DATA + "[clusters.c1]\ntags = 5\n"})
    with patch(LIVE, _ok_live()):
        result = _run("--offline")

    assert result.exit_code == 1
    assert "Doctor found" in result.output
    assert "Fix the field in the data file" in result.output


def test_warnings_do_not_fail(tmp_path: Path) -> None:
    _write(tmp_path, VALID)
    result = _run("--offline")  # missing caches are warnings

    assert result.exit_code == 0, result.output
    assert "warning" in result.output


def test_missing_config_dir_and_unknown_scope(tmp_path: Path) -> None:
    assert _run("--offline").exit_code == 1
    _write(tmp_path, VALID)
    result = _run("--offline", "--scope", "Nope")
    assert result.exit_code == 1
    assert "Nope" in result.output


def test_offline_makes_no_network_call(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _write(tmp_path, VALID)

    def boom(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("network used with --offline")

    monkeypatch.setattr(socket.socket, "connect", boom)
    monkeypatch.setattr(socket, "create_connection", boom)
    monkeypatch.setattr(requests.Session, "send", boom)
    with patch(LIVE) as live:
        result = _run("--offline")

    assert result.exit_code == 0, result.output
    live.assert_not_called()
    assert "(offline)" in result.output


def test_json_output_groups_and_summary(tmp_path: Path) -> None:
    _write(tmp_path, VALID)
    with patch(LIVE, _ok_live()):
        result = _run("--json")

    assert result.exit_code == 0, result.output
    document = json.loads(result.output)
    assert document["offline"] is False
    assert {s["group"] for s in document["sections"]} == {"static", "environment", "live"}
    assert set(document["summary"]) == {"ok", "warning", "error", "skipped"}
    first = document["sections"][0]["results"][0]
    assert set(first) == {"subject", "status", "label", "errors", "hint"}


def test_json_error_exits_one_with_valid_json(tmp_path: Path) -> None:
    _write(tmp_path, {**VALID, "inv.toml": DATA + "[clusters.c1]\ntags = 5\n"})
    result = _run("--offline", "--json")

    assert result.exit_code == 1
    document = json.loads(result.output)
    assert document["summary"]["error"] >= 1
    assert document["offline"] is True


def test_api_filter_limits_live_and_cache(tmp_path: Path) -> None:
    _write(tmp_path, {**VALID, "inv.toml": VALID["inv.toml"] + '\n[aiqums.a1]\nip = "192.0.2.3"\n'})
    with patch(LIVE, _ok_live()) as live:
        result = _run("--api", "AIQUM", "--json")

    assert result.exit_code in (0, 1)
    assert live.call_args.kwargs["apis"] == ("aiqum",)
    titles = [s["title"] for s in json.loads(result.output)["sections"]]
    assert "Caches" in titles
    subjects = [r["subject"] for s in json.loads(result.output)["sections"] for r in s["results"]]
    assert "cache.aiqum" in subjects
    assert "cache.ontap" not in subjects


def test_unknown_api_is_usage_error(tmp_path: Path) -> None:
    _write(tmp_path, VALID)
    result = _run("--api", "bogus")

    assert result.exit_code == 2
    assert "bogus" in result.output


def test_scope_limits_probed_clusters(tmp_path: Path) -> None:
    _write(tmp_path, VALID)
    with patch(LIVE, _ok_live()) as live:
        result = _run("--scope", "Org1")

    assert result.exit_code == 0, result.output
    assert list(live.call_args.kwargs["clusters"]) == ["o1"]
    assert live.call_args.kwargs["scope"] == "Org1"


def test_filter_limits_clusters(tmp_path: Path) -> None:
    _write(tmp_path, VALID)
    with patch(LIVE, _ok_live()) as live:
        result = _run("-f", '{"env":"Prod"}')

    assert result.exit_code == 0, result.output
    assert list(live.call_args.kwargs["clusters"]) == ["c1"]


@pytest.mark.parametrize("bad", ["{not json", "[1]"])
def test_invalid_filter_is_click_exception(tmp_path: Path, bad: str) -> None:
    _write(tmp_path, VALID)
    result = _run("--offline", "-f", bad)

    assert result.exit_code == 1
    assert "Invalid filter JSON" in result.output


@pytest.mark.parametrize("as_json", [False, True])
def test_no_secret_in_output(tmp_path: Path, as_json: bool) -> None:
    _write(
        tmp_path,
        {**VALID, "users.toml": f'[clusters]\nuser = "u"\nenc = "{CIPHERTEXT}"\n'},
    )
    (tmp_path / "age-keys.txt").write_text("placeholder")
    args = ["--offline", *(["--json"] if as_json else [])]
    with patch(INSTALLED, return_value=True), patch(DECRYPT, return_value=SENTINEL):
        result = _run(*args)

    assert result.exit_code == 0, result.output
    assert SENTINEL not in result.output
    assert CIPHERTEXT not in result.output


def _imported_modules(code: str) -> list[str]:
    out = subprocess.run(
        [sys.executable, "-c", textwrap.dedent(code)], check=True, capture_output=True, text=True
    )
    return json.loads(out.stdout.strip().splitlines()[-1])  # type: ignore[no-any-return]


@pytest.mark.parametrize("argv", [["--help"], ["doctor", "--help"]])
def test_help_does_not_import_doctor_modules(argv: list[str]) -> None:
    loaded = _imported_modules(
        f"""
        import json, sys
        try:
            from pynetappfoundry.cli import nf
            nf({argv!r})
        except SystemExit:
            pass
        print(json.dumps([m for m in sys.modules if m.startswith("pynetappfoundry.doctor.")]))
        """
    )
    assert loaded == []
