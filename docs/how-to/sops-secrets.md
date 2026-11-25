---
title: Set Up a Config Directory and SOPS Secrets
description: Create the config directory, generate an age key and store credentials encrypted with SOPS
audience:
  - users
tags:
  - how-to
  - configuration
  - sops
---

# Set Up a Config Directory and SOPS Secrets

**Goal:** create a config directory and an age key, so every credential you store with `nf config set-credential` is written encrypted.

## Before you start

- `nf` is installed (see [Installation](../getting-started/installation.md)).
- `sops` and `age` are on your `PATH`. Install them from your package manager and check:

  ```bash
  sops --version
  age --version
  ```

SOPS is optional, since `set-credential --no-encrypt` stores plain text, but it is the recommended setup.

## Steps

### 1. Create the config directory

`nf` reads `./config`, relative to the directory you run it from. To use another directory, pass `nf -c PATH` or set `NF_CONFIG_DIR`.

```bash
mkdir -p config/apis config/environments
```

Every `.toml` file under the directory is loaded. Settings files for each API go in `<config>/apis/<api>/`. Inventory goes in data files, such as `<config>/environments/clusters.toml`. The layout is described in [Config schema: Directory Structure](../reference/config-schema.md#directory-structure).

### 2. Generate the age key

Run this from the directory you will run `nf` from:

```bash
nf config init-sops
```

```
Generating age keypair at ~/.sops/age/keys.txt...
Age keypair generated successfully!

Private key: ~/.sops/age/keys.txt
Public key:  age1...

Created .envrc.local
Added SOPS_AGE_KEY_FILE to .envrc.local
Saved public key to .sops-public-key.txt
Created .gitignore with .sops-public-key.txt
```

It writes:

- the private key to `~/.sops/age/keys.txt`;
- `.envrc.local`, which exports `SOPS_AGE_KEY_FILE` for direnv users;
- `.sops-public-key.txt`, to share with anyone else who encrypts values for this config;
- a `.gitignore` that ignores `.sops-public-key.txt`.

**Back up the private key.** Encrypted values cannot be read without it.

### 3. Make sure `nf` can find the key

With the key at the default path, `~/.sops/age/keys.txt`, nothing else is needed.

If you passed `--key-path` to put the key somewhere else, export its location in every shell that runs `nf`. Either run `direnv allow` to load `.envrc.local`, or add this line to your shell profile:

```bash
export SOPS_AGE_KEY_FILE=/path/to/keys.txt
```

### 4. Store a credential

`nf config set-credential` prompts for the secret without echoing it, encrypts it, and writes it to the right file. Each setup guide gives the exact command, for example:

```bash
nf config set-credential --cluster cluster1 --user admin
```

```
Encrypting with key: age1...
Password encrypted successfully.
Credentials updated for cluster 'cluster1'
  File: config/environments/clusters.toml
  User: admin
  Password: (encrypted)
```

The value lands in the file as `enc = "SOPS[...]"`. The fields that accept an encrypted value are listed in [Config schema: SOPS-encrypted values](../reference/config-schema.md#sops-encrypted-values).

## Check it worked

`nf doctor --offline` checks `sops`, the key, and that every stored value decrypts. It makes no network request.

```bash
nf doctor --offline
```

```
├── SOPS
│   ├── sops is installed
│   ├── age key: key file ~/.sops/age/keys.txt
│   └── clusters.cluster1.enc: decrypts
```

Before you store any value, the last line reads `No SOPS values in the configuration`.

A known secret field that still holds a plaintext value (a cluster `enc`, a `users.toml` `enc`, a Cloud Insights `rw_enc`, or a token in a settings file) gets a warning row with the command that encrypts it. The row never shows the value:

```
│   └── clusters.cluster2.enc: plaintext (not SOPS-encrypted)
│       └── Store it encrypted with: nf config set-credential --cluster cluster2 --user admin
```

A warning does not fail `nf doctor`, so a config you left unencrypted on purpose still exits 0.

## If it fails

| `nf doctor` shows | Cause | Fix |
| :--- | :--- | :--- |
| `sops is not installed` | `sops` is not on `PATH`, but the config has encrypted values | Install `sops` and `age`. |
| `age key missing: key file <path>` | No key at the path shown | Run `nf config init-sops`, or set `SOPS_AGE_KEY_FILE` to your key. |
| `<field>: plaintext (not SOPS-encrypted)` (warning) | A secret field holds a plaintext value | Run the `nf config set-credential` command in the hint. |
| `<field>: SOPS value does not decrypt (SOPSError)` | The value was encrypted with a different key, or `SOPS_AGE_KEY_FILE` points to the wrong file | Point `SOPS_AGE_KEY_FILE` to the key that encrypted it, or store the value again with `nf config set-credential`. |

## Next

- [Add an ONTAP cluster and validate it](add-ontap-cluster.md)
- [Set up the DII API](setup-dii.md)
- [CLI Reference: config](../reference/cli.md#config): every `init-sops` and `set-credential` option
