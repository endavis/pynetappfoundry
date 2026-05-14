"""Tests for Config class."""

from __future__ import annotations

from pathlib import Path

import pytest

from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.core.models import (
    ConsoleAPISettings,
    DIIAPISettings,
    LicensingSettings,
    ONTAPAPISettings,
    SMTPSettings,
)


@pytest.fixture
def temp_config_dir(tmp_path: Path) -> Path:
    """Create a temporary config directory with test TOML files."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()

    # Create a data TOML file
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

[clusters.test-cluster-3]
name = "test-cluster-3"
ip = "10.0.0.3"
bu = "Finance"
env = "Prod"
tags = ["active", "critical"]
""")

    # Create a settings TOML file
    settings_toml = config_dir / "settings.toml"
    settings_toml.write_text("""
[settings.clusters]
searchable_keys = ["bu", "env", "tags"]

[ontapapi.general]
base_api_path = "/api"
""")

    # Create a users TOML file
    users_toml = config_dir / "users.toml"
    users_toml.write_text("""
[users.clusters]
user = "admin"
enc = "encoded_password_123"
""")

    return config_dir


@pytest.fixture
def config_instance(temp_config_dir: Path, tmp_path: Path) -> Config:
    """Create a Config instance with the temporary config directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    # Change to tmp_path so relative paths work
    import os

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


class TestConfigParsing:
    """Tests for TOML parsing and data loading."""

    def test_loads_data_toml(self, config_instance: Config) -> None:
        """Test that data TOML files are loaded into the data attribute."""
        assert "clusters" in config_instance.data
        assert "test-cluster-1" in config_instance.data["clusters"]
        assert "test-cluster-2" in config_instance.data["clusters"]
        assert "test-cluster-3" in config_instance.data["clusters"]

    def test_loads_settings_toml(self, config_instance: Config) -> None:
        """Test that settings TOML files are loaded into the settings attribute."""
        # Settings files are loaded by their filename (without .toml)
        # e.g., settings.toml is loaded into config.settings["settings"]
        assert "settings" in config_instance.settings
        assert "ontapapi" in config_instance.settings["settings"]

    def test_cluster_data_structure(self, config_instance: Config) -> None:
        """Test that cluster data has expected structure."""
        cluster = config_instance.data["clusters"]["test-cluster-1"]
        assert cluster["name"] == "test-cluster-1"
        assert cluster["ip"] == "10.0.0.1"
        assert cluster["bu"] == "Engineering"
        assert cluster["env"] == "Dev"
        assert "active" in cluster["tags"]
        assert "workload" in cluster["tags"]

    def test_handles_missing_config_dir(self, tmp_path: Path) -> None:
        """Test behavior when config directory doesn't exist."""
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            # Create required output dir
            output_dir = tmp_path / "output"
            output_dir.mkdir()
            # Config should handle missing config dir gracefully (no TOML files to load)
            config = Config(
                config_dir="nonexistent",
                output_dir=str(output_dir),
                script_name="test",
            )
            # Data should be empty (no files to load)
            assert config.data == {}
        finally:
            os.chdir(original_cwd)


class TestConfigSearch:
    """Tests for search functionality."""

    def test_search_by_single_field(self, config_instance: Config) -> None:
        """Test search with a single field."""
        results = config_instance.search("clusters", {"bu": "Engineering"})
        assert len(results) == 2
        assert "test-cluster-1" in results
        assert "test-cluster-2" in results

    def test_search_by_multiple_fields(self, config_instance: Config) -> None:
        """Test search with multiple fields."""
        results = config_instance.search("clusters", {"bu": "Engineering", "env": "Prod"})
        assert len(results) == 1
        assert "test-cluster-2" in results

    def test_search_with_or_operator(self, config_instance: Config) -> None:
        """Test search with || (OR) operator."""
        results = config_instance.search("clusters", {"env": "Dev || Prod"})
        assert len(results) == 3

    def test_search_with_and_operator_on_list(self, config_instance: Config) -> None:
        """Test search with && (AND) operator on list field."""
        results = config_instance.search("clusters", {"tags": "active && workload"})
        assert len(results) == 1
        assert "test-cluster-1" in results

    def test_search_no_match(self, config_instance: Config) -> None:
        """Test search with no matching results."""
        results = config_instance.search("clusters", {"bu": "NonExistent"})
        assert len(results) == 0

    def test_search_empty_dict_returns_all(self, config_instance: Config) -> None:
        """Test that empty search dict returns all items."""
        results = config_instance.search("clusters", {})
        assert len(results) == 3

    def test_get_clusters_convenience_method(self, config_instance: Config) -> None:
        """Test the get_clusters convenience method."""
        results = config_instance.get_clusters({"env": "Prod"})
        assert len(results) == 2


class TestFindClosest:
    """Tests for find_closest functionality."""

    def test_find_closest_exact_match(self, config_instance: Config) -> None:
        """Test find_closest with exact match."""
        tree = {"bu": "Engineering", "env": "Prod"}
        result = config_instance.find_closest("clusters", tree)
        assert result is not None
        assert result["name"] == "test-cluster-2"

    def test_find_closest_relaxes_criteria(self, config_instance: Config) -> None:
        """Test find_closest relaxes criteria when no exact match."""
        tree = {"bu": "Finance", "env": "Prod", "app": "NonExistent"}
        result = config_instance.find_closest("clusters", tree)
        assert result is not None
        assert result["name"] == "test-cluster-3"

    def test_find_closest_no_match(self, config_instance: Config) -> None:
        """Test find_closest returns None when nothing matches."""
        tree = {"bu": "NonExistent"}
        result = config_instance.find_closest("clusters", tree)
        assert result is None

    def test_find_closest_removes_empty_keys(self, config_instance: Config) -> None:
        """Test that find_closest removes empty keys before searching."""
        tree = {"bu": "Finance", "env": "", "app": ""}
        result = config_instance.find_closest("clusters", tree)
        assert result is not None
        assert result["name"] == "test-cluster-3"


class TestGetUser:
    """Tests for credential retrieval."""

    def test_get_user_from_settings(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test getting user credentials from settings."""
        # Rewrite users.toml with correct structure for the code
        # settings["users"] accesses users.toml, then ["clusters"] accesses [clusters] section
        users_toml = temp_config_dir / "users.toml"
        users_toml.write_text("""
[clusters]
user = "admin"
enc = "encoded_password_123"
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            user, enc = config.get_user("clusters")
            assert user == "admin"
            assert enc == "encoded_password_123"
        finally:
            os.chdir(original_cwd)

    def test_get_user_from_data(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test getting user credentials from data object."""
        # Add a cluster with specific credentials
        clusters_toml = temp_config_dir / "clusters_with_creds.toml"
        clusters_toml.write_text("""
[settings]
type = "data"

[clusters.cluster-with-creds]
name = "cluster-with-creds"
ip = "10.0.0.10"
user = "cluster_admin"
enc = "cluster_encoded_password"
""")

        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            user, enc = config.get_user("clusters", "cluster-with-creds")
            assert user == "cluster_admin"
            assert enc == "cluster_encoded_password"
        finally:
            os.chdir(original_cwd)

    def test_get_user_missing_credentials_raises(
        self, temp_config_dir: Path, tmp_path: Path
    ) -> None:
        """Test that get_user raises ConfigurationError when credentials not found."""
        # Create config without users.toml
        import os

        # Remove the users.toml file
        users_file = temp_config_dir / "users.toml"
        users_file.unlink()

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            with pytest.raises(ConfigurationError) as exc_info:
                config.get_user("clusters", "nonexistent")
            assert "Could not find user" in str(exc_info.value)
        finally:
            os.chdir(original_cwd)


class TestCheckTermMethods:
    """Tests for check_term, chk_and, chk_or methods."""

    def test_chk_and_with_list_all_match(self, config_instance: Config) -> None:
        """Test chk_and when all terms are in the list."""
        result = config_instance.chk_and("a && b", ["a", "b", "c"])
        assert result is True

    def test_chk_and_with_list_partial_match(self, config_instance: Config) -> None:
        """Test chk_and when not all terms are in the list."""
        result = config_instance.chk_and("a && d", ["a", "b", "c"])
        assert result is False

    def test_chk_and_with_string_returns_false(self, config_instance: Config) -> None:
        """Test chk_and returns False for string values."""
        result = config_instance.chk_and("a && b", "a")
        assert result is False

    def test_chk_or_with_list_match(self, config_instance: Config) -> None:
        """Test chk_or with list containing a match."""
        result = config_instance.chk_or("a || d", ["a", "b", "c"])
        assert result is True

    def test_chk_or_with_list_no_match(self, config_instance: Config) -> None:
        """Test chk_or with list not containing any match."""
        result = config_instance.chk_or("x || y", ["a", "b", "c"])
        assert result is False

    def test_chk_or_with_string_match(self, config_instance: Config) -> None:
        """Test chk_or with string containing a match."""
        result = config_instance.chk_or("a || b", "a")
        assert result is True

    def test_chk_or_with_string_no_match(self, config_instance: Config) -> None:
        """Test chk_or with string not matching."""
        result = config_instance.chk_or("x || y", "a")
        assert result is False

    def test_check_term_simple_match_string(self, config_instance: Config) -> None:
        """Test check_term with simple string match."""
        result = config_instance.check_term("value", "value")
        assert result is True

    def test_check_term_simple_match_list(self, config_instance: Config) -> None:
        """Test check_term with simple match in list."""
        result = config_instance.check_term("a", ["a", "b"])
        assert result is True

    def test_check_term_delegates_to_or(self, config_instance: Config) -> None:
        """Test check_term delegates || to chk_or."""
        result = config_instance.check_term("a || b", "a")
        assert result is True

    def test_check_term_delegates_to_and(self, config_instance: Config) -> None:
        """Test check_term delegates && to chk_and."""
        result = config_instance.check_term("a && b", ["a", "b"])
        assert result is True


class TestSchemaLocation:
    """Tests for get_schema_location method."""

    def test_returns_correct_path(self, config_instance: Config) -> None:
        """Test that get_schema_location returns correct path."""
        path = config_instance.get_schema_location("ontap")
        assert path.name == "ontap"
        assert "apis" in str(path)


class TestCount:
    """Tests for count method."""

    def test_count_clusters(self, config_instance: Config) -> None:
        """Test counting unique items in clusters."""
        count = config_instance.count("clusters")
        assert count == 3

    def test_count_by_field(self, config_instance: Config) -> None:
        """Test counting by a specific field."""
        count = config_instance.count("clusters", "bu")
        # Engineering and Finance = 2 unique values
        assert count == 2


class TestGetSetting:
    """Tests for get_setting accessor method."""

    def test_get_setting_single_key(self, config_instance: Config) -> None:
        """Test get_setting with a single key."""
        result = config_instance.get_setting("settings")
        assert isinstance(result, dict)
        assert "ontapapi" in result

    def test_get_setting_nested_keys(self, config_instance: Config) -> None:
        """Test get_setting with nested keys."""
        result = config_instance.get_setting("settings", "ontapapi", "general", "base_api_path")
        assert result == "/api"

    def test_get_setting_with_default(self, config_instance: Config) -> None:
        """Test get_setting returns default for missing key."""
        result = config_instance.get_setting("nonexistent", default="default_value")
        assert result == "default_value"

    def test_get_setting_missing_key_raises(self, config_instance: Config) -> None:
        """Test get_setting raises ConfigurationError for missing key."""
        with pytest.raises(ConfigurationError) as exc_info:
            config_instance.get_setting("nonexistent", "key")
        assert "Missing configuration key" in str(exc_info.value)
        assert "nonexistent" in str(exc_info.value)

    def test_get_setting_nested_missing_key_raises(self, config_instance: Config) -> None:
        """Test get_setting raises ConfigurationError for missing nested key."""
        with pytest.raises(ConfigurationError) as exc_info:
            config_instance.get_setting("settings", "nonexistent")
        assert "Missing configuration key" in str(exc_info.value)
        assert "settings.nonexistent" in str(exc_info.value)

    def test_get_setting_non_dict_access_raises(
        self, temp_config_dir: Path, tmp_path: Path
    ) -> None:
        """Test get_setting raises ConfigurationError when accessing non-dict."""
        # Create a settings file with a scalar value
        settings_toml = temp_config_dir / "scalar.toml"
        settings_toml.write_text("""
value = "scalar_string"
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            with pytest.raises(ConfigurationError) as exc_info:
                config.get_setting("scalar", "value", "nested")
            assert "Cannot access" in str(exc_info.value)
        finally:
            os.chdir(original_cwd)


class TestGetSmtpSettings:
    """Tests for get_smtp_settings accessor method."""

    def test_get_smtp_settings_success(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test get_smtp_settings returns SMTPSettings object."""
        # SMTP settings go in settings.toml under [SMTP] section
        # which becomes config.settings["settings"]["SMTP"]
        smtp_toml = temp_config_dir / "settings.toml"
        smtp_toml.write_text("""
[SMTP]
server = "smtp.example.com"
port = 587
user = "smtp_user"
password = "smtp_pass"
auth = "True"
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            result = config.get_smtp_settings()
            assert isinstance(result, SMTPSettings)
            assert result.server == "smtp.example.com"
            assert result.port == 587
            assert result.user == "smtp_user"
            assert result.password == "smtp_pass"
            assert result.auth == "True"
        finally:
            os.chdir(original_cwd)

    def test_get_smtp_settings_missing_raises(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test get_smtp_settings raises ConfigurationError when not configured."""
        # Remove settings.toml to ensure no SMTP config exists
        settings_file = temp_config_dir / "settings.toml"
        settings_file.write_text("""
[other]
key = "value"
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            with pytest.raises(ConfigurationError) as exc_info:
                config.get_smtp_settings()
            assert "SMTP" in str(exc_info.value) or "Missing configuration" in str(exc_info.value)
        finally:
            os.chdir(original_cwd)


class TestGetOntapApiSettings:
    """Tests for get_ontap_api_settings accessor method."""

    def test_get_ontap_api_settings_success(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test get_ontap_api_settings returns ONTAPAPISettings object."""
        # ONTAP API settings go in ontapapi.toml under [general] section
        # which becomes config.settings["ontapapi"]["general"]
        ontapapi_toml = temp_config_dir / "ontapapi.toml"
        ontapapi_toml.write_text("""
[general]
base_api_path = "/api"
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            result = config.get_ontap_api_settings()
            assert isinstance(result, ONTAPAPISettings)
            assert result.base_api_path == "/api"
        finally:
            os.chdir(original_cwd)

    def test_get_ontap_api_settings_missing_raises(
        self, temp_config_dir: Path, tmp_path: Path
    ) -> None:
        """Test get_ontap_api_settings raises ConfigurationError when not configured."""
        # Create config without ontapapi settings
        settings_file = temp_config_dir / "settings.toml"
        settings_file.write_text("""
[other]
key = "value"
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            with pytest.raises(ConfigurationError) as exc_info:
                config.get_ontap_api_settings()
            assert "ontapapi" in str(exc_info.value) or "Missing configuration" in str(
                exc_info.value
            )
        finally:
            os.chdir(original_cwd)


class TestGetDiiApiSettings:
    """Tests for get_dii_api_settings accessor method."""

    def test_get_dii_api_settings_success(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test get_dii_api_settings returns DIIAPISettings object."""
        # DII API settings go in diiapi.toml under [general] section
        # which becomes config.settings["diiapi"]["general"]
        diiapi_toml = temp_config_dir / "diiapi.toml"
        diiapi_toml.write_text("""
[general]
api_ro_token = "test_token"
base_url = "https://dii.example.com"
base_api_path = "/rest/v1"
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            result = config.get_dii_api_settings()
            assert isinstance(result, DIIAPISettings)
            assert result.api_ro_token == "test_token"
            assert result.base_url == "https://dii.example.com"
            assert result.base_api_path == "/rest/v1"
        finally:
            os.chdir(original_cwd)

    def test_get_dii_api_settings_missing_raises(
        self, temp_config_dir: Path, tmp_path: Path
    ) -> None:
        """Test get_dii_api_settings raises ConfigurationError when not configured."""
        settings_file = temp_config_dir / "settings.toml"
        settings_file.write_text("""
[other]
key = "value"
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            with pytest.raises(ConfigurationError) as exc_info:
                config.get_dii_api_settings()
            assert "diiapi" in str(exc_info.value) or "Missing configuration" in str(exc_info.value)
        finally:
            os.chdir(original_cwd)


class TestGetConsoleApiSettings:
    """Tests for get_console_api_settings accessor method."""

    def test_get_console_api_settings_success(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """get_console_api_settings returns a populated ConsoleAPISettings."""
        consoleapi_toml = temp_config_dir / "consoleapi.toml"
        consoleapi_toml.write_text("""
[general]
user_token = "user-jwt"
service_token = "service-jwt"
base_url = "https://api.bluexp.netapp.com"
base_api_path = "/"
org_id = "org-abc"
timeout = 15.0
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            result = config.get_console_api_settings()
            assert isinstance(result, ConsoleAPISettings)
            assert result.user_token == "user-jwt"
            assert result.service_token == "service-jwt"
            assert result.base_url == "https://api.bluexp.netapp.com"
            assert result.org_id == "org-abc"
            assert result.timeout == 15.0
        finally:
            os.chdir(original_cwd)

    def test_get_console_api_settings_service_token_optional(
        self, temp_config_dir: Path, tmp_path: Path
    ) -> None:
        """service_token may be omitted; defaults to None."""
        consoleapi_toml = temp_config_dir / "consoleapi.toml"
        consoleapi_toml.write_text("""
[general]
user_token = "user-jwt"
base_url = "https://api.bluexp.netapp.com"
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            result = config.get_console_api_settings()
            assert result.service_token is None
            assert result.org_id is None
        finally:
            os.chdir(original_cwd)

    def test_get_console_api_settings_missing_raises(
        self, temp_config_dir: Path, tmp_path: Path
    ) -> None:
        """get_console_api_settings raises ConfigurationError when not configured."""
        settings_file = temp_config_dir / "settings.toml"
        settings_file.write_text("""
[other]
key = "value"
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            with pytest.raises(ConfigurationError):
                config.get_console_api_settings()
        finally:
            os.chdir(original_cwd)


class TestGetLicensingSettings:
    """Tests for get_licensing_settings accessor method."""

    def test_get_licensing_settings_success(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test get_licensing_settings returns LicensingSettings object."""
        # Licensing settings go in settings.toml under [licensing] section
        # which becomes config.settings["settings"]["licensing"]
        settings_toml = temp_config_dir / "settings.toml"
        settings_toml.write_text("""
[licensing]
mailfrom = "from@example.com"
mailto = "to@example.com"
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            result = config.get_licensing_settings()
            assert isinstance(result, LicensingSettings)
            assert result.mailfrom == "from@example.com"
            assert result.mailto == "to@example.com"
        finally:
            os.chdir(original_cwd)

    def test_get_licensing_settings_missing_returns_none(
        self, temp_config_dir: Path, tmp_path: Path
    ) -> None:
        """Test get_licensing_settings returns None when not configured."""
        settings_file = temp_config_dir / "settings.toml"
        settings_file.write_text("""
[other]
key = "value"
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            result = config.get_licensing_settings()
            assert result is None
        finally:
            os.chdir(original_cwd)


class TestGetRelaxationOrder:
    """Tests for get_relaxation_order method."""

    def test_explicit_relaxation_order(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test that explicit relaxation_order in settings is used."""
        settings_file = temp_config_dir / "settings.toml"
        settings_file.write_text("""
[clusters]
searchable_keys = ['div', 'bu', 'env']
relaxation_order = ['env', 'bu', 'div']
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            result = config.get_relaxation_order("clusters")
            assert result == ["env", "bu", "div"]
        finally:
            os.chdir(original_cwd)

    def test_falls_back_to_reversed_searchable_keys(
        self, temp_config_dir: Path, tmp_path: Path
    ) -> None:
        """Test that reversed searchable_keys is used when relaxation_order not set."""
        settings_file = temp_config_dir / "settings.toml"
        settings_file.write_text("""
[clusters]
searchable_keys = ['div', 'bu', 'env', 'app']
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            result = config.get_relaxation_order("clusters")
            # Should be reversed searchable_keys
            assert result == ["app", "env", "bu", "div"]
        finally:
            os.chdir(original_cwd)

    def test_falls_back_to_default_order(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test that default order is used when no settings exist."""
        settings_file = temp_config_dir / "settings.toml"
        settings_file.write_text("""
[other]
key = "value"
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            result = config.get_relaxation_order("clusters")
            # Should be the default fallback order
            assert result == ["region", "subapp", "cloud", "env", "app", "bu", "div"]
        finally:
            os.chdir(original_cwd)

    def test_different_data_types_can_have_different_orders(
        self, temp_config_dir: Path, tmp_path: Path
    ) -> None:
        """Test that different data types can have different relaxation orders."""
        settings_file = temp_config_dir / "settings.toml"
        settings_file.write_text("""
[clusters]
relaxation_order = ['region', 'env', 'bu']

[connectors]
relaxation_order = ['cloud', 'app', 'div']
""")
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            clusters_order = config.get_relaxation_order("clusters")
            connectors_order = config.get_relaxation_order("connectors")
            assert clusters_order == ["region", "env", "bu"]
            assert connectors_order == ["cloud", "app", "div"]
        finally:
            os.chdir(original_cwd)


class TestClusterEntryWrapping:
    """Tests for ClusterEntry wrapping of cluster data."""

    def test_clusters_wrapped_as_cluster_entries(
        self, temp_config_dir: Path, tmp_path: Path
    ) -> None:
        """Test that clusters are wrapped as ClusterEntry instances."""
        import os

        from pynetappfoundry.core.cluster_entry import ClusterEntry

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )

            for cluster_name in config.data.get("clusters", {}):
                cluster = config.data["clusters"][cluster_name]
                assert isinstance(cluster, ClusterEntry)
        finally:
            os.chdir(original_cwd)

    def test_no_cache_default_false(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Config() default leaves wrapped ClusterEntry _no_cache=False."""
        import os

        from pynetappfoundry.core.cluster_entry import ClusterEntry

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )
            assert config.no_cache is False
            for cluster in config.data["clusters"].values():
                assert isinstance(cluster, ClusterEntry)
                assert cluster._no_cache is False
        finally:
            os.chdir(original_cwd)

    def test_no_cache_propagates_to_cluster_entries(
        self, temp_config_dir: Path, tmp_path: Path
    ) -> None:
        """Config(no_cache=True) propagates to wrapped ClusterEntry instances."""
        import os

        from pynetappfoundry.core.cluster_entry import ClusterEntry

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
                no_cache=True,
            )
            assert config.no_cache is True
            for cluster in config.data["clusters"].values():
                assert isinstance(cluster, ClusterEntry)
                assert cluster._no_cache is True
        finally:
            os.chdir(original_cwd)

    def test_cluster_entry_static_access(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test that TOML fields are accessible via entry['key'] and entry.key."""
        import os

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)
            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )

            cluster = config.data["clusters"]["test-cluster-1"]
            # Dict-style access
            assert cluster["ip"] == "10.0.0.1"
            assert cluster["bu"] == "Engineering"
            # Attribute-style access
            assert cluster.ip == "10.0.0.1"
            assert cluster.bu == "Engineering"
        finally:
            os.chdir(original_cwd)

    def test_cluster_entry_lazy_cache_access(self, temp_config_dir: Path, tmp_path: Path) -> None:
        """Test that entry.ontap returns metadata when cache exists."""
        import os

        from pynetappfoundry.cache import CachedClusterMetadata
        from pynetappfoundry.cache.db import ClusterMetadataDB
        from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)

            # Create config to set up the cache directory
            config1 = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )

            # Populate cache for one cluster
            db = ClusterMetadataDB(config=config1)
            cached_metadata = CachedClusterMetadata(
                cluster_name="test-cluster-1",
                cloud=[
                    CloudMetadata(
                        provider="Azure",
                        region="eastus",
                        account_id="sub-12345",
                        resource_group_name="rg-test",
                        instance_type="Standard_E20ds_v5",
                    )
                ],
            )
            db.set("test-cluster-1", cached_metadata)
            db.close()

            # New config should wrap clusters with ClusterEntry
            config2 = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )

            # Access cached data via .ontap
            cluster1 = config2.data["clusters"]["test-cluster-1"]
            ontap = cluster1.ontap
            assert ontap is not None
            assert ontap.cloud[0].provider == "Azure"
            assert ontap.cloud[0].region == "eastus"
            assert ontap.cloud[0].account_id == "sub-12345"
            assert ontap.cloud[0].resource_group_name == "rg-test"
            assert ontap.cloud[0].instance_type == "Standard_E20ds_v5"
        finally:
            os.chdir(original_cwd)

    def test_cluster_entry_no_cache_returns_datasource_backed(
        self, temp_config_dir: Path, tmp_path: Path
    ) -> None:
        """When no cache DB exists, entry.ontap returns DataSource-backed lazy metadata."""
        import os

        from pynetappfoundry.cache._lazy import LazyClusterMetadata

        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            output_dir = tmp_path / "output"
            output_dir.mkdir(exist_ok=True)

            # Ensure no cache DB file exists
            cache_path = temp_config_dir / ".cache" / "cluster_metadata.db"
            assert not cache_path.exists()

            config = Config(
                config_dir=str(temp_config_dir),
                output_dir=str(output_dir),
                script_name="test_script",
            )

            cluster = config.data["clusters"]["test-cluster-1"]
            # With Config available, ontap returns a DataSource-backed lazy proxy
            result = cluster.ontap
            assert isinstance(result, LazyClusterMetadata)
            assert result._config is not None
        finally:
            os.chdir(original_cwd)
