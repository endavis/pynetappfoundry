---
title: pynetappfoundry Documentation
description: ONTAP administration library and CLI tools
audience:
  - users
  - contributors
tags:
  - overview
  - getting-started
---

# pynetappfoundry Documentation

ONTAP administration library and CLI tools for NetApp storage management.

## Overview

pynetappfoundry provides a comprehensive Python library and command-line interface for managing NetApp ONTAP clusters. It supports both REST API and SSH CLI access for flexible administration tasks.

## Preferred ONTAP Access Patterns

For new CLI commands, reports, and scripts that read or write ONTAP data, use these patterns in priority order:

1. **`ClusterEntry.ontap`** — cached high-level reads with on-demand `DataSource` fallback and `--live` bypass ([ADR-0010](decisions/0010-clusterentry-and-namespace-access-pattern.md))
2. **`QuerySet(config=)` / `DataSource`** — ad-hoc filtered/ordered/limited live reads, plus mutations ([ADR-0013](decisions/0013-datasource-as-a-thin-facade-over-the-collector.md))
3. **`netapp_ontap` SDK** — fallback only for endpoints not yet covered by a `TypeMapping`

See [DataSource Guide](usage/data-source.md), [Query Layer Guide](usage/query-layer.md), and [ONTAP Access Patterns](usage/ontap-access-patterns.md) for details.

## Quick Links

- [Installation Guide](getting-started/installation.md)
- [Usage Guide](usage/basics.md)
- [Configuration Schema](reference/config-schema.md)
- [CLI Reference](reference/cli.md)
- [API Reference](reference/api.md)
- [Contributing](https://github.com/endavis/pynetappfoundry/blob/main/.github/CONTRIBUTING.md)

## Features

- **License Management** - Track and report on cluster licenses
- **Space Reporting** - Generate detailed storage capacity reports
- **Event Tracking** - Monitor and analyze EMS events
- **Metrics Collection** - Gather performance and usage metrics
- **Multi-cluster Support** - Manage multiple ONTAP clusters
- **REST API Support** - Full ONTAP REST API integration via netapp-ontap SDK
- **SSH CLI Support** - Direct CLI access via Paramiko
- **Auto Dependency Sync** - Post-merge and post-checkout hooks keep dependencies in sync
- **Mutation Testing** - mutmut for test suite effectiveness analysis
- **Property-Based Testing** - Hypothesis for invariant-based testing with random inputs
- **Benchmark Tracking** - Historical CI benchmarks with regression detection
- **SBOM Generation** - CycloneDX Software Bill of Materials for compliance and security

## Quick Start

```bash
# Install from PyPI
pip install pynetappfoundry

# Or install with uv
uv add pynetappfoundry

# Run CLI
nf --help

# Optional: cache a cluster defined in ./config for fast reads
nf cache refresh cluster1
```

```python
from typing import cast

from pynetappfoundry import Config, ONTAPAPIClient
from pynetappfoundry.core.cluster_entry import ClusterEntry

# Load the configuration directory (default: ./config)
config = Config()
cluster = cast(ClusterEntry, config.data["clusters"]["cluster1"])

# Preferred: read cluster data through ClusterEntry.ontap. It serves the
# cache that `nf cache refresh` fills, and fetches live when there is none.
metadata = cluster.ontap
if metadata is not None:
    print(metadata.cluster.ontap_version)

# Low level: call the ONTAP REST API directly (cluster first, then config)
client = ONTAPAPIClient(cluster, config)
print(client.call_endpoint(path_template="/cluster?fields=name,version"))
```

## Documentation Sections

### For Users

- **[Installation](getting-started/installation.md)** - How to install the package
- **[Usage Guide](usage/basics.md)** - How to use the package
- **[DataSource Guide](usage/data-source.md)** - Unified entry point for reading cluster data
- **[ONTAP Access Patterns](usage/ontap-access-patterns.md)** - Guide to choosing between SDK, SSH, and REST access
- **[Configuration Schema](reference/config-schema.md)** - Complete TOML configuration reference
- **[CLI Reference](reference/cli.md)** - Command-line interface documentation
- **[API Reference](reference/api.md)** - Python API documentation
- **[Cache System](reference/cache.md)** - Cluster metadata caching and history tracking
- **[Compliance Checks](usage/compliance-checks.md)** - Configure and run config-driven compliance checks

### For Contributors

- **[Contributing Guide](https://github.com/endavis/pynetappfoundry/blob/main/.github/CONTRIBUTING.md)** - Development workflow, coding standards, and best practices
- **[Code of Conduct](https://github.com/endavis/pynetappfoundry/blob/main/.github/CODE_OF_CONDUCT.md)** - Community guidelines
- **[AI Agent Setup](development/AI_SETUP.md)** - Setup guide for AI coding assistants
- **[Development Tasks](development/doit-tasks-reference.md)** - doit task runner reference

## Support

- **Issues:** [GitHub Issues](https://github.com/endavis/pynetappfoundry/issues)
- **Discussions:** [GitHub Discussions](https://github.com/endavis/pynetappfoundry/discussions)
- **Security:** See [SECURITY.md](https://github.com/endavis/pynetappfoundry/blob/main/.github/SECURITY.md)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/endavis/pynetappfoundry/blob/main/LICENSE) file for details.
