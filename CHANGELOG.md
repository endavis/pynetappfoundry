# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### BREAKING CHANGE

- `nf metrics dump-dii`: the `--days` option is removed and replaced by the
  required `--date YYYY-MM-DD` option.  The command now issues one POST per
  metric per volume to the DII `/lake/query/timeseries` endpoint (6 POSTs per
  volume) with a 3-day window centred on *date* (date − 1 day to date + 2 days,
  60-second aggregation interval).  The SQLite database filename now includes
  the date (`{cluster}_{date}_metrics.db`) and each table stores data for a
  single SVM/volume pair (`{vserver_name}-{volume_name}`), replacing the
  previous per-cluster table layout.

### Added

- Initial release
- Core ONTAP client functionality
- CLI tools for storage administration
- SSH and REST API support

[Unreleased]: https://github.com/endavis/pynetappfoundry/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/endavis/pynetappfoundry/releases/tag/v0.1.0

## v0.1.0a1 (2026-04-21)

### Fix

- untrack _version.py so builds produce PyPI-compliant versions (merges PR #662, addresses #661)
- align testpypi.yml tag trigger with PEP440 pre-release tags (merges PR #660, addresses #659)

## v0.1.0a0 (2026-04-21)

### BREAKING CHANGE

- doit release no longer commits directly to main; it
opens a release PR that a reviewer merges, after which doit release_tag
tags main. doit release_dev and doit release_pr are removed. Migration:
  - doit release (old direct-to-main) -> doit release + merge PR +
    doit release_tag
  - doit release_dev --type=alpha      -> doit release --prerelease=alpha
  - doit release_pr                    -> doit release
  - doit release_tag                   -> doit release_tag (unchanged)
- the `client: Any` parameter on all four public functions
in `pynetappfoundry.query.realtime` is replaced with positional
`config: Config` and `cluster: str`, placed immediately after
`model_class`. Migration:
`fetch_realtime(MyModel, my_client, uuid)` ->
`fetch_realtime(MyModel, config, cluster="prod", uuid=uuid)`. This change
was made without a compatibility shim because there are zero production
callers inside `src/` (verified by grep); only test code and
`query/__init__.py` re-exports touch these functions. External users of
`pynetappfoundry.query.realtime` will need to update their call sites.
- ClusterMetadataDB.get_lazy() now requires the
ClusterMetadataDB to have been constructed with config= (not just
db_path=). Calling get_lazy() on a config-less DB raises ValueError.
Migration: pass config= when constructing ClusterMetadataDB if you
intend to call get_lazy(). LazyClusterMetadata constructed directly
(without going through get_lazy) is unaffected.
- ClusterData.fetched_data dict attribute has been
removed and replaced with typed model attributes: cluster_info,
nodes, svms, cifs_services, and management_ip.
- All cache model class names changed to Ontap* prefix.
- ClusterInfo.model has been removed.
Use ClusterInfo.version_generation instead.

### Feat

- stream subprocess output during release tasks instead of silent capture (merges PR #633, addresses #631)
- add DII API backend to DataSource (merges PR #613, addresses #600)
- add parallel cluster processing to cache refresh (merges PR #595, addresses #149)
- add glob matching to filter predicate values (merges PR #590, addresses #589)
- add filter predicates to cache query syntax (merges PR #588, addresses #190)
- add nf reports inventory command (merges PR #583, addresses #581)
- add vm_name derived field to CloudMetadata (merges PR #582, addresses #580)
- HTML report cloud VM sub-sections, service processor, and node details (merges PR, addresses #562) (merges PR #566, addresses #562)
- HTML report cloud VM sub-sections, service processor, and node details
- add per-mapping batch_size override and chunking edge-case tests (merges PR, addresses #538) (merges PR #560, addresses #538)
- add per-mapping batch_size override and chunking edge-case tests
- add typed filter expressions for DataSource queries (merges PR, addresses #497) (merges PR #557, addresses #497)
- add typed filter expressions for DataSource queries
- add DataSource SSH/CLI backend (merges PR, addresses #532) (merges PR #556, addresses #532)
- add DataSource SSH/CLI backend dispatch (ADR-0013 Gap 2)
- add mapping audit task and unmapped-model regression guard (merges PR, addresses #534) (merges PR #555, addresses #534)
- add mapping_audit doit task and regression guard for unmapped models
- support parent-keyed mappings in DataSource partial-fetch (merges PR, addresses #544) (merges PR #553, addresses #544)
- support parent-keyed mappings in DataSource partial-fetch
- add QueryBuilder.where() for SQL-like filter expressions (merges PR #513, addresses #512)
- add QueryBuilder.where() for SQL-like filter expressions (#512)
- implement OntapBackend.query() partial-fetch (phase 3a of #495) (merges PR #501, addresses #500)
- implement OntapBackend.query() partial-fetch via Approach C
- spike unified DataSource accessor against OntapVolume (phase 2 of #495) (merges PR #499, addresses #498)
- spike unified DataSource accessor against OntapVolume
- add Config.no_cache flag and --live CLI option to bypass cache (merges PR #475, addresses #472)
- add config-driven compliance checks with per-cluster overrides (merges PR #462, addresses #455)
- add performance benchmarks for core data paths (merges PR #461, addresses #460)
- add nf cache check CLI command for ad-hoc cache queries (merges PR #457, addresses #454)
- add SQL query engine with json_extract() support for cache DB (merges PR #456, addresses #453)
- auto-fetch config fields from ONTAP API (merges PR #451, addresses #445)
- add FieldGroupFetcher for live ONTAP field-group retrieval
- add cloud sections to HTML report for clusters and nodes (merges PR #442, addresses #440)
- rewrite reports html command with QuerySet (merges PR #439, addresses #438)
- rewrite licenses savings command with QuerySet (merges PR #437, addresses #95)
- rewrite reports space-usage command with QuerySet (merges PR #435, addresses #434)
- rewrite licenses check with QuerySet and styled HTML email (merges PR #431, addresses #93)
- rewrite utils validate command with QuerySet (merges PR #427, addresses #426)
- rewrite reports locks command with QuerySet (merges PR #425, addresses #424)
- rewrite licenses get command with QuerySet (merges PR #421, addresses #420)
- rewrite licenses get command with QuerySet and restore original functionality
- add relationship traversal between ONTAP resources (merges PR #418, addresses #411)
- add relationship traversal functions for ONTAP resources
- add on-demand fetching for realtime fields (merges PR #416, addresses #410)
- add async job tracking for long-running ONTAP operations (merges PR #415, addresses #409)
- add write operations (POST/PATCH/DELETE) to ONTAP query layer (merges PR #414, addresses #406)
- add Mutation class for ONTAP write operations (POST/PATCH/DELETE)
- add active query layer for ONTAP models (merges PR #413, addresses #407)
- wire up SVM top-metrics users as parameterized endpoint integration (merges PR #336, addresses #321)
- add parameterized endpoint support via parent_mapping iteration (merges PR #334, addresses #321)
- replace _enrich_with_cache with ClusterEntry lazy cache accessors (merges PR #333, addresses #320)
- generic derived field evaluation post-collection (merges PR #332, addresses #318)
- dynamic ?fields= expansion from requires_explicit_fetch annotations (merges PR #328, addresses #317)
- add TOML overlay loader for cache field strategies (merges PR #327, addresses #316)
- per-model SQL table storage for cache layer (merges PR #310, addresses #309)
- add OpenAPI codegen tool for cache model and mapping generation (merges PR #304, addresses #301)
- add OpenAPI spec conversion tooling and OCCM spec (merges PR #302, addresses #301)
- format cache query output with color-coded values and shared formatter (merges PR #285, addresses #284)
- deep URL-tree structure with automatic model and mapping discovery (merges PR #266, addresses #257)
- integrate get_all_records() into MetadataCollector._cached_api_call() (merges PR #264, addresses #263)
- add configurable pagination support to APIWrapper (merges PR #262, addresses #260)
- generalize field mapping framework for multi-API data collection (merges PR #261, addresses #259)
- add UUID index to CachedClusterMetadata for cross-reference lookups (merges PR #255, addresses #254)
- add standalone unit registry for ONTAP API field measurements (merges PR #252, addresses #251)
- add cache inspect command for troubleshooting (merges PR #219, closes #218)
- add declarative field mapping framework (pilot: VolumeInfo) (merges PR #189, closes #188)
- add debug logging for missing API response fields in collector (merges PR #187, closes #186)
- reset cache schema to v1.0 (merges PR #184, closes #167)
- add cache history tracking with snapshot command (merges PR #166, closes #165)
- add filter argument (-f) to cache refresh command (merges PR #164, closes #162)
- add azure_account and access_key to CloudTargetInfo (merges PR #159, closes #158)
- add structured log prefixes for SSH and API operations (merges PR #155, closes #154)
- add cloud targets to cache storage namespace (merges PR #147, closes #145)
- add timeout support to ONTAPCLI SSH commands (merges PR #146, closes #144)
- add cloud console resource links to cached metadata (merges PR #141, closes #140)
- add --csv output option to nf cache query (merges PR #137, closes #136)
- add wildcard array access [*] to cache query (merges PR #135, closes #132)
- add nf cache schema command (merges PR #134, closes #133)
- add nf cache schema command to display metadata structure
- add nf cache query command (merges PR #131, closes #130)
- add nf cache query command for querying cached metadata fields
- add verbose logging to cache refresh command (merges PR #127, closes #126)
- add base SQLiteDB class with version-based migrations (merges PR #114, closes #111)
- track SMB client impact during Azure maintenance events (merges PR #109, part of #92)
- rewrite save-azure to parse EMS events for full maintenance lifecycle (merges PR #102, part of #92)
- rewrite space-usage report with xlsxwriter 3-sheet structure (merges PR #87, closes #85)
- add name filtering, CSV output, and sort options to events get (merges PR #88, closes #86)
- refactor HTML report to use cache-enriched cloud metadata (merges PR #78, closes #77)
- integrate cache metadata into Config.get_clusters() (merges PR #76, closes #75)
- add SSH access validation to utils validate command (merges PR #74, closes #73)
- add Windows support for SOPS tools and CI integration tests (merges PR #70, part of #60)
- add --type option to set-credential for global defaults (merges PR #68, part of #60)
- auto-configure .envrc.local with SOPS_AGE_KEY_FILE (merges PR #66, part of #60)
- add doit tasks to install age and sops tools (merges PR #64, part of #60)
- add SOPS-encrypted credential storage with age (merges PR #63, closes #60, #61)
- add NF_CONFIG_DIR environment variable support for CLI (merges PR #40, closes #37)
- add cluster metadata cache for ONTAP clusters (merges PR #31, closes #32)
- add integration test examples and update API documentation (merges PR #30, closes #29)
- add configurable timeout for API clients (merges PR #28, closes #27)
- add response validation and retry logic to APIWrapper (merges PR #24, closes #23)
- add config CLI commands and environment variable support (merges PR #22, closes #21)
- add Pydantic models for type-safe configuration (merges PR #14, closes #13)

### Fix

- use head:release/ in release_tag gh pr search (merges PR #658, addresses #657)
- allow release type in doit pr_merge title validator (merges PR #656, addresses #655)
- accept release as a conventional type in PR and governance validators (merges PR #654, addresses #653)
- wire release CLI params to action function (not closure) (merges PR #651, addresses #650)
- wire release CLI params to action function instead of closure
- refuse doit release --prerelease on tagless repos (merges PR #645, addresses #644)
- pass --yes to cz bump --get-next and parse its output defensively (merges PR #642, addresses #641)
- bound validate_merge_commits walk when no tags exist (merges PR #640, addresses #639)
- add --prerelease flag to release_pr for PR-based pre-releases (merges PR #637, addresses #632)
- widen release_tag version regex to accept PEP440 and semver pre-releases (merges PR #634, addresses #632)
- widen release_tag version regex to accept PEP440 and semver pre-releases (#632)
- **codegen**: validate API-default parent_id_field before emitting parent linkage (merges PR #612, addresses #611)
- **codegen**: validate parent_id_field against dedup-winner model fields (merges PR #610, addresses #609)
- **codegen**: resolve parent_id_field and schema_lookup for child endpoints on regen (merges PR #607, addresses #606)
- **codegen**: derive parent_id_field from identifier map; build schema_lookup from pre-dedup endpoints
- **codegen**: disambiguate shared response schemas; add non-ONTAP support (merges PR #604, addresses #603)
- **codegen**: preserve identifier_field and TOML strategy overrides on regen (merges PR #602, addresses #601)
- **refresh**: prevent parallel workers from writing to stdout directly (merges PR #599, addresses #598)
- pre-load cluster snapshots on main thread for parallel refresh (merges PR #597, addresses #596)
- skip clusters with empty query results in cache query (merges PR #594, addresses #592)
- add v4→v5 cache DB migration for vm_name column (merges PR #585, addresses #584)
- move CLOUD phase after NODES so cloud metadata is collected (merges PR, addresses #564) (merges PR #565, addresses #564)
- move CLOUD phase after NODES so cloud metadata is collected
- HTML report node management IP and VServer title formatting (merges PR, addresses #562) (merges PR #563, addresses #562)
- HTML report node management IP and VServer title formatting
- add "Node:" prefix to HTML report node titles (merges PR, addresses #440) (merges PR #561, addresses #440)
- add "Node:" prefix to HTML report node titles
- thread config and honor shim connection lifetime in ClusterEntry cache (merges PR #551, addresses #548)
- skip cloud metadata fetch for on-prem clusters via is_cloud gate (merges PR #550, addresses #547)
- migrate nf reports html to DataSource for LIF home_node (merges PR #546, addresses #524)
- add cache-miss to live fallback for DataSource source=auto (merges PR #529, addresses #528)
- use startswith check for fields=* preservation in live URL builder (merges PR #527, addresses #522)
- preserve fields=* in DataSource live URL builder to avoid ONTAP 400 errors (merges PR #523, addresses #522)
- serialize pydantic submodels in cache history change summary (merges PR #484, addresses #483)
- include realtime fields in QuerySet live queries (merges PR #436, addresses #434)
- include realtime fields in parse_api_record by default
- use full command path for CLI output directory naming (merges PR #433, addresses #432)
- correct codegen sub-model field name prefixes (merges PR #423, addresses #422)
- use leaf field names instead of full api_path in codegen sub-models
- strip realtime fields from cache show output to hide meaningless defaults (merges PR #398, addresses #397)
- filter realtime fields from cache DB storage to prevent snapshot churn (merges PR #394, addresses #393)
- mark volatile fields as realtime to prevent snapshot churn (merges PR #392, addresses #391)
- mark volatile fields (metrics, space, sessions, transfers) as realtime in TOML overlays and mappings
- emit api_path on transform-only FieldMappings for correct expensive field URL construction (merges PR #388, addresses #387)
- correct 'aiquims' typo to 'aiqums' in VALID_DATA_TYPES (merges PR #384, addresses #383)
- scope _ensure_init_files to api_type namespace directory (merges PR #359, addresses #349)
- use relative paths in command-blocking.md (merges PR #356, addresses #355)
- use temp file for griffe output to avoid CI overflow (merges PR #331, addresses #329)
- handle int-typed key/display fields in diff engine (merges PR #326, addresses #325)
- remove hardcoded collector endpoints and wire cache_strategy into parsing (merges PR #313, addresses #312)
- codegen endpoint dedup, singularize exceptions, ApiType-prefixed naming, and typed sub-models (merges PR #306, addresses #305, #301)
- sanitize DII and AIQUM specs to remove dangling refs and fake paths (merges PR #303, addresses #301)
- derive diff tracked fields dynamically from model_fields (merges PR #270, addresses #269)
- explicitly request sidl_enabled in aggregate API endpoint (merges PR #229, closes #191)
- use csv.reader in separator parser to handle quoted values (merges PR #226, closes #225)
- add dual API calls to cache inspect for comparison (merges PR #221, part of #218)
- show API endpoint and CLI command in cache inspect output (merges PR #220, closes #218)
- read cluster peer addresses from remote.ip_addresses (merges PR #183, closes #182)
- handle string values in SnapMirror and cluster peer API parsing (merges PR #181, closes #178)
- add cluster context to all collector log messages (merges PR #180, closes #176)
- include endpoint path in API response log messages (merges PR #179, closes #176)
- add cluster name prefix to collector log messages (merges PR #177, closes #176)
- increase HTTP connection pool size for parallel API calls (merges PR #175, closes #174)
- pass timeout to SSH connection establishment (merges PR #171, closes #170)
- request only needed fields for snapmirror API endpoint (merges PR #169, closes #168)
- pass AWS SSO config to MetadataCollector during cache refresh (merges PR #163, closes #161)
- use cluster-based naming for Azure VM portal links (merges PR #160, closes #152)
- add thread-safe locking to ONTAPCLI.connect() (merges PR #157, closes #156)
- use recv_ready() instead of select() for SSH timeout (merges PR #153, closes #144)
- use application-level timeout for SSH CLI commands (merges PR #148, closes #144)
- handle invalid cluster name gracefully in cache show (merges PR #143, closes #142)
- store cloud metadata as list to capture all HA nodes (merges PR #139, closes #138)
- use core logging module for cache refresh command (merges PR #129, closes #128)
- preserve timing data across callhome.reboot.giveback reset (merges PR #121, closes #120)
- preserve timing data when recovering from missing scheduled event (merges PR #118, closes #117)
- prevent Unknown event_id in Azure maintenance tracking (merges PR #116, closes #115)
- add missing generate_doc_toc.py script (merges PR #113, closes #112)
- handle az_maint_complete when callhome.reboot.giveback comes first (merges PR #106, part of #92)
- use direct access for EmsEventParameter objects (merges PR #107, part of #92)
- improve save-azure performance by avoiding to_dict() on every event (merges PR #105, part of #92)
- show specific missing fields in az event error messages (merges PR #104, part of #92)
- improve az event warning messages with event IDs and context (merges PR #103, part of #92)
- align space-usage report with sysadmin script structure (merges PR #90, part of #85)
- correct Usage Breakdown table total_row configuration (merges PR #89, part of #85)
- remove duplicate console logging from CLI (merges PR #84, part of #83)
- isolate CLI tests from NF_CONFIG_DIR environment variable (merges PR #81, closes #80)
- store full SOPS JSON for proper encryption/decryption (merges PR #69, part of #60)
- handle non-dict membership field in nodes collection (merges PR #59, closes #58)
- add fields=* parameter to cache collector API calls (merges PR #57, closes #56)
- add fields=* parameter to all cache collector API calls
- suppress InsecureRequestWarning for ONTAP API client (merges PR #55, closes #52)
- coerce ClusterInfo.model field to string (merges PR #54, closes #51)
- disable SSL verification for ONTAP API client (merges PR #50, closes #49)
- pin Python 3.11 and fix DEBUG logging segfaults (merges PR #45, closes #46)
- show exception traceback when --debug is enabled (merges PR #44, closes #43)
- handle non-UTF-8 characters in ONTAP CLI output (merges PR #42, closes #41)
- remove invalid griffe --exclude argument (merges PR #12, closes #11)
- remove invalid griffe --exclude argument and filter output instead

### Perf

- parallelize API calls in metadata collector (merges PR #151, closes #150)

### Refactor

- consolidate release tasks around the PR-based flow (merges PR #638, addresses #632)
- auto-register TypeMappings via _ensure_bootstrapped guard (merges PR #579, addresses #578)
- remove shim deviations and legacy fallbacks (ADR-0012 Phase 4, merges PR, addresses #515) (merges PR #554, addresses #515)
- remove shim deviations and legacy fallbacks (ADR-0012 Phase 4)
- retire _LEGACY_DEP_KEYS compat shim in fetchers.py (merges PR #552, addresses #549)
- rewrite OntapBackend as thin fetch() delegator (ADR-0013 Phase 3) (merges PR #545, addresses #542)
- rewrite OntapBackend as thin fetch() delegator
- generic fetch() dispatcher over TypeMapping (ADR-0013 Phase 2) (merges PR #543, addresses #541)
- migrate nf reports html to DataSource shim (phase 3f/5 of #510) (merges PR #521, addresses #510)
- migrate nf utils validate to DataSource shim (phase 3f/4 of #510) (merges PR #520, addresses #510)
- migrate nf reports locks to DataSource shim (phase 3f/2 of #510) (merges PR #519, addresses #510)
- migrate nf licenses check/savings to DataSource shim (phase 3f/1 of #510) (merges PR #518, addresses #510)
- migrate nf cache check/query to DataSource shim + add --live (phase 3e of #495) (merges PR #514, addresses #509)
- migrate fetch_realtime to DataSource shim (phase 3d of #495) (merges PR #511, addresses #508)
- migrate QuerySet to DataSource shim (phase 3c of #495) (merges PR #507, addresses #506)
- migrate LazyClusterMetadata to DataSource shim (phase 3b of #495) (merges PR #503, addresses #502)
- convert nf licenses get to cache + on-demand fetch (merges PR #473, addresses #464)
- default api_path to cache_attr in FieldMapping (merges PR #452, addresses #447)
- regenerate nested models and mappings (phase 2) (merges PR #450, addresses #444)
- regenerate all models and mappings with nested structure
- prepare codegen and framework for nested model pattern (phase 1) (merges PR #449, addresses #444)
- prepare codegen, framework, and cache for nested models
- move ONTAP API models from cache/ to models/ package (merges PR #403, addresses #402)
- decouple diff engine _ENTITY_CONFIGS from hardcoded ONTAP models (merges PR #364, addresses #350)
- replace hardcoded _ENTITY_CONFIGS with dynamic introspection builder
- defer per-field-group cache queries with LazyClusterMetadata (merges PR #363, addresses #352)
- fix diff engine config for generated models and add tests (merges PR #322, addresses #319)
- optimize test performance by reducing unnecessary DB creation (merges PR #324, addresses #323)
- namespace cache models under ontap/ api-type directory (merges PR #315, addresses #314)
- rename cache models to Ontap* convention and regenerate from codegen (merges PR #308, addresses #307)
- align cache field names and containers with ONTAP API endpoint hierarchy (merges PR #297, addresses #295)
- flatten NetworkInfo LIF lists into single lifs list (merges PR #294, addresses #293)
- migrate NetworkLIF to declarative field mapping framework (merges PR #292, addresses #211)
- migrate BroadcastDomain to declarative field mapping framework (merges PR #288, addresses #212)
- migrate LicenseInfo to declarative field mapping framework (merges PR #283, addresses #213)
- migrate SVMInfo to declarative field mapping framework (merges PR #278, addresses #192)
- migrate DNSInfo to declarative field mapping framework (merges PR #275, addresses #205)
- replace DNSInfo hand-written parser with declarative field mapping
- replace ClusterInfo.model with version fields (merges PR #274, addresses #209)
- replace ClusterInfo.model with version_generation, version_major, version_minor
- migrate ClusterInfo to declarative field mapping framework (merges PR #273, addresses #209)
- replace HAInfo with MediatorInfo backed by field mapping framework (merges PR #272, addresses #214)
- split cache models into ONTAP REST API category modules (merges PR #265, addresses #256)
- split cache models.py into ONTAP REST API category modules
- migrate SnapMirrorRelationship to field mapping framework (merges PR #253, addresses #215)
- add authentication_in_use and encryption_state to ClusterPeer mapping (merges PR #250, addresses #216)
- migrate ClusterPeer to field mapping framework (merges PR #249, addresses #216)
- migrate ClusterPeer to declarative field mapping framework
- migrate CloudMetadata to field mapping framework (merges PR #248, addresses #217)
- implement all-or-nothing collection with no CLI fallback (merges PR #238)
- migrate NodeInfo to declarative field mapping framework (merges PR #232, closes #210, part of #167)
- add volume_count field to AggregateInfo (merges PR #230, part of #191)
- add new structural fields to AggregateInfo (merges PR #227, closes #191)
- add new structural fields to AggregateInfo model and mapping
- migrate AggregateInfo to declarative field mapping framework (merges PR #224, closes #191)
- update CLI collectors to use separator parsing method (merges PR #173, closes #172)
- consolidate CLI logging with dual console/file output (merges PR #82, closes #79)
- move cluster metadata cache to config directory (merges PR #39, closes #38)
- make find_closest key order configurable (merges PR #26, closes #25)
- add Config accessor methods to reduce tight coupling (merges PR #16, closes #15)
- improve code quality, testing, and security (merges PR #8, closes #7)

## v0.0.0 (2024-09-05)
