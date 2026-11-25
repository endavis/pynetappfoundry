"""Tests for ``nf doctor`` (#1113). No test makes a network call."""

from __future__ import annotations

import json
import socket
import subprocess
import sys
import textwrap
import time
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import requests
from click.testing import CliRunner, Result

from pynetappfoundry.cli.main import nf
from pynetappfoundry.core.config_checks import CheckResult, CheckSection, CheckStatus
from tests.unit.clients.digitaladvisor.helpers import gql, make_jwt, response

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
    (tmp_path / "age-keys.txt").write_text("placeholder", encoding="utf-8")
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


# --- Digital Advisor (#1117) ---

DA_PAT = "PLACEHOLDER-da-pat"
DA_OLD_REFRESH = "PLACEHOLDER-da-old-refresh"
DA_NEW_REFRESH = "PLACEHOLDER-da-new-refresh"
DA_NEW_ACCESS = make_jwt(time.time() + 7200, {"tag": "rotated"})
DA_EXPIRED = make_jwt(1.0, {"tag": "expired"})


def _da_files(refresh: bool) -> dict[str, str]:
    body = (
        f'refresh_token = "{DA_OLD_REFRESH}"\naccess_token = "{DA_EXPIRED}"\n'
        if refresh
        else f'personal_access_token = "{DA_PAT}"\n'
    )
    return {**VALID, "digitaladvisorapi.toml": f"[general]\n{body}"}


def _fake_post(calls: list[str]) -> Any:
    def post(self: Any, url: str, **kwargs: Any) -> requests.Response:
        calls.append(url)
        if "json" in kwargs and "query" in kwargs["json"]:
            return gql({"volumes": {"cursor": None}})
        return response(200, {"access_token": DA_NEW_ACCESS, "refresh_token": DA_NEW_REFRESH})

    return post


@pytest.mark.parametrize("as_json", [False, True])
def test_digitaladvisor_pat_end_to_end(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, as_json: bool
) -> None:
    _write(tmp_path, _da_files(refresh=False))
    calls: list[str] = []
    monkeypatch.setattr(requests.Session, "post", _fake_post(calls))

    result = _run("--api", "digitaladvisor", *(["--json"] if as_json else []))

    assert result.exit_code == 0, result.output
    assert "Digital Advisor" in result.output
    assert DA_PAT not in result.output
    assert len(calls) == 1


@pytest.mark.parametrize("as_json", [False, True])
def test_digitaladvisor_refresh_end_to_end_hides_rotated_tokens(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, as_json: bool
) -> None:
    _write(tmp_path, _da_files(refresh=True))
    calls: list[str] = []
    monkeypatch.setattr(requests.Session, "post", _fake_post(calls))

    result = _run("--api", "digitaladvisor", *(["--json"] if as_json else []))

    assert result.exit_code == 0, result.output
    assert "wrote the rotated tokens" in result.output.replace("\n", " ") or as_json
    for token in (DA_OLD_REFRESH, DA_NEW_REFRESH, DA_NEW_ACCESS, DA_EXPIRED):
        assert token not in result.output
    assert DA_NEW_REFRESH in (tmp_path / "cfg" / "digitaladvisorapi.toml").read_text()
    assert len(calls) == 2


def test_digitaladvisor_offline_makes_no_network_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write(tmp_path, _da_files(refresh=False))

    def boom(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("network used with --offline")

    monkeypatch.setattr(socket.socket, "connect", boom)
    monkeypatch.setattr(socket, "create_connection", boom)
    monkeypatch.setattr(requests.Session, "send", boom)

    result = _run("--offline", "--api", "digitaladvisor")

    assert result.exit_code == 0, result.output
    assert "(offline)" in result.output
    assert "token works" not in result.output


def test_api_option_accepts_digitaladvisor_case_insensitively(tmp_path: Path) -> None:
    _write(tmp_path, VALID)
    with patch(LIVE, _ok_live()) as live:
        result = _run("--api", "DigitalAdvisor")

    assert result.exit_code == 0, result.output
    assert live.call_args.kwargs["apis"] == ("digitaladvisor",)


# --- --api limits every check (#1122) ---

ALL_API_FILES = {
    "inv.toml": DATA
    + '[clusters.c1]\nip = "192.0.2.1"\n\n[aiqums.a1]\nip = "192.0.2.2"\n'
    + '\n[cloudinsights.t1]\nurl = "https://example.invalid"\n'
    + '\n[connectors.k1]\nip = "192.0.2.3"\n',
    "users.toml": f'[clusters]\nuser = "u"\nenc = "{CIPHERTEXT}"\n'
    f'\n[aiqums]\nuser = "u"\nenc = "{CIPHERTEXT}"\n'
    f'\n[console]\nuser = "u"\nenc = "{CIPHERTEXT}"\n'
    f'\n[cloudinsights]\nenc = "{CIPHERTEXT}"\n',
    "ontapapi.toml": '[general]\nbase_api_path = "/api"\n',
    "aiqumapi.toml": '[general]\nbase_api_path = "/api"\n',
    "diiapi.toml": '[general]\nbase_api_path = "/api"\n',
    "consoleapi.toml": '[general]\nbase_api_path = "/api"\n',
    "digitaladvisorapi.toml": f'[general]\npersonal_access_token = "{CIPHERTEXT}"\n',
    "settings.toml": '[SMTP]\nserver = "smtp.invalid"\n',
    "licensing.toml": "",
}


def _subjects(result: Result) -> set[str]:
    document = json.loads(result.output)
    return {r["subject"] for section in document["sections"] for r in section["results"]}


def _offline_json(tmp_path: Path, *args: str) -> Result:
    _write(tmp_path, ALL_API_FILES)
    (tmp_path / "age-keys.txt").write_text("placeholder", encoding="utf-8")
    with patch(INSTALLED, return_value=True), patch(DECRYPT, return_value=SENTINEL):
        return _run("--offline", "--json", *args)


@pytest.mark.parametrize(
    ("api", "present", "absent_prefixes"),
    [
        (
            "digitaladvisor",
            {
                "digitaladvisorapi.general",
                "env.sops",
                "env.age_key",
                "sops.settings.digitaladvisorapi.general.personal_access_token",
            },
            ("clusters", "users", "aiqum", "cloudinsights", "connectors", "licensing"),
        ),
        (
            "ontap",
            {"clusters.c1.credentials", "ontapapi.general", "env.sops"},
            ("aiqum", "cloudinsights", "digitaladvisorapi", "licensing", "settings.SMTP"),
        ),
        (
            "dii",
            {"cloudinsights.t1.credentials", "diiapi.general", "env.sops"},
            ("clusters", "aiqum", "digitaladvisorapi", "licensing"),
        ),
    ],
)
def test_api_limits_static_and_sops_rows(
    tmp_path: Path, api: str, present: set[str], absent_prefixes: tuple[str, ...]
) -> None:
    result = _offline_json(tmp_path, "--api", api)

    subjects = _subjects(result)
    assert present <= subjects, subjects
    for prefix in absent_prefixes:
        assert not any(s == prefix or s.startswith(prefix + ".") for s in subjects), (
            prefix,
            subjects,
        )


def test_api_union_of_two_apis(tmp_path: Path) -> None:
    result = _offline_json(tmp_path, "--api", "ontap,dii")

    subjects = _subjects(result)
    assert {"ontapapi.general", "diiapi.general"} <= subjects
    assert not any(s.startswith(("aiqumapi", "digitaladvisorapi", "licensing")) for s in subjects)


def test_no_api_leaves_static_and_sops_unfiltered(tmp_path: Path) -> None:
    from pynetappfoundry.core.config import Config
    from pynetappfoundry.core.config_checks import run_static_checks
    from pynetappfoundry.doctor.environment import check_sops

    result = _offline_json(tmp_path)
    document = json.loads(result.output)
    with patch(INSTALLED, return_value=True), patch(DECRYPT, return_value=SENTINEL):
        config = Config(config_dir="cfg", script_name="test")
        expected_sops = [r.subject for r in check_sops(config)]
        expected = run_static_checks(config)

    static = [s for s in document["sections"] if s["group"] == "static"]
    assert [s["title"] for s in static] == [f"Config: {s.title}" for s in expected]
    for got, want in zip(static, expected, strict=True):
        assert [r["subject"] for r in got["results"]] == [r.subject for r in want.results]
        assert [r["status"] for r in got["results"]] == [r.status.value for r in want.results]
        assert [r["label"] for r in got["results"]] == [r.label for r in want.results]
    sops = [s for s in document["sections"] if s["title"] == "SOPS"]
    assert [r["subject"] for r in sops[0]["results"]] == expected_sops


def test_exit_code_reflects_only_shown_checks(tmp_path: Path) -> None:
    files = {
        **ALL_API_FILES,
        "inv.toml": DATA + "[clusters.c1]\ntags = 5\n",
        "users.toml": '[console]\nuser = "u"\n',
    }
    _write(tmp_path, files)
    (tmp_path / "age-keys.txt").write_text("placeholder", encoding="utf-8")
    with patch(INSTALLED, return_value=True), patch(DECRYPT, return_value=SENTINEL):
        assert _run("--offline", "--api", "digitaladvisor").exit_code == 0
        assert _run("--offline", "--api", "ontap").exit_code == 1


def test_undecryptable_value_of_selected_api_exits_one(tmp_path: Path) -> None:
    from pynetappfoundry.utils.sops import SOPSError

    _write(tmp_path, ALL_API_FILES)
    (tmp_path / "age-keys.txt").write_text("placeholder", encoding="utf-8")
    with patch(INSTALLED, return_value=True), patch(DECRYPT, side_effect=SOPSError("x")):
        result = _run("--offline", "--api", "digitaladvisor")

    assert result.exit_code == 1


def test_api_help_mentions_every_check() -> None:
    result = CliRunner().invoke(nf, ["doctor", "--help"])

    assert "every check" in " ".join(result.output.split())


# --- Console cluster names (#1127) ---


def _console_cache(tmp_path: Path, *, we_name: str) -> None:
    from datetime import UTC, datetime

    from pynetappfoundry.cache._metadata import CachedClusterMetadata
    from pynetappfoundry.cache.db import ClusterMetadataDB
    from pynetappfoundry.cache.occm_collector import OccmAgentSnapshot, OccmSnapshot
    from pynetappfoundry.cache.occm_db import OccmCacheDB
    from pynetappfoundry.console.discovery import ConsoleInventory
    from pynetappfoundry.models.ontap.cluster.model import OntapCluster

    uuid = "00000000-0000-0000-0000-000000000001"
    cache = tmp_path / "cfg" / ".cache"
    cache.mkdir(parents=True, exist_ok=True)
    now = datetime.now(UTC)
    record = {
        "publicId": "w1",
        "name": "we-w1",
        "ontapClusterProperties": {"clusterName": we_name, "clusterUuid": uuid},
    }
    agent = OccmAgentSnapshot(
        agent_id="a1",
        scope=None,
        organization_id="org-1",
        cached_at=now,
        records={"OccmOnpremWorkingEnvironment": [record]},
    )
    with OccmCacheDB(db_path=cache / "occm_cache.db") as occm:
        occm.set(
            OccmSnapshot(
                cached_at=now,
                inventory=ConsoleInventory(),
                agents=(agent,),
                failed_agents=(),
                skipped_agents=(),
            )
        )
    with ClusterMetadataDB(db_path=cache / "cluster_metadata.db") as db:
        db.set(
            "c1",
            CachedClusterMetadata(
                cluster_name="c1", cached_at=now, cluster=OntapCluster(name="c1", uuid=uuid)
            ),
        )


CONSOLE_FILES = {
    **VALID,
    "consoleapi.toml": (
        '[general]\nbase_url = "https://console.invalid"\nuser_token = "placeholder-token"\n'
    ),
}


def _console_rows(result: Result) -> dict[str, str]:
    document = json.loads(result.output)
    return {
        r["subject"]: r["status"]
        for s in document["sections"]
        if s["title"] == "Console clusters"
        for r in s["results"]
    }


def test_console_cluster_rename_is_an_error(tmp_path: Path) -> None:
    _write(tmp_path, CONSOLE_FILES)
    _console_cache(tmp_path, we_name="prod-c1")

    result = _run("--offline", "--json")

    assert result.exit_code == 1
    document = json.loads(result.output)
    section = next(s for s in document["sections"] if s["title"] == "Console clusters")
    assert section["group"] == "environment"
    assert _console_rows(result)["console_clusters.root.c1"] == "error"


def test_console_cluster_matching_names_exit_zero(tmp_path: Path) -> None:
    _write(tmp_path, CONSOLE_FILES)
    _console_cache(tmp_path, we_name="c1")

    result = _run("--offline", "--json", "-f", '{"env":"Prod"}')

    assert result.exit_code == 0, result.output
    assert not any(s.endswith("console_only") for s in _console_rows(result))


def test_console_clusters_follow_api(tmp_path: Path) -> None:
    _write(tmp_path, CONSOLE_FILES)
    _console_cache(tmp_path, we_name="c1")

    assert _console_rows(_run("--offline", "--json", "--api", "digitaladvisor")) == {}
    assert _console_rows(_run("--offline", "--json", "--api", "ontap")) != {}


def test_live_error_lines_and_hints_carry_the_section_title(tmp_path: Path) -> None:
    _write(tmp_path, VALID)
    bad = CheckSection(
        "AIQUM",
        (
            CheckResult(
                "live.aiqum",
                CheckStatus.ERROR,
                "host-a unreachable",
                errors=("host-a unreachable",),
                hint="Check the host name",
            ),
        ),
    )
    with patch(LIVE, MagicMock(return_value=[bad])):
        result = _run()

    assert result.exit_code == 1
    assert "- AIQUM: host-a unreachable" in result.output
    assert "AIQUM: Check the host name" in result.output


def test_static_error_line_carries_the_section_title(tmp_path: Path) -> None:
    _write(tmp_path, {**VALID, "inv.toml": DATA + "[clusters.c1]\ntags = 5\n"})
    with patch(LIVE, _ok_live()):
        result = _run("--offline")

    assert result.exit_code == 1
    assert "- Config: " in result.output


_PLAIN_DII = {
    "diiapi.toml": '[general]\nbase_url = "https://dii.invalid"\nbase_api_path = "/api"\n'
    f'api_ro_token = "{SENTINEL}"\n'
}


def test_plaintext_secret_warns_exits_zero_and_hides_value(tmp_path: Path) -> None:
    _write(tmp_path, _PLAIN_DII)
    with patch(INSTALLED, return_value=True):
        result = _run("--offline")

    assert result.exit_code == 0, result.output
    assert "plaintext (not SOPS-encrypted)" in result.output
    assert "nf config set-credential --setting diiapi.api_ro_token" in " ".join(
        result.output.split()
    )
    assert SENTINEL not in result.output


def test_plaintext_secret_json_api_dii_is_warning(tmp_path: Path) -> None:
    _write(tmp_path, _PLAIN_DII)
    with patch(INSTALLED, return_value=True):
        result = _run("--offline", "--json", "--api", "dii")

    assert result.exit_code == 0, result.output
    rows = {
        r["subject"]: r
        for section in json.loads(result.output)["sections"]
        for r in section["results"]
    }
    assert rows["sops.settings.diiapi.general.api_ro_token"]["status"] == "warning"
    assert SENTINEL not in result.output
