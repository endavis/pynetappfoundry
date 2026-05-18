---
title: ONTAP Access Patterns
description: Guide to choosing between the three ONTAP access methods
audience:
  - users
  - contributors
tags:
  - ontap
  - api
  - ssh
  - sdk
---

# ONTAP Access Patterns

pynetappfoundry provides three different ways to interact with ONTAP clusters. Each pattern has specific use cases, advantages, and trade-offs. This guide helps you choose the right approach for your task.

## Overview

| Pattern | Connection | Best For |
|---------|------------|----------|
| `ClusterEntry.ontap` namespace | Cache DB + HTTPS REST (+ SSH for `cloud`) | High-level reads of cached cluster metadata with on-demand DataSource fallback |
| `QuerySet` + `Mutation` | HTTPS REST | Type-safe ONTAP queries and writes with model attribute translation (see [Query Layer](query-layer.md)) |
| `netapp_ontap` SDK | HTTPS REST | Fallback for endpoints not yet covered by a `TypeMapping` (most callers should use `ClusterEntry.ontap` or `QuerySet`/`DataSource` instead) |
| `ONTAPCLI` | SSH | Ad-hoc CLI commands, operations not in REST API |
| `APIWrapper` | HTTPS REST | Custom queries, OpenAPI-based workflows, DII integration |

## Pattern Details

### 1. ClusterEntry Namespace Access (Recommended for High-Level Reads)

The `ClusterEntry.ontap` namespace is the highest-level way to read cluster metadata. It transparently serves data from a per-cluster SQLite cache when available and falls back to an on-demand live fetch when the cache is missing or has been explicitly bypassed. This is the pattern new CLI commands and reports should prefer for read-only workloads.

See [ADR-0010](../decisions/0010-clusterentry-and-namespace-access-pattern.md) for the architectural rationale and [ADR-0009](../decisions/0009-sql-table-storage.md) for the cache storage model.

**When to Use:**

- Reading cluster-wide metadata (licenses, nodes, storage, network, protocols, cloud placement) from CLI commands, reports, or scripts
- Any workload that benefits from the cache (dashboards, iterative development, bulk reporting across many clusters)
- Cases where "live, but only if the cache is stale" is the desired default
- New CLI commands that need an on-demand freshness override via `--live`

**Advantages:**

- Single, uniform entry point: `config.data["clusters"][name].ontap`
- Sub-millisecond cache reads from per-cluster SQLite (per-model SQL tables, see ADR-0009)
- Transparent fallback: a cache miss triggers `DataSource` to fetch the needed field group live — callers do not change their code
- Namespace separation (`.ontap`, and reserved `.occm` / `.aiqum` / `.dii`) prevents naming collisions between TOML config keys and fetched data from different API sources
- `--live` / `Config(no_cache=True)` toggles the bypass without requiring alternative code paths

**Limitations:**

- Read-only; writes must use `Mutation` (Pattern #2) or the `netapp_ontap` SDK (Pattern #3)
- Cached data freshness is bounded by the last refresh; use `--live` when freshness is critical
- Only the `cloud` field group requires SSH (REST first, with an SSH `virtual-machine instance show` fallback). All other field groups are REST-only.
- As of this writing, `nf licenses get` is the only shipping CLI migrated to this pattern; other field-group attributes listed below are valid but are illustrative until further CLIs are migrated

#### Three Access Modes

All three modes use the same call site — `cluster_entry.ontap` — and differ only in how `Config` is constructed and whether a cache DB exists for the cluster.

1. **Cache hit** — the per-cluster SQLite cache exists, so `LazyClusterMetadata` serves attributes directly from DB rows. Sub-millisecond reads. This is the default on any cluster whose cache has been populated.
2. **Cache miss → on-demand fetch** — no cache DB (or the requested field group is absent). `LazyClusterMetadata` delegates to `DataSource` for live data. One REST round-trip per field group requested.
3. **Forced live** — the caller built `Config(no_cache=True)` (the CLI sets this when `--live` is passed via `@with_config`). `ClusterEntry.ontap` skips the DB entirely and returns a fetcher-only proxy, so every attribute access fetches live from the ONTAP API (or SSH for `cloud`).

#### Available Field Groups

`LazyClusterMetadata` exposes the same attributes as `CachedClusterMetadata`:

| Attribute | Type | Source |
|---|---|---|
| `cloud` | `list[CloudMetadata]` | REST, SSH fallback (`virtual-machine instance show`) |
| `cluster` | `ClusterInfo` | REST |
| `nodes` | `list[OntapNodeResponse]` | REST |
| `network` | `NetworkInfo` | REST |
| `storage` | `StorageInfo` | REST |
| `license_packages` | `list[OntapLicensePackageResponse]` | REST |
| `mediator` | `OntapMediatorResponse` | REST |
| `relationships` | `RelationshipsInfo` | REST |
| `protocols` | `ProtocolsInfo` | REST |

Only `cloud` requires SSH, and only as a fallback when the REST endpoint does not return usable data. All other field groups are REST-only.

#### Performance Trade-offs

| Mode | Latency | Freshness | Use when |
|---|---|---|---|
| Cache hit | sub-ms (SQLite) | Bounded by last refresh | Reports, dashboards, dev iteration |
| Cache miss, on-demand fetch | seconds (single REST call per field group) | Live | First access after cache reset or new field group |
| Forced live (`--live`) | seconds to tens of seconds per group | Always live | Verifying remediation, audits, troubleshooting |

#### Example Usage

The canonical pattern — used by `nf licenses get` — is to grab `cluster_entry.ontap` into a local variable, null-check it, and then read field-group attributes off the local.

```python
from typing import cast

from pynetappfoundry.core.cluster_entry import ClusterEntry
from pynetappfoundry.core.config import Config

# Cache-first (default): served from SQLite when available, otherwise
# fetched on demand via DataSource.
config = Config()
cluster_entry = cast(ClusterEntry, config.data["clusters"]["mycluster"])
metadata = cluster_entry.ontap  # LazyClusterMetadata | None
if metadata is None:
    # No cache and no live fetcher could be built (e.g., missing credentials).
    raise SystemExit("No cached or fetchable data for mycluster")

packages = metadata.license_packages or []
for pkg in packages:
    for lic in pkg.licenses:
        print(pkg.name, lic.owner, lic.state)
```

`cluster_entry.ontap` is a `@cached_property`, so the local-variable pattern above is for clarity and null-checking — repeated `.ontap` accesses on the same `ClusterEntry` do not re-trigger loads.

Forcing a live fetch bypasses the cache entirely:

```python
from typing import cast

from pynetappfoundry.core.cluster_entry import ClusterEntry
from pynetappfoundry.core.config import Config

# Forced live: every .ontap access fetches from the ONTAP API (or SSH for `cloud`).
config = Config(no_cache=True)
cluster_entry = cast(ClusterEntry, config.data["clusters"]["mycluster"])
metadata = cluster_entry.ontap
fresh_packages = metadata.license_packages if metadata else []
```

Other field-group attributes are valid per `CachedClusterMetadata` but not yet consumed by any shipping CLI — the following examples are illustrative:

```python
# Illustrative: not yet used by any shipping CLI command as of this writing.
if metadata is not None:
    volumes = metadata.storage.volumes
    node_count = len(metadata.nodes)
    cloud_placements = metadata.cloud
```

**CLI equivalent:**

```bash
nf licenses get                # cache-first (default)
nf licenses get --live         # bypass cache, fetch live for every cluster
```

The `--live` flag is wired through `@with_config`, which constructs `Config(no_cache=True)` so that every `ClusterEntry` built from that `Config` inherits the bypass.

#### Why Namespace Separation Exists

`ClusterEntry` is a `MutableMapping` that wraps the raw TOML config dict for a cluster, so existing dict-style access (`cluster_entry["name"]`, `cluster_entry["ip"]`) keeps working. Fetched metadata lives under dedicated namespaces (`.ontap` today, `.occm` / `.aiqum` / `.dii` reserved) so that:

- TOML config keys never collide with attribute names fetched from different API sources
- Each namespace can carry its own cache, fetcher, and lifecycle
- Future BlueXP/OCCM, AIQUM, or DII data can be added without reshaping the cluster config surface

**Commands Using This Pattern:**

- `nf licenses get` — reads `metadata.license_packages` (supports `--live`)

---

### 2. QuerySet + Query + Mutation (Query Layer)

`pynetappfoundry.query` is a thin, fluent layer over the ONTAP REST API that uses the project's `TypeMapping` metadata to translate model attribute filters into API requests and to parse responses back into Pydantic models. It covers collection reads (`QuerySet`), RPC-style POST reads (`Query`), writes (`Mutation`), async job polling (`JobTracker`), relationship traversal (`related` / `related_one`), and on-demand realtime field access.

Choose `cluster_entry.ontap` for cached field-group reads with a `--live` bypass, and reach for `QuerySet`, `Query`, or `Mutation` whenever you need ad-hoc filtering, POST-for-data RPC calls, or any write operation.

See the dedicated [Query Layer](query-layer.md) guide for the full API reference, worked examples, and exception semantics.

---

### 3. netapp_ontap SDK (Fallback)

NetApp's official Python SDK provides ORM-like objects for ONTAP resources. Reach for it only when no `TypeMapping` exists for the endpoint you need, or for mutations on uncovered resources. For everything else, prefer `ClusterEntry.ontap` (Pattern #1) for cached high-level reads or `QuerySet`/`DataSource` (Pattern #2) for ad-hoc filtered/ordered/limited live reads — see [ADR-0010](../decisions/0010-clusterentry-and-namespace-access-pattern.md) and [ADR-0013](../decisions/0013-datasource-as-a-thin-facade-over-the-collector.md).

**When to Use:**

- Generating reports (licenses, space usage, cluster health)
- Retrieving structured data (volumes, aggregates, nodes)
- Operations that benefit from typed objects and IDE autocompletion
- When you need reliable, well-tested API interactions

**Advantages:**

- Official NetApp support and documentation
- Type-safe objects with clear attributes
- Handles pagination automatically
- Well-defined error handling

**Limitations:**

- Requires `netapp-ontap` package
- Some advanced CLI operations not available via REST
- Less flexible for custom queries

**Example Usage:**

```python
# Modern equivalent: DataSource is the unified read accessor (ADR-0013).
# Cache-first by default; pass source="live" to bypass the cache.
from pynetappfoundry.core.config import Config
from pynetappfoundry.data.source import DataSource
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume

config = Config()
ds = DataSource(config)
for volume in ds.query(OntapVolume, cluster="mycluster", source="auto"):
    print(volume.name, volume.size)
```

When `cluster_entry.ontap.<field_group>` is available, prefer that — see Pattern #1 for the canonical cached high-level reads. Direct `netapp_ontap` SDK usage (`HostConnection`, `Volume.get_collection()`, etc.) is a fallback for endpoints not yet covered by a `TypeMapping`; consult the upstream NetApp documentation when you need it.

**Commands Using This Pattern:**

- `nf licenses get/check/savings` - License management
- `nf events get/save-azure` - EMS event retrieval
- `nf reports locks/space-usage/html` - Report generation
- `nf utils validate` - Cluster validation

**Configuration Required:**

```toml
# In clusters data file (e.g., clusters.toml)
[mycluster]
name = "mycluster"
ip = "192.168.1.100"

# In users data file (e.g., users.toml)
[clusters.mycluster]
user = "admin"
password = "base64_encoded_password"
```

---

### 4. ONTAPCLI (SSH Access)

Direct SSH connection using Paramiko for executing ONTAP CLI commands.

**When to Use:**

- Running CLI commands not available via REST API
- Ad-hoc administrative tasks
- Debugging or troubleshooting
- Commands that require interactive prompts
- When you need raw CLI output

**Advantages:**

- Access to all CLI commands (including advanced/hidden)
- Familiar CLI syntax for ONTAP administrators
- Can handle interactive prompts
- Useful for automation of CLI-only operations

**Limitations:**

- Slower than REST (SSH overhead)
- Output parsing required (text-based)
- Connection management overhead
- Less structured error handling

**Example Usage:**

```python
from pynetappfoundry.clients.ontap.cli import ONTAPCLI

# Connect via SSH
config = Config()
cluster = config.clusters["mycluster"]
user = config.get_user("clusters", cluster.name)

cli = ONTAPCLI(
    name=cluster.name,
    host_or_ip=cluster.ip,
    username=user.user,
    password=user.get_password()
)

try:
    cli.connect()

    # Run a command
    output = cli.run_command("volume show -fields size,used")
    print(output)

    # Run and parse output
    volumes = cli.run_command_and_parse("volume show")
    for vol in volumes:
        print(f"Volume: {vol['Vserver']}/{vol['Volume']}")

finally:
    cli.disconnect()
```

**Commands Using This Pattern:**

- `nf utils run-cmd` - Execute arbitrary CLI commands

**Configuration Required:**

Same as netapp_ontap SDK (cluster IP and credentials).

---

### 5. APIWrapper / ONTAPAPIClient (Custom REST)

Custom OpenAPI-based REST client that works with any OpenAPI/Swagger specification.

**When to Use:**

- Querying Data Infrastructure Insights (DII) API
- Custom REST endpoints not covered by the SDK
- When you need fine-grained control over requests
- Working with OpenAPI 2.0 (Swagger) specifications
- Building extensible API integrations

**Advantages:**

- Works with any OpenAPI-compliant API
- Request body validation against schema
- Endpoint discovery and parameter suggestions
- Configurable SSL verification and timeouts
- Reusable for multiple API types (ONTAP, DII, custom)

**Limitations:**

- No response validation (yet)
- Requires OpenAPI specification files
- More setup than SDK for simple operations
- Returns raw dictionaries (no typed objects)

**Example Usage:**

```python
from pynetappfoundry.clients.ontap.api import ONTAPAPIClient

# Using ONTAPAPIClient (ONTAP-specific wrapper)
config = Config()
cluster = config.clusters["mycluster"]

client = ONTAPAPIClient(cluster, config)

# Call an endpoint
response = client.call_endpoint(
    path="/storage/volumes",
    method="GET",
    query_params={"fields": "name,size,state"}
)

for volume in response.get("records", []):
    print(f"Volume: {volume['name']}")
```

```python
from pynetappfoundry.clients.dii.api import DIIAPIClient

# Using DIIAPIClient for Data Infrastructure Insights
config = Config()
dii_config = config.diis["production"]

client = DIIAPIClient(dii_config, config)

# Query DII workload-volume timeseries
response = client.call_endpoint(
    path="/lake/query/timeseries",
    method="POST",
    body={
        "category": "netapp_ontap",
        "measurement": "workload_volume",
        "metric": "read_ops",
        "filter": 'vserver_name = "svm1" AND volume_name = "vol1"',
        "fromTimeMs": 1744416000000,
        "toTimeMs": 1744675200000,
        "timeAggregationInterval": "60s",
    },
)
```

**Commands Using This Pattern:**

- `nf metrics dump-dii` - Query per-volume DII metrics via `/lake/query/timeseries`

**Configuration Required:**

```toml
# In settings.toml
[ontapapi.general]
base_api_path = "/api"

[ontapapi.schema]
location = "/path/to/apis/ontap"
filename = "all.json"

[diiapi.general]
base_api_path = "/rest/v1"

[diiapi.schema]
location = "/path/to/apis/dii"
filename = "all.json"
```

---

## Decision Matrix

Use this matrix to choose the right pattern:

| Scenario | Recommended Pattern | Reason |
|----------|---------------------|--------|
| Read cached cluster metadata (licenses, nodes, storage, etc.) | `ClusterEntry.ontap` | Sub-ms SQLite reads, transparent fallback |
| Read cluster metadata when the cache is empty | `ClusterEntry.ontap` | On-demand `DataSource` fallback, no caller changes needed |
| Force-live read of cluster metadata | `ClusterEntry.ontap` with `Config(no_cache=True)` / `--live` | Bypasses cache entirely, same call site |
| Query ONTAP resources | `QuerySet` | Type-safe filtering, model attribute translation — see [Query Layer](query-layer.md) |
| Create/update/delete resources | `Mutation` | Nested JSON from flat attrs, retry safety — see [Query Layer](query-layer.md) |
| List volumes/aggregates | `QuerySet` | Fluent API, field projection, pagination — see [Query Layer](query-layer.md) |
| Fetch live IOPS/latency metrics | `fetch_realtime` | On-demand realtime fields — see [Query Layer](query-layer.md) |
| Poll metrics over time | `watch_realtime` | Generator-based polling — see [Query Layer](query-layer.md) |
| Bulk data export | `QuerySet` | Handles pagination, typed results — see [Query Layer](query-layer.md) |
| Generate a report from cached cluster metadata | `ClusterEntry.ontap` | Sub-ms cache reads with `--live` bypass (see Pattern #1) |
| Check license status | `ClusterEntry.ontap` | `nf licenses get` reads `metadata.license_packages`; supports `--live` |
| Run CLI-only command | `ONTAPCLI` | No REST equivalent |
| Debug cluster issue | `ONTAPCLI` | Full CLI access |
| Query DII metrics | `APIWrapper` | DII uses different API |
| Custom REST endpoint | `APIWrapper` | Flexible, schema-validated |
| Interactive troubleshooting | `ONTAPCLI` | Familiar CLI interface |

## Configuration Flow

All patterns share a common configuration flow:

```
┌─────────────────┐
│  settings.toml  │ ← API settings (paths, timeouts, SSL)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  clusters.toml  │ ← Cluster definitions (name, IP)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   users.toml    │ ← Credentials (username, encoded password)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Config class   │ ← Unified access to all configuration
└────────┬────────┘
         │
         ├──► ClusterEntry.ontap ──► LazyClusterMetadata
         │                              │
         │                              ├──► cache DB (per-cluster SQLite)
         │                              │      (cache hit — sub-ms reads)
         │                              │
         │                              └──► DataSource
         │                                     (cache miss or no_cache=True)
         │                                     │
         │                                     └──► ONTAP REST API
         │
         ├──► netapp_ontap SDK (HostConnection)
         ├──► ONTAPCLI (SSH connection)
         └──► APIWrapper (REST client)
```

## Best Practices

1. **Prefer the cached / unified accessors** — Reach for `ClusterEntry.ontap` (Pattern #1) for cached cluster metadata reads and `QuerySet`/`DataSource` (Pattern #2) for ad-hoc queries. Drop down to the `netapp_ontap` SDK only when no `TypeMapping` covers the endpoint.

2. **Use SSH sparingly** - Reserve `ONTAPCLI` for operations that genuinely require CLI access.

3. **Validate SSL in production** - Set `verify=True` or provide a CA bundle for production environments.

4. **Handle credentials securely** - Use the Config class's credential management rather than hardcoding passwords.

5. **Close connections** - Always use context managers or try/finally to ensure connections are closed.

## See Also

- [Configuration Schema](../reference/config-schema.md) - Complete configuration reference
- [Usage Guide](basics.md) - General usage patterns
- [CLI Reference](../reference/cli.md) - Available CLI commands
- [ADR-0010: ClusterEntry and namespace access pattern](../decisions/0010-clusterentry-and-namespace-access-pattern.md) - Rationale for the `ClusterEntry.ontap` namespace design
- [ADR-0009: SQL table storage](../decisions/0009-sql-table-storage.md) - Per-model SQL table layout backing the cache
- [DataSource Guide](data-source.md) — unified read accessor for all cluster data
- [Query Layer Guide](query-layer.md) — `QuerySet`, `Mutation`, realtime fields
- [ADR-0013: DataSource as a Thin Facade Over the Collector](../decisions/0013-datasource-as-a-thin-facade-over-the-collector.md) — current architectural direction for `DataSource`
