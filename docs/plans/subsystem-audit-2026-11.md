---
title: "Subsystem Audit (2026-11)"
description: Audit of every pynetappfoundry subsystem covering patterns, libraries, bugs, refactors, documentation drift and test gaps, with a ranked backlog.
audience:
  - contributors
tags:
  - plan
---

# Subsystem Audit (2026-11)

This audit was taken at `main` @ `0cea9cab`. It covers `src/pynetappfoundry/`:

- about 110k lines in 2,417 files;
- of which `cache/` is 55k lines and `models/` is 52k lines, mostly generated.

Each finding has a status:

- **Verified** means the line was re-read during the audit.
- **Reported** means one audit pass saw it, but it was not re-checked.

Security-relevant findings are not listed here. They are handled privately under
[SECURITY.md](../../.github/SECURITY.md).

## Status (2026-11-10)

This section tracks progress on the audit since it was written. The rest of the document is the
audit as written; its corrections are listed below.

### Backlog items completed

| Backlog item | Issue | PR | Merge commit |
| :--- | :--- | :--- | :--- |
| 1. Fail closed on a SOPS decrypt failure (B1) | #891 | #913 | `b838dce2` |
| 2. `with_config` exception scope, non-zero exits (B2, B3) | #892 | #921 | `693a623d` |
| 3. DII offset/limit pagination per ADR-0015 (B4) | #893 | #916 | `dba861b0` |
| 4. Codegen class-name collisions, no-duplicate registry test (B5) | #894 | #924 | `8fd0555e` |
| 5. `db.query` keeps the model-owned `cluster_name` (B6) | #895 | #922 | `2f00d1cc` |
| 6. Remove unused runtime deps, `doit` to dev, `pydantic` floor | #896 | #928 | `e434ed6c` |
| 7. Compliance rule errors surface in the results (B8) | #897 | #914 | `e4f8abae` |
| 8. Refresh orchestration out of the CLI (R1) | #898 | #927 | `84515aa9` |
| 9. Split `src/pynetappfoundry/cache/collector.py` (R2) | #899 | #930 | `a04ebcfe` |
| 14. CLI conventions and one Excel writer (R6 in part, R7, B9), part 1 | #904 | #947 | `de2cd3d9` |
| 14. Part 2: shared click options | #941 | #948 | `47aedd9e` |
| 14. Part 3: one exit convention (`CliError`, ADR-0022) | #942 | #950 | `ddd61d31` |
| 14. Part 5: one Excel library (`xlsxwriter`) | #944 | #949 | `a678a8e5` |

### Follow-ups found while fixing, completed

| Issue | Summary | PR | Merge commit |
| :--- | :--- | :--- | :--- |
| #915 | DII envelope endpoints parsed and paged | #917 | `164413c4` |
| #918 | `DiiBackend` honours `records_path` | #920 | `ad69e507` |
| #919 | DII `InstallCommand` modelled as one record | #926 | `1cf7ad4d` |
| #923 | Case-insensitive codegen class-name collision check | #931 | `c1b8f359` |
| #925 | ONTAP single-object responses modelled as singletons (11 of 12 mappings) | #936 | `36f1eb87` |
| #929 | `/cluster/nodes` fetched once per `collect_all` | #940 | `ff6f3d97` |
| #934 | Collection beats item endpoint in ONTAP dedup (snaplock litigations, file-fingerprints) | #953 | `228487c1` |
| #937 | Filtered and counted live queries on singleton mappings | #951 | `d11e4577` |
| #938 | `GITHUB_TOKEN` for the CI SOPS install steps | #939 | `269029d8` |

### Still open

- **Backlog:** #900 (R3, R4), #901 (codegen drift check), #902 (documentation drift), #903 (R8).
- **#904 remainder:** #943 (drop the subcommand `-o`, breaking) and #945 (report data-building, R6).
- **ONTAP and DII codegen:**
  - #932: `support/ems/filters` naming;
  - #933: full ONTAP regeneration review;
  - #934: the `file_security/permissions` case only;
  - #935: DII `"."` sentinel to `response_shape`;
  - #952: unfillable placeholder endpoints.
- **Other:** #946 (`NF_OUTPUT_DIR` and `NF_DEBUG` environment variables).
- **Not filed:** B7, R5 and R9.

### Breaking changes since the audit

Six merges carry a `BREAKING CHANGE:` footer, all of them to generated model shapes or CLI exit
behaviour: #914, #924, #926, #931, #936 and #953.

### Corrections to the audit

- **`cryptography` is not removable.** The Libraries table and backlog item 6 recommend removing
  it. It has no import in `src/`, but it is kept as a CVE floor for `paramiko`'s transitive
  dependency (#818, #819), and #896 kept it.
- **R6 is partly addressed.** #949 consolidated the Excel writer. Moving data-building out of
  rendering is #945.

## Snapshot

| Subsystem | Lines | Coverage | Shape |
| :--- | ---: | ---: | :--- |
| `cache/` | 55,184 | 87% | `collector.py` (1,648), `db.py` (899), `diff.py`, 294 generated `mapping.py` (~30.8k), 482 TOML |
| `models/` | 51,585 | 78% | Pydantic v2 `OntapModel`. `console/` has a generated header and a CI drift check. `ontap/` and `dii/` have neither. |
| `cli/` | 10,405 | 73% | click group `nf`. Business logic leaks into `src/pynetappfoundry/cli/commands/cache/refresh.py`, `reports/*`. |
| `data/` | 2,026 | 93% | DataSource facade, ONTAP and DII backends |
| `core/` | 1,314 | 95% | `config.py` (TOML + SOPS) |
| `clients/` | 1,567 | 82% | `requests` session + tenacity, paramiko SSH, `netapp_ontap` |
| `query/` | 1,280 | 98% | |
| `utils/`, `db/`, `units/`, `compliance/`, `console/` | ~3,000 | 74–95% | |

The coverage figures come from `uv run doit coverage`: 6,153 passed, 5 skipped, 78.92% total
against a 75% gate. Vulture is clean at confidence 80. There are 269 `# noqa` in `src`.

## Libraries

These are the core libraries and what each is used for:

- `click` for the CLI;
- `rich` for console output;
- `pydantic` v2 for the models;
- `requests` with `tenacity` for HTTP and retries;
- `paramiko` for SSH;
- `netapp-ontap` for the REST passthrough;
- stdlib `sqlite3` for the cache;
- `yattag` for HTML reports;
- `tomllib` and `tomli_w` for config;
- `sops`/`age` subprocesses for secrets.

**Dependency hygiene (verified, `grep -rlE "^\s*(import|from) <pkg>\b" src`):**

| Dependency | Imports in `src/` | Recommendation |
| :--- | ---: | :--- |
| `pandas` | 0 (never, per `git log -S`) | Remove from runtime deps |
| `psutil` | 0 | Remove |
| `cryptography` | 0 | Remove (check that no transitive pin intends it) |
| `doit` | 0 (only `tools/doit/`) | Move to the dev extra |
| `xlsxwriter` | 1 (`src/pynetappfoundry/cli/commands/reports/space_usage.py`) | Pick one Excel writer. `openpyxl` is used in 3 files. |
| `pydantic>=2.0` | — | Raise the floor. `_perf_patches.py` depends on a private helper that may not exist in early 2.x. |

## Bugs

Ranked by impact.

### B1. A SOPS decrypt failure returns the ciphertext as the password (verified)

`core/config.py:462-465` catches `SOPSError`, logs a warning and returns the encrypted blob.

- The blob is then sent as the ONTAP password.
- The result is an auth failure that looks like a bad password, plus failed-login counts on the cluster.
- **Fix:** fail closed by raising a config error that names the cluster.

### B2. `with_config` rewraps every exception raised inside the command (verified)

`src/pynetappfoundry/cli/decorators.py:56-77` puts `return func(...)` inside the `try`, and the handler is
`except Exception` → `ClickException(f"{action}: {e}")`.

- A `JSONDecodeError` from inside a command is reported as "Invalid filter JSON".
- The command's own `ClickException` messages get a second prefix.
- **Fix:** call `func` outside the `try`. Also reject a filter that is not a dict.

### B3. Commands exit 0 on failure (verified for `run_cmd`)

`utils/run_cmd.py:65-66` catches `Exception`, prints it and returns. The same pattern is reported in:

- `utils/sqlite_to_excel.py:76`;
- `cifs/session.py:392`;
- `src/pynetappfoundry/cli/commands/reports/locks.py:104-107`.

Scripts cannot detect the failure. **Fix:** raise `click.ClickException` or exit non-zero once errors
are collected.

### B4. DII pagination is not implemented; ADR-0015 §3 is unmet (verified)

`src/pynetappfoundry/data/dii_backend.py` and `src/pynetappfoundry/clients/dii/api.py` contain no `offset`/`limit` handling. ADR-0015 says
the client paginates. Any DII endpoint with a page cap returns a truncated list silently.

### B5. A duplicate model class name drops a registry mapping (verified)

`models/dii/au/acquisitionUnit/model.py:9` and `models/dii/au/acquisitionUnits/model.py:9` both
define `DiiAuAcquisitionunit`.

- At import, the registry logs "Duplicate mapping registration" and keeps the last one.
- That drops `/au/acquisitionUnit/{auUuid}`.
- Other duplicate names are reported too (`OntapPortsetInterface*`, `OntapVolumeEfficiencyPolicy`,
  `OntapRolePrivilege`), as are case-variant sibling directories (`datasourceTypes` /
  `datasource_types`).
- **Fix:** make the codegen path-to-class name step collision-free, and add a test asserting no
  duplicate registrations.

### B6. `db.query()` strips `cluster_name` even when the model owns it (verified for the code; impact reported)

`src/pynetappfoundry/cache/db.py:811` and `:871` always drop `cluster_name`. `ClusterInfo` declares a `cluster_name`
field, and the shared `_query_registry_subset` handles this correctly. The result is
`ClusterInfo(cluster_name="")`.

### B7. A crash during migration can leave the cache stuck (reported)

- `sqlite3` legacy transaction mode does not wrap DDL.
- `_get_schema_version()` returns 1 when `_schema_version` is empty.
- So a crash between `_create_schema` and `_set_schema_version` makes the next open run
  `_upgrade_to_v2` against a v8 schema, which fails.
- ADR-0018 accepts rebuilds, but the failure should be detected (a missing version on a non-empty
  schema → rebuild), not left as a `SchemaUpgradeError` loop.

### B8. Compliance rules fail silently (reported)

- `src/pynetappfoundry/compliance/config.py` logs "Invalid compliance rule %r, skipping" without the validation error.
- `engine.py` catches only `ValueError` per rule and leaves no trace in the results.
- A broken rule therefore reads as "no violations".

### B9. Smaller bugs (reported)

- **`openapi.py`:** retry exhaustion raises `tenacity.RetryError`, not `HTTPError`, and retries also
  apply to POST, PATCH and DELETE.
- **`src/pynetappfoundry/data/filters.py:~213`:** `_quote` does not escape `'`, and it renders `bool` as an int.
- **Rich markup:** remote output and exception text are interpolated into rich markup
  (`src/pynetappfoundry/cli/utils.py`, `run_cmd.py:63`). A `[/x]` in ONTAP output raises `MarkupError`.
- **`_cached_api_call`:** it checks under the lock and fetches outside it, so parallel phases
  duplicate ONTAP calls.
- **`ClusterMetadataDB.__init__`:** it leaks the connection when a migration raises.
- **`src/pynetappfoundry/cli/commands/cache/refresh.py`:** it ignores the global `--output-dir`, and `ctx.exit(1)` skips
  `db.close()`.
- **`src/pynetappfoundry/cli/commands/reports/locks.py`:** it does not truncate sheet names to Excel's 31-character limit.
- **`src/pynetappfoundry/console/__init__.py`:** it builds the client before validating `org_id`.

## Anti-patterns and refactors

### R1. Move collection orchestration out of the CLI

`src/pynetappfoundry/cli/commands/cache/refresh.py` (975 lines) does all of the following:

- builds API and SSH clients;
- loads previous snapshots;
- persists;
- categorises failures;
- defines an inline `ClusterObj`.

`_refresh_normal` and `_refresh_verbose` are near-duplicates. This breaks the layering rules in
[architectural conventions](../development/ai/architectural-conventions.md). Move the logic into
`cache/`, and keep progress display in the CLI.

### R2. Split `src/pynetappfoundry/cache/collector.py` (1,648 lines)

Separate it into a phase runner, SSH/CLI, cloud (Azure link patching), progress, and derived
fields. Merge `_collect_all_parallel` and `_collect_all_sequential` into one runner that takes an
executor strategy. Name the magic pool sizes (5, 12, 3, 5).

### R3. Shrink the generated mapping layer

The 294 `mapping.py` files are mostly repeated `_transform_*` functions wrapped in
`try: … except Exception: items = []`.

- That wrapper hides real bugs.
- `record.get("x", [])` (141 sites) crashes on an explicit `null`.
- A generic nested-list `FieldMapping` (model class + dotted path), driven from TOML, would remove
  most of the ~30.8k lines.

### R4. Consolidate dotted-path helpers

There are five implementations:

- `utils/dict_path.get_nested_value`;
- `src/pynetappfoundry/cache/db.py:_get_by_path`;
- `src/pynetappfoundry/cache/fetchers.py`;
- `src/pynetappfoundry/cache/collector.py:_resolve_dotted_attr`;
- `src/pynetappfoundry/cli/commands/cache/query.py:_set_nested`.

### R5. Shared lazy client cache in `Backend`

`OntapBackend` and `DiiBackend` each check-then-set a per-cluster client dict without a lock, and
can open two SSH sessions for one cluster. Hoist one locked helper into the base class.

### R6. Add a reporting layer

- `src/pynetappfoundry/cli/commands/reports/html.py` (1,349 lines, embedded CSS and JS) mixes data access with rendering.
- So do `space_usage.py` (xlsxwriter) and `inventory.py` (openpyxl).
- A library-side report model and one Excel writer would deduplicate them.

### R7. Make CLI conventions consistent

- `--filter` is declared 17 times. Add a shared `filter_option`.
- Exits use three mechanisms (`ctx.exit`, `ClickException`, `SystemExit`). Standardise on one.
- `nf` has no top-level exception handler, so uncaught errors print raw tracebacks.
- `-o` means `--output-dir` on the group and `--output` on subcommands.
- `print_exception` and its callers both call `logger.exception`, so errors are logged twice.

### R8. Cut import time

- `import pynetappfoundry` takes ~875 ms, mostly `jsonschema` pulled in eagerly through
  `clients.openapi`.
- `import pynetappfoundry.cache` takes ~2.3 s and loads 1,060 model modules, because of the eager
  `walk_packages` over every `mapping.py`.
- Lazy registration would make CLI startup fast.

### R9. Smaller refactors

- **`RetryConfig` decorator:** it is rebuilt on every request. Build it once.
- **Migrations v4–v7:** they repeat the DDL and index loop. They also import *current* models, so
  they will drift.
- **`get_lazy()`:** it writes a private attribute on another layer's object.
- **Model defaults:** `str = ""`, `int = 0` and `bool = False` conflate absent with zero.
  - `uuid` is validated (`OntapUUID`) on 45 fields but is a plain `str` on 678.
- **`ALL_UNITS`:** it is built by scanning `dir(module)`. Use an explicit tuple.
- **`ONTAPCLI.pkey`:** it is never set by the constructor, so its branch is dead or set externally.

## Codegen and model drift

- `models/ontap/` and `models/dii/` have no "generated" header and no CI regeneration check. Only
  `console_models_check` runs in CI. Add a header and a `generate_models` drift check, so that
  hand edits and generator drift are caught.
- `tools/codegen/openapi_codegen.py` docstring still documents `--output …/cache/ontap/`. Per
  ADR-0008, models go under `models/`.

## Documentation drift

| Where | Drift | Status |
| :--- | :--- | :--- |
| ADR-0018 | Says `SCHEMA_VERSION` is "currently `5`". `src/pynetappfoundry/cache/db.py` is 8. | verified |
| ADR-0015 §3 | Client-layer pagination is described but not implemented (B4). | verified |
| ADR-0008 | Mentions a `models/occm/` that does not exist. | reported |
| ADR-0021, `docs/development/cache-models.md:628` | `nf cache diff`. The real command is `nf cache history diff`. | reported |
| `docs/reference/config-schema.md:312` | `nf events azevents`. The real command is `nf events save-azure`. | reported |
| `src/pynetappfoundry/cache/__init__.py` comment | "This PR lands only two DII endpoints…" is stale. | reported |
| `ClusterMetadataDB.__init__` docstring | Wrong path (`{data_dir}/cache/…` vs `config_dir/.cache`). | reported |
| `docs/plans/cache-query-command.md`, `first-pass-refactor.md` | The work has shipped. Mark them done or archive them. | reported |
| `docs/todo.txt` | Untracked free-form TODOs. Convert them to issues or delete them. | reported |
| Console | No usage or reference page. The only doc is ADR-0019, while 5 open issues target it. | reported |

## Test gaps

- **`cli/commands`:** 73% coverage, 1,191 missed lines. There are no tests for `run_cmd`,
  `sqlite_to_excel`, `config/credentials`, `init_sops`, `show` or `validate`.
- **Exit codes:** nothing tests B2 or B3.
- **Migrations:** no idempotency tests for v5, v6 or v8, no test for the v3→v4 destructive
  migration, and no partial-migration recovery test.
- **Registry:** no test that it has no duplicate class names (B5).
- **DII:** no multi-page test (B4).
- **Bad input:** no tests for a SOPS decrypt failure, a malformed compliance rule, or `_quote` with
  quotes or bools.

## Suggested backlog

Each item is filed as an issue. Order is priority.

1. #891 `fix`: fail closed on a SOPS decrypt failure (B1).
2. #892 `fix`: `with_config` exception scope and non-zero exits for failing commands (B2, B3).
3. #893 `fix`: DII offset/limit pagination per ADR-0015 (B4).
4. #894 `fix`: codegen class-name collisions plus a no-duplicate registry test (B5).
5. #895 `fix`: `db.query` keeps the model-owned `cluster_name` (B6).
6. #896 `chore`: drop `pandas`, `psutil` and `cryptography`; move `doit` to dev; raise the `pydantic`
   floor.
7. #897 `fix`: compliance rule errors surface in the results (B8).
8. #898 `refactor`: move refresh orchestration from the CLI into `cache/` (R1).
9. #899 `refactor`: split `collector.py` (R2).
10. #900 `refactor`: generic nested-list mapping to shrink the generated layer (R3, R4).
11. #901 `ci`: drift check for the ontap and dii models (codegen section).
12. #902 `docs`: fix the drift table entries, and add a Console usage page.
13. #903 `perf`: lazy model registration and lazy `jsonschema` import (R8).
14. #904 `refactor`: shared CLI options, a top-level error handler, and one Excel writer (R6, R7, B9).

B7, R5 and R9 are not filed yet; they can be picked up opportunistically or filed later.
