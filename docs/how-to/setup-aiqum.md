---
title: Set Up AIQUM
description: Add Active IQ Unified Manager instances, store their credentials, and check the connection
audience:
  - users
tags:
  - how-to
  - configuration
  - aiqum
---

# Set Up AIQUM

**Goal:** connect `nf` to one or more Active IQ Unified Manager (AIQUM) instances, and confirm that each one answers a read-only REST request.

## Before you start

- A config directory, and SOPS set up if you want encrypted passwords: [Set up a config directory and SOPS secrets](sops-secrets.md).
- The address of each AIQUM instance.
- An AIQUM user that can read the REST API. `nf doctor` reads `/datacenter/cluster/clusters`.

## Steps

### 1. Add the AIQUM API settings

Create `<config>/apis/aiqum/aiqumapi.toml`. The `[general]` table is required as soon as any AIQUM is configured, even if it is empty:

```toml
[general]
# base_api_path = "/api"      # default
# timeout = 30.0              # seconds
# verify_ssl = false          # see "TLS" below
# max_parent_requests = 500
```

Without the `[general]` table, `nf config validate` fails with `aiqumapi.toml has no [general] section, required by the [aiqums] inventory`. See [Config schema: aiqumapi.toml](../reference/config-schema.md#aiqumapitoml) for every key.

### 2. Add the instances

Add each instance to a data file, such as `<config>/environments/aiqums.toml`. The file needs the `[settings] type = "data"` marker, or it is not read as inventory:

```toml
[settings]
type = "data"

[aiqums.aiqum1]
ip = "192.0.2.20"
```

The key (`aiqum1`) is the name `nf` uses for the instance. An entry can carry the same descriptive keys as a cluster entry (`bu`, `env`, `region` and so on). See [Config schema: AIQUMs](../reference/config-schema.md#aiqums).

### 3. Store the credentials

When one user works on every instance, store it once as the default for all AIQUMs. It goes in `users.toml`:

```bash
nf config set-credential --type aiqums --user admin
```

```
Password encrypted successfully.
Default credentials updated for type 'aiqums'
  File: config/users.toml
  User: admin
  Password: (encrypted)
```

For an instance that needs its own user, add `--name`. Those credentials are stored on the instance's data file entry and override the default:

```bash
nf config set-credential --type aiqums --name aiqum1 --user admin
```

Both commands prompt for the password without echoing it.

### 4. Download the API spec

```bash
nf config download-spec --api aiqum
```

```
Wrote config/apis/aiqum/all.json
```

### 5. TLS (optional)

By default `nf` does not validate the certificate chain. It records each instance's certificate fingerprint on first contact and refuses to connect if it changes later. To validate against a CA instead, set `ca_bundle` or `verify_ssl` on an instance or in `[general]`. See [AIQUM API: TLS](../usage/aiqum-api.md#tls).

## Check it worked

```bash
nf config validate
```

Among its lines:

```
│   ├── AIQUM API
...
├── AIQUM
│   └── aiqum1
├── AIQUM Credentials
│   └── aiqum1: admin
└── Spec Files
    └── AIQUM spec

Configuration is valid
```

Then the live check. It sends one read-only `GET /datacenter/cluster/clusters?max_records=1` to each instance:

```bash
nf doctor --api aiqum
```

The output below comes from a working setup with default credentials in `users.toml`, shortened to two instances. One answers; the other is unreachable from where `nf` runs, so the run exits 1:

```
nf doctor
├── Config: Users
│   └── aiqums
├── Config: Settings
│   └── AIQUM API
├── Config: AIQUM
│   ├── aiqum1
│   └── aiqum2
├── Config: AIQUM Credentials
│   ├── aiqum1: admin
│   └── aiqum2: admin
├── Config: Spec Files
│   └── AIQUM spec
├── SOPS
│   ├── sops is installed
│   ├── age key: key file ~/.sops/age/keys.txt
│   └── settings.users.aiqums.enc: decrypts
└── AIQUM
    ├── aiqum1: connected
    └── aiqum2: unreachable (ConnectionError)
        └── Check the address, the network path and any proxy.

╭─────────────────────────────── Doctor Errors ────────────────────────────────╮
│ - AIQUM: aiqum2: unreachable                                                 │
│ (ConnectionError)                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯
```

When every instance answers, each AIQUM row reads `connected` and the run exits 0.

## If it fails

| `nf config validate` or `nf doctor` shows | Cause | Fix |
| :--- | :--- | :--- |
| `aiqumapi.toml has no [general] section, required by the [aiqums] inventory` | `aiqumapi.toml` is missing, or has no `[general]` table | Create it as in step 1. |
| `aiqum1: Missing credentials` | No user or password for the instance, on its entry or in `users.toml` `[aiqums]` | `nf config set-credential --type aiqums --name aiqum1 --user USER` |
| `AIQUM spec: missing` | `<config>/apis/aiqum/all.json` does not exist | `nf config download-spec --api aiqum` |
| `aiqum1: unreachable (ConnectionError)` | The `ip` is wrong, or the network path or a proxy blocks it | Check the `ip`, routing and any proxy. |
| `aiqum1: HTTP 401` | The instance rejected the credentials | Store them again with `nf config set-credential --type aiqums --name aiqum1 --user USER`. |
| `aiqum1: HTTP 403` | The user authenticated but cannot read the clusters endpoint | Use a user with read access to the REST API. |
| `aiqum1: identity changed` | The instance's TLS certificate changed since it was first recorded | Follow the reset hint printed below it, after confirming the change is expected. |
| `<field>: SOPS value does not decrypt (SOPSError)` | The key cannot decrypt the stored password | See [SOPS: If it fails](sops-secrets.md#if-it-fails). |

## Next

- [AIQUM API](../usage/aiqum-api.md): query AIQUM from Python
- [Add an ONTAP cluster and validate it](add-ontap-cluster.md)
- [Set up Digital Advisor](setup-digital-advisor.md)
