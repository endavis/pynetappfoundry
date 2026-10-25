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
- [ADR-9001: Use uv for package management](decisions/9001-use-uv-for-package-management.md) - Use uv for dependency management, virtual environments and package installation
- [ADR-9002: Use doit for task automation](decisions/9002-use-doit-for-task-automation.md) - Use doit as the task runner for testing, linting, building and other routine operations
- [ADR-9003: Use ruff for linting and formatting](decisions/9003-use-ruff-for-linting-and-formatting.md) - Use ruff as the one tool for linting and formatting, in place of flake8, black and isort
- [ADR-9004: Auto-discover doit tasks from modules](decisions/9004-auto-discover-doit-tasks.md) - Import every task_* function under tools/doit/ automatically instead of listing each one in dodo.py
- [ADR-9005: AI agent command restrictions via hooks](decisions/9005-ai-agent-command-restrictions.md) - Block dangerous commands such as --force, --admin and --no-verify at the tool level, through each AI agent's hooks
- [ADR-9006: Merge-gate workflow requiring ready-to-merge label](decisions/9006-merge-gate-workflow.md) - A merge-gate workflow, enforced by branch protection, keeps a PR from merging until it carries the ready-to-merge label
- [ADR-9007: Use mypy for static type checking](decisions/9007-use-mypy-for-type-checking.md) - Use mypy in strict mode, run by doit check, the pre-commit hooks and CI
- [ADR-9008: PR-based development workflow](decisions/9008-pr-based-development-workflow.md) - Every change goes Issue → Branch → Commit → PR → Merge, and nothing is committed to main directly
- [ADR-9009: Use pre-commit hooks for quality gates](decisions/9009-use-pre-commit-hooks-for-quality-gates.md) - Run quality and safety checks through the pre-commit framework before every commit
- [ADR-9010: Use conventional commits format](decisions/9010-use-conventional-commits-format.md) - Write every commit message, merge commits included, in the Conventional Commits format
- [ADR-9011: Use pytest for testing](decisions/9011-use-pytest-for-testing.md) - Use pytest, with pytest-xdist for parallel runs and pytest-cov for coverage
- [ADR-9012: Use mkdocs with Material theme for documentation](decisions/9012-use-mkdocs-with-material-theme-for-documentation.md) - Build the documentation with MkDocs and the Material theme, and host it on GitHub Pages
- [ADR-9013: Python version support policy with bookend CI strategy](decisions/9013-python-version-support-policy.md) - Support the last three Python versions, testing the oldest and newest on every PR and older ones on demand
- [ADR-9014: Use click for application CLI](decisions/9014-use-click-for-application-cli.md) - Build the package's user-facing command-line interface with click, registered as a console script
- [ADR-9015: install_tools framework: archive extraction and custom URLs](decisions/9015-install-tools-framework-archive-extraction-and-custom-urls.md) - Extend the install_tools framework with archive extraction and custom download URLs, keeping it backward compatible
- [ADR-9016: Unify ADR directories under docs/decisions](decisions/9016-unify-adr-directories.md) - Keep every ADR in docs/decisions/, numbering template decisions 9XXX and project decisions from 0001
- [ADR-9017: Template tooling and its tests are template-owned](decisions/9017-template-tooling-and-its-tests-are-template-owned.md) - A test under tests/template/ is template-owned when its target does not survive configuration
- [ADR-9018: AGENTS.md carries only shared, always-on instructions](decisions/9018-agentsmd-carries-only-shared-always-on-instructions.md) - Content belongs in AGENTS.md only when it holds for every agent and must be in effect at all times
- [ADR-9019: The dangerous-command hook is a guardrail, not a security boundary](decisions/9019-the-dangerous-command-hook-is-a-guardrail-not-a-security-boundary.md) - The dangerous-command hook guards against a non-adversarial agent, not a determined one
- [ADR-9020: A template version is a commit SHA](decisions/9020-a-template-version-is-a-commit-sha.md) - A template version is a commit SHA, not a release tag or a branch name
- [ADR-9021: A PR may target the unmerged branch it builds on](decisions/9021-a-pr-may-target-the-unmerged-branch-it-builds-on.md) - A PR may target the unmerged branch it builds on, but it merges only into main
- [ADR-9022: Worktrees live in worktrees/, each with its own environment](decisions/9022-worktrees-live-in-worktrees-each-with-its-own-environment.md) - A worktree lives in worktrees/<branch>, is created with doit worktree, and has its own environment
- [ADR-9023: Shared workflow skills are written once in .agents/skills/ and generated for Claude](decisions/9023-shared-workflow-skills-live-in-agents-skills-generated-for-claude.md) - Shared workflow skills live once in .agents/skills/ and doit skills_sync generates Claude's copy
- [ADR-9024: One implement-issue skill takes an issue to a green PR](decisions/9024-one-implement-issue-skill-takes-an-issue-to-a-green-pr.md) - One shared implement-issue skill replaces /claude:plan, /claude:implement, /ghi-finalize and the per-agent plan/implement matrix
- [ADR-9025: Delegated agents receive GitHub data from the host and run without network](decisions/9025-delegated-agents-receive-github-data-from-the-host-and-run-without-network.md) - The host fetches GitHub issue/PR data with doit delegation_context and writes it to files, so delegated agent prompts read those instead of calling gh
- [AI Agent Setup Guide](development/AI_SETUP.md) - Configure Claude, Copilot, Codex, and Antigravity for this project
- [AI Agent Token-Efficiency Add-Ons](development/ai/token-efficiency-add-ons.md) - Opt-in catalogue of external tools for reducing token usage in Claude Code sessions
- [AI Architectural Conventions](development/ai/architectural-conventions.md) - Imperative-form architectural rules AI agents must follow when generating code
- [AI Command Blocking](development/ai/command-blocking.md) - Hooks that block dangerous commands from AI agents
- [AI Enforcement Principles](development/ai/enforcement-principles.md) - How we enforce AI agent behavior in code and settings
- [API Reference](reference/api.md) - Python API documentation
- [Auto-Checkpoint and Session-Restore Hooks](development/ai/auto-checkpoint-hook.md) - PreCompact and SessionStart hooks that preserve context across autocompact events
- [Cache Model Architecture](development/cache-models.md) - End-to-end guide for the codegen pipeline, cache models, field strategies, and SQL storage
- [Cache System](reference/cache.md) - Architecture, storage layout, lazy loading, and CLI for the cluster metadata cache
- [CI/CD Testing Guide](development/ci-cd-testing.md) - GitHub Actions pipelines for testing, linting, and coverage
- [Claude Code Statusline](development/ai/statusline.md) - Custom statusline showing git branch, Python version, and project info
- [CLI Guide](usage/cli.md) - The application's user-facing command-line interface and how to extend it
- [Cross-Agent Delegation Matrix](development/ai/cross-agent-delegation.md) - Commands that let any supported AI CLI hand a review task to any other; plan and implement are handled by the shared implement-issue skill instead
- [Dependabot Auto-merge](development/dependabot-automerge.md) - How the dependabot auto-merge workflow evaluates, enables, and skips PRs
- [Development Deployment Guide](deployment/development.md) - Guide for setting up and running the application in development environments
- [Doit Tasks Reference](development/doit-tasks-reference.md) - Complete reference for all doit automation tasks
- [Field Mapping Framework](development/field-mapping.md) - Declarative framework for mapping API/CLI data to cache models
- [First 5 Minutes with an AI Agent](development/ai/first-5-minutes.md) - Narrative walkthrough of the AI agent workflow from issue to merge
- [GitHub Repository Settings](development/github-repository-settings.md) - Complete reference for all GitHub repository settings the template expects
- [install_tools Framework](development/install-tools-framework.md) - Reusable framework for installing developer tools from GitHub releases or other URLs into ~/.local/bin
- [Installation Guide](getting-started/installation.md) - How to install and set up your project
- [LSP Tool and Diagnostic Noise](development/ai/lsp-tool.md) - What the LSP tool gives an AI agent, why pyright diagnostics arrive stale, and the two opt-outs agents can flip on themselves
- [ONTAP Access Patterns](usage/ontap-access-patterns.md) - Guide to choosing between the three ONTAP access methods
- [Optional Extensions](development/extensions.md) - Additional tools and extensions for testing, security, and more
- [Per-Stack Rule Files](development/ai/rule-files.md) - How to author, load and mirror the short self-check rule files in .claude/rules/
- [Performance Benchmarks](development/benchmarks.md) - Running, interpreting, and comparing the pytest-benchmark suite
- [Production Deployment Guide](deployment/production.md) - Comprehensive guide for deploying Python applications to production
- [pynetappfoundry Documentation](index.md) - ONTAP administration library and CLI tools
- [Python Project Coding Standards](development/coding-standards.md) - Guidelines for exceptions, typing, structure, testing, and documentation
- [Query Layer](usage/query-layer.md) - Guide to the REST query layer (QuerySet, Query, Mutation, JobTracker, related, realtime)
- [Release Automation & Security](development/release-and-automation.md) - Automated versioning, release management, and security tooling
- [Review Focus Areas](development/ai/review-focus-areas.md) - Checklists for the errors, tests, types and comments focus areas available to every review and adversarial-review surface
- [Ruff Auto-Fix on Edit Hook](development/ai/ruff-fix-hook.md) - PostToolUse hook that runs ruff --fix on edited Python files
- [Slash Commands and Workflows](development/ai/slash-commands.md) - Reference for the slash commands and dual-agent workflow this template ships with
- [Template Tools Reference](template/tools-reference.md) - Complete reference for all template tools in tools/pyproject_template/
- [Tooling Roles and Architectural Boundaries](development/tooling-roles.md) - What each tool is for, who uses it, and where runtime code ends and dev tooling begins
- [Unit Registry](development/unit-registry.md) - Standalone unit registry for ONTAP API field measurements
<!-- END:audience=contributors -->

### For AI Agents
<!-- BEGIN:audience=ai-agents -->
- [AI Agent Setup Guide](development/AI_SETUP.md) - Configure Claude, Copilot, Codex, and Antigravity for this project
- [AI Agent Sync Checklist](template/ai-sync-checklist.md) - Step-by-step checklist for AI agents synchronizing downstream projects with pyproject-template
- [AI Agent Token-Efficiency Add-Ons](development/ai/token-efficiency-add-ons.md) - Opt-in catalogue of external tools for reducing token usage in Claude Code sessions
- [AI Architectural Conventions](development/ai/architectural-conventions.md) - Imperative-form architectural rules AI agents must follow when generating code
- [AI Command Blocking](development/ai/command-blocking.md) - Hooks that block dangerous commands from AI agents
- [AI Enforcement Principles](development/ai/enforcement-principles.md) - How we enforce AI agent behavior in code and settings
- [Auto-Checkpoint and Session-Restore Hooks](development/ai/auto-checkpoint-hook.md) - PreCompact and SessionStart hooks that preserve context across autocompact events
- [Claude Code Statusline](development/ai/statusline.md) - Custom statusline showing git branch, Python version, and project info
- [Cross-Agent Delegation Matrix](development/ai/cross-agent-delegation.md) - Commands that let any supported AI CLI hand a review task to any other; plan and implement are handled by the shared implement-issue skill instead
- [First 5 Minutes with an AI Agent](development/ai/first-5-minutes.md) - Narrative walkthrough of the AI agent workflow from issue to merge
- [LSP Tool and Diagnostic Noise](development/ai/lsp-tool.md) - What the LSP tool gives an AI agent, why pyright diagnostics arrive stale, and the two opt-outs agents can flip on themselves
- [Review Focus Areas](development/ai/review-focus-areas.md) - Checklists for the errors, tests, types and comments focus areas available to every review and adversarial-review surface
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
- [ADR-0019: Console runtime client architecture: org-scoped access and per-token-type wrapper isolation](decisions/0019-console-runtime-client-architecture-org-scoped-access-and-per-token-type-wrapper-isolation.md)
- [ADR-9001: Use uv for package management](decisions/9001-use-uv-for-package-management.md) - Use uv for dependency management, virtual environments and package installation
- [ADR-9002: Use doit for task automation](decisions/9002-use-doit-for-task-automation.md) - Use doit as the task runner for testing, linting, building and other routine operations
- [ADR-9003: Use ruff for linting and formatting](decisions/9003-use-ruff-for-linting-and-formatting.md) - Use ruff as the one tool for linting and formatting, in place of flake8, black and isort
- [ADR-9004: Auto-discover doit tasks from modules](decisions/9004-auto-discover-doit-tasks.md) - Import every task_* function under tools/doit/ automatically instead of listing each one in dodo.py
- [ADR-9005: AI agent command restrictions via hooks](decisions/9005-ai-agent-command-restrictions.md) - Block dangerous commands such as --force, --admin and --no-verify at the tool level, through each AI agent's hooks
- [ADR-9006: Merge-gate workflow requiring ready-to-merge label](decisions/9006-merge-gate-workflow.md) - A merge-gate workflow, enforced by branch protection, keeps a PR from merging until it carries the ready-to-merge label
- [ADR-9007: Use mypy for static type checking](decisions/9007-use-mypy-for-type-checking.md) - Use mypy in strict mode, run by doit check, the pre-commit hooks and CI
- [ADR-9008: PR-based development workflow](decisions/9008-pr-based-development-workflow.md) - Every change goes Issue → Branch → Commit → PR → Merge, and nothing is committed to main directly
- [ADR-9009: Use pre-commit hooks for quality gates](decisions/9009-use-pre-commit-hooks-for-quality-gates.md) - Run quality and safety checks through the pre-commit framework before every commit
- [ADR-9010: Use conventional commits format](decisions/9010-use-conventional-commits-format.md) - Write every commit message, merge commits included, in the Conventional Commits format
- [ADR-9011: Use pytest for testing](decisions/9011-use-pytest-for-testing.md) - Use pytest, with pytest-xdist for parallel runs and pytest-cov for coverage
- [ADR-9012: Use mkdocs with Material theme for documentation](decisions/9012-use-mkdocs-with-material-theme-for-documentation.md) - Build the documentation with MkDocs and the Material theme, and host it on GitHub Pages
- [ADR-9013: Python version support policy with bookend CI strategy](decisions/9013-python-version-support-policy.md) - Support the last three Python versions, testing the oldest and newest on every PR and older ones on demand
- [ADR-9014: Use click for application CLI](decisions/9014-use-click-for-application-cli.md) - Build the package's user-facing command-line interface with click, registered as a console script
- [ADR-9015: install_tools framework: archive extraction and custom URLs](decisions/9015-install-tools-framework-archive-extraction-and-custom-urls.md) - Extend the install_tools framework with archive extraction and custom download URLs, keeping it backward compatible
- [ADR-9016: Unify ADR directories under docs/decisions](decisions/9016-unify-adr-directories.md) - Keep every ADR in docs/decisions/, numbering template decisions 9XXX and project decisions from 0001
- [ADR-9017: Template tooling and its tests are template-owned](decisions/9017-template-tooling-and-its-tests-are-template-owned.md) - A test under tests/template/ is template-owned when its target does not survive configuration
- [ADR-9018: AGENTS.md carries only shared, always-on instructions](decisions/9018-agentsmd-carries-only-shared-always-on-instructions.md) - Content belongs in AGENTS.md only when it holds for every agent and must be in effect at all times
- [ADR-9019: The dangerous-command hook is a guardrail, not a security boundary](decisions/9019-the-dangerous-command-hook-is-a-guardrail-not-a-security-boundary.md) - The dangerous-command hook guards against a non-adversarial agent, not a determined one
- [ADR-9020: A template version is a commit SHA](decisions/9020-a-template-version-is-a-commit-sha.md) - A template version is a commit SHA, not a release tag or a branch name
- [ADR-9021: A PR may target the unmerged branch it builds on](decisions/9021-a-pr-may-target-the-unmerged-branch-it-builds-on.md) - A PR may target the unmerged branch it builds on, but it merges only into main
- [ADR-9022: Worktrees live in worktrees/, each with its own environment](decisions/9022-worktrees-live-in-worktrees-each-with-its-own-environment.md) - A worktree lives in worktrees/<branch>, is created with doit worktree, and has its own environment
- [ADR-9023: Shared workflow skills are written once in .agents/skills/ and generated for Claude](decisions/9023-shared-workflow-skills-live-in-agents-skills-generated-for-claude.md) - Shared workflow skills live once in .agents/skills/ and doit skills_sync generates Claude's copy
- [ADR-9024: One implement-issue skill takes an issue to a green PR](decisions/9024-one-implement-issue-skill-takes-an-issue-to-a-green-pr.md) - One shared implement-issue skill replaces /claude:plan, /claude:implement, /ghi-finalize and the per-agent plan/implement matrix
- [ADR-9025: Delegated agents receive GitHub data from the host and run without network](decisions/9025-delegated-agents-receive-github-data-from-the-host-and-run-without-network.md) - The host fetches GitHub issue/PR data with doit delegation_context and writes it to files, so delegated agent prompts read those instead of calling gh
- [AI Agent Setup Guide](development/AI_SETUP.md) - Configure Claude, Copilot, Codex, and Antigravity for this project
- [AI Agent Sync Checklist](template/ai-sync-checklist.md) - Step-by-step checklist for AI agents synchronizing downstream projects with pyproject-template
- [AI Agent Token-Efficiency Add-Ons](development/ai/token-efficiency-add-ons.md) - Opt-in catalogue of external tools for reducing token usage in Claude Code sessions
- [AI Architectural Conventions](development/ai/architectural-conventions.md) - Imperative-form architectural rules AI agents must follow when generating code
- [AI Command Blocking](development/ai/command-blocking.md) - Hooks that block dangerous commands from AI agents
- [AI Enforcement Principles](development/ai/enforcement-principles.md) - How we enforce AI agent behavior in code and settings
- [API Examples](examples/api.md) - Detailed Python API usage examples
- [API Reference](reference/api.md) - Python API documentation
- [Architecture Decision Records](decisions/README.md)
- [Auto-Checkpoint and Session-Restore Hooks](development/ai/auto-checkpoint-hook.md) - PreCompact and SessionStart hooks that preserve context across autocompact events
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
- [Consumer Notes](template/consumer-notes.md) - Breaking changes and behaviour changes that arrive when a project syncs from the template.
- [Cross-Agent Delegation Matrix](development/ai/cross-agent-delegation.md) - Commands that let any supported AI CLI hand a review task to any other; plan and implement are handled by the shared implement-issue skill instead
- [DataSource](usage/data-source.md) - Unified entry point for reading cluster data from cache or live API
- [Dependabot Auto-merge](development/dependabot-automerge.md) - How the dependabot auto-merge workflow evaluates, enables, and skips PRs
- [Development Deployment Guide](deployment/development.md) - Guide for setting up and running the application in development environments
- [Doit Tasks Reference](development/doit-tasks-reference.md) - Complete reference for all doit automation tasks
- [Examples](examples/README.md) - Code examples for pynetappfoundry
- [Field Mapping Framework](development/field-mapping.md) - Declarative framework for mapping API/CLI data to cache models
- [First 5 Minutes with an AI Agent](development/ai/first-5-minutes.md) - Narrative walkthrough of the AI agent workflow from issue to merge
- [GitHub Repository Settings](development/github-repository-settings.md) - Complete reference for all GitHub repository settings the template expects
- [install_tools Framework](development/install-tools-framework.md) - Reusable framework for installing developer tools from GitHub releases or other URLs into ~/.local/bin
- [Installation Guide](getting-started/installation.md) - How to install and set up your project
- [Keeping Up to Date](template/updates.md) - Stay in sync with improvements to the pyproject-template
- [LSP Tool and Diagnostic Noise](development/ai/lsp-tool.md) - What the LSP tool gives an AI agent, why pyright diagnostics arrive stale, and the two opt-outs agents can flip on themselves
- [Migration Guide](template/migration.md) - Migrate existing Python projects to use this template
- [New Project Setup](template/new-project.md) - Create a new Python project from this template
- [ONTAP Access Patterns](usage/ontap-access-patterns.md) - Guide to choosing between the three ONTAP access methods
- [Optional Extensions](development/extensions.md) - Additional tools and extensions for testing, security, and more
- [Per-Stack Rule Files](development/ai/rule-files.md) - How to author, load and mirror the short self-check rule files in .claude/rules/
- [Performance Benchmarks](development/benchmarks.md) - Running, interpreting, and comparing the pytest-benchmark suite
- [Plan: Add `nf cache query` Command](plans/cache-query-command.md)
- [Production Deployment Guide](deployment/production.md) - Comprehensive guide for deploying Python applications to production
- [PyNetAppFoundry Code Review & Improvement Plan](plans/first-pass-refactor.md)
- [pynetappfoundry Documentation](index.md) - ONTAP administration library and CLI tools
- [Python Project Coding Standards](development/coding-standards.md) - Guidelines for exceptions, typing, structure, testing, and documentation
- [Query Layer](usage/query-layer.md) - Guide to the REST query layer (QuerySet, Query, Mutation, JobTracker, related, realtime)
- [Release Automation & Security](development/release-and-automation.md) - Automated versioning, release management, and security tooling
- [Review Focus Areas](development/ai/review-focus-areas.md) - Checklists for the errors, tests, types and comments focus areas available to every review and adversarial-review surface
- [Ruff Auto-Fix on Edit Hook](development/ai/ruff-fix-hook.md) - PostToolUse hook that runs ruff --fix on edited Python files
- [Slash Commands and Workflows](development/ai/slash-commands.md) - Reference for the slash commands and dual-agent workflow this template ships with
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
