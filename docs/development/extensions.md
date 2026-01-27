---
title: Extensions
description: How to extend pynetappfoundry
audience:
  - contributors
tags:
  - development
  - extensions
---

# Extensions

This guide covers how to extend pynetappfoundry with custom functionality.

## Adding New CLI Commands

### Create a New Command Group

```python
# src/pynetappfoundry/cli/custom.py
import click
from pynetappfoundry.cli import nf

@nf.group()
def custom():
    """Custom commands."""
    pass

@custom.command()
@click.option("--name", required=True, help="Name to greet")
def greet(name: str):
    """Greet someone."""
    click.echo(f"Hello, {name}!")
```

### Register the Command

Add the import to `src/pynetappfoundry/cli.py`:

```python
from pynetappfoundry.cli.custom import custom  # noqa: F401
```

## Adding New Clients

### Create a Custom Client

```python
# src/pynetappfoundry/clients/custom/api.py
from pynetappfoundry.clients.openapi import APIWrapper
from pynetappfoundry.core.config import Config

class CustomAPIClient(APIWrapper):
    """Client for custom API."""

    def __init__(self, config: Config, name: str):
        super().__init__(config, name)
        self.base_url = config.get_endpoint(name)

    def get_resources(self) -> list[dict]:
        """Get resources from API."""
        return self._get("/resources")

    def create_resource(self, data: dict) -> dict:
        """Create a new resource."""
        return self._post("/resources", data)
```

### Export from Package

Add to `src/pynetappfoundry/__init__.py`:

```python
from pynetappfoundry.clients.custom.api import CustomAPIClient

__all__ = [
    # ... existing exports
    "CustomAPIClient",
]
```

## Adding New Database Models

### Create a Database Class

```python
# src/pynetappfoundry/db/custom.py
import sqlite3
from pathlib import Path

class CustomDB:
    """Database for custom data."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS custom_data (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def store(self, name: str, value: str) -> int:
        """Store data."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO custom_data (name, value) VALUES (?, ?)",
                (name, value)
            )
            return cursor.lastrowid

    def get(self, name: str) -> list[dict]:
        """Get data by name."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM custom_data WHERE name = ?",
                (name,)
            )
            return [dict(row) for row in cursor.fetchall()]
```

## Adding New Report Types

### Create a Report Generator

```python
# src/pynetappfoundry/reports/custom.py
from pathlib import Path
from pynetappfoundry.core.config import Config

class CustomReport:
    """Generate custom reports."""

    def __init__(self, config: Config):
        self.config = config

    def generate(self, data: list[dict], output: Path) -> None:
        """Generate report from data."""
        # Implementation here
        pass
```

## Testing Extensions

### Write Tests for Custom Code

```python
# tests/test_custom.py
import pytest
from pynetappfoundry.clients.custom.api import CustomAPIClient

@pytest.fixture
def mock_config(tmp_path):
    """Create mock configuration."""
    # Setup mock config
    pass

def test_custom_client_get_resources(mock_config):
    """Test getting resources."""
    client = CustomAPIClient(mock_config, "test")
    # Add test assertions
    pass
```

## Best Practices

1. **Follow existing patterns** - Look at existing code for examples
2. **Add type hints** - All public functions should have type annotations
3. **Write tests** - Aim for high test coverage
4. **Document public APIs** - Add docstrings to all public functions
5. **Handle errors gracefully** - Use appropriate exception types
