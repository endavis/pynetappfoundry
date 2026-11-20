"""Tests for ``nf config download-spec`` (#1129). The HTTP layer is mocked."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests
from click.testing import CliRunner

from pynetappfoundry.cli.main import nf
from pynetappfoundry.core import spec_source

CMD = "pynetappfoundry.cli.commands.config.download_spec"
SPEC = json.dumps({"paths": {"/a": {}}})
YAML_SPEC = "paths:\n  /a: {}\n"
SHA_VERSION = "0.1.1.dev275+g1369c1b98"


def _resp(status: int = 200, text: str = SPEC) -> MagicMock:
    response = MagicMock()
    response.status_code = status
    response.text = text
    return response


def _get(url: str, **_: object) -> MagicMock:
    return _resp(text=YAML_SPEC if url.endswith(".yaml") else SPEC)


@pytest.fixture
def config_dir(tmp_path: Path) -> Path:
    cfg = tmp_path / "cfg"
    cfg.mkdir()
    (cfg / "ontapapi.toml").write_text("[general]\n")
    (cfg / "aiqumapi.toml").write_text("[general]\n")
    (cfg / "consoleapi.toml").write_text("[general]\n")
    return cfg


@pytest.fixture(autouse=True)
def repo() -> object:
    with (
        patch(f"{CMD}.installed_repository", return_value=("example-owner", "example-repo")),
        patch(f"{CMD}.__version__", SHA_VERSION),
    ):
        yield


def _invoke(cfg: Path, *extra: str) -> tuple[int, str]:
    result = CliRunner().invoke(nf, ["--config-dir", str(cfg), "config", "download-spec", *extra])
    return result.exit_code, result.output


def _spec(cfg: Path, api: str, name: str = "all.json") -> Path:
    return cfg / "apis" / api / name


def test_writes_missing_specs_of_configured_apis_verbatim(config_dir: Path) -> None:
    with patch(f"{CMD}.requests.get", side_effect=_get) as get:
        code, _ = _invoke(config_dir)

    assert code == 0
    assert _spec(config_dir, "ontap").read_text() == SPEC
    assert _spec(config_dir, "aiqum").read_text() == SPEC
    assert _spec(config_dir, "console", "console_openapi.yaml").read_text() == YAML_SPEC
    assert not _spec(config_dir, "dii").exists()
    assert not (config_dir / "apis" / "occm").exists()
    urls = sorted(call.args[0] for call in get.call_args_list)
    assert (
        "https://raw.githubusercontent.com/example-owner/example-repo/1369c1b98/"
        "docs/example-config/apis/ontap/all.json"
    ) in urls
    assert all(call.kwargs["timeout"] == 120.0 for call in get.call_args_list)


def test_api_limits_to_one_api_even_when_unconfigured(config_dir: Path) -> None:
    with patch(f"{CMD}.requests.get", side_effect=_get) as get:
        code, _ = _invoke(config_dir, "--api", "dii")

    assert code == 0
    assert get.call_count == 1
    assert _spec(config_dir, "dii").read_text() == SPEC
    assert not _spec(config_dir, "ontap").exists()


def test_existing_spec_is_kept_without_force_and_replaced_with_it(config_dir: Path) -> None:
    _spec(config_dir, "ontap").parent.mkdir(parents=True)
    _spec(config_dir, "ontap").write_text("old")
    with patch(f"{CMD}.requests.get", side_effect=_get):
        _invoke(config_dir, "--api", "ontap")
        assert _spec(config_dir, "ontap").read_text() == "old"
        code, _ = _invoke(config_dir, "--api", "ontap", "--force")

    assert code == 0
    assert _spec(config_dir, "ontap").read_text() == SPEC


def test_nothing_to_do_exits_zero_without_a_request(tmp_path: Path) -> None:
    with patch(f"{CMD}.requests.get") as get:
        code, output = _invoke(tmp_path)

    assert code == 0
    assert "Nothing to download" in output
    get.assert_not_called()


@pytest.mark.parametrize(
    "outcome",
    [
        _resp(404, "not found"),
        _resp(500, "boom"),
        requests.ConnectionError("x"),
        _resp(200, json.dumps({"info": {}})),
        _resp(200, "{not json"),
    ],
)
def test_failed_download_writes_nothing_and_exits_1(config_dir: Path, outcome: object) -> None:
    with patch(f"{CMD}.requests.get", side_effect=[outcome]):
        code, output = _invoke(config_dir, "--api", "ontap")

    assert code == 1
    assert "failed" in output
    assert not (config_dir / "apis").exists() or not any((config_dir / "apis").rglob("*"))


def test_404_names_repository_ref_and_file(config_dir: Path) -> None:
    with patch(f"{CMD}.requests.get", return_value=_resp(404)):
        code, output = _invoke(config_dir, "--api", "ontap")

    assert code == 1
    flat = " ".join(output.split())
    assert "example-owner/example-repo" in flat
    assert "1369c1b98" in flat
    assert "docs/example-config/apis/ontap/all.json" in flat
    assert "pushed" in flat


def test_one_failure_does_not_stop_the_others(config_dir: Path) -> None:
    def get(url: str, **_: object) -> MagicMock:
        return _resp(500) if "/ontap/" in url else _get(url)

    with patch(f"{CMD}.requests.get", side_effect=get):
        code, output = _invoke(config_dir)

    assert code == 1
    assert "ONTAP" in output
    assert not _spec(config_dir, "ontap").exists()
    assert _spec(config_dir, "aiqum").read_text() == SPEC


def test_unresolvable_version_fails_before_any_request(config_dir: Path) -> None:
    with (
        patch(f"{CMD}.__version__", "0.1.1.dev3"),
        patch(f"{CMD}.requests.get") as get,
    ):
        code, output = _invoke(config_dir)

    assert code == 1
    assert "0.1.1.dev3" in output
    get.assert_not_called()


def test_dirty_version_warns_and_still_writes(config_dir: Path) -> None:
    with (
        patch(f"{CMD}.__version__", f"{SHA_VERSION}.d20260101"),
        patch(f"{CMD}.requests.get", side_effect=_get),
    ):
        code, output = _invoke(config_dir, "--api", "ontap")

    assert code == 0
    assert "Local changes" in output
    assert _spec(config_dir, "ontap").read_text() == SPEC


def test_release_version_uses_the_tag(config_dir: Path) -> None:
    with (
        patch(f"{CMD}.__version__", "1.2.3"),
        patch(f"{CMD}.requests.get", side_effect=_get) as get,
    ):
        _invoke(config_dir, "--api", "ontap")

    assert "/v1.2.3/" in get.call_args.args[0]


def test_config_help_lists_the_command() -> None:
    result = CliRunner().invoke(nf, ["config", "--help"])
    assert "download-spec" in result.output
    assert spec_source.TAG_PREFIX == "v"
