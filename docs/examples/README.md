---
title: Examples
description: Code examples for pynetappfoundry
audience:
  - users
tags:
  - examples
  - tutorial
---

# Examples

This section contains example code demonstrating common use cases for pynetappfoundry.

## Quick Examples

### Connect to a Cluster

```python
from pynetappfoundry import Config, ONTAPAPIClient

# Load configuration
config = Config()

# Create client
client = ONTAPAPIClient(config, "cluster1")

# Get cluster info
info = client.get_cluster_info()
print(f"Cluster: {info['name']}")
```

### Run CLI Commands

```python
from pynetappfoundry import Config, ONTAPCLI

config = Config()
cli = ONTAPCLI(config, "cluster1")

# Run a command
output = cli.run_command("volume show -fields size,used")
print(output)
```

### Collect Metrics

```python
from pynetappfoundry import MetricDB, ONTAPAPIClient, Config

config = Config()
client = ONTAPAPIClient(config, "cluster1")
db = MetricDB("metrics.db")

# Collect volume metrics
volumes = client.get_volumes()
for vol in volumes:
    db.store_metric("cluster1", f"volume_{vol['name']}_used", vol['used'])
```

### Monitor Events

```python
from pynetappfoundry import EmsEventsDB, ONTAPAPIClient, Config

config = Config()
client = ONTAPAPIClient(config, "cluster1")
db = EmsEventsDB("events.db")

# Fetch and store events
events = client.get_ems_events(hours=24)
for event in events:
    db.store_event(event)

# Query errors
errors = db.get_events(severity="error")
```

## CLI Examples

### License Management

```bash
# List all licenses
nf licenses list

# Export to Excel
nf licenses export --format xlsx -o licenses.xlsx
```

### Report Generation

```bash
# Generate space report
nf reports space --all-clusters

# Generate volume report for specific SVM
nf reports volume --cluster cluster1 --svm svm1 -o volumes.html
```

### Event Monitoring

```bash
# Fetch recent events
nf events fetch --hours 24 --all-clusters

# Export error events
nf events export --severity error --format csv -o errors.csv
```

## More Examples

- [API Examples](api.md) - Detailed API usage examples
