"""Tests for cache schema CLI command."""

from __future__ import annotations

import json

import pytest
from click.testing import CliRunner

from pynetappfoundry.cli.main import nf


class TestCacheSchemaCommand:
    """Tests for nf cache schema command."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a CLI runner."""
        return CliRunner()

    def test_schema_tree_output(self, runner: CliRunner) -> None:
        """Test default tree output."""
        result = runner.invoke(nf, ["cache", "schema"])

        assert result.exit_code == 0
        assert "CachedClusterMetadata" in result.output
        assert "cluster_name" in result.output
        assert "cloud" in result.output
        assert "cluster" in result.output
        assert "nodes" in result.output

    def test_schema_flat_output(self, runner: CliRunner) -> None:
        """Test flat output with --flat flag."""
        result = runner.invoke(nf, ["cache", "schema", "--flat"])

        assert result.exit_code == 0
        assert "Queryable Field Paths" in result.output
        # Check for dotted paths - cloud is now a list
        assert "cloud[N].provider" in result.output
        assert "cloud[N].instance_type" in result.output
        assert "cluster.ontap_version" in result.output
        # Check for array notation
        assert "nodes[N]" in result.output
        assert "nodes[N].name" in result.output

    def test_schema_json_output(self, runner: CliRunner) -> None:
        """Test JSON schema output with --json flag."""
        result = runner.invoke(nf, ["cache", "schema", "--json"])

        assert result.exit_code == 0
        # Should be valid JSON
        schema = json.loads(result.output)
        assert "properties" in schema
        assert "cluster_name" in schema["properties"]
        assert "cloud" in schema["properties"]

    def test_schema_contains_all_top_level_fields(self, runner: CliRunner) -> None:
        """Test that schema includes all top-level fields."""
        result = runner.invoke(nf, ["cache", "schema", "--flat"])

        assert result.exit_code == 0
        # All top-level sections should be present
        assert "cloud[N]." in result.output  # cloud is now a list
        assert "cluster." in result.output
        assert "nodes[N]." in result.output
        assert "network." in result.output
        assert "storage." in result.output
        assert "license_packages[N]." in result.output
        assert "mediator." in result.output
        assert "relationships." in result.output

    def test_schema_contains_nested_fields(self, runner: CliRunner) -> None:
        """Test that schema includes nested fields."""
        result = runner.invoke(nf, ["cache", "schema", "--flat"])

        assert result.exit_code == 0
        # Check deeply nested paths
        assert "network.ip_interfaces[N].ip_address" in result.output
        assert "storage.aggregates[N].name" in result.output
        assert "license_packages[N].name" in result.output

    def test_schema_shows_types(self, runner: CliRunner) -> None:
        """Test that schema shows field types."""
        result = runner.invoke(nf, ["cache", "schema", "--flat"])

        assert result.exit_code == 0
        # Types should be displayed
        assert "str" in result.output
        assert "int" in result.output
        assert "bool" in result.output

    def test_schema_help(self, runner: CliRunner) -> None:
        """Test schema command help."""
        result = runner.invoke(nf, ["cache", "schema", "--help"])

        assert result.exit_code == 0
        assert "Display the cache metadata schema" in result.output
        assert "--json" in result.output
        assert "--flat" in result.output
