"""Tests for the shared static config checks (#1111)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from pynetappfoundry.core.config import Config
from pynetappfoundry.core.config_checks import (
    CheckResult,
    CheckStatus,
    check_aiqum_credentials,
    check_aiqums,
    check_cloudinsights,
    check_cloudinsights_credentials,
    check_cluster_credentials,
    check_clusters,
    check_connectors,
    check_scope_settings,
    check_settings,
    check_spec_files,
    check_users,
    run_static_checks,
)
from pynetappfoundry.utils.sops import SOPSError

DECRYPT = "pynetappfoundry.utils.sops.decrypt_value"
CIPHERTEXT = "SOPS[placeholder-ciphertext]"
PLAIN = "placeholder-plain-token"
DATA = '[settings]\ntype = "data"\n\n'


@pytest.fixture(autouse=True)
def _isolate(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    for name in ("C1", "C2", "AIQ1", "AIQ2", "T1", "T2"):
        monkeypatch.delenv(f"NF_{name}_USER", raising=False)
        monkeypatch.delenv(f"NF_{name}_PASSWORD", raising=False)


def _config(tmp_path: Path, files: dict[str, str]) -> Config:
    config_dir = tmp_path / "cfg"
    config_dir.mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        path = config_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return Config(config_dir=str(config_dir), script_name="test")


def _by_subject(results: list[CheckResult]) -> dict[str, CheckResult]:
    return {r.subject: r for r in results}


def _everything(results: list[CheckResult]) -> str:
    return "\n".join(f"{r.label}|{r.errors}|{r.hint}" for r in results)


# --- moved checks ---


def test_clusters_valid_invalid_and_empty(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        {"inv.toml": DATA + '[clusters.c1]\nip = "192.0.2.1"\n\n[clusters.c2]\ntags = 5\n'},
    )

    rows = _by_subject(check_clusters(config))

    assert rows["clusters.c1"].status is CheckStatus.OK
    assert rows["clusters.c1"].label == "c1"
    bad = rows["clusters.c2"]
    assert bad.status is CheckStatus.ERROR
    assert bad.label == "c2: Invalid"
    assert bad.errors == ("clusters.c2.tags: Input should be a valid list",)
    assert bad.hint is not None
    assert "--scope" not in bad.hint

    empty = check_clusters(_config(tmp_path / "e", {}))
    assert empty == [CheckResult("clusters", CheckStatus.WARNING, "No clusters configured")]


def test_users_valid_invalid_empty_and_scope_hint() -> None:
    assert check_users({}) == [CheckResult("users", CheckStatus.WARNING, "No users configured")]

    rows = _by_subject(
        check_users({"clusters": {"user": "u", "enc": "e"}, "bad": {"user": 5}, "skip": {"x": 1}})
    )

    assert set(rows) == {"users.clusters", "users.bad"}
    assert rows["users.clusters"].status is CheckStatus.OK
    assert rows["users.bad"].errors == (
        "users.bad.user: Input should be a valid string",
        "users.bad.enc: Field required",
    )
    assert rows["users.bad"].hint is not None
    assert "--scope" not in rows["users.bad"].hint

    scoped = check_users({"clusters": {"user": 5}}, label_prefix="Org1/users", scope="Org1")[0]
    assert scoped.errors[0].startswith("Org1/users.clusters.user:")
    assert scoped.hint is not None
    assert "Org1/users.toml" in scoped.hint
    assert "--type clusters --scope Org1" in scoped.hint


def test_settings_rows_in_order_with_texts_and_statuses(tmp_path: Path) -> None:
    results = check_settings(_config(tmp_path, {}))

    assert [(r.label, r.status) for r in results] == [
        ("ONTAP API: Not configured", CheckStatus.WARNING),
        ("DII API: Not configured (optional)", CheckStatus.SKIPPED),
        ("SMTP: Not configured (optional)", CheckStatus.SKIPPED),
        ("Console: Not configured (optional)", CheckStatus.SKIPPED),
        ("Licensing: Not configured (optional)", CheckStatus.SKIPPED),
    ]
    assert all(r.hint is None for r in results)


def test_invalid_settings_section_carries_error_and_docs_hint(tmp_path: Path) -> None:
    config = _config(tmp_path, {"settings.toml": '[SMTP]\nserver = "s"\nport = "x"\n'})

    smtp = _by_subject(check_settings(config))["settings.SMTP"]

    assert smtp.status is CheckStatus.ERROR
    assert smtp.label == "SMTP: Invalid"
    assert smtp.errors[0].startswith("settings.SMTP: Invalid SMTP configuration")
    assert smtp.hint == "See docs/reference/config-schema.md (settings.SMTP)."


def test_console_refresh_token_hint_is_a_sibling_row(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        {
            "consoleapi.toml": '[general]\nbase_url = "https://api.example.invalid"\n'
            'client_id = "placeholder-id"\n',
            "users.toml": '[console]\nuser = "u"\nenc = "placeholder-enc"\n',
        },
    )

    console = _by_subject(check_settings(config))["consoleapi.general"]

    assert console.status is CheckStatus.ERROR
    assert console.hint is not None
    assert "nf config set-credential --setting consoleapi.client_secret" in console.hint
    assert "--scope" not in console.hint
    assert console.hint_as_sibling


def test_scope_settings_use_the_scope_prefix_and_hint(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        {
            "Org1/scope.toml": "",
            "Org1/consoleapi.toml": '[general]\nbase_url = "https://api.example.invalid"\n'
            'client_id = "placeholder-id"\n',
            "Org1/users.toml": '[console]\nuser = "u"\nenc = "placeholder-enc"\n',
        },
    )

    monitoring, console = check_scope_settings(config, "Org1")

    assert monitoring.label == "Monitoring: Not configured (optional)"
    assert console.errors[0].startswith("Org1/consoleapi.general:")
    assert console.hint is not None
    assert "consoleapi.client_secret --scope Org1" in console.hint


def test_cluster_credentials_ok_and_missing(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        {
            "inv.toml": DATA
            + '[clusters.c1]\nip = "192.0.2.1"\nuser = "own"\nenc = "own-pw"\n\n'
            + '[clusters.c2]\nip = "192.0.2.2"\n',
        },
    )

    rows = _by_subject(check_cluster_credentials(config))

    assert rows["clusters.c1.credentials"].label == "c1: own"
    missing = rows["clusters.c2.credentials"]
    assert missing.status is CheckStatus.ERROR
    assert missing.label == "c2: Missing credentials"
    assert missing.errors == ("Cluster 'c2' has no credentials configured",)
    assert missing.hint == "Set them with: nf config set-credential --cluster c2 --user USER"


# --- AIQUM ---


def test_aiqum_api_row_absent_valid_invalid_and_inventory_without_settings(
    tmp_path: Path,
) -> None:
    inv = {"inv.toml": DATA + '[aiqums.aiq1]\nip = "192.0.2.5"\n'}

    absent = _by_subject(check_settings(_config(tmp_path / "a", {})))
    assert "aiqumapi.general" not in absent

    valid = _by_subject(
        check_settings(_config(tmp_path / "b", {"aiqumapi.toml": "[general]\ntimeout = 10\n"}))
    )
    assert valid["aiqumapi.general"].status is CheckStatus.OK
    assert valid["aiqumapi.general"].label == "AIQUM API"

    invalid = _by_subject(
        check_settings(_config(tmp_path / "c", {"aiqumapi.toml": '[general]\ntimeout = "x"\n'}))
    )["aiqumapi.general"]
    assert invalid.status is CheckStatus.ERROR
    assert invalid.errors[0].startswith("aiqumapi.general: Invalid AIQUM API configuration")

    missing = _by_subject(check_settings(_config(tmp_path / "d", inv)))["aiqumapi.general"]
    assert missing.status is CheckStatus.ERROR
    assert missing.label == "AIQUM API: Not configured"
    assert missing.errors == (
        "aiqumapi.general: aiqumapi.toml has no [general] section, "
        "required by the [aiqums] inventory",
    )
    assert missing.hint is not None
    assert "<config>/apis/aiqum/aiqumapi.toml" in missing.hint


def test_aiqums_missing_ip_and_invalid_field(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        {
            "inv.toml": DATA
            + '[aiqums.aiq1]\nip = "192.0.2.5"\n\n[aiqums.aiq2]\ndiv = "d"\n\n'
            + "[aiqums.aiq3]\nip = 5\n",
        },
    )

    rows = _by_subject(check_aiqums(config))

    assert rows["aiqums.aiq1"].status is CheckStatus.OK
    assert rows["aiqums.aiq2"].errors == ("aiqums.aiq2.ip: ip is required",)
    assert rows["aiqums.aiq3"].status is CheckStatus.ERROR
    assert rows["aiqums.aiq3"].errors[0].startswith("aiqums.aiq3.ip:")


def test_aiqum_credentials_entry_default_none_and_decrypt_failure(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        {
            "inv.toml": DATA
            + '[aiqums.aiq1]\nip = "192.0.2.5"\nuser = "own"\nenc = "own-pw"\n\n'
            + '[aiqums.aiq2]\nip = "192.0.2.6"\n',
        },
    )
    rows = _by_subject(check_aiqum_credentials(config))
    assert rows["aiqums.aiq1.credentials"].label == "aiq1: own"
    assert rows["aiqums.aiq2.credentials"].status is CheckStatus.ERROR
    assert rows["aiqums.aiq2.credentials"].errors == ("AIQUM 'aiq2' has no credentials configured",)
    assert rows["aiqums.aiq2.credentials"].hint == (
        "Set them with: nf config set-credential --type aiqums --name aiq2 --user USER"
    )

    with_default = _config(
        tmp_path / "d",
        {
            "inv.toml": DATA + '[aiqums.aiq2]\nip = "192.0.2.6"\n',
            "users.toml": '[aiqums]\nuser = "default-user"\nenc = "default-pw"\n',
        },
    )
    assert check_aiqum_credentials(with_default)[0].label == "aiq2: default-user"

    encrypted = _config(
        tmp_path / "e",
        {"inv.toml": DATA + f'[aiqums.aiq1]\nip = "192.0.2.5"\nuser = "u"\nenc = "{CIPHERTEXT}"\n'},
    )
    with patch(DECRYPT, side_effect=SOPSError(f"failed on {CIPHERTEXT}")):
        failed = check_aiqum_credentials(encrypted)
    assert failed[0].status is CheckStatus.ERROR
    assert CIPHERTEXT not in _everything(failed)
    assert "placeholder-ciphertext" not in _everything(failed)


# --- connectors, Cloud Insights ---


def test_connectors_valid_and_invalid(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        {"inv.toml": DATA + '[connectors.con1]\nip = "192.0.2.7"\n\n[connectors.con2]\nip = 5\n'},
    )

    rows = _by_subject(check_connectors(config))

    assert rows["connectors.con1"].status is CheckStatus.OK
    assert rows["connectors.con2"].status is CheckStatus.ERROR
    assert rows["connectors.con2"].errors[0].startswith("connectors.con2.ip:")


def test_cloudinsights_valid_and_invalid(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        {
            "inv.toml": DATA + '[cloudinsights.t1]\nbase_url = "https://t1.example.invalid"\n'
            "\n[cloudinsights.t2]\nip = 5\n"
        },
    )

    rows = _by_subject(check_cloudinsights(config))

    assert rows["cloudinsights.t1"].status is CheckStatus.OK
    assert rows["cloudinsights.t2"].status is CheckStatus.ERROR


def test_cloudinsights_credentials_tenant_token_general_token_and_none(tmp_path: Path) -> None:
    url = 'base_url = "https://t1.example.invalid"\n'
    tenant = _config(
        tmp_path / "a", {"inv.toml": DATA + f'[cloudinsights.t1]\n{url}enc = "{PLAIN}"\n'}
    )
    result = check_cloudinsights_credentials(tenant)
    assert result[0].status is CheckStatus.OK
    assert PLAIN not in _everything(result)

    general = _config(
        tmp_path / "b",
        {
            "inv.toml": DATA + f"[cloudinsights.t1]\n{url}",
            "diiapi.toml": f'[general]\napi_ro_token = "{PLAIN}"\n',
        },
    )
    result = check_cloudinsights_credentials(general)
    assert result[0].status is CheckStatus.OK
    assert PLAIN not in _everything(result)

    none = _config(tmp_path / "c", {"inv.toml": DATA + f"[cloudinsights.t1]\n{url}"})
    result = check_cloudinsights_credentials(none)
    assert result[0].status is CheckStatus.ERROR
    assert result[0].errors == ("Cloud Insights 't1' has no API token or base_url configured",)
    assert result[0].hint is not None
    assert "--type cloudinsights --name t1 --user token" in result[0].hint


def test_cloudinsights_credentials_decrypt_failure_leaks_nothing(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        {
            "inv.toml": DATA + '[cloudinsights.t1]\nbase_url = "https://t1.example.invalid"\n'
            f'enc = "{CIPHERTEXT}"\n'
        },
    )

    with patch(DECRYPT, side_effect=SOPSError(f"failed on {CIPHERTEXT} {PLAIN}")):
        result = check_cloudinsights_credentials(config)

    assert result[0].status is CheckStatus.ERROR
    assert "placeholder-ciphertext" not in _everything(result)
    assert PLAIN not in _everything(result)


# --- spec files ---


def _spec_rows(config: Config) -> dict[str, CheckResult]:
    return _by_subject(check_spec_files(config))


def test_spec_present_gives_ok_and_missing_gives_warning_with_source(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        {
            "ontapapi.toml": "[general]\n",
            "aiqumapi.toml": "[general]\n",
            "apis/ontap/all.json": "{}",
        },
    )

    rows = _spec_rows(config)

    assert rows["spec.ontap"] == CheckResult("spec.ontap", CheckStatus.OK, "ONTAP spec")
    missing = rows["spec.aiqum"]
    assert missing.status is CheckStatus.WARNING
    assert missing.label == f"AIQUM spec: missing {config.config_dir / 'apis/aiqum/all.json'}"
    assert missing.hint is not None
    assert "docs/example-config/apis/aiqum/all.json" in missing.hint
    assert "docs/getting-started/configuration.md (Spec files)" in missing.hint
    assert "--scope" not in missing.hint
    assert not missing.errors


def test_spec_unconfigured_apis_have_no_row_and_occm_never_does(tmp_path: Path) -> None:
    assert check_spec_files(_config(tmp_path, {})) == []

    config = _config(tmp_path / "o", {"ontapapi.toml": "[general]\n"})
    assert set(_spec_rows(config)) == {"spec.ontap"}


def test_spec_dii_configured_by_a_tenant_alone(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        {"inv.toml": DATA + '[cloudinsights.t1]\nbase_url = "https://t1.example.invalid"\n'},
    )

    rows = _spec_rows(config)

    assert set(rows) == {"spec.dii"}
    assert rows["spec.dii"].label.startswith("DII spec: missing")


def test_spec_console_configured_by_a_scope_only_account(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        {
            "Org1/scope.toml": "",
            "Org1/consoleapi.toml": '[general]\nbase_url = "https://api.example.invalid"\n',
        },
    )

    rows = _spec_rows(config)

    assert set(rows) == {"spec.console"}
    assert "console_openapi.yaml" in rows["spec.console"].label


def test_spec_check_does_not_decrypt(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        {"diiapi.toml": f'[general]\napi_ro_token = "{CIPHERTEXT}"\n'},
    )

    with patch(DECRYPT) as decrypt:
        check_spec_files(config)

    decrypt.assert_not_called()


# --- run_static_checks ---


def test_root_sections_always_present_and_in_order(tmp_path: Path) -> None:
    sections = run_static_checks(_config(tmp_path, {}))

    assert [s.title for s in sections] == [
        "Clusters",
        "Users",
        "Settings",
        "Cluster Credentials",
    ]
    assert sections[3].results == ()


def test_all_sections_in_display_order(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        {
            "inv.toml": DATA
            + '[aiqums.aiq1]\nip = "192.0.2.5"\nuser = "u"\nenc = "p"\n\n'
            + '[connectors.con1]\nip = "192.0.2.7"\n\n'
            + '[cloudinsights.t1]\nbase_url = "https://t1.example.invalid"\nenc = "tok"\n',
            "aiqumapi.toml": "[general]\n",
        },
    )

    titles = [s.title for s in run_static_checks(config)]

    assert titles == [
        "Clusters",
        "Users",
        "Settings",
        "Cluster Credentials",
        "AIQUM",
        "AIQUM Credentials",
        "Connectors",
        "Cloud Insights",
        "Cloud Insights Credentials",
        "Spec Files",
    ]


def test_scope_mode_has_no_spec_files_and_filters_inventory(tmp_path: Path) -> None:
    config = _config(
        tmp_path,
        {
            "ontapapi.toml": "[general]\n",
            "inv.toml": DATA + '[aiqums.root-aiq]\nip = "192.0.2.5"\n',
            "Org1/scope.toml": "",
            "Org1/inv.toml": DATA + '[aiqums.org-aiq]\nip = "192.0.2.6"\n',
        },
    )

    sections = {s.title: s for s in run_static_checks(config, "Org1")}

    assert "Spec Files" not in sections
    assert "Scope settings (Org1)" in sections
    assert [r.subject for r in sections["AIQUM"].results] == ["aiqums.org-aiq"]
    assert [r.subject for r in sections["AIQUM Credentials"].results] == [
        "aiqums.org-aiq.credentials"
    ]
