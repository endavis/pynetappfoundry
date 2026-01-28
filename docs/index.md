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

## Quick Start

```bash
# Install from PyPI
pip install pynetappfoundry

# Or install with uv
uv add pynetappfoundry

# Run CLI
nf --help
```

```python
from pynetappfoundry import ONTAPAPIClient, Config

# Initialize configuration
config = Config()

# Connect to ONTAP cluster
client = ONTAPAPIClient(config, "cluster1")
```

## Documentation Sections

### For Users

- **[Installation](getting-started/installation.md)** - How to install the package
- **[Usage Guide](usage/basics.md)** - How to use the package
- **[ONTAP Access Patterns](usage/ontap-access-patterns.md)** - Guide to choosing between SDK, SSH, and REST access
- **[Configuration Schema](reference/config-schema.md)** - Complete TOML configuration reference
- **[CLI Reference](reference/cli.md)** - Command-line interface documentation
- **[API Reference](reference/api.md)** - Python API documentation

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
