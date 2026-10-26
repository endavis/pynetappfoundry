# pynetappfoundry

[![CI](https://github.com/endavis/pynetappfoundry/actions/workflows/ci.yml/badge.svg)](https://github.com/endavis/pynetappfoundry/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/endavis/pynetappfoundry/branch/main/graph/badge.svg)](https://codecov.io/gh/endavis/pynetappfoundry)
[![PyPI version](https://badge.fury.io/py/pynetappfoundry.svg)](https://badge.fury.io/py/pynetappfoundry)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

ONTAP administration library and CLI tools for NetApp storage management.

## Features

- **Multi-cluster support** - Manage many ONTAP clusters from one YAML configuration
- **REST and SSH access** - ONTAP REST API via the `netapp-ontap` SDK, and direct CLI access via Paramiko
- **Metadata cache** - Cached cluster reads with on-demand live fallback (`nf cache`)
- **Reports** - License, space, CIFS and event reporting
- **Metrics and events** - Collect metrics and track EMS events in local databases

## Installation

```bash
pip install pynetappfoundry

# Or with uv
uv add pynetappfoundry
```

See the [Installation Guide](docs/getting-started/installation.md) for installing from source.

## Quick Start

### CLI

The package installs the `nf` command:

```bash
nf --help                       # List command groups
nf --config-dir ./config --help # Point at a configuration directory (or set NF_CONFIG_DIR)
```

Command groups: `cache`, `cifs`, `config`, `events`, `licenses`, `metrics`, `reports`, `utils`.
See the [CLI Reference](docs/reference/cli.md).

### Library

```python
from pynetappfoundry import Config

# Load configuration from the default config/ directory
config = Config()

# Find clusters by attribute
prod_clusters = config.search("clusters", {"env": "Prod"})
```

For reading and writing ONTAP data, see [ONTAP Access Patterns](docs/usage/ontap-access-patterns.md),
the [DataSource Guide](docs/usage/data-source.md) and the [Query Layer Guide](docs/usage/query-layer.md).

## Documentation

📚 **Full documentation is available in the [docs/](docs/) directory**

Build and view locally:
```bash
doit docs_serve  # Opens at http://127.0.0.1:8000
```

Key documentation files:
- [Installation Guide](docs/getting-started/installation.md) - Setup instructions
- [Usage Guide](docs/usage/basics.md) - Configuration and library usage
- [Configuration Schema](docs/reference/config-schema.md) - Configuration file reference
- [CLI Reference](docs/reference/cli.md) - `nf` command reference
- [API Reference](docs/reference/api.md) - Complete API documentation

## Development Setup

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- [direnv](https://direnv.net/) - Automatic environment variable loading (optional but recommended)

### Quick Start

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone https://github.com/endavis/pynetappfoundry.git
cd pynetappfoundry

# Create virtual environment and install dependencies
uv sync --all-extras --dev

# Install pre-commit hooks
doit pre_commit_install

# Optional: Install direnv for automatic environment management
# macOS:
brew install direnv

# Linux (using doit helper):
doit install_direnv

# Hook direnv into your shell (one-time setup)
# Bash:
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
source ~/.bashrc

# Zsh:
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
source ~/.zshrc

# Allow direnv to load .envrc
direnv allow

# Optional: Create .envrc.local for personal overrides
cp .envrc.local.example .envrc.local
```

## Versioning & Releases

This project uses automated versioning and releases powered by `commitizen` and `hatch-vcs`.

- **Single Source of Truth:** The Git tag is the definitive version. `pyproject.toml` and `_version.py` are generated at build time from tags (no manual edits).
- **Versioning Scheme:**
    - **Production:** Standard SemVer (e.g., `v1.0.0`).
    - **Development:** SemVer Pre-release (e.g., `v1.0.0-alpha.1`, `v1.0.0-beta.0`).

### Keeping Up to Date with the Template

This project is built from [pyproject-template](https://github.com/endavis/pyproject-template). To check for template improvements:

```bash
python tools/pyproject_template/check_template_updates.py
```

This compares your project against the latest template and shows what's changed.

📖 See [Keeping Up to Date](docs/template/updates.md) for the update workflow.

### Creating a Release

**Production Release (PyPI):**
```bash
doit release
```
This automated task will:
1.  Calculate the next version based on conventional commits.
2.  Update `CHANGELOG.md`, merging any pre-release entries (commitizen `--merge-prerelease`).
3.  Create a git tag (e.g., `v1.0.0`).
4.  Push commits and tags to GitHub, triggering the `release` workflow.

**Development/Pre-release (TestPyPI):**
```bash
doit release_dev              # Defaults to alpha
doit release_dev --type beta  # Specify type (alpha, beta, rc)
```
This automated task will:
1.  Bump the version to the next pre-release (e.g., `v1.0.0-alpha.1`).
2.  Update `CHANGELOG.md` for the prerelease.
3.  Create a prerelease git tag (e.g., `v1.0.0-alpha.1`).
4.  Push to GitHub, triggering the `testpypi` workflow.

### Environment Variables

This project uses direnv for automatic environment management. After setup:
- `.envrc` (committed) contains project defaults and is loaded automatically
- `.envrc.local` (git-ignored) is for personal overrides and credentials
- Environment variables are set automatically when you enter the project directory
- Virtual environment is activated automatically

### Manual Setup (without direnv)

If you prefer not to use direnv:

```bash
# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Set environment variables manually
export UV_CACHE_DIR="$(pwd)/tmp/.uv_cache"

# Install dependencies
uv sync --all-extras --dev
```

## Available Tasks

View all available tasks:

```bash
doit list
```

### Quick Commands

```bash
# Testing
doit test          # Run tests (parallel execution with pytest-xdist)
doit coverage      # Run tests with coverage report

# Code Quality
doit format        # Format code with ruff
doit lint          # Run linting
doit type_check    # Run type checking with mypy
doit check         # Run ALL checks (format, lint, type check, security, audit, spell, test)

# Security
doit security      # Run security scan with bandit
doit audit         # Run dependency vulnerability audit
doit spell_check   # Check for typos with codespell
doit licenses      # Check licenses of dependencies

# Code Formatting
doit fmt_pyproject # Format pyproject.toml with pyproject-fmt

# Version Management (Commitizen)
doit commit        # Interactive commit with conventional format
doit release       # Production release (commitizen-driven)
doit release_dev   # Pre-release/TestPyPI (commitizen-driven)

# Documentation
doit docs_serve    # Serve docs locally with live reload
doit docs_build    # Build documentation site
doit docs_deploy   # Deploy docs to GitHub Pages

# Maintenance
doit cleanup       # Clean build artifacts and caches
doit update_deps   # Update dependencies and run tests
```

See the [Usage Guide](docs/usage/basics.md) for comprehensive documentation of all development workflows.

## Running Tests

```bash
# Run all tests (parallel execution - fast!)
doit test

# Run with coverage
doit coverage

# View coverage report
open tmp/htmlcov/index.html

# Advanced: Run specific test directly
uv run pytest tests/unit/cli/test_main.py -v
```

## Code Quality

This project includes comprehensive tooling:

### Core Tools
- **uv** - Fast Python package installer and dependency manager
- **ruff** - Extremely fast Python linter and formatter
- **mypy** - Static type checker with strict mode
- **pytest** - Testing framework with parallel execution (pytest-xdist)

### Quality & Security
- **bandit** - Security vulnerability scanner
- **codespell** - Spell checker for code and documentation
- **pip-audit** - Dependency vulnerability auditor
- **pip-licenses** - License compliance checker
- **pre-commit** - Git hooks for automated quality checks
- **pyproject-fmt** - Keep pyproject.toml formatted and organized
- **commitizen** - Enforce conventional commit message standards

### Documentation
- **MkDocs** - Documentation site generator
- **mkdocs-material** - Material Design theme for MkDocs

Run all quality checks:

```bash
doit check
```

### Pre-commit Hooks

Install hooks to run checks automatically before each commit:

```bash
doit pre_commit_install
```

Hooks include:
- Code formatting (ruff)
- Type checking (mypy)
- Security scanning (bandit)
- Spell checking (codespell)
- YAML/TOML validation
- Trailing whitespace removal
- Private key detection

## AI Agent Support

This template supports **Claude Code**, **GitHub Copilot CLI**, **Codex CLI**, and **Antigravity CLI** (`agy`). All four agents ship a complete cross-agent review command surface for self-action and cross-agent delegation, with slash names that differ by host: Claude uses colon separators (`/claude:review`, `/claude:adversarial-review`); Copilot and Codex use hyphen separators (`/copilot-review`, `$codex-adversarial-review`) because their command surface is skills and skill names cannot contain colons; Antigravity activates skills by `description:` match with no prefix. The shared workflow is: say "implement issue N" → review the PR → `doit pr_merge --auto-close`.

### Requirements

> **Important:** [GitHub CLI (`gh`)](https://cli.github.com/) is **required** for AI-assisted workflows.
>
> Many `doit` tasks use `gh` for issue creation, PR management, and repository operations.
> Install and authenticate before using AI agents:
> ```bash
> # Install (macOS)
> brew install gh
>
> # Install (Linux) - see https://github.com/cli/cli/blob/trunk/docs/install_linux.md
>
> # Authenticate
> gh auth login
> ```

### Features

- **AGENTS.md** - Instructions and protocols for AI agents
- **Dangerous command blocking** - Hooks prevent destructive operations (force push to main, branch deletion, etc.)
- **Workflow automation** - `doit issue` and `doit pr` for GitHub operations

See [AI Agent Setup](docs/development/AI_SETUP.md) and [AI Command Blocking](docs/development/ai/command-blocking.md) for details.

## Contributing

See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for the development workflow (issue → branch → PR),
commit message format and code standards. Run `doit check` before opening a pull request.

See [CHANGELOG.md](CHANGELOG.md) for release history.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
