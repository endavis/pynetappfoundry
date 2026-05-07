# pynetappfoundry

ONTAP administration library and CLI tools.

## Installation

```bash
pip install pynetappfoundry
```

For development:

```bash
pip install -e ".[dev]"
```

## CLI Usage

pynetappfoundry provides a single CLI entry point `nf` with subcommand groups:

```bash
# License management
nf licenses check --filter '{"bu":"Business"}'
nf licenses get --config-dir /path/to/config
nf licenses savings --output-dir ./output

# Reports
nf reports space-usage --filter '{"env":"Prod"}'
nf reports locks
nf reports html

# Events
nf events get --filter '{"name":"cluster1"}'
nf events save-azure

# Metrics
nf metrics dump-dii --date 2025-04-13

# Utilities
nf utils validate
nf utils run-cmd "vol show"
nf utils sqlite-to-excel cluster1_2025-04-13_metrics.db
```

### Common Options

All commands support these global options:

- `--config-dir, -c`: Configuration directory path (default: `config`)
- `--output-dir, -o`: Output directory path
- `--debug/--no-debug`: Enable debug logging
- `--filter, -f`: JSON filter for cluster selection

### Filter Syntax

The filter option accepts JSON with AND/OR logic:

```bash
# Match all criteria
-f '{"bu":"Business", "env":"Prod", "tags":"active"}'

# AND operator for tags
-f '{"tags":"active && workload"}'

# OR operator
-f '{"app": "app1 || app2"}'

# Multiple clusters by name
-f '{"name":"cluster1 || cluster2"}'
```

## Library Usage

pynetappfoundry can also be used as a library in your own scripts:

```python
from pynetappfoundry import Config, ONTAPAPIClient, ONTAPCLI
from pynetappfoundry.db import MetricDB
from pynetappfoundry.utils import approximate_size

# Load configuration
config = Config("/path/to/config")
clusters = config.get_clusters({"env": "Prod", "bu": "Business"})

# Query clusters
for name, details in clusters.items():
    # Using the ONTAP Python SDK (via HostConnection)
    user, password = config.get_user("clusters", name)

    # Or use the CLI wrapper for SSH commands
    cli = ONTAPCLI(name, details["ip"], user, password)
    output = cli.run_command("vol show")
    cli.disconnect()

# Work with metrics database
db = MetricDB(config)
db.create_table("cluster_metrics")
db.upsert_data("cluster_metrics", {"timestamp": "2024-01-01", "read_ops": 100})
```

## Configuration

Create a `config` directory with TOML files:

### settings.toml

```toml
[settings]
[settings.clusters]
searchable_keys = ["name", "bu", "env", "app", "tags"]

[settings.SMTP]
server = "smtp.example.com"
port = 25
user = ""
password = ""
auth = "False"

[settings.licensing]
mailfrom = "netapp-alerts@example.com"
mailto = "admin@example.com"
```

### users.toml

```toml
[users.clusters]
user = "admin"
enc = "password"
```

### clusters.toml

```toml
[settings]
type = "data"

[clusters.cluster1]
name = "cluster1"
ip = "10.0.0.1"
bu = "Business"
env = "Prod"
tags = ["active", "production"]

[clusters.cluster2]
name = "cluster2"
ip = "10.0.0.2"
bu = "Business"
env = "Dev"
tags = ["active", "development"]
```

## Development

```bash
# Clone the repository
git clone https://github.com/endavis/pynetappfoundry.git
cd pynetappfoundry

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check src/

# Run type checking
mypy src/
```

## License

MIT License - see LICENSE file for details.
