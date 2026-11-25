"""Tests for the offline environment checks of ``nf doctor`` (#1113)."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest

from pynetappfoundry.cache.aiqum_db import AiqumCacheDB
from pynetappfoundry.cache.db import ClusterMetadataDB
from pynetappfoundry.cache.occm_db import OccmCacheDB
from pynetappfoundry.core.config import Config
from pynetappfoundry.core.config_checks import CheckResult, CheckStatus
from pynetappfoundry.doctor.environment import (
    CACHE_STALE_DAYS,
    check_caches,
    check_sops,
    find_plaintext_secrets,
    find_sops_values,
    run_environment_checks,
)
from pynetappfoundry.utils.sops import SOPSError

INSTALLED = "pynetappfoundry.utils.sops.is_sops_installed"
DECRYPT = "pynetappfoundry.utils.sops.decrypt_value"
CIPHERTEXT = "SOPS[placeholder-ciphertext]"
SENTINEL = "SENTINEL-plaintext-value"
DATA = '[settings]\ntype = "data"\n\n'


@pytest.fixture(autouse=True)
def _isolate(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("SOPS_AGE_KEY", raising=False)
    monkeypatch.setenv("SOPS_AGE_KEY_FILE", str(tmp_path / "age-keys.txt"))


def _config(tmp_path: Path, files: dict[str, str]) -> Config:
    config_dir = tmp_path / "cfg"
    config_dir.mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        path = config_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return Config(config_dir=str(config_dir), script_name="test")


SOPS_FILES = {
    "users.toml": f'[clusters]\nuser = "u"\nenc = "{CIPHERTEXT}"\n',
    "ontapapi.toml": f'[general]\napi_token = "{CIPHERTEXT}"\n',
    "inv.toml": DATA + f'[clusters.c1]\nip = "192.0.2.1"\nenc = "{CIPHERTEXT}"\n',
    "Org1/scope.toml": "",
    "Org1/users.toml": f'[console]\nuser = "u"\nenc = "{CIPHERTEXT}"\n',
}


def _by_subject(results: list[CheckResult]) -> dict[str, CheckResult]:
    return {r.subject: r for r in results}


def _rendered(results: list[CheckResult]) -> str:
    return "\n".join(f"{r.label}|{r.errors}|{r.hint}" for r in results)


# --- sops and age key ---


def test_find_sops_values_covers_settings_scopes_and_data(tmp_path: Path) -> None:
    config = _config(tmp_path, SOPS_FILES)

    assert set(find_sops_values(config)) == {
        "settings.users.clusters.enc",
        "settings.ontapapi.general.api_token",
        "scope.Org1.users.console.enc",
        "clusters.c1.enc",
    }
    assert set(find_sops_values(config, "Org1")) == {"scope.Org1.users.console.enc"}


def test_sops_missing_with_values_is_error(tmp_path: Path) -> None:
    config = _config(tmp_path, SOPS_FILES)
    with patch(INSTALLED, return_value=False):
        rows = _by_subject(check_sops(config))

    assert rows["env.sops"].status is CheckStatus.ERROR
    assert rows["env.sops"].hint is not None
    assert "docs/getting-started/configuration.md" in rows["env.sops"].hint
    assert not any(s.startswith("sops.") for s in rows)


def test_sops_missing_without_values_is_skipped(tmp_path: Path) -> None:
    config = _config(tmp_path, {})
    with patch(INSTALLED, return_value=False):
        rows = _by_subject(check_sops(config))

    assert rows["env.sops"].status is CheckStatus.SKIPPED
    assert rows["env.sops"].hint is not None
    assert "nf config init-sops" in rows["env.sops"].hint
    assert rows["env.age_key"].status is CheckStatus.SKIPPED
    assert rows["sops.values"].status is CheckStatus.SKIPPED


def test_age_key_from_file_env_and_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config = _config(tmp_path, SOPS_FILES)
    with patch(INSTALLED, return_value=True), patch(DECRYPT, return_value=SENTINEL):
        missing = _by_subject(check_sops(config))["env.age_key"]
        assert missing.status is CheckStatus.ERROR
        assert missing.hint is not None
        assert "nf config init-sops" in missing.hint

        (tmp_path / "age-keys.txt").write_text("placeholder key file")
        assert _by_subject(check_sops(config))["env.age_key"].status is CheckStatus.OK

        (tmp_path / "age-keys.txt").unlink()
        monkeypatch.setenv("SOPS_AGE_KEY", "placeholder-key")
        row = _by_subject(check_sops(config))["env.age_key"]
        assert row.status is CheckStatus.OK
        assert "placeholder-key" not in row.label


def test_one_decrypt_row_per_value(tmp_path: Path) -> None:
    config = _config(tmp_path, SOPS_FILES)
    with patch(INSTALLED, return_value=True), patch(DECRYPT, return_value=SENTINEL) as decrypt:
        results = check_sops(config)

    decrypt_rows = [r for r in results if r.subject.startswith("sops.")]
    assert len(decrypt_rows) == 4
    assert all(r.status is CheckStatus.OK for r in decrypt_rows)
    assert decrypt.call_count == 4
    assert SENTINEL not in _rendered(results)
    assert CIPHERTEXT not in _rendered(results)


def test_decrypt_failure_is_error_without_leaking(tmp_path: Path) -> None:
    config = _config(tmp_path, SOPS_FILES)
    with (
        patch(INSTALLED, return_value=True),
        patch(DECRYPT, side_effect=SOPSError(f"contains {SENTINEL} {CIPHERTEXT}")),
    ):
        results = check_sops(config)

    bad = [r for r in results if r.subject.startswith("sops.")]
    assert len(bad) == 4
    assert all(r.status is CheckStatus.ERROR for r in bad)
    assert all("SOPSError" in r.label for r in bad)
    assert all(r.hint and "SOPS_AGE_KEY_FILE" in r.hint for r in bad)
    assert SENTINEL not in _rendered(results)
    assert CIPHERTEXT not in _rendered(results)


def test_scope_walk_decrypts_only_scope_values(tmp_path: Path) -> None:
    config = _config(tmp_path, SOPS_FILES)
    with patch(INSTALLED, return_value=True), patch(DECRYPT, return_value=SENTINEL) as decrypt:
        results = check_sops(config, "Org1")

    assert decrypt.call_count == 1
    assert [r.subject for r in results if r.subject.startswith("sops.")] == [
        "sops.scope.Org1.users.console.enc"
    ]


def test_no_sops_values_gives_one_skipped_row(tmp_path: Path) -> None:
    config = _config(tmp_path, {"users.toml": '[clusters]\nuser = "u"\n'})
    with patch(INSTALLED, return_value=True):
        rows = _by_subject(check_sops(config))

    assert rows["sops.values"].status is CheckStatus.SKIPPED
    assert [s for s in rows if s.startswith("sops.")] == ["sops.values"]


# --- plaintext secrets (#1204) ---

PLAIN_FILES = {
    "diiapi.toml": f'[general]\napi_ro_token = "{SENTINEL}"\napi_rw_token = "{CIPHERTEXT}"\n',
    "settings.toml": f'[SMTP]\npassword = "{SENTINEL}"\n',
    "digitaladvisorapi.toml": f'[general]\nrefresh_token = "{SENTINEL}"\n',
    "users.toml": f'[clusters]\nuser = "adm in"\nenc = "{SENTINEL}"\n'
    f'\n[console]\nenc = "{SENTINEL}"\n',
    "inv.toml": DATA
    + f'[clusters.c1]\nip = "192.0.2.1"\nenc = "{SENTINEL}"\n'
    + f'\n[aiqums.a1]\nip = "192.0.2.3"\nuser = "q"\nenc = "{SENTINEL}"\n'
    + f'\n[cloudinsights.t1]\nuser = "tok"\nenc = "{CIPHERTEXT}"\nrw_enc = "{SENTINEL}"\n'
    + f'\n[connectors.k1]\nrw_enc = "{SENTINEL}"\n',
    "Org1/scope.toml": "",
    "Org1/consoleapi.toml": f'[general]\nclient_secret = "{SENTINEL}"\n',
    "Org1/users.toml": f'[console]\nuser = "u"\nenc = "{SENTINEL}"\n',
}


def test_find_plaintext_secrets_commands(tmp_path: Path) -> None:
    config = _config(tmp_path, PLAIN_FILES)

    found = find_plaintext_secrets(config)

    assert found == {
        "settings.diiapi.general.api_ro_token": (
            "nf config set-credential --setting diiapi.api_ro_token"
        ),
        "settings.settings.SMTP.password": (
            "nf config set-credential --setting settings.smtp_password"
        ),
        "settings.digitaladvisorapi.general.refresh_token": (
            "nf config set-credential --setting digitaladvisorapi.refresh_token"
        ),
        "settings.users.clusters.enc": "nf config set-credential --type clusters --user 'adm in'",
        "settings.users.console.enc": "nf config set-credential --type console --user <user>",
        "scope.Org1.consoleapi.general.client_secret": (
            "nf config set-credential --setting consoleapi.client_secret --scope Org1"
        ),
        "scope.Org1.users.console.enc": (
            "nf config set-credential --type console --scope Org1 --user u"
        ),
        "clusters.c1.enc": "nf config set-credential --cluster c1 --user <user>",
        "aiqums.a1.enc": "nf config set-credential --type aiqums --name a1 --user q",
        "cloudinsights.t1.rw_enc": (
            "nf config set-credential --type cloudinsights --name t1 --read-write"
        ),
    }


def test_rw_enc_only_on_cloudinsights(tmp_path: Path) -> None:
    config = _config(tmp_path, PLAIN_FILES)

    assert not any(s.startswith("connectors.") for s in find_plaintext_secrets(config))


def test_encrypted_blank_absent_and_non_string_give_no_row(tmp_path: Path) -> None:
    files = {
        "diiapi.toml": f'[general]\napi_ro_token = "{CIPHERTEXT}"\napi_rw_token = "  "\n',
        "settings.toml": "[SMTP]\npassword = 5\n",
        "users.toml": '[clusters]\nuser = "u"\nenc = ""\n',
        "inv.toml": DATA + '[clusters.c1]\nip = "192.0.2.1"\nenc = 7\n',
    }
    config = _config(tmp_path, files)

    assert find_plaintext_secrets(config) == {}


def test_find_plaintext_secrets_limited_to_api_and_scope(tmp_path: Path) -> None:
    config = _config(tmp_path, PLAIN_FILES)

    assert set(find_plaintext_secrets(config, apis=("dii",))) == {
        "settings.diiapi.general.api_ro_token",
        "cloudinsights.t1.rw_enc",
    }
    assert set(find_plaintext_secrets(config, apis=("digitaladvisor",))) == {
        "settings.digitaladvisorapi.general.refresh_token"
    }
    assert set(find_plaintext_secrets(config, "Org1")) == {
        "scope.Org1.consoleapi.general.client_secret",
        "scope.Org1.users.console.enc",
    }
    assert "settings.settings.SMTP.password" not in find_plaintext_secrets(config, apis=("dii",))


def test_check_sops_plaintext_rows_warn_and_hide_value(tmp_path: Path) -> None:
    config = _config(tmp_path, PLAIN_FILES)
    with patch(INSTALLED, return_value=True), patch(DECRYPT, return_value="x"):
        results = check_sops(config)
    rows = _by_subject(results)

    row = rows["sops.settings.diiapi.general.api_ro_token"]
    assert row.status is CheckStatus.WARNING
    assert row.label == "settings.diiapi.general.api_ro_token: plaintext (not SOPS-encrypted)"
    assert row.hint == (
        "Store it encrypted with: nf config set-credential --setting diiapi.api_ro_token"
    )
    assert rows["sops.settings.diiapi.general.api_rw_token"].status is CheckStatus.OK
    assert SENTINEL not in _rendered(results)


def test_check_sops_plaintext_rows_when_sops_not_installed(tmp_path: Path) -> None:
    config = _config(tmp_path, {"diiapi.toml": f'[general]\napi_ro_token = "{SENTINEL}"\n'})
    with patch(INSTALLED, return_value=False):
        results = check_sops(config)
    rows = _by_subject(results)

    assert rows["sops.values"].status is CheckStatus.SKIPPED
    assert rows["sops.settings.diiapi.general.api_ro_token"].status is CheckStatus.WARNING
    assert SENTINEL not in _rendered(results)


def test_check_sops_plaintext_rows_when_values_exist_but_sops_missing(tmp_path: Path) -> None:
    files = {
        "diiapi.toml": f'[general]\napi_ro_token = "{SENTINEL}"\napi_rw_token = "{CIPHERTEXT}"\n'
    }
    config = _config(tmp_path, files)
    with patch(INSTALLED, return_value=False):
        rows = _by_subject(check_sops(config))

    assert rows["env.sops"].status is CheckStatus.ERROR
    assert rows["sops.settings.diiapi.general.api_ro_token"].status is CheckStatus.WARNING


def test_check_sops_with_apis_keeps_plaintext_only_rows(tmp_path: Path) -> None:
    config = _config(tmp_path, PLAIN_FILES)
    with patch(INSTALLED, return_value=True):
        rows = _by_subject(check_sops(config, apis=("digitaladvisor",)))

    assert rows["sops.settings.digitaladvisorapi.general.refresh_token"].status is (
        CheckStatus.WARNING
    )
    assert check_sops(config, apis=("ibm",)) == []


# --- caches ---

INV = (
    DATA
    + '[clusters.c1]\nip = "192.0.2.1"\n\n[clusters.c2]\nip = "192.0.2.2"\n'
    + '\n[aiqums.a1]\nip = "192.0.2.3"\n'
)
CONSOLE = {"consoleapi.toml": '[general]\nuser_token = "placeholder-token"\n'}


def _make_ontap_cache(config: Config, *, names: tuple[str, ...], age_days: int = 0) -> Path:
    path = ClusterMetadataDB.default_path(config)
    path.parent.mkdir(parents=True, exist_ok=True)
    db = ClusterMetadataDB(db_path=path)
    stamp = (datetime.now(UTC) - timedelta(days=age_days)).isoformat()
    for name in names:
        db.conn.execute(
            "INSERT INTO cluster_metadata (cluster_name, cached_at, cache_version) "
            "VALUES (?, ?, ?)",
            (name, stamp, "3.0"),
        )
    db.conn.commit()
    db.conn.close()
    return path


def _set_version(path: Path, version: int) -> None:
    conn = sqlite3.connect(path)
    conn.execute("UPDATE _schema_version SET version = ?", (version,))
    conn.commit()
    conn.close()


def _caches(config: Config, apis: tuple[str, ...] = ("ontap",)) -> dict[str, CheckResult]:
    clusters = config.get_clusters({})
    return {r.subject: r for r in check_caches(config, apis, clusters)}


def test_missing_cache_warns_and_creates_nothing(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": INV})

    row = _caches(config)["cache.ontap"]

    assert row.status is CheckStatus.WARNING
    assert row.hint is not None
    assert "nf cache refresh --all" in row.hint
    assert not (tmp_path / "cfg" / ".cache").exists()


def test_empty_cache_warns(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": INV})
    _make_ontap_cache(config, names=())

    row = _caches(config)["cache.ontap"]

    assert row.status is CheckStatus.WARNING
    assert "empty" in row.label


def test_fresh_cache_is_ok(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": INV})
    _make_ontap_cache(config, names=("c1", "c2"))

    row = _caches(config)["cache.ontap"]

    assert row.status is CheckStatus.OK
    assert f"v{ClusterMetadataDB.SCHEMA_VERSION}" in row.label


def test_stale_cache_warns(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": INV})
    _make_ontap_cache(config, names=("c1", "c2"), age_days=CACHE_STALE_DAYS + 10)

    row = _caches(config)["cache.ontap"]

    assert row.status is CheckStatus.WARNING
    assert "past 30 days" in row.label


def test_lower_version_warns_and_file_is_unchanged(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": INV})
    path = _make_ontap_cache(config, names=("c1", "c2"))
    _set_version(path, ClusterMetadataDB.SCHEMA_VERSION - 1)
    before = path.read_bytes()

    row = _caches(config)["cache.ontap"]

    assert row.status is CheckStatus.WARNING
    assert f"schema v{ClusterMetadataDB.SCHEMA_VERSION - 1}" in row.label
    assert row.hint is not None
    assert "upgrades on the next cache command" in row.hint
    assert path.read_bytes() == before


def test_higher_version_is_error(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": INV})
    path = _make_ontap_cache(config, names=("c1", "c2"))
    _set_version(path, ClusterMetadataDB.SCHEMA_VERSION + 1)

    row = _caches(config)["cache.ontap"]

    assert row.status is CheckStatus.ERROR
    assert "ADR-0018" in row.errors[0]
    assert row.hint is not None
    assert "nf cache clear" in row.hint


def test_uncached_clusters_listed(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": INV})
    _make_ontap_cache(config, names=("c1",))

    row = _caches(config)["cache.ontap.coverage"]

    assert row.status is CheckStatus.WARNING
    assert "c2" in row.label
    assert "c1" not in row.label.split("not cached:")[1]


def test_uncached_clusters_list_is_capped(tmp_path: Path) -> None:
    body = DATA + "".join(f'[clusters.c{i}]\nip = "192.0.2.{i}"\n\n' for i in range(1, 9))
    config = _config(tmp_path, {"inv.toml": body})
    _make_ontap_cache(config, names=("other",))

    row = _caches(config)["cache.ontap.coverage"]

    assert "and 3 more" in row.label


def test_corrupt_cache_is_error(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": INV})
    path = ClusterMetadataDB.default_path(config)
    path.parent.mkdir(parents=True)
    path.write_bytes(b"this is not a sqlite database" * 50)

    row = _caches(config)["cache.ontap"]

    assert row.status is CheckStatus.ERROR
    assert row.hint is not None
    assert "nf cache clear" in row.hint


def test_aiqum_and_occm_caches(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": INV, **CONSOLE})
    for db_class in (AiqumCacheDB, OccmCacheDB):
        path = db_class.default_path(config)
        path.parent.mkdir(parents=True, exist_ok=True)
        db_class(db_path=path).conn.close()

    rows = _caches(config, ("aiqum", "console"))

    assert rows["cache.aiqum"].status is CheckStatus.WARNING
    assert "empty" in rows["cache.aiqum"].label
    assert rows["cache.occm"].status is CheckStatus.WARNING
    assert rows["cache.occm"].hint is not None
    assert "nf cache occm refresh" in rows["cache.occm"].hint


def test_caches_follow_selected_apis_and_configuration(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": INV})

    assert _caches(config, ("dii",)) == {}
    assert set(_caches(config, ("ontap", "aiqum", "console"))) == {"cache.ontap", "cache.aiqum"}
    bare = _config(tmp_path / "bare", {})
    assert _caches(bare, ("ontap", "aiqum", "console")) == {}


def test_run_environment_checks_sections(tmp_path: Path) -> None:
    config = _config(tmp_path, {"inv.toml": INV})
    with patch(INSTALLED, return_value=True):
        sections = run_environment_checks(
            config, scope=None, apis=("ontap",), clusters=config.get_clusters({})
        )

    assert [s.title for s in sections] == ["SOPS", "Caches"]
    no_caches = run_environment_checks(config, scope=None, apis=("dii",), clusters={})
    assert [s.title for s in no_caches] == ["SOPS"]


# --- selection by API (#1122) ---

API_SOPS_FILES = {
    **SOPS_FILES,
    "users.toml": f'[clusters]\nuser = "u"\nenc = "{CIPHERTEXT}"\n'
    f'\n[console]\nenc = "{CIPHERTEXT}"\n\n[azure]\nenc = "{CIPHERTEXT}"\n',
    "settings.toml": f'[SMTP]\npassword = "{CIPHERTEXT}"\n',
    "digitaladvisorapi.toml": f'[general]\npersonal_access_token = "{CIPHERTEXT}"\n',
    "inv.toml": DATA
    + f'[clusters.c1]\nip = "192.0.2.1"\nenc = "{CIPHERTEXT}"\n'
    + f'\n[cloudinsights.t1]\nenc = "{CIPHERTEXT}"\n'
    + f'\n[connectors.k1]\nenc = "{CIPHERTEXT}"\n',
}


@pytest.mark.parametrize(
    ("api", "expected"),
    [
        (
            "ontap",
            {
                "settings.users.clusters.enc",
                "settings.ontapapi.general.api_token",
                "clusters.c1.enc",
            },
        ),
        ("aiqum", set()),
        ("dii", {"cloudinsights.t1.enc"}),
        (
            "console",
            {
                "settings.users.console.enc",
                "scope.Org1.users.console.enc",
                "connectors.k1.enc",
            },
        ),
        ("digitaladvisor", {"settings.digitaladvisorapi.general.personal_access_token"}),
    ],
)
def test_find_sops_values_limited_to_api(tmp_path: Path, api: str, expected: set[str]) -> None:
    config = _config(tmp_path, API_SOPS_FILES)

    assert set(find_sops_values(config, apis=(api,))) == expected


def test_find_sops_values_apis_none_equals_unfiltered_and_hides_globals(tmp_path: Path) -> None:
    config = _config(tmp_path, API_SOPS_FILES)
    everything = find_sops_values(config)

    assert find_sops_values(config, apis=None) == everything
    assert "settings.settings.SMTP.password" in everything
    assert "settings.users.azure.enc" in everything
    for api in ("ontap", "aiqum", "dii", "console", "digitaladvisor"):
        hidden = set(find_sops_values(config, apis=(api,)))
        assert "settings.settings.SMTP.password" not in hidden
        assert "settings.users.azure.enc" not in hidden


def test_check_sops_with_apis_and_no_values_returns_no_rows(tmp_path: Path) -> None:
    config = _config(tmp_path, SOPS_FILES)
    with patch(INSTALLED, return_value=True):
        assert check_sops(config, apis=("digitaladvisor",)) == []


def test_check_sops_with_apis_checks_only_their_values(tmp_path: Path) -> None:
    config = _config(tmp_path, API_SOPS_FILES)
    Path("age-keys.txt").write_text("placeholder", encoding="utf-8")
    with patch(INSTALLED, return_value=True), patch(DECRYPT, return_value=SENTINEL):
        rows = _by_subject(check_sops(config, apis=("digitaladvisor",)))

    assert set(rows) == {
        "env.sops",
        "env.age_key",
        "sops.settings.digitaladvisorapi.general.personal_access_token",
    }


def test_run_environment_checks_sops_apis_without_values_has_no_sops_section(
    tmp_path: Path,
) -> None:
    config = _config(tmp_path, SOPS_FILES)
    with patch(INSTALLED, return_value=True), patch(DECRYPT, return_value=SENTINEL):
        sections = run_environment_checks(config, scope=None, sops_apis=("dii",), clusters={})

    assert "SOPS" not in [s.title for s in sections]
