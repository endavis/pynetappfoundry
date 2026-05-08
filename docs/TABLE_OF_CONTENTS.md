# All Documents

Complete index of all documentation, organized by audience and as a full alphabetical list.

> These lists are auto-generated from document frontmatter.
> Run `python tools/generate_doc_toc.py` to update.

## By Audience

### For Users
<!-- BEGIN:audience=users -->
- [API Examples](examples/api.md) - Detailed Python API usage examples
- [API Reference](reference/api.md) - Python API documentation
- [Basic Usage](usage/basics.md) - Getting started with pynetappfoundry
- [Cache System](reference/cache.md) - Architecture, storage layout, lazy loading, and CLI for the cluster metadata cache
- [CLI Guide](usage/cli.md) - The application's user-facing command-line interface and how to extend it
- [CLI Reference](reference/cli.md) - Command-line interface documentation
- [Compliance Checks](usage/compliance-checks.md) - Configure and run config-driven compliance checks against cached cluster metadata
- [Configuration Schema Reference](reference/config-schema.md) - Complete reference for pynetappfoundry TOML configuration files
- [DataSource](usage/data-source.md) - Unified entry point for reading cluster data from cache or live API
- [Development Deployment Guide](deployment/development.md) - Guide for setting up and running the application in development environments
- [Doit Tasks Reference](development/doit-tasks-reference.md) - Complete reference for all doit automation tasks
- [Examples](examples/README.md) - Code examples for pynetappfoundry
- [GitHub Repository Settings](development/github-repository-settings.md) - Complete reference for all GitHub repository settings the template expects
- [Installation Guide](getting-started/installation.md) - How to install and set up your project
- [Keeping Up to Date](template/updates.md) - Stay in sync with improvements to the pyproject-template
- [Migration Guide](template/migration.md) - Migrate existing Python projects to use this template
- [New Project Setup](template/new-project.md) - Create a new Python project from this template
- [ONTAP Access Patterns](usage/ontap-access-patterns.md) - Guide to choosing between the three ONTAP access methods
- [Production Deployment Guide](deployment/production.md) - Comprehensive guide for deploying Python applications to production
- [pynetappfoundry Documentation](index.md) - ONTAP administration library and CLI tools
- [Query Layer](usage/query-layer.md) - Guide to the REST query layer (QuerySet, Query, Mutation, JobTracker, related, realtime)
- [Template Management](template/manage.md) - Unified interface for creating projects, checking updates, and syncing
- [Template Tools Reference](template/tools-reference.md) - Complete reference for all template tools in tools/pyproject_template/
- [Using This Template](template/index.md) - Overview of using pyproject-template for your Python projects
<!-- END:audience=users -->

### For Contributors
<!-- BEGIN:audience=contributors -->
- [Add a Feature: End-to-End Walkthrough](examples/add-a-feature.md) - Step-by-step example of adding a module, CLI subcommand, tests, and docs to the project
- [Adding a New API Backend](development/adding-backends.md) - Developer guide for extending the DataSource framework with new API backends
- [AI Agent Setup Guide](development/AI_SETUP.md) - Configure Claude, Gemini, Copilot, and Codex for this project
- [AI Architectural Conventions](development/ai/architectural-conventions.md) - Imperative-form architectural rules AI agents must follow when generating code
- [AI Command Blocking](development/ai/command-blocking.md) - Hooks that block dangerous commands from AI agents
- [AI Enforcement Principles](development/ai/enforcement-principles.md) - How we enforce AI agent behavior in code and settings
- [API Reference](reference/api.md) - Python API documentation
- [Cache Model Architecture](development/cache-models.md) - End-to-end guide for the codegen pipeline, cache models, field strategies, and SQL storage
- [Cache System](reference/cache.md) - Architecture, storage layout, lazy loading, and CLI for the cluster metadata cache
- [CI/CD Testing Guide](development/ci-cd-testing.md) - GitHub Actions pipelines for testing, linting, and coverage
- [Claude Code Statusline](development/ai/statusline.md) - Custom statusline showing git branch, Python version, and project info
- [CLI Guide](usage/cli.md) - The application's user-facing command-line interface and how to extend it
- [Dependabot Auto-merge](development/dependabot-automerge.md) - How the dependabot auto-merge workflow evaluates, enables, and skips PRs
- [Development Deployment Guide](deployment/development.md) - Guide for setting up and running the application in development environments
- [Doit Tasks Reference](development/doit-tasks-reference.md) - Complete reference for all doit automation tasks
- [Field Mapping Framework](development/field-mapping.md) - Declarative framework for mapping API/CLI data to cache models
- [First 5 Minutes with an AI Agent](development/ai/first-5-minutes.md) - Narrative walkthrough of the AI agent workflow from issue to merge
- [GitHub Repository Settings](development/github-repository-settings.md) - Complete reference for all GitHub repository settings the template expects
- [Installation Guide](getting-started/installation.md) - How to install and set up your project
- [ONTAP Access Patterns](usage/ontap-access-patterns.md) - Guide to choosing between the three ONTAP access methods
- [Optional Extensions](development/extensions.md) - Additional tools and extensions for testing, security, and more
- [Performance Benchmarks](development/benchmarks.md) - Running, interpreting, and comparing the pytest-benchmark suite
- [Production Deployment Guide](deployment/production.md) - Comprehensive guide for deploying Python applications to production
- [pynetappfoundry Documentation](index.md) - ONTAP administration library and CLI tools
- [Python Project Coding Standards](development/coding-standards.md) - Guidelines for exceptions, typing, structure, testing, and documentation
- [Query Layer](usage/query-layer.md) - Guide to the REST query layer (QuerySet, Query, Mutation, JobTracker, related, realtime)
- [Release Automation & Security](development/release-and-automation.md) - Automated versioning, release management, and security tooling
- [Ruff Auto-Fix on Edit Hook](development/ai/ruff-fix-hook.md) - PostToolUse hook that runs ruff --fix on edited Python files
- [Slash Commands and Workflows](development/ai/slash-commands.md) - Reference for the slash commands and dual-agent workflow this template ships with
- [Template Tools Reference](template/tools-reference.md) - Complete reference for all template tools in tools/pyproject_template/
- [Tooling Roles and Architectural Boundaries](development/tooling-roles.md) - What each tool is for, who uses it, and where runtime code ends and dev tooling begins
- [Unit Registry](development/unit-registry.md) - Standalone unit registry for ONTAP API field measurements
<!-- END:audience=contributors -->

### For AI Agents
<!-- BEGIN:audience=ai-agents -->
- [AI Agent Setup Guide](development/AI_SETUP.md) - Configure Claude, Gemini, Copilot, and Codex for this project
- [AI Agent Sync Checklist](template/ai-sync-checklist.md) - Step-by-step checklist for AI agents synchronizing downstream projects with pyproject-template
- [AI Architectural Conventions](development/ai/architectural-conventions.md) - Imperative-form architectural rules AI agents must follow when generating code
- [AI Command Blocking](development/ai/command-blocking.md) - Hooks that block dangerous commands from AI agents
- [AI Enforcement Principles](development/ai/enforcement-principles.md) - How we enforce AI agent behavior in code and settings
- [Claude Code Statusline](development/ai/statusline.md) - Custom statusline showing git branch, Python version, and project info
- [First 5 Minutes with an AI Agent](development/ai/first-5-minutes.md) - Narrative walkthrough of the AI agent workflow from issue to merge
- [Ruff Auto-Fix on Edit Hook](development/ai/ruff-fix-hook.md) - PostToolUse hook that runs ruff --fix on edited Python files
- [Slash Commands and Workflows](development/ai/slash-commands.md) - Reference for the slash commands and dual-agent workflow this template ships with
- [Tooling Roles and Architectural Boundaries](development/tooling-roles.md) - What each tool is for, who uses it, and where runtime code ends and dev tooling begins
<!-- END:audience=ai-agents -->

## Complete Index
<!-- BEGIN:all -->
- [Add a Feature: End-to-End Walkthrough](examples/add-a-feature.md) - Step-by-step example of adding a module, CLI subcommand, tests, and docs to the project
- [Adding a New API Backend](development/adding-backends.md) - Developer guide for extending the DataSource framework with new API backends
- [ADR-0001: Use SQLite for cluster metadata caching](decisions/0001-use-sqlite-for-cluster-metadata-caching.md)
- [ADR-0002: Track SMB Client Impact During Azure Maintenance Events](decisions/0002-track-smb-client-impact-azure-maintenance.md)
- [ADR-0003: Use base SQLiteDB class with version-based migrations](decisions/0003-use-base-sqlitedb-class-with-version-based-migrations.md)
- [ADR-0004: Declarative field mapping framework for ONTAP collection](decisions/0004-declarative-field-mapping-framework.md)
- [ADR-0005: UUID index for cache cross-references](decisions/0005-uuid-index-for-cache-cross-references.md)
- [ADR-0006: Generalize field mapping framework for multi-API data collection](decisions/0006-generalize-field-mapping-for-multi-api.md)
- [ADR-0007: Deep URL-tree structure with automatic model and mapping discovery](decisions/0007-url-tree-model-registry.md)
- [ADR-0008: OpenAPI codegen for model and mapping generation](decisions/0008-openapi-codegen-for-model-generation.md)
- [ADR-0009: Per-Model SQL Table Storage for Cache Layer](decisions/0009-sql-table-storage.md)
- [ADR-0010: ClusterEntry and namespace access pattern](decisions/0010-clusterentry-and-namespace-access-pattern.md)
- [ADR-0011: Nested models to replace flat model pattern](decisions/0011-nested-models-to-replace-flat-model-pattern.md)
- [ADR-0012: Unified DataSource Accessor for All Cluster Reads](decisions/0012-unified-datasource-accessor.md)
- [ADR-0013: DataSource as a Thin Facade Over the Collector](decisions/0013-datasource-as-a-thin-facade-over-the-collector.md)
- [ADR-0014: Parallel Cluster Refresh](decisions/0014-parallel-cluster-refresh.md)
- [ADR-0015: DII backend: live-only, bare-array envelope, offset/limit pagination](decisions/0015-dii-backend-live-only-bare-array-envelope-offsetlimit-pagination.md)
- [ADR-0016: PR-based release is the only supported flow](decisions/0016-pr-based-release-is-the-only-supported-flow.md)
- [ADR-0017: where-expressions are cache-only (rationale)](decisions/0017-where-expressions-are-cache-only-rationale.md)
- [ADR-0018: Cache schema versioning and backward-compatibility policy](decisions/0018-cache-schema-versioning-and-backward-compatibility-policy.md)
- [ADR-9001: Use uv for package management](decisions/9001-use-uv-for-package-management.md)
- [ADR-9001: Use uv for package management](template/decisions/9001-use-uv-for-package-management.md)
- [ADR-9002: Use doit for task automation](decisions/9002-use-doit-for-task-automation.md)
- [ADR-9002: Use doit for task automation](template/decisions/9002-use-doit-for-task-automation.md)
- [ADR-9003: Use ruff for linting and formatting](decisions/9003-use-ruff-for-linting-and-formatting.md)
- [ADR-9003: Use ruff for linting and formatting](template/decisions/9003-use-ruff-for-linting-and-formatting.md)
- [ADR-9004: Auto-discover doit tasks from modules](decisions/9004-auto-discover-doit-tasks.md)
- [ADR-9004: Auto-discover doit tasks from modules](template/decisions/9004-auto-discover-doit-tasks.md)
- [ADR-9005: AI agent command restrictions via hooks](decisions/9005-ai-agent-command-restrictions.md)
- [ADR-9005: AI agent command restrictions via hooks](template/decisions/9005-ai-agent-command-restrictions.md)
- [ADR-9006: Merge-gate workflow requiring ready-to-merge label](decisions/9006-merge-gate-workflow.md)
- [ADR-9006: Merge-gate workflow requiring ready-to-merge label](template/decisions/9006-merge-gate-workflow.md)
- [ADR-9007: Use mypy for static type checking](decisions/9007-use-mypy-for-type-checking.md)
- [ADR-9007: Use mypy for static type checking](template/decisions/9007-use-mypy-for-type-checking.md)
- [ADR-9008: PR-based development workflow](decisions/9008-pr-based-development-workflow.md)
- [ADR-9008: PR-based development workflow](template/decisions/9008-pr-based-development-workflow.md)
- [ADR-9009: Use pre-commit hooks for quality gates](decisions/9009-use-pre-commit-hooks-for-quality-gates.md)
- [ADR-9009: Use pre-commit hooks for quality gates](template/decisions/9009-use-pre-commit-hooks-for-quality-gates.md)
- [ADR-9010: Use conventional commits format](decisions/9010-use-conventional-commits-format.md)
- [ADR-9010: Use conventional commits format](template/decisions/9010-use-conventional-commits-format.md)
- [ADR-9011: Use pytest for testing](decisions/9011-use-pytest-for-testing.md)
- [ADR-9011: Use pytest for testing](template/decisions/9011-use-pytest-for-testing.md)
- [ADR-9012: Use mkdocs with Material theme for documentation](decisions/9012-use-mkdocs-with-material-theme-for-documentation.md)
- [ADR-9012: Use mkdocs with Material theme for documentation](template/decisions/9012-use-mkdocs-with-material-theme-for-documentation.md)
- [ADR-9013: Python version support policy with bookend CI strategy](decisions/9013-python-version-support-policy.md)
- [ADR-9013: Python version support policy with bookend CI strategy](template/decisions/9013-python-version-support-policy.md)
- [ADR-9014: Use click for application CLI](decisions/9014-use-click-for-application-cli.md)
- [ADR-9014: Use click for application CLI](template/decisions/9014-use-click-for-application-cli.md)
- [ADR-9015: install_tools framework: archive extraction and custom URLs](decisions/9015-install-tools-framework-archive-extraction-and-custom-urls.md)
- [ADR-9015: install_tools framework: archive extraction and custom URLs](template/decisions/9015-install-tools-framework-archive-extraction-and-custom-urls.md)
- [ADR-9016: Unify ADR directories under docs/decisions](decisions/9016-unify-adr-directories.md)
- [ADR-NNNN: Title](decisions/adr-template.md)
- [AI Agent Setup Guide](development/AI_SETUP.md) - Configure Claude, Gemini, Copilot, and Codex for this project
- [AI Agent Sync Checklist](template/ai-sync-checklist.md) - Step-by-step checklist for AI agents synchronizing downstream projects with pyproject-template
- [AI Architectural Conventions](development/ai/architectural-conventions.md) - Imperative-form architectural rules AI agents must follow when generating code
- [AI Command Blocking](development/ai/command-blocking.md) - Hooks that block dangerous commands from AI agents
- [AI Enforcement Principles](development/ai/enforcement-principles.md) - How we enforce AI agent behavior in code and settings
- [API Examples](examples/api.md) - Detailed Python API usage examples
- [API Reference](reference/api.md) - Python API documentation
- [Architecture Decision Records](decisions/README.md)
- [Azure Maintenance SMB Client Impact Tracking](plans/azure-smb-impact-tracking.md)
- [Basic Usage](usage/basics.md) - Getting started with pynetappfoundry
- [Cache Model Architecture](development/cache-models.md) - End-to-end guide for the codegen pipeline, cache models, field strategies, and SQL storage
- [Cache System](reference/cache.md) - Architecture, storage layout, lazy loading, and CLI for the cluster metadata cache
- [CI/CD Testing Guide](development/ci-cd-testing.md) - GitHub Actions pipelines for testing, linting, and coverage
- [Claude Code Statusline](development/ai/statusline.md) - Custom statusline showing git branch, Python version, and project info
- [CLI Guide](usage/cli.md) - The application's user-facing command-line interface and how to extend it
- [CLI Reference](reference/cli.md) - Command-line interface documentation
- [Compliance Checks](usage/compliance-checks.md) - Configure and run config-driven compliance checks against cached cluster metadata
- [Configuration Schema Reference](reference/config-schema.md) - Complete reference for pynetappfoundry TOML configuration files
- [DataSource](usage/data-source.md) - Unified entry point for reading cluster data from cache or live API
- [Dependabot Auto-merge](development/dependabot-automerge.md) - How the dependabot auto-merge workflow evaluates, enables, and skips PRs
- [Development Deployment Guide](deployment/development.md) - Guide for setting up and running the application in development environments
- [Doit Tasks Reference](development/doit-tasks-reference.md) - Complete reference for all doit automation tasks
- [Examples](examples/README.md) - Code examples for pynetappfoundry
- [Field Mapping Framework](development/field-mapping.md) - Declarative framework for mapping API/CLI data to cache models
- [First 5 Minutes with an AI Agent](development/ai/first-5-minutes.md) - Narrative walkthrough of the AI agent workflow from issue to merge
- [GitHub Repository Settings](development/github-repository-settings.md) - Complete reference for all GitHub repository settings the template expects
- [install_tools Framework](development/install-tools-framework.md)
- [Installation Guide](getting-started/installation.md) - How to install and set up your project
- [Keeping Up to Date](template/updates.md) - Stay in sync with improvements to the pyproject-template
- [Migration Guide](template/migration.md) - Migrate existing Python projects to use this template
- [New Project Setup](template/new-project.md) - Create a new Python project from this template
- [ONTAP Access Patterns](usage/ontap-access-patterns.md) - Guide to choosing between the three ONTAP access methods
- [Optional Extensions](development/extensions.md) - Additional tools and extensions for testing, security, and more
- [Performance Benchmarks](development/benchmarks.md) - Running, interpreting, and comparing the pytest-benchmark suite
- [Plan: Add `nf cache query` Command](plans/cache-query-command.md)
- [Production Deployment Guide](deployment/production.md) - Comprehensive guide for deploying Python applications to production
- [PyNetAppFoundry Code Review & Improvement Plan](plans/first-pass-refactor.md)
- [pynetappfoundry Documentation](index.md) - ONTAP administration library and CLI tools
- [Python Project Coding Standards](development/coding-standards.md) - Guidelines for exceptions, typing, structure, testing, and documentation
- [Query Layer](usage/query-layer.md) - Guide to the REST query layer (QuerySet, Query, Mutation, JobTracker, related, realtime)
- [Release Automation & Security](development/release-and-automation.md) - Automated versioning, release management, and security tooling
- [Ruff Auto-Fix on Edit Hook](development/ai/ruff-fix-hook.md) - PostToolUse hook that runs ruff --fix on edited Python files
- [Slash Commands and Workflows](development/ai/slash-commands.md) - Reference for the slash commands and dual-agent workflow this template ships with
- [Template Architecture Decision Records](template/decisions/README.md)
- [Template Management](template/manage.md) - Unified interface for creating projects, checking updates, and syncing
- [Template Tools Reference](template/tools-reference.md) - Complete reference for all template tools in tools/pyproject_template/
- [Tooling Roles and Architectural Boundaries](development/tooling-roles.md) - What each tool is for, who uses it, and where runtime code ends and dev tooling begins
- [Unit Registry](development/unit-registry.md) - Standalone unit registry for ONTAP API field measurements
- [Using This Template](template/index.md) - Overview of using pyproject-template for your Python projects
<!-- END:all -->

---

## Contributing to Documentation

When adding new documentation:

1. Add frontmatter with `title`, `description`, `audience`, and `tags`:
   ```yaml
   ---
   title: My New Guide
   description: Short description for the index
   audience:
     - users
     - contributors
   tags:
     - setup
     - getting-started
   ---
   ```

2. Place the file in the appropriate directory

3. Run `python tools/generate_doc_toc.py` to update this index

4. The pre-commit hook will also run automatically on commit
