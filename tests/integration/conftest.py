"""Shared fixtures for integration tests.

These fixtures provide mock configurations, API specs, and test data
for integration testing without requiring actual ONTAP/DII connections.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_cluster() -> MagicMock:
    """Create a mock cluster object with required attributes."""
    cluster = MagicMock()
    cluster.name = "test-cluster"
    cluster.ip = "192.168.1.100"
    return cluster


@pytest.fixture
def mock_ontap_spec(tmp_path: Path) -> Path:
    """Create a minimal ONTAP-like OpenAPI spec for testing."""
    spec = {
        "swagger": "2.0",
        "basePath": "/api",
        "info": {"title": "ONTAP REST API", "version": "9.13"},
        "paths": {
            "/cluster": {
                "get": {
                    "summary": "Get cluster information",
                    "operationId": "cluster_get",
                    "responses": {
                        "200": {
                            "description": "Cluster information",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "uuid": {"type": "string"},
                                            "version": {
                                                "type": "object",
                                                "properties": {
                                                    "full": {"type": "string"},
                                                    "generation": {"type": "integer"},
                                                },
                                            },
                                        },
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/storage/volumes": {
                "get": {
                    "summary": "Get volumes",
                    "operationId": "volume_collection_get",
                    "parameters": [
                        {
                            "name": "svm.name",
                            "in": "query",
                            "type": "string",
                            "description": "Filter by SVM name",
                        },
                        {
                            "name": "fields",
                            "in": "query",
                            "type": "string",
                            "description": "Fields to return",
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "Volume collection",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "records": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "name": {"type": "string"},
                                                        "uuid": {"type": "string"},
                                                        "size": {"type": "integer"},
                                                        "space": {
                                                            "type": "object",
                                                            "properties": {
                                                                "used": {"type": "integer"},
                                                                "available": {"type": "integer"},
                                                            },
                                                        },
                                                    },
                                                },
                                            },
                                            "num_records": {"type": "integer"},
                                        },
                                    }
                                }
                            },
                        }
                    },
                }
            },
            "/storage/aggregates": {
                "get": {
                    "summary": "Get aggregates",
                    "operationId": "aggregate_collection_get",
                    "responses": {
                        "200": {
                            "description": "Aggregate collection",
                        }
                    },
                }
            },
        },
    }
    spec_dir = tmp_path / "apis" / "ontap"
    spec_dir.mkdir(parents=True)
    spec_file = spec_dir / "all.json"
    spec_file.write_text(json.dumps(spec))
    return spec_dir


@pytest.fixture
def mock_config_dir(tmp_path: Path, mock_ontap_spec: Path) -> Path:
    """Create a mock configuration directory with test data."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()

    # Create clusters data file
    clusters_toml = config_dir / "clusters.toml"
    clusters_toml.write_text("""
[settings]
type = "data"

[clusters.test-cluster]
name = "test-cluster"
ip = "192.168.1.100"
bu = "Engineering"
env = "Dev"
tags = ["test", "dev"]
""")

    # Create settings file
    settings_toml = config_dir / "settings.toml"
    settings_toml.write_text("""
[clusters]
searchable_keys = ['bu', 'env', 'tags']

[ontapapi.general]
base_api_path = "/api"
timeout = 30.0
""")

    # Create users file
    users_toml = config_dir / "users.toml"
    users_toml.write_text("""
[users.clusters]
user = "admin"
enc = "YWRtaW4="
""")

    # Create APIs directory structure pointing to our mock spec
    apis_dir = config_dir / "apis" / "ontap"
    apis_dir.mkdir(parents=True)

    # Copy the spec file
    spec_content = (mock_ontap_spec / "all.json").read_text()
    (apis_dir / "all.json").write_text(spec_content)

    return config_dir


@pytest.fixture
def sample_volume_response() -> dict[str, Any]:
    """Sample ONTAP volume API response."""
    return {
        "records": [
            {
                "name": "vol1",
                "uuid": "abc123",
                "size": 107374182400,  # 100GB
                "space": {"used": 53687091200, "available": 53687091200},
            },
            {
                "name": "vol2",
                "uuid": "def456",
                "size": 214748364800,  # 200GB
                "space": {"used": 107374182400, "available": 107374182400},
            },
        ],
        "num_records": 2,
    }


@pytest.fixture
def sample_cluster_response() -> dict[str, Any]:
    """Sample ONTAP cluster API response."""
    return {
        "name": "test-cluster",
        "uuid": "cluster-uuid-123",
        "version": {"full": "NetApp Release 9.13.1", "generation": 9},
    }
