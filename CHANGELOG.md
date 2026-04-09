# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- ONTAP administration library core functionality
- Click-based CLI (`nf` command)
- GitHub workflows for CI/CD
- Pre-commit hooks configuration
- Documentation with MkDocs

### Changed
- **BREAKING:** `ClusterMetadataDB.get_lazy()` now requires the
  `ClusterMetadataDB` to have been constructed with `config=` (not just
  `db_path=`). Calling `get_lazy()` on a config-less DB raises
  `ValueError`. This unblocks Phase 3b of the unified DataSource
  migration (#502, parent #495), which routes `LazyClusterMetadata`
  reads through `DataSource`. Migration: pass `config=` when
  constructing `ClusterMetadataDB` if you intend to call `get_lazy()`.
  The fetcher-only and default-only `LazyClusterMetadata` paths
  (constructed directly without going through `get_lazy`) are
  unaffected.

## [0.1.0] - TBD

### Added
- Initial release
- Core ONTAP client functionality
- CLI tools for storage administration
- SSH and REST API support

[Unreleased]: https://github.com/endavis/pynetappfoundry/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/endavis/pynetappfoundry/releases/tag/v0.1.0
