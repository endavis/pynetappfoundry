"""Tests for ``nf config encrypt-value`` (#1025)."""

from __future__ import annotations

from unittest.mock import patch

from click.testing import CliRunner

from pynetappfoundry.cli.main import nf

MODULE = "pynetappfoundry.cli.commands.config.credentials"
PLAIN = "placeholder-plain-value"
ENCRYPTED = "SOPS[placeholder-ciphertext]"


def _invoke(*args: str) -> tuple[int, str, str]:
    runner = CliRunner()
    result = runner.invoke(
        nf,
        ["config", "encrypt-value", *args],
        input=f"{PLAIN}\n{PLAIN}\n",
        env={"NF_CONFIG_DIR": ""},
    )
    return result.exit_code, result.stdout, result.stderr


def test_prints_only_the_sops_value_on_stdout() -> None:
    with (
        patch(f"{MODULE}.is_sops_installed", return_value=True),
        patch(f"{MODULE}.get_age_key_path") as key_path,
        patch(f"{MODULE}.get_public_key_from_file", return_value="age1placeholderkey"),
        patch(f"{MODULE}.encrypt_value", return_value=ENCRYPTED) as encrypt,
    ):
        key_path.return_value.exists.return_value = True
        code, stdout, stderr = _invoke()

    assert code == 0, stderr
    encrypt.assert_called_once_with(PLAIN, "age1placeholderkey")
    assert stdout.strip().splitlines()[-1] == ENCRYPTED
    assert PLAIN not in stdout
    assert PLAIN not in stderr


def test_value_option_skips_prompt() -> None:
    with (
        patch(f"{MODULE}.is_sops_installed", return_value=True),
        patch(f"{MODULE}.get_age_key_path") as key_path,
        patch(f"{MODULE}.get_public_key_from_file", return_value="age1placeholderkey"),
        patch(f"{MODULE}.encrypt_value", return_value=ENCRYPTED) as encrypt,
    ):
        key_path.return_value.exists.return_value = True
        result = CliRunner().invoke(
            nf, ["config", "encrypt-value", "--value", PLAIN], env={"NF_CONFIG_DIR": ""}
        )

    assert result.exit_code == 0
    encrypt.assert_called_once_with(PLAIN, "age1placeholderkey")


def test_missing_age_key_hints_init_sops() -> None:
    with (
        patch(f"{MODULE}.is_sops_installed", return_value=True),
        patch(f"{MODULE}.get_age_key_path") as key_path,
        patch(f"{MODULE}.encrypt_value") as encrypt,
    ):
        key_path.return_value.exists.return_value = False
        code, stdout, stderr = _invoke()

    assert code != 0
    encrypt.assert_not_called()
    assert "init-sops" in stdout + stderr
    assert PLAIN not in stdout + stderr


def test_sops_not_installed_fails_without_plaintext() -> None:
    with (
        patch(f"{MODULE}.is_sops_installed", return_value=False),
        patch(f"{MODULE}.encrypt_value") as encrypt,
    ):
        code, stdout, stderr = _invoke()

    assert code != 0
    encrypt.assert_not_called()
    assert PLAIN not in stdout + stderr
