"""Tests for the checks ``nf config validate`` runs (#1111)."""

from __future__ import annotations

import importlib
import io
import re
from pathlib import Path

import pytest
from click.testing import CliRunner
from rich.console import Console

from pynetappfoundry.cli.main import nf

VALIDATE_MODULE = "pynetappfoundry.cli.commands.config.validate"

# Captured with the pre-#1111 validate.py (Console width 300, tmp dir shown as <TMP>).
GOLDEN_VALID_ROOT_CODE = 0
GOLDEN_VALID_ROOT = (
    "\n"
    "Validating configuration in: <TMP>/cfg\n"
    "\n"
    "Configuration Validation\n"
    "├── Clusters\n"
    "│   ├── root-cl\n"
    "│   └── org1-cl\n"
    "├── Users\n"
    "│   └── clusters\n"
    "├── Settings\n"
    "│   ├── ONTAP API: Not configured\n"
    "│   ├── DII API: Not configured (optional)\n"
    "│   ├── Digital Advisor API: Not configured (optional)\n"
    "│   ├── SMTP: Not configured (optional)\n"
    "│   ├── Console: Not configured (optional)\n"
    "│   └── Licensing: Not configured (optional)\n"
    "└── Cluster Credentials\n"
    "    ├── root-cl: root-user\n"
    "    └── org1-cl: own\n"
    "\n"
    "Configuration is valid\n"
    ""
)
GOLDEN_VALID_SCOPE_CODE = 0
GOLDEN_VALID_SCOPE = (
    "\n"
    "Validating configuration in: <TMP>/cfg\n"
    "\n"
    "Configuration Validation\n"
    "├── Clusters\n"
    "│   └── org1-cl\n"
    "├── Users\n"
    "│   └── clusters\n"
    "├── Scope settings (Org1)\n"
    "│   ├── Monitoring: Not configured (optional)\n"
    "│   └── Console: Not configured (optional)\n"
    "└── Cluster Credentials\n"
    "    └── org1-cl: own\n"
    "\n"
    "Configuration is valid\n"
    ""
)
GOLDEN_INVALID_ROOT_CODE = 1
GOLDEN_INVALID_ROOT = (
    "\n"
    "Validating configuration in: <TMP>/cfg\n"
    "\n"
    "Configuration Validation\n"
    "├── Clusters\n"
    "│   ├── root-cl\n"
    "│   └── nocred\n"
    "├── Users\n"
    "│   ├── console\n"
    "│   └── bad: Invalid\n"
    "├── Settings\n"
    "│   ├── ONTAP API: Not configured\n"
    "│   ├── DII API: Not configured (optional)\n"
    "│   ├── Digital Advisor API: Not configured (optional)\n"
    "│   ├── SMTP: Invalid\n"
    "│   ├── Console: Not configured (optional)\n"
    "│   └── Licensing: Not configured (optional)\n"
    "└── Cluster Credentials\n"
    "    ├── root-cl: own\n"
    "    └── nocred: Missing credentials\n"
    "\n"
    "╭─ Validation Errors ─╮\n"
    "│ - users.bad.user: Input should be a valid string │\n"
    "│ - users.bad.enc: Field required │\n"
    "│ - settings.SMTP: Invalid SMTP configuration: 1 validation error for SMTPSettings │\n"
    "│ port │\n"
    "│   Input should be a valid integer, unable to parse string as an integer [type=int_parsing] │\n"  # noqa: E501  # verbatim golden output line
    "│     For further information visit https://errors.pydantic.dev/X/v/int_parsing. Ensure settings.toml has a valid [settings.SMTP] section with 'server', 'port', 'user', 'password', and 'auth' fields. │\n"  # noqa: E501  # verbatim golden output line
    "│ - Cluster 'nocred' has no credentials configured │\n"
    "╰─╯\n"
    "\n"
    "Validation failed with 4 error(s)\n"
    ""
)


VALID_FILES = {
    "root.toml": '[settings]\ntype = "data"\n\n[clusters.root-cl]\nip = "192.0.2.1"\n',
    "users.toml": '[clusters]\nuser = "root-user"\nenc = "placeholder-enc-root"\n',
    "Org1/scope.toml": 'description = "Org one scope"\n',
    "Org1/inv.toml": (
        '[settings]\ntype = "data"\n\n[clusters.org1-cl]\nip = "192.0.2.2"\n'
        'user = "own"\nenc = "own-pw"\n'
    ),
    "Org1/users.toml": '[clusters]\nuser = "org1-user"\nenc = "placeholder-enc-org1"\n',
}
INVALID_FILES = {
    "root.toml": (
        '[settings]\ntype = "data"\n\n[clusters.root-cl]\nip = "192.0.2.1"\n'
        'user = "own"\nenc = "own-pw"\n\n[clusters.nocred]\nip = "192.0.2.9"\n'
    ),
    "users.toml": (
        '[console]\nuser = "con-user"\nenc = "placeholder-enc-con"\n\n[bad]\nuser = 5\n'
    ),
    "settings.toml": (
        '[SMTP]\nserver = "smtp.example.invalid"\nuser = "mailer"\nport = "not-a-port"\n'
    ),
}
ONTAP_FILES = {
    "root.toml": VALID_FILES["root.toml"],
    "users.toml": VALID_FILES["users.toml"],
    "ontapapi.toml": '[general]\nbase_api_path = "/api"\n',
}
TOKEN = "placeholder-api-token-value"


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    for name in ("AIQ1", "AIQ2", "TENANT1", "ROOT_CL", "NOCRED", "ORG1_CL"):
        monkeypatch.delenv(f"NF_{name}_USER", raising=False)
        monkeypatch.delenv(f"NF_{name}_PASSWORD", raising=False)


def _config_dir(tmp_path: Path, files: dict[str, str]) -> Path:
    config_dir = tmp_path / "cfg"
    for rel, content in files.items():
        path = config_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return config_dir


def _run(config_dir: Path, *args: str) -> tuple[int, str]:
    result = CliRunner().invoke(nf, ["--config-dir", str(config_dir), "config", "validate", *args])
    return result.exit_code, " ".join(result.output.split())


def _run_wide(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, files: dict[str, str], *args: str
) -> tuple[int, str]:
    """Run validate with a 300-column, colourless console; return the raw text."""
    config_dir = _config_dir(tmp_path, files)
    buffer = io.StringIO()
    # legacy_windows=False: on Windows Rich swaps the panel's rounded box for a square one.
    con = Console(width=300, color_system=None, file=buffer, legacy_windows=False)
    monkeypatch.setattr(importlib.import_module(VALIDATE_MODULE), "console", con)
    result = CliRunner().invoke(nf, ["--config-dir", str(config_dir), "config", "validate", *args])
    # The config dir is printed with the OS separator; normalise it so the goldens hold on Windows.
    text = (
        (buffer.getvalue() + result.output)
        .replace(str(config_dir), "<TMP>/" + config_dir.name)
        .replace(str(tmp_path), "<TMP>")
    )
    return result.exit_code, text


def _squeeze(text: str) -> str:
    """Collapse the padding of the error panel, which only depends on the console width."""
    text = re.sub(r" {20,}", " ", text)
    text = re.sub(r"─{20,}", "─", text)
    return re.sub(r"errors\.pydantic\.dev/\d+\.\d+", "errors.pydantic.dev/X", text)


# --- golden output (captured before the checks moved to core.config_checks) ---


def test_golden_valid_root_is_byte_identical(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    code, text = _run_wide(monkeypatch, tmp_path, VALID_FILES)

    assert code == GOLDEN_VALID_ROOT_CODE
    assert text == GOLDEN_VALID_ROOT


def test_golden_valid_scope_is_byte_identical(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    code, text = _run_wide(monkeypatch, tmp_path, VALID_FILES, "--scope", "Org1")

    assert code == GOLDEN_VALID_SCOPE_CODE
    assert text == GOLDEN_VALID_SCOPE


def test_golden_invalid_root_only_gains_hint_lines(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    code, text = _run_wide(monkeypatch, tmp_path, INVALID_FILES)

    assert code == GOLDEN_INVALID_ROOT_CODE
    original = GOLDEN_INVALID_ROOT.splitlines()
    added: list[str] = []
    position = 0
    for line in _squeeze(text).splitlines():
        if position < len(original) and line == original[position]:
            position += 1
        else:
            added.append(line)
    assert position == len(original), "an original line is missing or out of order"
    assert added, "no hint line was added"
    markers = (
        "Fix [bad] in users.toml",
        "See docs/reference/config-schema.md (settings.SMTP)",
        "Set them with: nf config set-credential --cluster nocred --user USER",
    )
    for line in added:
        assert any(marker in line for marker in markers), line
    assert all("--scope" not in line for line in added)


# --- spec files ---


def test_missing_spec_is_a_warning_and_exits_0(tmp_path: Path) -> None:
    code, out = _run(_config_dir(tmp_path, ONTAP_FILES))

    assert code == 0, out
    assert "Spec Files" in out
    assert "ONTAP spec: missing" in out
    assert "docs/example-config/apis/ontap/all.json" in out
    assert "Configuration is valid" in out
    assert "--scope" not in out


def test_present_spec_is_an_ok_row(tmp_path: Path) -> None:
    files = {**ONTAP_FILES, "apis/ontap/all.json": "{}"}
    code, out = _run(_config_dir(tmp_path, files))

    assert code == 0, out
    assert "ONTAP spec" in out
    assert "missing" not in out


def test_no_api_and_no_inventory_adds_no_new_section(tmp_path: Path) -> None:
    code, out = _run(_config_dir(tmp_path, VALID_FILES))

    assert code == 0, out
    for title in (
        "AIQUM",
        "Connectors",
        "Cloud Insights",
        "Spec Files",
    ):
        assert title not in out


def test_console_spec_warning_in_root_mode_not_with_scope(tmp_path: Path) -> None:
    files = {
        **VALID_FILES,
        "consoleapi.toml": '[general]\nbase_url = "https://api.example.invalid"\n'
        'service_token = "placeholder-service-token"\norg_id = "org-1"\n',
    }
    config_dir = _config_dir(tmp_path, files)

    code, out = _run(config_dir)
    assert code == 0, out
    assert "Console spec: missing" in out

    code, out = _run(config_dir, "--scope", "Org1")
    assert code == 0, out
    assert "Spec Files" not in out
    assert "Console spec" not in out


# --- AIQUM, connectors, Cloud Insights ---


def test_aiqum_without_credentials_exits_1_with_hint(tmp_path: Path) -> None:
    files = {
        "inv.toml": '[settings]\ntype = "data"\n\n[aiqums.aiq1]\nip = "192.0.2.5"\n',
        "aiqumapi.toml": "[general]\ntimeout = 10\n",
    }
    code, out = _run(_config_dir(tmp_path, files))

    assert code == 1
    assert "AIQUM Credentials" in out
    assert "AIQUM 'aiq1' has no credentials configured" in out
    assert "nf config set-credential --type aiqums --name aiq1 --user USER" in out
    assert "--scope" not in out


def test_aiqum_inventory_without_settings_exits_1(tmp_path: Path) -> None:
    files = {
        "inv.toml": '[settings]\ntype = "data"\n\n[aiqums.aiq1]\nip = "192.0.2.5"\n',
        "users.toml": '[aiqums]\nuser = "aiq-user"\nenc = "placeholder-enc"\n',
    }
    code, out = _run(_config_dir(tmp_path, files))

    assert code == 1
    assert "AIQUM API: Not configured" in out
    assert "aiqumapi.general: aiqumapi.toml has no [general] section" in out


def test_valid_aiqum_passes(tmp_path: Path) -> None:
    files = {
        "inv.toml": '[settings]\ntype = "data"\n\n[aiqums.aiq1]\nip = "192.0.2.5"\n',
        "aiqumapi.toml": "[general]\ntimeout = 10\n",
        "users.toml": '[aiqums]\nuser = "aiq-user"\nenc = "placeholder-enc"\n',
        "apis/aiqum/all.json": "{}",
    }
    code, out = _run(_config_dir(tmp_path, files))

    assert code == 0, out
    assert "aiq1: aiq-user" in out
    assert "AIQUM spec" in out
    assert "placeholder-enc" not in out


def test_invalid_connector_exits_1(tmp_path: Path) -> None:
    files = {
        "inv.toml": '[settings]\ntype = "data"\n\n[connectors.con1]\nip = 5\n',
    }
    code, out = _run(_config_dir(tmp_path, files))

    assert code == 1
    assert "Connectors" in out
    assert "con1: Invalid" in out
    assert "connectors.con1.ip:" in out


def test_tenant_without_token_exits_1_and_never_prints_a_token(tmp_path: Path) -> None:
    files = {
        "inv.toml": (
            '[settings]\ntype = "data"\n\n[cloudinsights.tenant1]\n'
            'base_url = "https://tenant1.example.invalid"\n'
        ),
    }
    code, out = _run(_config_dir(tmp_path, files))

    assert code == 1
    assert "Cloud Insights Credentials" in out
    assert "Cloud Insights 'tenant1' has no API token or base_url configured" in out
    assert "nf config set-credential --type cloudinsights --name tenant1 --user token" in out


def test_tenant_token_is_never_printed(tmp_path: Path) -> None:
    files = {
        "inv.toml": (
            '[settings]\ntype = "data"\n\n[cloudinsights.tenant1]\n'
            f'base_url = "https://tenant1.example.invalid"\nenc = "{TOKEN}"\n'
        ),
    }
    code, out = _run(_config_dir(tmp_path, files))

    assert code == 0, out
    assert "tenant1: API token" in out
    assert TOKEN not in out
    assert "DII spec: missing" in out


def test_warning_hints_do_not_reach_the_error_hints(tmp_path: Path) -> None:
    files = {
        **ONTAP_FILES,
        "inv2.toml": '[settings]\ntype = "data"\n\n[aiqums.aiq1]\nip = "192.0.2.5"\n',
        "aiqumapi.toml": "[general]\ntimeout = 10\n",
    }
    result = CliRunner().invoke(
        nf, ["--config-dir", str(_config_dir(tmp_path, files)), "config", "validate"]
    )

    tail = result.output.split("Validation failed with")[1]
    assert result.exit_code == 1
    assert "nf config set-credential --type aiqums --name aiq1" in tail
    assert "nf config download-spec" not in tail
