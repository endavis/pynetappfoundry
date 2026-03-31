"""Tests for SOPS encryption utilities."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from pynetappfoundry.utils.sops import (
    SOPS_PREFIX,
    SOPS_SUFFIX,
    SOPSError,
    SOPSNotInstalledError,
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
