"""Tests for Config class."""

from __future__ import annotations

from pathlib import Path

import pytest

from pynetappfoundry.core.config import Config, ConfigurationError


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
