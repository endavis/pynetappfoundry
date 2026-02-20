"""Pytest configuration and fixtures."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True, scope="session")
def _warm_table_registry() -> None:
    """Pre-warm the table registry once per session to avoid repeated discovery."""
    from pynetappfoundry.cache.db_schema import _ensure_registry

    _ensure_registry()


@pytest.fixture
def sample_cluster_data() -> dict[str, dict[str, str]]:
    """Sample cluster data for testing."""
    return {
        "test-cluster-1": {
            "name": "test-cluster-1",
            "ip": "10.0.0.1",
            "bu": "Test",
            "env": "Dev",
        },
        "test-cluster-2": {
            "name": "test-cluster-2",
            "ip": "10.0.0.2",
            "bu": "Test",
            "env": "Prod",
        },
    }
