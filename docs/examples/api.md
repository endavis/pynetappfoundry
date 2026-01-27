---
title: API Examples
description: Detailed Python API usage examples
audience:
  - users
tags:
  - examples
  - api
---

# API Examples

Detailed examples for using the pynetappfoundry Python API.

## Configuration Examples

### Custom Configuration Directory

```python
from pynetappfoundry import Config

# Use custom config directory
config = Config(config_dir="/path/to/config")
```

### Multiple Clusters

```python
from pynetappfoundry import Config, ONTAPAPIClient

config = Config()

# Create clients for multiple clusters
clusters = ["cluster1", "cluster2", "cluster3"]
clients = {name: ONTAPAPIClient(config, name) for name in clusters}

# Query all clusters
for name, client in clients.items():
    info = client.get_cluster_info()
    print(f"{name}: {info['version']}")
```

## ONTAP API Examples

### Get Volume Information

```python
from pynetappfoundry import Config, ONTAPAPIClient

config = Config()
client = ONTAPAPIClient(config, "cluster1")

# Get all volumes
volumes = client.get_volumes()
for vol in volumes:
    print(f"Volume: {vol['name']}, Size: {vol['size']}, Used: {vol['used']}")

# Get volumes for specific SVM
svm_volumes = client.get_volumes(svm="svm1")
```

### Get Aggregate Information

```python
# Get all aggregates
aggregates = client.get_aggregates()
for aggr in aggregates:
    pct_used = (aggr['used'] / aggr['size']) * 100
    print(f"Aggregate: {aggr['name']}, Used: {pct_used:.1f}%")
```

### Get LIF Information

```python
# Get all network interfaces
lifs = client.get_lifs()
for lif in lifs:
    print(f"LIF: {lif['name']}, IP: {lif['ip']}, Status: {lif['status']}")
```

## CLI Examples

### Run ONTAP CLI Commands

```python
from pynetappfoundry import Config, ONTAPCLI

config = Config()
cli = ONTAPCLI(config, "cluster1")

# Run system commands
output = cli.run_command("system node show")
print(output)

# Run volume commands
output = cli.run_command("volume show -fields size,used,available")
print(output)
```

### Parse CLI Output

```python
# Run command and parse output
output = cli.run_command("df -h")
lines = output.strip().split('\n')
for line in lines[1:]:  # Skip header
    parts = line.split()
    if len(parts) >= 4:
        print(f"Filesystem: {parts[0]}, Used: {parts[2]}")
```

## Database Examples

### Metrics Collection and Querying

```python
from pynetappfoundry import MetricDB
from datetime import datetime, timedelta

db = MetricDB("metrics.db")

# Store metrics
db.store_metric("cluster1", "volume_count", 150)
db.store_metric("cluster1", "aggregate_used_pct", 75.5)

# Query recent metrics
metrics = db.get_metrics(
    cluster="cluster1",
    start_time=datetime.now() - timedelta(hours=24)
)

for metric in metrics:
    print(f"{metric['name']}: {metric['value']} at {metric['timestamp']}")
```

### Event Storage and Querying

```python
from pynetappfoundry import EmsEventsDB

db = EmsEventsDB("events.db")

# Store events (usually from API fetch)
event = {
    "cluster": "cluster1",
    "time": "2024-01-15T10:30:00Z",
    "severity": "error",
    "message": "Disk failed in aggregate aggr1"
}
db.store_event(event)

# Query events
errors = db.get_events(severity="error", limit=100)
for error in errors:
    print(f"[{error['time']}] {error['message']}")
```

## Error Handling

### Handle Connection Errors

```python
from pynetappfoundry import Config, ONTAPAPIClient
from pynetappfoundry.clients.ontap.cli import CLICommandError

config = Config()

try:
    client = ONTAPAPIClient(config, "cluster1")
    volumes = client.get_volumes()
except ConnectionError as e:
    print(f"Failed to connect: {e}")
except CLICommandError as e:
    print(f"CLI command failed: {e}")
```

### Retry Logic

```python
import time
from pynetappfoundry import Config, ONTAPAPIClient

config = Config()

def get_volumes_with_retry(cluster, max_retries=3):
    for attempt in range(max_retries):
        try:
            client = ONTAPAPIClient(config, cluster)
            return client.get_volumes()
        except ConnectionError:
            if attempt < max_retries - 1:
                time.sleep(5 * (attempt + 1))
            else:
                raise
    return []

volumes = get_volumes_with_retry("cluster1")
```
