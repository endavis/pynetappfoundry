# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v0.2.0 (2026-11-25)

### BREAKING CHANGE

- nf config encrypt-value is removed. Use
nf config set-credential --setting <file>.<field> [--scope NAME], which
encrypts and writes the value itself. nf config validate now also checks the
root Console account, so a broken root consoleapi.toml fails validation.
- a duplicate object name across two root data files is
now a load error naming both files. Before, the later file silently won,
in filesystem order. To migrate, rename or remove one copy, including
stray .toml copies in non-scope subdirectories.
- SMTPSettings.password, DIIAPISettings.api_ro_token,
ConsoleAPISettings.service_token and ConsoleAPISettings.user_token are
now pydantic SecretStr instead of str. Read them with
.get_secret_value().
- `doit issue --type=feature` and `--type=bug` are renamed to
`--type=feat` and `--type=fix`, and an issue title must start with the
matching `<type>:` prefix. The old names exit with a rename message.
- ONTAPCLI constructed without trust_store= no longer
accepts SSH hosts that are missing from the system known_hosts. Pass
trust_store=config.get_trust_store() to record hosts on first use, or
add the host to ~/.ssh/known_hosts. Every caller inside the package
already passes a trust store.
- ClusterInfo is removed; /cluster is the generated
OntapCluster. Migration:
- ClusterInfo -> OntapCluster; CLUSTER_MAPPING -> ONTAPCLUSTER_MAPPING
  (registered as "OntapCluster", not "Cluster").
- cluster_name -> name; cluster_uuid -> uuid; ontap_version ->
  version.full; version_generation/major/minor -> version.generation/
  major/minor; timezone -> timezone.name; peering_policy_* ->
  peering_policy.*; management_interface_uuids ->
  [m.uuid for m in management_interfaces].
- is_ha / is_cloud -> ClusterTraits (metadata.cluster_traits).
- compute_is_ha, compute_is_cloud, _is_cloud_node and the CVO prefix
  tuples moved to pynetappfoundry.cache.ontap.cluster.traits.mapping.
- nf cache query paths: cluster.ontap_version -> cluster.version.full,
  cluster.is_ha -> cluster_traits.is_ha.
- Cache snapshots from 2.x are not loadable and the SQLite cache is
  cleared on upgrade: run `nf cache refresh`.
- pynetappfoundry.data.dii_backend.SINGLE_OBJECT_RECORDS_PATH
is removed. It was added after v0.1.0 and never released; code that
compared a mapping's records_path to it should check
mapping.response_shape == "singleton" instead.
- OntapEmsFilter modelled a single rule and now models the
filter. Removed fields: index, message_criteria, parameter_criteria, type_.
Added fields: access_control_role, name, rules, system_defined. Removed
classes OntapEmsFilterMessageCriteria and OntapEmsFilterParameterCriteria;
use OntapEmsFilterRuleMessageCriteria and OntapEmsFilterRuleParameterCriteria
under the new OntapEmsFilterRule (reached through OntapEmsFilter.rules).
Migration: read rule data from filter.rules[i].index, .type_,
.message_criteria and .parameter_criteria instead of from the filter itself.
EMS filters are not a cached table, so no cache migration is needed.
- `nf events get`, `nf licenses get` and
`nf utils sqlite-to-excel` no longer accept `-o`; use `--output`.
- OntapExportPolicy's top-level rule fields
(allow_device_creation, allow_suid, anonymous_user, chown_mode, clients,
index, ntfs_unix_security, protocols, ro_rule, rw_rule, superuser) move to
OntapExportPolicy.rules[] (OntapExportPolicyRule); the model gains id, name
and svm. OntapExportPolicyClient is renamed OntapExportPolicyRuleClient.
cache query / compliance paths protocols.nfs_export_policies.<rule-field>
become protocols.nfs_export_policies.rules[].<rule-field>. The diff key for
export policies changes from index to id. The cache migration clears cached
metadata; refresh after upgrading. The removed fields never held collected
data.
- these generated modules (mapping under
pynetappfoundry.cache.ontap.<path>, model under
pynetappfoundry.models.ontap.<path>) and their classes are removed:
application.applications.components.snapshots, name_services.netgroup_files,
name_services.unix_groups.users, protocols.cifs.local_groups.members,
protocols.cifs.shares.acls, protocols.cifs.users_and_groups.bulk_import,
protocols.file_security (permissions), protocols.ndmp.svms.passwords,
protocols.nfs.export_policies.rules.clients, protocols.s3.services.buckets.rules,
protocols.s3.services.buckets.snapshots, protocols.san.lun_maps.reporting_nodes,
security.key_managers.keys (key_ids), security.roles.privileges,
storage.qtrees.metrics, storage.snaplock.file,
storage.snaplock.litigations.operations, storage.volumes.files.
None could be fetched. CIFS share ACLs, LUN-map reporting nodes, role
privileges and litigation operations remain available as nested fields on
OntapCifsShare, OntapLunMap, OntapRole and OntapSnaplockLitigation.
- OntapSnaplockLitigation loses `path` and its operation
model loses num_files_failed, num_files_processed, num_files_skipped,
num_inodes_ignored, path, state and type_. OntapSnaplockFileFingerprint
loses algorithm, data_fingerprint, file_size, file_type,
metadata_fingerprint, path, scope and state.
- field sets of public pynetappfoundry.models.ontap.*
classes change for the 11 endpoints above (modules under cluster.software,
security.anti_ransomware, support.autosupport, cluster.metrocluster,
security.authentication.cluster.nis, protocols.file_security.permissions,
storage.snaplock.litigations, protocols.fpolicy, protocols.vscan,
cluster.counter.tables, storage.flexcache.origins). Bogus array-item
models are replaced by the real object's fields and sub-model classes are
added or removed.
- generated DII model classes under
pynetappfoundry.models.dii.collector.datasourceTypes are renamed:
DiiCollectorDatasourcetype -> DiiCollectorDatasourceTypes;
DiiCollectorDatasourcetypePackageAttribute -> DiiCollectorDatasourceTypesPackageAttribute;
DiiCollectorDatasourcetypePackage -> DiiCollectorDatasourceTypesPackage;
DiiCollectorDatasourcetypeVendormodelDatasourcetypevendormodelid -> DiiCollectorDatasourceTypesVendormodelDatasourcetypevendormodelid;
DiiCollectorDatasourcetypeVendormodel -> DiiCollectorDatasourceTypesVendormodel.
- DiiAuOnetimetoken and DiiAuInstallcommand (and their nested
classes) now hold InstallCommand fields (token, installCommand, imageZipUrl,
supportedOS, ...) instead of ExtraInstallInstruction fields (commands,
description, download, ...). Queries return one record instead of one per
instruction; read the instructions from the nested
additionalInstructionsForManualInstallation list.
- DiiAuAcquisitionunit is removed. Use DiiAuAcquisitionUnit
(/au/acquisitionUnit/{auUuid}) or DiiAuAcquisitionUnits (/au/acquisitionUnits).
- invalid or failing compliance rules now make
`nf cache compliance` exit 2; rule tables reject unknown fields and a
`name` key; `severity` must be one of the allowed levels. Migration: fix
or remove the offending keys.
- for wildcard and filter-predicate fields, --json now
returns a list of {"key": ..., "value": ...} records instead of a flat
list of values, --csv adds a "key" column after "cluster", and --raw
prints "key<TAB>value" per line. Scripts parsing the old flat output must
read the "value" field (JSON) or the second column (raw). Queries with
no wildcard or filter field are unchanged.
- `nf metrics dump-dii` now requires `--date YYYY-MM-DD`
instead of `--days` and writes per-volume tables to `{cluster}_{date}_metrics.db`.

### Feat

- support a read-write DII key per cloudinsights tenant (merges PR #1189, addresses #1184)
- support DII action and sub-resource write endpoints in the mutation layer (merges PR #1188, addresses #1185)
- report the DII read-write key in nf doctor --api dii (merges PR #1187, addresses #1186)
- add dii writes with a read-write api key (merges PR #1183, addresses #1003)
- add nf config download-spec to fetch the API specs of the installed release (merges PR #1130, addresses #1129)
- check in nf doctor that config clusters and Console working environments match by name (merges PR #1128, addresses #1127)
- add an Active IQ Digital Advisor DataSource backend (merges PR #1125, addresses #1116)
- make nf doctor --api limit every check to the chosen APIs (merges PR #1123, addresses #1122)
- let a Digital Advisor refresh token back up the personal access token (merges PR #1121, addresses #1120)
- add a Digital Advisor live check to nf doctor (merges PR #1119, addresses #1117)
- add an Active IQ Digital Advisor GraphQL client (merges PR #1118, addresses #1051)
- add nf doctor to check config, environment and API access (merges PR #1115, addresses #1113)
- share static config checks and extend nf config validate (merges PR #1114, addresses #1111)
- create missing API settings files in apis/<name>/ from set-credential (merges PR #1109, addresses #1107)
- link System Manager from the OCCM record in the reports (merges PR #1106, addresses #1105)
- read report cloud details from the OCCM cache with Console links (merges PR #1104, addresses #1086)
- resolve one cluster across the ONTAP, AIQUM and OCCM caches (merges PR #1101, addresses #1097)
- resolve Console agents by name and owning account from the OCCM cache (merges PR #1100, addresses #1083)
- add nf cache aiqum commands for the AIQUM cache (merges PR #1099, addresses #1072)
- add nf cache occm commands to refresh and inspect the OCCM cache (merges PR #1098, addresses #1087)
- add the cloud working-environment lists to the occm backend and cache (merges PR #1094, addresses #1074)
- store every secret through set-credential --setting and remove encrypt-value (merges PR #1090, addresses #1089)
- cache Console agent working environments and map them to agents (merges PR #1088, addresses #1076)
- scope-aware config CLI, search by scope, and unique names across root files (merges PR #1085, addresses #1081)
- discover Console organizations, working environments and agents per scope account (merges PR #1084, addresses #1078)
- scope directories in the config dir (merges PR #1082, addresses #1080)
- build URLs that open Console objects directly (merges PR #1079, addresses #1077)
- add a Console agent (OCCM) DataSource backend (merges PR #1075, addresses #1050)
- add an AIQUM collector and cache-backed DataSource queries (merges PR #1073, addresses #1055)
- add an AIQUM collector and cache-backed DataSource queries (addresses #1055)
- add parent_filters for AIQUM per-parent metrics queries (merges PR #1066, addresses #1061)
- add parent_filters for AIQUM per-parent metrics queries (addresses #1061)
- route DataSource DII queries to a named tenant (merges PR #1065, addresses #1053)
- fetch single AIQUM objects by key through DataSource (merges PR #1063, addresses #1060)
- fetch single AIQUM objects by key through DataSource (addresses #1060)
- AIQUM per-parent fetch for {key}/metrics mappings (merges PR #1062, addresses #1057)
- AIQUM per-parent fetch for {key}/metrics mappings (addresses #1057)
- support path_params in the AIQUM DataSource backend (merges PR #1059, addresses #1054)
- add an AIQUM DataSource backend (merges PR #1056, addresses #1049)
- per-object credentials for any inventory type (merges PR #1048, addresses #1045)
- add CA validation (verify_ssl/ca_bundle) for the AIQUM client (merges PR #1047, addresses #1044)
- add an AIQUM API client (merges PR #1042, addresses #1002)
- generate list models for Console array responses (merges PR #1041, addresses #1032)
- parse the Console dw (licenses and subscriptions) subservice (merges PR #1039, addresses #1034)
- add Console marketplace subscription lookup (merges PR #1035, addresses #875)
- typed models for the generated tenancy Console ops (merges PR #1030, addresses #1027)
- generate typed Console client operations from a manifest (merges PR #1029, addresses #735)
- allow SOPS-encrypted secrets in all settings files (merges PR #1026, addresses #1025)
- add an OAuth refresh-token grant for the console user token (merges PR #1023, addresses #736)
- add the connector field to ConsoleInfo (merges PR #1022, addresses #734)
- add a console agent (occm) api client (merges PR #1020, addresses #1001)
- parse the Console agent (cvo/) API docs into the Console OpenAPI spec (merges PR #1017, addresses #1009)
- add an oauth client-credentials grant to the console api client (merges PR #1010, addresses #1000)
- optional CA validation for ONTAP REST clients (verify_ssl / ca_bundle) (merges PR #1005, addresses #982)
- skip the parent fetch when a live child query's filter names the parent (merges PR #992, addresses #986)
- accept caller-supplied path values for DII placeholder endpoints (merges PR #991, addresses #990)
- pin ONTAP SSH host keys and TLS certificates on first use (merges PR #981, addresses #980)
- mask credential values in ClusterEntry repr (merges PR #979, addresses #978)
- multi-placeholder parent fill for ONTAP child mappings (merges PR #972, addresses #955)
- add Console folder and project to the ConsoleInfo cache (merges PR #876, addresses #734)
- collect SVM web services into the cache through the private CLI (merges PR #867, addresses #866)
- support dotted field paths in nf cache query filter predicates (merges PR #851, addresses #850)
- label nf cache query wildcard results with their source item (merges PR #849, addresses #848)
- add cifs session command to query active CIFS sessions (merges PR #778, addresses #775)
- add Console SaaS v1 runtime client and cache integration (merges PR #732, addresses #713)
- add -h short alias for --help in CLI (merges PR #731, addresses #719)
- generate Pydantic models from Console OpenAPI spec (merges PR #700, addresses #699)
- add BlueXP/Console SaaS docs to OpenAPI 3.1 parser (merges PR #698, addresses #697)
- rewrite dump-dii for DII timeseries (merges PR #691, addresses #96)
- add Query for RPC-style POST endpoints (merges PR #689, addresses #688)
- validate where expressions before query execution (merges PR #682, addresses #618)

### Fix

- raise ConfigurationError for a non-string enc in get_secret (merges PR #1179, addresses #1177)
- remove the dead datetime converters from AzEventsDB and EmsEventsDB (merges PR #1174, addresses #1172)
- report the caller's path in dict_path errors raised after a wildcard or filter (merges PR #1168, addresses #1162)
- show "% Used" on the space-usage Volumes sheet and highlight data rows only on both sheets (merges PR #1160, addresses #1158)
- go back to mutmut's default timeout_multiplier so slow-runner mutants are not false timeouts (merges PR #1147, addresses #1143)
- exclude generated Console client code from mutation and raise the mutation run's time limit (merges PR #1138, addresses #1137)
- name the section of each error and hint in nf doctor's error summary (merges PR #1134, addresses #1133)
- match Console working environments without a clusterName by their working environment name (merges PR #1132, addresses #1131)
- declare the Digital Advisor platformType and operatingMode filters as enum lists (merges PR #1126, addresses #1124)
- map null AIQUM fields to their defaults in the generated models (merges PR #1103, addresses #1102)
- accept real cloud working environments in the generated CVO models (merges PR #1096, addresses #1095, #1093)
- let Console discovery and the OCCM refresh run against real agents (merges PR #1092, addresses #1091)
- run CI jobs on the Python setup-python installs (merges PR #1070, addresses #1068)
- run CI jobs on the Python setup-python installs (addresses #1068)
- route source=auto live on the DII backend (merges PR #1058, addresses #1052)
- route source=auto live on the DII backend (addresses #1052)
- fetch the AIQUM spec through a UI login session (merges PR #1046, addresses #1043)
- type cvo list responses as arrays in the Console spec (merges PR #1031, addresses #1021)
- make generated cvo response models accept live agent responses (merges PR #1019, addresses #1018)
- route console operations to their own spec server path (merges PR #1014, addresses #1012)
- route console operations to their own spec server path (addresses #1012)
- load .yaml/.yml OpenAPI specs in APIWrapper (merges PR #1013, addresses #1011)
- fill or refuse DII endpoint path placeholders in live queries (merges PR #989, addresses #985)
- treat a 404 on a singleton mapping as no record (merges PR #988, addresses #977)
- substitute a parent identifier of 0 instead of skipping the parent (merges PR #987, addresses #976)
- fetch parents for live queries of parent-keyed ONTAP mappings (merges PR #984, addresses #975)
- apply DII TOML overlays alongside ONTAP overlays (merges PR #962, addresses #959)
- model ONTAP export policies as policies and migrate the cache (merges PR #958, addresses #956)
- model ONTAP export policies as policies and migrate the cache (addresses #956)
- stop generating unfetchable ONTAP endpoints with unfilled path placeholders (merges PR #957, addresses #952, #934)
- envelope collection beats item endpoint in ONTAP codegen dedup (merges PR #953, addresses #934)
- honor singleton response_shape on filtered and counted live queries (merges PR #951, addresses #937)
- model ONTAP single-object responses as singletons in codegen (merges PR #936, addresses #925)
- model ONTAP single-object responses as singletons in codegen (addresses #925)
- make codegen class-name collision check case-insensitive (DII datasourceTypes table name) (merges PR #931, addresses #923)
- make codegen class-name collision check case-insensitive (addresses #923)
- model DII single-object InstallCommand responses as one record (merges PR #926, addresses #919)
- model DII au/oneTimeToken and au/installCommand as one InstallCommand record
- make codegen class names collision-free for the model registry (merges PR #924, addresses #894)
- keep declared cluster_name in cache db query results (merges PR #922, addresses #895)
- exit non-zero when CLI commands fail and stop with_config rewrapping errors (merges PR #921, addresses #892)
- exit non-zero when CLI commands fail and stop with_config rewrapping errors (addresses #892)
- honour records_path for DII wrapper responses (merges PR #920, addresses #918)
- parse and page DII envelope responses (merges PR #917, addresses #915)
- paginate DII bare-array endpoints with offset/limit (merges PR #916, addresses #893)
- report invalid or failing compliance rules instead of skipping them (merges PR #914, addresses #897)
- fail closed when a SOPS-encrypted password cannot be decrypted (merges PR #913, addresses #891)
- cap QuerySet.limit(n) at n records instead of n per page (merges PR #874, addresses #872)
- make ClusterEntry.ontap fetch live when there is no cache or --live (merges PR #870, addresses #869)
- look up cluster IP from config in OntapBackend._get_api_client (merges PR #748, addresses #740)
- point breaking-change-detection workflow at pynetappfoundry module (merges PR #727, addresses #726)
- bump urllib3 to 2.7.0 to resolve CVE-2026-44431/44432 (merges PR #722, addresses #721)
- use bracket access for HA detection in azevents (merges PR #687, addresses #92)
- use message.severity filter and default to wildcard (merges PR #686)
- correct nf events get EMS field mapping (merges PR #685, addresses #108)
- QueryBuilder.filter() leaves partial state on early-validation rejection (merges PR #684, addresses #683)
- address review feedback for early where validation
- bump lxml to 6.1.0 in uv.lock to resolve CVE-2026-41066 (merges PR #670, addresses #669)

### Refactor

- remove the unreachable ValueError handler in ONTAPCLI.parse_generic_output (merges PR #1182, addresses #1181)
- parse the committed Console spec once per test session and load it with libyaml (merges PR #1149, addresses #1148)
- parse the real Console spec once per test session instead of once per test (merges PR #1142, addresses #1139)
- key Console spec operations by their full path from the host (merges PR #1016, addresses #1015)
- consolidate dotted-path helpers into utils/dict_path (merges PR #1006, addresses #965)
- scope InsecureRequestWarning suppression to the ONTAP client (merges PR #1004, addresses #983)
- lazy-load the CachedClusterMetadata / models.ontap chain at CLI startup (merges PR #999, addresses #960)
- generate /cluster as OntapCluster and remove ClusterInfo (merges PR #974, addresses #967)
- move is_ha/is_cloud into a hand-written ClusterTraits model (merges PR #973, addresses #967)
- replace DII records_path="." sentinel with response_shape="singleton" (merges PR #971, addresses #935)
- make a full ONTAP regeneration reproduce the committed tree (merges PR #969, addresses #933)
- model support/ems/filters as the filter object (merges PR #968, addresses #932)
- model support/ems/filters as the filter object (addresses #932)
- replace generated per-list transform functions with a generic nested-list mapping (merges PR #966, addresses #900)
- drop subcommand -o short flag in favour of --output (merges PR #963, addresses #943)
- register cache mappings lazily and import jsonschema on demand (merges PR #961, addresses #903)
- one CLI exit convention via CliError, with ADR (merges PR #950, addresses #942)
- one Excel library (xlsxwriter) via a shared writer helper (merges PR #949, addresses #944)
- shared click option decorators for --filter, --json, --csv, --all (merges PR #948, addresses #941)
- shared click option decorators for --filter, --json, --csv, --all (addresses #941)
- add top-level nf error handler and escape rich markup (#904 part 1) (merges PR #947, addresses #904)
- fetch /cluster/nodes once per collect_all (merges PR #940, addresses #929)
- split cache/collector.py into runner, cloud, API and progress modules (merges PR #930, addresses #899)
- split cache/collector.py into runner, cloud, API and progress modules (addresses #899)
- move cache refresh orchestration out of the CLI into cache/ (merges PR #927, addresses #898)
- read nf events data through QuerySet instead of the netapp_ontap SDK (merges PR #873, addresses #741)
- **codegen**: remove dead datamodel-code-generator call (merges PR #693, addresses #692)
- remove dead datamodel-code-generator call from parse_openapi_spec

## v0.1.0 (2026-04-21)

### Fix

- split SBOMs into separate release artifact so twine accepts dist (merges PR #666, addresses #665)

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
