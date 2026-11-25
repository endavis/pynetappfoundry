---
title: Use Scopes to Separate Environments
description: Split the config directory into scopes, each with its own inventory, credentials and thresholds, and check one scope at a time
audience:
  - users
tags:
  - how-to
  - configuration
  - scopes
---

# Use Scopes to Separate Environments

**Goal:** split one config directory into scopes, such as one per business unit, so each scope has its own clusters, default credentials and thresholds, and check one scope at a time.

## Before you start

- A config directory with at least one cluster: [Add an ONTAP cluster and validate it](add-ontap-cluster.md).
- SOPS set up, if you store the scope's credentials encrypted: [Set up a config directory and SOPS secrets](sops-secrets.md).
- A name for each scope. The name is the directory name, such as `bu1`. It is case-sensitive.

The example below has one cluster outside any scope (`cluster1`, `cluster2`) and one scope, `bu1`, with one cluster (`cluster3`):

```
<config>/
├── environments/clusters.toml   # cluster1, cluster2: not in a scope
├── users.toml                   # default credentials, for objects outside a scope
└── bu1/                         # the scope
    ├── scope.toml               # the marker
    ├── clusters.toml            # cluster3
    ├── users.toml               # default credentials of the scope
    └── monitoring.toml          # thresholds of the scope
```

## Steps

### 1. Create the scope directory and its marker

A top-level directory of the config directory is a scope when it contains `scope.toml`. Every key in the file is optional, and an empty file is valid:

```toml
name = "bu1"                     # optional; when set, it must equal the directory name
description = "Business unit 1"  # optional
tags = ["example"]               # optional
```

Without the marker, the directory is not a scope, and its files load as ordinary root files. `scope.toml` is valid only directly inside a top-level directory: at the config root, nested deeper, or inside `apis` or a hidden directory, it is an error.

### 2. Add the scope's inventory

Put data files anywhere under the scope directory. Each needs the `[settings] type = "data"` marker:

```toml
# <config>/bu1/clusters.toml
[settings]
type = "data"

[clusters.cluster3]
ip = "192.0.2.12"
env = "Prod"
bu = "bu1"
```

Object names must be unique across the whole config directory, per data type. A name that appears in the root and in a scope, in two scopes, or twice in one scope stops the load. The same name under two different data types, such as a cluster and a connector, is fine.

### 3. Store the scope's credentials

Credentials for objects in the scope, as the default for a data type. This writes `<config>/bu1/users.toml`:

```bash
nf config set-credential --type clusters --scope bu1 --user bu1-admin
```

```
Encrypting with key: age1...
Password encrypted successfully.
Default credentials updated for type 'clusters' in scope 'bu1'
  File: config/bu1/users.toml
  User: bu1-admin
  Password: (encrypted)
```

The command prompts for the password without echoing it, and encrypts it. For one object, add `--cluster cluster3` instead of `--type`, as in [Add an ONTAP cluster](add-ontap-cluster.md).

For a cluster in the scope, `nf` looks up credentials in this order: the `NF_<NAME>_USER` and `NF_<NAME>_PASSWORD` environment variables, the cluster's own entry, the scope's `users.toml`, then the root `users.toml`. `user` and `enc` fall back independently. A cluster outside any scope never reads a scope's `users.toml`.

### 4. Set the scope's thresholds (optional)

A scope may hold three settings files: `users.toml`, `monitoring.toml` and `consoleapi.toml`. For `monitoring.toml`, a key the scope does not set falls back to the root file:

```toml
# <config>/bu1/monitoring.toml
[settings]
default_thresholds = {inodes=70, aggregate=85, volume=85}
```

A scope's Console account is strict: a scope without its own `consoleapi.toml` has no Console account and never uses the root one. See [Set up Console and its agents](setup-console.md).

Any other settings file in a scope, such as `ontapapi.toml`, `aiqumapi.toml`, `diiapi.toml` or `settings.toml`, is an error. Those stay at the root.

## Check it worked

Check the whole config, then one scope with `--scope`:

```bash
nf config validate --scope bu1
```

```
Validating configuration in: config/

Configuration Validation
├── Clusters
│   └── cluster3
├── Users
│   └── clusters
├── Scope settings (bu1)
│   ├── Monitoring
│   └── Console: Not configured (optional)
└── Cluster Credentials
    └── cluster3: bu1-admin

Configuration is valid
```

Without `--scope`, `nf config validate` checks every cluster, and the credential row shows which user each one resolves to. Here `cluster3` uses the scope's default and the others use the root default:

```
└── Cluster Credentials
    ├── cluster3: bu1-admin
    ├── cluster1: admin
    └── cluster2: admin
```

To see what a scope holds, `nf config show --scope bu1` prints its own files only. Secrets are masked, and a key the scope does not set falls back to the root:

```bash
nf config show --scope bu1
```

```
Configuration from: config/

Scope: bu1 (its own files only; keys the scope does not set fall back to the
root)
Description: Business unit 1

Scope bu1
├── clusters
│   └── cluster3
│       ├── ip: 192.0.2.12
│       ├── env: Prod
│       ├── bu: bu1
│       ├── name: cluster3
│       └── region:
├── monitoring
│   └── settings
│       └── default_thresholds
│           ├── inodes: 70
│           ├── aggregate: 85
│           └── volume: 85
└── users
    └── clusters
        ├── user: bu1-admin
        └── enc: ********
```

Then the offline `nf doctor` for the scope. It checks the scope's objects and settings, and the SOPS values in its `users.toml`. Add `--api` to limit it to one API, and drop `--offline` to send the live requests:

```bash
nf doctor --offline --scope bu1
```

```
nf doctor
├── Config: Clusters
│   └── cluster3
├── Config: Users
│   └── clusters
├── Config: Scope settings (bu1)
│   ├── Monitoring
│   └── Console: Not configured (optional)
├── Config: Cluster Credentials
│   └── cluster3: bu1-admin
├── SOPS
│   ├── sops is installed
│   ├── age key: key file ~/.sops/age/keys.txt
│   └── scope.bu1.users.clusters.enc: decrypts
└── Caches
    └── ONTAP cache: v12, 3 entries, oldest entry 0 day(s) old

Summary: 8 ok, 0 warning, 0 error, 1 skipped (offline)
```

The age key line shows the path of your own key.

Commands that take `-f` can select a scope's objects with the built-in `scope` key, for example `nf cache compliance -f '{"scope":"bu1"}'`. `{"scope":""}` selects the objects outside any scope.

## If it fails

| `nf config validate` or `nf doctor` shows | Cause | Fix |
| :--- | :--- | :--- |
| `Unknown scope 'bu1' (available scopes: ...)` | The directory has no `scope.toml`, or the name is misspelled. The command exits 1. | Add `<config>/bu1/scope.toml`, which may be empty. Scope names are case-sensitive. |
| `Failed to load configuration: ...scope.toml: name 'other' must equal the directory name 'bu1' (or be omitted).` | `name` in `scope.toml` differs from the directory name | Remove `name`, or make it equal the directory name. |
| `Failed to load configuration: Duplicate clusters name 'cluster1' in ... and ...; object names must be unique across the config directory` | Two files define the same object name | Rename one of them. The message names both files. |
| `Failed to load configuration: ...ontapapi.toml: a scope may only contain the settings files consoleapi.toml, monitoring.toml, users.toml (plus data files); 'ontapapi.toml' is not allowed in scope 'bu1'.` | A settings file other than the three allowed ones is in the scope directory | Move it to the root: API settings files go in `<config>/apis/<name>/`. |
| `Cluster 'cluster3' has no credentials configured` | No user and password for the cluster in its entry, the scope's `users.toml` or the root `users.toml` | `nf config set-credential --type clusters --scope bu1 --user USER` |
| `Fix [clusters] in bu1/users.toml: it needs 'user' and 'enc'.` | The scope's `users.toml` has a `user` but no encrypted password | Run the `nf config set-credential --type clusters --scope bu1 --user USER` command in the hint. |
| `<field>: SOPS value does not decrypt (SOPSError)` | The key cannot decrypt the stored password | See [SOPS: If it fails](sops-secrets.md#if-it-fails). |

## Next

- [Config schema: Scopes](../reference/config-schema.md#scopes): every rule, including the Console account of a scope
- [Set up Console and its agents](setup-console.md): one Console account per scope
- [Diagnose a failing setup with nf doctor](diagnose-with-doctor.md)
- [ADR-0028](../decisions/0028-scope-directories-partition-the-config-dir-with-per-scope-credentials-thresholds-and-console-account.md): why scopes work this way
