---
title: Add an ONTAP Cluster and Validate It
description: Add a cluster to the inventory, store its credentials, and check the connection with nf doctor
audience:
  - users
tags:
  - how-to
  - configuration
  - ontap
---

# Add an ONTAP Cluster and Validate It

**Goal:** add one ONTAP cluster to the config, store its credentials, and confirm `nf` can reach it.

## Before you start

- A config directory, and SOPS set up if you want encrypted credentials: [Set up a config directory and SOPS secrets](sops-secrets.md).
- The cluster's real name, its management IP, and an account that can read the ONTAP REST API.

## Steps

### 1. Add the cluster to a data file

Create `<config>/environments/clusters.toml`, or add to an existing data file:

```toml
[settings]
type = "data"

[clusters.cluster1]
ip = "192.0.2.10"
```

- **`[settings] type = "data"` is required.** Without it, the file is read as a settings file and the cluster is not loaded: `nf config validate` shows `No clusters configured`.
- **The key, `cluster1`, must be the cluster's real name.** That is the name ONTAP reports, which Console shows as the cluster name. `nf doctor` warns when they differ.
- **Optional fields**, such as `env`, `bu`, `tags` and `region`, let you filter clusters with `-f`. They are listed in [Config schema: Clusters](../reference/config-schema.md#clusters).

### 2. Store the credentials

For this cluster only, which writes `user` and `enc` onto its entry:

```bash
nf config set-credential --cluster cluster1 --user admin
```

Or once, as the default for every cluster without its own, which writes `[clusters]` in `<config>/users.toml`:

```bash
nf config set-credential --type clusters --user admin
```

Both prompt for the password and encrypt it. Credentials are looked up in this order:

1. the environment variables `NF_<NAME>_USER` and `NF_<NAME>_PASSWORD` (the name in upper case, with `-` replaced by `_`);
2. the cluster's own entry;
3. the scope's `users.toml`;
4. the root `users.toml`.

See [Config schema: Credential Resolution Order](../reference/config-schema.md#credential-resolution-order).

### 3. Add the ONTAP API settings

Create `<config>/apis/ontap/ontapapi.toml`:

```toml
[general]
base_api_path = "/api"
```

TLS certificate validation (`verify_ssl`, `ca_bundle`) is off by default. It can be set here for every cluster, or on a cluster's entry; see [Config schema: ontapapi.toml](../reference/config-schema.md#ontapapitoml).

### 4. Download the API spec

The ONTAP client needs the OpenAPI spec, which the installed package does not include:

```bash
nf config download-spec --api ontap
```

```
Wrote config/apis/ontap/all.json
```

## Check it worked

First, the offline checks:

```bash
nf config validate
```

```
Configuration Validation
├── Clusters
│   └── cluster1
├── Users
│   └── No users configured
├── Settings
│   ├── ONTAP API
│   ├── DII API: Not configured (optional)
│   ├── Digital Advisor API: Not configured (optional)
│   ├── SMTP: Not configured (optional)
│   ├── Console: Not configured (optional)
│   └── Licensing: Not configured (optional)
├── Cluster Credentials
│   └── cluster1: admin
└── Spec Files
    └── ONTAP spec

Configuration is valid
```

Then the live check, which sends one read-only `GET /api/cluster` to the cluster and compares the name it reports with the key:

```bash
nf doctor --api ontap
```

With many clusters, `-f '{"name": "cluster1"}'` limits the live check to one cluster. The config sections still list every cluster.

On success the `ONTAP` section ends with `connected`, and the command exits 0. The output below comes from a working setup where the credentials are the `[clusters]` default in `users.toml`. Other clusters' lines and the cache and Console sections are cut:

```
nf doctor
├── Config: Clusters
│   └── cluster1
├── Config: Users
│   └── clusters
├── Config: Settings
│   └── ONTAP API
├── Config: Cluster Credentials
│   └── cluster1: svc_user
├── Config: Spec Files
│   └── ONTAP spec
├── SOPS
│   ├── sops is installed
│   ├── age key: key file ~/.sops/age/keys.txt
│   └── settings.users.clusters.enc: decrypts
...
└── ONTAP
    └── cluster1: connected
```

On the first connection, `nf` records the cluster's TLS certificate fingerprint and checks it on every later connection. See [Host identity](../usage/basics.md#host-identity-ssh-host-keys-and-tls-certificates).

## If it fails

| `nf config validate` or `nf doctor` shows | Cause | Fix |
| :--- | :--- | :--- |
| `No clusters configured` | The data file has no `[settings] type = "data"` | Add it at the top of the file. |
| `cluster1: Missing credentials` | No user or password for the cluster anywhere in the lookup order | `nf config set-credential --cluster cluster1 --user USER` |
| `ONTAP spec: missing` | `<config>/apis/ontap/all.json` does not exist | `nf config download-spec --api ontap` |
| `cluster1: unreachable (ConnectTimeout)` | The IP is wrong, or the network path or a proxy blocks it | Check the `ip`, routing and any proxy. |
| `cluster1: HTTP 401` | The cluster rejected the credentials | Store them again with `nf config set-credential --cluster cluster1 --user USER`. |
| `cluster1: HTTP 403` | The account authenticated but cannot read `/api/cluster` | Use an account with read access to the REST API. |
| `cluster1: Config name cluster1 does not match cluster name <real>` | The key is not the cluster's real name | Rename the `[clusters.<key>]` entry, or check the `ip`. |
| `cluster1: identity changed` | The cluster's TLS certificate changed since it was first recorded | Follow the reset hint printed below it, after confirming the change is expected. |
| `<field>: SOPS value does not decrypt (SOPSError)` | The key cannot decrypt the stored password | See [SOPS: If it fails](sops-secrets.md#if-it-fails). |

## Next

- [Set up the DII API](setup-dii.md)
- [Basic Usage: Cluster Metadata Caching](../usage/basics.md#cluster-metadata-caching): fill the cache with `nf cache refresh`
- [Config schema: Clusters](../reference/config-schema.md#clusters): every cluster field
