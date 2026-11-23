"""Tests for SOPS encryption utilities."""

from __future__ import annotations

import logging
import stat
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from pynetappfoundry.utils.sops import (
    SOPS_PREFIX,
    SOPS_SUFFIX,
    AgeNotInstalledError,
    SOPSError,
    SOPSNotInstalledError,
    create_sops_config,
    generate_age_keypair,
    get_age_key_path,
    get_public_key_from_file,
    is_age_installed,
    is_encrypted,
    is_sops_installed,
)


class TestIsSOPSInstalled:
    """Tests for is_sops_installed."""

    def test_returns_true_when_installed(self) -> None:
        """Test returns True when sops is in PATH."""
        with patch("shutil.which", return_value="/usr/bin/sops"):
            assert is_sops_installed() is True

    def test_returns_false_when_not_installed(self) -> None:
        """Test returns False when sops is not in PATH."""
        with patch("shutil.which", return_value=None):
            assert is_sops_installed() is False


class TestIsAgeInstalled:
    """Tests for is_age_installed."""

    def test_returns_true_when_both_installed(self) -> None:
        """Test returns True when both age and age-keygen are in PATH."""
        with patch("shutil.which", side_effect=lambda x: f"/usr/bin/{x}"):
            assert is_age_installed() is True

    def test_returns_false_when_age_missing(self) -> None:
        """Test returns False when age is not in PATH."""
        with patch("shutil.which", side_effect=lambda x: None if x == "age" else f"/usr/bin/{x}"):
            assert is_age_installed() is False

    def test_returns_false_when_keygen_missing(self) -> None:
        """Test returns False when age-keygen is not in PATH."""
        with patch(
            "shutil.which",
            side_effect=lambda x: None if x == "age-keygen" else f"/usr/bin/{x}",
        ):
            assert is_age_installed() is False


class TestGetAgeKeyPath:
    """Tests for get_age_key_path."""

    def test_uses_env_var_when_set(self) -> None:
        """Test uses SOPS_AGE_KEY_FILE env var when set."""
        with patch.dict("os.environ", {"SOPS_AGE_KEY_FILE": "/custom/path/key.txt"}):
            result = get_age_key_path()
            assert result == Path("/custom/path/key.txt")

    def test_uses_default_when_no_env_var(self) -> None:
        """Test uses default path when env var not set."""
        # Only remove SOPS_AGE_KEY_FILE, keep other env vars (HOME, USERPROFILE, etc.)
        with patch.dict("os.environ", {"SOPS_AGE_KEY_FILE": ""}, clear=False):
            # Temporarily remove the key if it exists
            import os

            orig = os.environ.pop("SOPS_AGE_KEY_FILE", None)
            try:
                result = get_age_key_path()
                assert result.name == "keys.txt"
                assert "age" in str(result)
            finally:
                if orig is not None:
                    os.environ["SOPS_AGE_KEY_FILE"] = orig


class TestIsEncrypted:
    """Tests for is_encrypted."""

    def test_encrypted_value(self) -> None:
        """Test detects encrypted value."""
        encrypted = f"{SOPS_PREFIX}base64encodeddata{SOPS_SUFFIX}"
        assert is_encrypted(encrypted) is True

    def test_plain_value(self) -> None:
        """Test detects plain value."""
        assert is_encrypted("plaintext") is False

    def test_partial_prefix(self) -> None:
        """Test partial prefix not detected."""
        assert is_encrypted("SOPS[abc") is False

    def test_empty_string(self) -> None:
        """Test empty string not detected."""
        assert is_encrypted("") is False


class TestGetPublicKeyFromFile:
    """Tests for get_public_key_from_file."""

    def test_extracts_public_key(self, tmp_path: Path) -> None:
        """Test extracts public key from file."""
        key_file = tmp_path / "keys.txt"
        key_file.write_text(
            "# created: 2024-01-01T00:00:00Z\n"
            "# public key: age1abc123def456\n"
            "AGE-SECRET-KEY-1ABCDEF\n"
        )
        result = get_public_key_from_file(key_file)
        assert result == "age1abc123def456"

    def test_raises_when_file_missing(self, tmp_path: Path) -> None:
        """Test raises when file doesn't exist."""
        key_file = tmp_path / "missing.txt"
        with pytest.raises(SOPSError, match="not found"):
            get_public_key_from_file(key_file)

    def test_raises_when_no_public_key(self, tmp_path: Path) -> None:
        """Test raises when no public key in file."""
        key_file = tmp_path / "keys.txt"
        key_file.write_text("AGE-SECRET-KEY-1ABCDEF\n")
        with pytest.raises(SOPSError, match="Could not find public key"):
            get_public_key_from_file(key_file)


class TestEncryptValue:
    """Tests for encrypt_value."""

    def test_raises_when_sops_not_installed(self) -> None:
        """Test raises SOPSNotInstalledError when sops not available."""
        with patch("pynetappfoundry.utils.sops.is_sops_installed", return_value=False):
            from pynetappfoundry.utils.sops import encrypt_value

            with pytest.raises(SOPSNotInstalledError):
                encrypt_value("secret", "age1abc")


class TestDecryptValue:
    """Tests for decrypt_value."""

    def test_raises_when_sops_not_installed(self) -> None:
        """Test raises SOPSNotInstalledError when sops not available."""
        with patch("pynetappfoundry.utils.sops.is_sops_installed", return_value=False):
            from pynetappfoundry.utils.sops import decrypt_value

            with pytest.raises(SOPSNotInstalledError):
                decrypt_value("SOPS[base64data]")


class TestGenerateAgeKeypair:
    """Tests for generate_age_keypair with subprocess and shutil mocked.

    These run on every OS without age installed; the real round-trip is
    covered by TestSOPSIntegration.
    """

    PUBKEY = "age1abcdefghijklmnopqrstuvwxyz0123456789"

    @staticmethod
    def _completed(stderr: str) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=["age-keygen"], returncode=0, stdout="", stderr=stderr
        )

    def test_raises_when_age_not_installed(self, tmp_path: Path) -> None:
        """Raises AgeNotInstalledError and never runs age-keygen."""
        with (
            patch("pynetappfoundry.utils.sops.shutil.which", return_value=None),
            patch("pynetappfoundry.utils.sops.subprocess.run") as run,
            pytest.raises(AgeNotInstalledError) as exc,
        ):
            generate_age_keypair(tmp_path / "key.txt")
        assert str(exc.value) == (
            "age is not installed. Install it with: brew install age (macOS) "
            "or see https://github.com/FiloSottile/age#installation"
        )
        run.assert_not_called()

    def test_checks_both_age_binaries(self, tmp_path: Path) -> None:
        """Looks up both age and age-keygen before generating."""
        key_path = tmp_path / "key.txt"
        with (
            patch(
                "pynetappfoundry.utils.sops.shutil.which", side_effect=lambda x: f"/usr/bin/{x}"
            ) as which,
            patch(
                "pynetappfoundry.utils.sops.subprocess.run",
                return_value=self._completed(f"Public key: {self.PUBKEY}\n"),
            ),
        ):
            key_path.write_text("x", encoding="utf-8")
            generate_age_keypair(key_path)
        looked_up = [c.args[0] for c in which.call_args_list]
        assert "age" in looked_up
        assert "age-keygen" in looked_up

    def test_runs_age_keygen_with_expected_argv(self, tmp_path: Path) -> None:
        """Builds the exact argv and subprocess options."""
        key_path = tmp_path / "key.txt"
        key_path.write_text("x", encoding="utf-8")
        with (
            patch("pynetappfoundry.utils.sops.shutil.which", return_value="/usr/bin/x"),
            patch(
                "pynetappfoundry.utils.sops.subprocess.run",
                return_value=self._completed(f"Public key: {self.PUBKEY}\n"),
            ) as run,
        ):
            generate_age_keypair(key_path)
        run.assert_called_once()
        assert run.call_args.args[0] == ["age-keygen", "-o", str(key_path)]
        assert run.call_args.kwargs == {
            "capture_output": True,
            "text": True,
            "check": True,
        }

    def test_returns_public_key_from_stderr_and_path(self, tmp_path: Path) -> None:
        """Parses the public key from stderr and returns the key path string."""
        key_path = tmp_path / "key.txt"
        key_path.write_text("x", encoding="utf-8")
        stderr = f"some preamble\nPublic key: {self.PUBKEY}\ntrailing\n"
        with (
            patch("pynetappfoundry.utils.sops.shutil.which", return_value="/usr/bin/x"),
            patch(
                "pynetappfoundry.utils.sops.subprocess.run",
                return_value=self._completed(stderr),
            ),
        ):
            public_key, returned_path = generate_age_keypair(key_path)
        assert public_key == self.PUBKEY
        assert Path(returned_path) == key_path

    def test_stderr_key_wins_over_file_content(self, tmp_path: Path) -> None:
        """The stderr key is used without consulting the key file."""
        key_path = tmp_path / "key.txt"
        key_path.write_text("# public key: age1fromfile\n", encoding="utf-8")
        with (
            patch("pynetappfoundry.utils.sops.shutil.which", return_value="/usr/bin/x"),
            patch(
                "pynetappfoundry.utils.sops.subprocess.run",
                return_value=self._completed(f"Public key: {self.PUBKEY}\n"),
            ),
            patch("pynetappfoundry.utils.sops.get_public_key_from_file") as from_file,
        ):
            public_key, _ = generate_age_keypair(key_path)
        assert public_key == self.PUBKEY
        from_file.assert_not_called()

    def test_falls_back_to_key_file_when_stderr_has_no_key(self, tmp_path: Path) -> None:
        """Reads the public key from the key file when stderr lacks it."""
        key_path = tmp_path / "key.txt"
        key_path.write_text(
            f"# created: now\n# public key: {self.PUBKEY}\nAGE-SECRET-KEY-1XYZ\n",
            encoding="utf-8",
        )
        with (
            patch("pynetappfoundry.utils.sops.shutil.which", return_value="/usr/bin/x"),
            patch(
                "pynetappfoundry.utils.sops.subprocess.run",
                return_value=self._completed("nothing useful\n"),
            ),
        ):
            public_key, _ = generate_age_keypair(key_path)
        assert public_key == self.PUBKEY

    def test_fallback_raises_when_key_file_missing(self, tmp_path: Path) -> None:
        """Raises SOPSError when neither stderr nor the key file has the key."""
        key_path = tmp_path / "key.txt"
        with (
            patch("pynetappfoundry.utils.sops.shutil.which", return_value="/usr/bin/x"),
            patch(
                "pynetappfoundry.utils.sops.subprocess.run",
                return_value=self._completed(""),
            ),
            pytest.raises(SOPSError, match="not found"),
        ):
            generate_age_keypair(key_path)

    def test_wraps_called_process_error(self, tmp_path: Path) -> None:
        """A failing age-keygen becomes SOPSError carrying its stderr."""
        err = subprocess.CalledProcessError(1, ["age-keygen"], stderr="boom: no such dir")
        with (
            patch("pynetappfoundry.utils.sops.shutil.which", return_value="/usr/bin/x"),
            patch("pynetappfoundry.utils.sops.subprocess.run", side_effect=err),
            pytest.raises(
                SOPSError, match="Failed to generate age keypair: boom: no such dir"
            ) as exc,
        ):
            generate_age_keypair(tmp_path / "key.txt")
        assert exc.value.__cause__ is err

    def test_creates_missing_parent_directories(self, tmp_path: Path) -> None:
        """Creates the key file's parent directories before running age-keygen."""
        key_path = tmp_path / "a" / "b" / "key.txt"
        parent_existed: list[bool] = []

        def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
            parent_existed.append(key_path.parent.is_dir())
            key_path.write_text("x", encoding="utf-8")
            return self._completed(f"Public key: {self.PUBKEY}\n")

        with (
            patch("pynetappfoundry.utils.sops.shutil.which", return_value="/usr/bin/x"),
            patch("pynetappfoundry.utils.sops.subprocess.run", side_effect=fake_run),
        ):
            generate_age_keypair(key_path)
        assert parent_existed == [True]

    def test_existing_parent_directory_is_fine(self, tmp_path: Path) -> None:
        """An existing parent directory does not raise."""
        key_path = tmp_path / "key.txt"
        key_path.write_text("x", encoding="utf-8")
        with (
            patch("pynetappfoundry.utils.sops.shutil.which", return_value="/usr/bin/x"),
            patch(
                "pynetappfoundry.utils.sops.subprocess.run",
                return_value=self._completed(f"Public key: {self.PUBKEY}\n"),
            ),
        ):
            generate_age_keypair(key_path)

    def test_default_key_path_from_env(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """With no key_path, uses get_age_key_path (SOPS_AGE_KEY_FILE)."""
        key_path = tmp_path / "sub" / "env-key.txt"
        monkeypatch.setenv("SOPS_AGE_KEY_FILE", str(key_path))

        def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
            key_path.write_text("x", encoding="utf-8")
            return self._completed(f"Public key: {self.PUBKEY}\n")

        with (
            patch("pynetappfoundry.utils.sops.shutil.which", return_value="/usr/bin/x"),
            patch("pynetappfoundry.utils.sops.subprocess.run", side_effect=fake_run) as run,
        ):
            _, returned_path = generate_age_keypair()
        assert Path(returned_path) == key_path
        assert run.call_args.args[0] == ["age-keygen", "-o", str(key_path)]

    @pytest.mark.skipif(
        sys.platform == "win32", reason="POSIX file mode bits are not enforced on Windows"
    )
    def test_sets_restrictive_permissions(self, tmp_path: Path) -> None:
        """The key file ends up with mode 0o600."""
        key_path = tmp_path / "key.txt"
        key_path.write_text("x", encoding="utf-8")
        key_path.chmod(0o644)
        with (
            patch("pynetappfoundry.utils.sops.shutil.which", return_value="/usr/bin/x"),
            patch(
                "pynetappfoundry.utils.sops.subprocess.run",
                return_value=self._completed(f"Public key: {self.PUBKEY}\n"),
            ),
        ):
            generate_age_keypair(key_path)
        assert stat.S_IMODE(key_path.stat().st_mode) == 0o600

    def test_logs_generated_path(self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        """Logs an info message naming the key path."""
        key_path = tmp_path / "key.txt"
        key_path.write_text("x", encoding="utf-8")
        with (
            patch("pynetappfoundry.utils.sops.shutil.which", return_value="/usr/bin/x"),
            patch(
                "pynetappfoundry.utils.sops.subprocess.run",
                return_value=self._completed(f"Public key: {self.PUBKEY}\n"),
            ),
            caplog.at_level(logging.INFO, logger="pynetappfoundry.utils.sops"),
        ):
            generate_age_keypair(key_path)
        assert f"Generated age keypair at {key_path}" in caplog.messages


class TestCreateSopsConfig:
    """Tests for create_sops_config."""

    def test_writes_rule_with_defaults(self, tmp_path: Path) -> None:
        """Default path_regex targets .toml files."""
        config_path = tmp_path / ".sops.yaml"
        create_sops_config(config_path, ["age1aaa"])
        data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        assert data == {"creation_rules": [{"path_regex": r".*\.toml$", "age": "age1aaa"}]}

    def test_joins_multiple_keys_with_comma(self, tmp_path: Path) -> None:
        """Multiple public keys are joined with a bare comma."""
        config_path = tmp_path / ".sops.yaml"
        create_sops_config(config_path, ["age1aaa", "age1bbb", "age1ccc"])
        data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        assert data["creation_rules"][0]["age"] == "age1aaa,age1bbb,age1ccc"

    def test_custom_path_regex(self, tmp_path: Path) -> None:
        """A custom path_regex is written verbatim."""
        config_path = tmp_path / ".sops.yaml"
        create_sops_config(config_path, ["age1aaa"], path_regex=r"secrets/.*\.yaml$")
        data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        assert data["creation_rules"][0]["path_regex"] == r"secrets/.*\.yaml$"

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        """Missing parent directories are created."""
        config_path = tmp_path / "x" / "y" / ".sops.yaml"
        create_sops_config(config_path, ["age1aaa"])
        assert config_path.is_file()

    def test_existing_parent_directory_is_fine(self, tmp_path: Path) -> None:
        """An existing parent directory does not raise."""
        config_path = tmp_path / ".sops.yaml"
        create_sops_config(config_path, ["age1aaa"])
        create_sops_config(config_path, ["age1bbb"])
        data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        assert data["creation_rules"][0]["age"] == "age1bbb"

    def test_opens_config_file_as_utf8(self, tmp_path: Path) -> None:
        """The config file is opened for writing with an explicit utf-8 encoding."""
        config_path = tmp_path / ".sops.yaml"
        with patch("pynetappfoundry.utils.sops.open", create=True, wraps=open) as spy:
            create_sops_config(config_path, ["age1aaa"])
        spy.assert_called_once_with(config_path, "w", encoding="utf-8")

    def test_uses_block_style_yaml(self, tmp_path: Path) -> None:
        """Output is block style, not flow style."""
        config_path = tmp_path / ".sops.yaml"
        create_sops_config(config_path, ["age1aaa"])
        text = config_path.read_text(encoding="utf-8")
        assert "{" not in text
        assert "[" not in text
        assert "creation_rules:" in text

    def test_logs_created_path(self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        """Logs an info message naming the config path."""
        config_path = tmp_path / ".sops.yaml"
        with caplog.at_level(logging.INFO, logger="pynetappfoundry.utils.sops"):
            create_sops_config(config_path, ["age1aaa"])
        assert f"Created SOPS config at {config_path}" in caplog.messages


class TestSOPSIntegration:
    """Integration tests for SOPS encryption/decryption.

    These tests require age and sops to be installed.
    """

    @pytest.fixture(scope="class")
    def age_keypair(self, tmp_path_factory: pytest.TempPathFactory) -> tuple[str, Path]:
        """Generate a temporary age keypair once per test class."""
        from pynetappfoundry.utils.sops import generate_age_keypair, is_age_installed

        if not is_age_installed():
            pytest.skip("age is not installed")

        key_path = tmp_path_factory.mktemp("sops") / "age-key.txt"
        public_key, _ = generate_age_keypair(key_path)
        return public_key, key_path

    def test_encrypt_decrypt_roundtrip(self, age_keypair: tuple[str, Path]) -> None:
        """Test that encrypt and decrypt work together."""
        import os

        from pynetappfoundry.utils.sops import (
            decrypt_value,
            encrypt_value,
            is_sops_installed,
        )

        if not is_sops_installed():
            pytest.skip("sops is not installed")

        public_key, key_path = age_keypair

        # Set the key file path for decryption
        original_env = os.environ.get("SOPS_AGE_KEY_FILE")
        os.environ["SOPS_AGE_KEY_FILE"] = str(key_path)

        try:
            # Test with a simple secret
            secret = "my-secret-password-123"
            encrypted = encrypt_value(secret, public_key)

            # Verify it's in the expected format
            assert encrypted.startswith("SOPS[")
            assert encrypted.endswith("]")

            # Decrypt and verify
            decrypted = decrypt_value(encrypted)
            assert decrypted == secret
        finally:
            # Restore original env
            if original_env is not None:
                os.environ["SOPS_AGE_KEY_FILE"] = original_env
            elif "SOPS_AGE_KEY_FILE" in os.environ:
                del os.environ["SOPS_AGE_KEY_FILE"]

    def test_encrypt_decrypt_special_characters(self, age_keypair: tuple[str, Path]) -> None:
        """Test encryption/decryption with special characters."""
        import os

        from pynetappfoundry.utils.sops import (
            decrypt_value,
            encrypt_value,
            is_sops_installed,
        )

        if not is_sops_installed():
            pytest.skip("sops is not installed")

        public_key, key_path = age_keypair
        os.environ["SOPS_AGE_KEY_FILE"] = str(key_path)

        try:
            # Test with special characters
            secret = "p@ssw0rd!#$%^&*()_+-=[]{}|;':\",./<>?"
            encrypted = encrypt_value(secret, public_key)
            decrypted = decrypt_value(encrypted)
            assert decrypted == secret
        finally:
            if "SOPS_AGE_KEY_FILE" in os.environ:
                del os.environ["SOPS_AGE_KEY_FILE"]

    def test_encrypt_decrypt_unicode(self, age_keypair: tuple[str, Path]) -> None:
        """Test encryption/decryption with unicode characters."""
        import os

        from pynetappfoundry.utils.sops import (
            decrypt_value,
            encrypt_value,
            is_sops_installed,
        )

        if not is_sops_installed():
            pytest.skip("sops is not installed")

        public_key, key_path = age_keypair
        os.environ["SOPS_AGE_KEY_FILE"] = str(key_path)

        try:
            # Test with unicode
            secret = "密码🔐пароль"
            encrypted = encrypt_value(secret, public_key)
            decrypted = decrypt_value(encrypted)
            assert decrypted == secret
        finally:
            if "SOPS_AGE_KEY_FILE" in os.environ:
                del os.environ["SOPS_AGE_KEY_FILE"]

    def test_is_encrypted_with_real_encrypted_value(self, age_keypair: tuple[str, Path]) -> None:
        """Test is_encrypted with a real encrypted value."""
        from pynetappfoundry.utils.sops import (
            encrypt_value,
            is_encrypted,
            is_sops_installed,
        )

        if not is_sops_installed():
            pytest.skip("sops is not installed")

        public_key, _ = age_keypair
        encrypted = encrypt_value("test", public_key)
        assert is_encrypted(encrypted) is True
