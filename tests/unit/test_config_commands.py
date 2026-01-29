"""Tests for config CLI commands and environment variable support."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cli.main import nf
from pynetappfoundry.core.config import Config, ConfigurationError


def _create_test_config_files(config_dir: Path) -> None:
    """Create standard test configuration files in the given directory.

    Note: The file name determines the first-level key in config.settings:
    - users.toml -> config.settings["users"]
    - settings.toml -> config.settings["settings"]
    - ontapapi.toml -> config.settings["ontapapi"]

    So users.toml should have [clusters] not [users.clusters] for
    config.settings["users"]["clusters"] to work correctly.
    """
    # Create a data TOML file (marked with settings.type = "data")
    data_toml = config_dir / "clusters.toml"
    data_toml.write_text("""
[settings]
type = "data"

[clusters.test-cluster-1]
name = "test-cluster-1"
ip = "10.0.0.1"
bu = "Engineering"
env = "Dev"
tags = ["active", "workload"]

[clusters.test-cluster-2]
name = "test-cluster-2"
ip = "10.0.0.2"
bu = "Engineering"
env = "Prod"
tags = ["active"]
user = "cluster2-admin"
enc = "cluster2-encoded-pass"
""")

    # Create a settings TOML file
    # Stored at config.settings["settings"]
    settings_toml = config_dir / "settings.toml"
    settings_toml.write_text("""
[clusters]
searchable_keys = ["bu", "env", "tags"]
""")

    # Create ONTAP API settings file
    # Stored at config.settings["ontapapi"]
    # Accessed via get_ontap_api_settings() -> get_setting("ontapapi", "general")
    ontapapi_toml = config_dir / "ontapapi.toml"
    ontapapi_toml.write_text("""
[general]
base_api_path = "/api"
""")

    # Create a users TOML file
    # Stored at config.settings["users"]
    # [clusters] at root means settings["users"]["clusters"] works correctly
    users_toml = config_dir / "users.toml"
    users_toml.write_text("""
[clusters]
user = "admin"
enc = "encoded_password_123"
""")


@pytest.fixture
def temp_config_dir(tmp_path: Path) -> Path:
    """Create a temporary config directory with test TOML files."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    _create_test_config_files(config_dir)
    return config_dir


@pytest.fixture
def config_instance(temp_config_dir: Path, tmp_path: Path) -> Config:
    """Create a Config instance with the temporary config directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        config = Config(
            config_dir=str(temp_config_dir),
            output_dir=str(output_dir),
            script_name="test_script",
        )
    finally:
        os.chdir(original_cwd)
    return config


class TestConfigShowCommand:
    """Tests for nf config show command."""

    def test_show_displays_config(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test that config show displays configuration."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Copy config dir to isolated filesystem
            import shutil

            shutil.copytree(temp_config_dir, Path.cwd() / "config")

            result = runner.invoke(nf, ["config", "show"])
            assert result.exit_code == 0
            assert "Configuration from:" in result.output
            assert "clusters" in result.output.lower()

    def test_show_section_filter(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test that --section filters output."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            import shutil

            shutil.copytree(temp_config_dir, Path.cwd() / "config")

            result = runner.invoke(nf, ["config", "show", "-s", "clusters"])
            assert result.exit_code == 0
            assert "test-cluster-1" in result.output

    def test_show_invalid_section(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test that invalid section shows error."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            import shutil

            shutil.copytree(temp_config_dir, Path.cwd() / "config")

            result = runner.invoke(nf, ["config", "show", "-s", "nonexistent"])
            assert result.exit_code == 1
            assert "not found" in result.output.lower()

    def test_show_masks_passwords(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test that passwords are masked by default."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            import shutil

            shutil.copytree(temp_config_dir, Path.cwd() / "config")

            result = runner.invoke(nf, ["config", "show"])
            assert result.exit_code == 0
            # The encoded password should be masked
            assert "encoded_password_123" not in result.output
            assert "********" in result.output

    def test_show_unmask_reveals_passwords(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test that --unmask reveals passwords."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            import shutil

            shutil.copytree(temp_config_dir, Path.cwd() / "config")

            result = runner.invoke(nf, ["config", "show", "--unmask"])
            assert result.exit_code == 0
            assert "encoded_password_123" in result.output

    def test_show_missing_config_dir(self, tmp_path: Path) -> None:
        """Test error when config directory doesn't exist."""
        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(nf, ["config", "show"])
            assert result.exit_code == 1
            assert "not found" in result.output.lower()


class TestConfigValidateCommand:
    """Tests for nf config validate command."""

    def test_validate_valid_config(self, tmp_path: Path) -> None:
        """Test that valid config passes validation."""
        # Create config directory in tmp_path
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        _create_test_config_files(config_dir)

        runner = CliRunner()
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            result = runner.invoke(nf, ["config", "validate"])
            assert result.exit_code == 0, f"Output: {result.output}"
            assert "valid" in result.output.lower()
        finally:
            os.chdir(original_cwd)

    def test_validate_missing_config_dir(self, tmp_path: Path) -> None:
        """Test error when config directory doesn't exist."""
        runner = CliRunner()
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            result = runner.invoke(nf, ["config", "validate"])
            assert result.exit_code == 1
            assert "not found" in result.output.lower()
        finally:
            os.chdir(original_cwd)

    def test_validate_shows_clusters(self, tmp_path: Path) -> None:
        """Test that validation shows cluster information."""
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        _create_test_config_files(config_dir)

        runner = CliRunner()
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            result = runner.invoke(nf, ["config", "validate"])
            assert result.exit_code == 0, f"Output: {result.output}"
            assert "test-cluster-1" in result.output
        finally:
            os.chdir(original_cwd)


class TestEnvironmentVariableSupport:
    """Tests for environment variable configuration overrides."""

    def test_env_var_config_dir(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test that NF_CONFIG_DIR environment variable overrides config directory."""
        runner = CliRunner()
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            # Set env var to point to valid config, don't pass --config-dir
            # CLI should use env var as default
            result = runner.invoke(
                nf, ["config", "validate"], env={"NF_CONFIG_DIR": str(temp_config_dir)}
            )
            assert result.exit_code == 0, f"Output: {result.output}"
            assert "test-cluster-1" in result.output
        finally:
            os.chdir(original_cwd)

    def test_env_var_user_override(
        self, temp_config_dir: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that NF_<CLUSTER>_USER environment variable overrides user."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            # Create config first, then set env var
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test",
            )
            # Set env var AFTER config creation but BEFORE get_user call
            monkeypatch.setenv("NF_TEST_CLUSTER_1_USER", "env-user")
            user, enc = config.get_user("clusters", "test-cluster-1")
            assert user == "env-user"
            # Password should fall back to config
            assert enc == "encoded_password_123"
        finally:
            os.chdir(original_cwd)

    def test_env_var_password_override(
        self, temp_config_dir: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that NF_<CLUSTER>_PASSWORD environment variable overrides password."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test",
            )
            monkeypatch.setenv("NF_TEST_CLUSTER_1_PASSWORD", "env-encoded-pass")
            user, enc = config.get_user("clusters", "test-cluster-1")
            # User should fall back to config
            assert user == "admin"
            assert enc == "env-encoded-pass"
        finally:
            os.chdir(original_cwd)

    def test_env_var_full_override(
        self, temp_config_dir: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that both user and password can be overridden via environment."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test",
            )
            monkeypatch.setenv("NF_TEST_CLUSTER_1_USER", "env-user")
            monkeypatch.setenv("NF_TEST_CLUSTER_1_PASSWORD", "env-pass")
            user, enc = config.get_user("clusters", "test-cluster-1")
            assert user == "env-user"
            assert enc == "env-pass"
        finally:
            os.chdir(original_cwd)

    def test_env_var_name_conversion(self, config_instance: Config) -> None:
        """Test that cluster names are properly converted to env var format."""
        # Test the internal method
        assert config_instance._get_env_var_name("cluster-prod") == "NF_CLUSTER_PROD"
        assert config_instance._get_env_var_name("my-cluster-1") == "NF_MY_CLUSTER_1"
        assert config_instance._get_env_var_name("simple") == "NF_SIMPLE"

    def test_env_var_priority_over_object_config(
        self, temp_config_dir: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that env vars take priority over object-specific config."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test",
            )
            # test-cluster-2 has its own credentials in config
            monkeypatch.setenv("NF_TEST_CLUSTER_2_USER", "env-override")
            user, enc = config.get_user("clusters", "test-cluster-2")
            # Env var should win
            assert user == "env-override"
            # Password should come from object config
            assert enc == "cluster2-encoded-pass"
        finally:
            os.chdir(original_cwd)

    def test_credentials_fallback_chain(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test the full credential fallback chain."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test",
            )
            # No env vars, no object config -> falls back to default users
            user, enc = config.get_user("clusters", "test-cluster-1")
            assert user == "admin"
            assert enc == "encoded_password_123"

            # Object has config -> uses that
            user, enc = config.get_user("clusters", "test-cluster-2")
            assert user == "cluster2-admin"
            assert enc == "cluster2-encoded-pass"
        finally:
            os.chdir(original_cwd)

    def test_error_message_includes_env_var_hint(self, tmp_path: Path) -> None:
        """Test that error messages mention environment variables."""
        # Create config without default users
        config_dir = tmp_path / "config_no_users"
        config_dir.mkdir()
        (config_dir / "clusters.toml").write_text("""
[settings]
type = "data"

[clusters.orphan-cluster]
name = "orphan-cluster"
ip = "10.0.0.99"
""")
        (config_dir / "settings.toml").write_text("""
[ontapapi.general]
base_api_path = "/api"
""")

        output_dir = tmp_path / "output"
        output_dir.mkdir()
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            config = Config(
                config_dir=str(config_dir),
                output_dir=str(output_dir),
                script_name="test",
            )
            with pytest.raises(ConfigurationError) as exc_info:
                config.get_user("clusters", "orphan-cluster")
            # Error message should mention the env var
            assert "NF_ORPHAN_CLUSTER_USER" in str(exc_info.value)
        finally:
            os.chdir(original_cwd)


class TestInitSopsCommand:
    """Tests for nf config init-sops command."""

    def test_init_sops_force_removes_existing_key(self, tmp_path: Path) -> None:
        """Test that --force removes existing key file before generating new one."""
        runner = CliRunner()

        # Create a fake existing key file
        key_dir = tmp_path / ".sops" / "age"
        key_dir.mkdir(parents=True)
        key_file = key_dir / "keys.txt"
        key_file.write_text(
            "# created: 2024-01-01T00:00:00Z\n# public key: age1oldkey123\nAGE-SECRET-KEY-OLD\n"
        )

        # Mock the tools as installed and the keypair generation
        with (
            runner.isolated_filesystem(temp_dir=tmp_path),
            patch(
                "pynetappfoundry.cli.commands.config.init_sops.is_sops_installed",
                return_value=True,
            ),
            patch(
                "pynetappfoundry.cli.commands.config.init_sops.is_age_installed",
                return_value=True,
            ),
            patch(
                "pynetappfoundry.cli.commands.config.init_sops.generate_age_keypair",
                return_value=("age1newkey456", str(key_file)),
            ) as mock_generate,
        ):
            result = runner.invoke(
                nf,
                ["config", "init-sops", "--key-path", str(key_file), "--force"],
            )

            # The command should succeed
            assert result.exit_code == 0, f"Output: {result.output}"
            # The existing file should have been removed before generation
            assert "Removed existing key" in result.output
            # generate_age_keypair should have been called
            mock_generate.assert_called_once()

    def test_init_sops_without_force_shows_existing_key(self, tmp_path: Path) -> None:
        """Test that without --force, existing key is shown and not overwritten."""
        runner = CliRunner()

        # Create a fake existing key file
        key_dir = tmp_path / ".sops" / "age"
        key_dir.mkdir(parents=True)
        key_file = key_dir / "keys.txt"
        key_file.write_text(
            "# created: 2024-01-01T00:00:00Z\n"
            "# public key: age1existingkey789\n"
            "AGE-SECRET-KEY-EXISTING\n"
        )

        with (
            runner.isolated_filesystem(temp_dir=tmp_path),
            patch(
                "pynetappfoundry.cli.commands.config.init_sops.is_sops_installed",
                return_value=True,
            ),
            patch(
                "pynetappfoundry.cli.commands.config.init_sops.is_age_installed",
                return_value=True,
            ),
        ):
            result = runner.invoke(
                nf,
                ["config", "init-sops", "--key-path", str(key_file)],
            )

            # Exit code 0 (key exists, info displayed)
            assert result.exit_code == 0, f"Output: {result.output}"
            assert "already exists" in result.output
            assert "age1existingkey789" in result.output
            assert "--force" in result.output
