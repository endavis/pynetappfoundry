---
title: Configuration Guide
description: Set up a config directory and each API (ONTAP, AIQUM, DII, Console) from a fresh install
audience:
  - users
tags:
  - getting-started
  - configuration
---

# Configuration Guide

This guide takes you from a fresh install to a working config directory, with one setup section per API. It tells you what to create and where, and links to the reference pages for every field.

## Create the config directory

The default config directory is `./config`, relative to the directory you run from. Point at another one in one of these ways:

- **CLI:** `nf --config-dir PATH` (or `-c PATH`), or the `NF_CONFIG_DIR` environment variable. `NF_CONFIG_DIR` applies to the `nf` CLI only.
- **Python:** `Config(config_dir="/absolute/path/to/config")`. Pass `config_dir=` yourself; the environment variable is not read here.

A relative path is taken from the current directory and an absolute path is used as is. `~` is not expanded, so use a full path.

```bash
mkdir -p config/apis
```

## Start from the example

The repository ships a complete example in `docs/example-config/`. A PyPI install does not include it, so copy it from a clone or from GitHub at the release tag you installed:

```bash
git clone --branch <tag> https://github.com/endavis/pynetappfoundry.git
cp -r pynetappfoundry/docs/example-config/. config/
```

Then trim the placeholder inventory (the clusters, AIQUM instances and connectors in the data files) down to your own. The file layout and what each file holds are in [Config schema: Directory Structure](../reference/config-schema.md#directory-structure) and [Config schema: Where the settings files go](../reference/config-schema.md#where-the-settings-files-go). In short, each API's settings file and its spec go together in `<config>/apis/<name>/`.

## Encrypt credentials with SOPS (optional, recommended)

Step by step, with the output to expect: [How-to: Set up a config directory and SOPS secrets](../how-to/sops-secrets.md).

`nf config init-sops` creates an age key and wires SOPS so credentials are stored encrypted:

```bash
nf config init-sops
```

It writes `.envrc.local`, `.sops-public-key.txt` and `.gitignore` in the current directory, and the age private key to `~/.sops/age/keys.txt`. Back up that key; encrypted values cannot be read without it. See [CLI Reference: config](../reference/cli.md#config) for its options and [Config schema: SOPS-encrypted values](../reference/config-schema.md#sops-encrypted-values) for which fields accept an encrypted value.

## Spec files

The API clients read an OpenAPI spec from `<config>/apis/<name>/` when they are constructed. A missing spec raises `FileNotFoundError`.

The installed package does not contain any spec. The wheel that `pip` and `uv` install holds only the Python code. `nf config download-spec` downloads the committed spec of each configured API from GitHub into `<config>/apis/<api>/`:

```bash
nf config download-spec                # every configured API whose spec is missing
nf config download-spec --api ontap    # one API, even when it is not configured
nf config download-spec --force        # replace a spec that already exists
```

The spec comes from the repository at the release you installed, not from a live system. The generated models come from the committed spec, and a spec taken from one ONTAP or AIQUM instance could drop paths the code calls, so it would stop matching them. The release also needs no device credentials and covers Console, whose spec cannot be fetched live. The git ref is chosen from the installed version:

- a release installs from the tag `v<version>`;
- a development build names its commit (`+g<sha>`), and that commit must be pushed to GitHub. Local changes are not in the download, and the command warns about them;
- a version without a commit, such as a plain `.devN` or `0.0.0`, is an error. Install a release, or copy the file by hand as below.

The download must parse and have a `paths` map before it is written. A failed download writes nothing and exits 1; the other APIs are still downloaded.

You can also copy the committed spec by hand, from a clone or from GitHub at the tag you installed. From a checkout you can refresh a spec from a live system. `doit fetch_spec` writes `docs/example-config/apis/<api>/all.json` in the repo, sanitizing the spec on the way, and you copy that file into `<config>/apis/<api>/`.

| API | File | Copy from | Refresh from a checkout |
| :--- | :--- | :--- | :--- |
| ONTAP | `<config>/apis/ontap/all.json` | `docs/example-config/apis/ontap/all.json` | `doit fetch_spec --api=ontap --host=<cluster> --username=<user> --password=<password>` |
| AIQUM | `<config>/apis/aiqum/all.json` | `docs/example-config/apis/aiqum/all.json` | `doit fetch_spec --api=aiqum --host=<aiqum> --username=<user> --password=<password>` |
| DII | `<config>/apis/dii/all.json` | `docs/example-config/apis/dii/all.json` | `doit fetch_spec --api=dii --host=<tenant> --api-key=<token>` |
| Console | `<config>/apis/console/console_openapi.yaml` | `tools/console_openapi/generated/console_openapi.yaml` | `doit console_openapi_refresh` |

`nf config validate` and `nf doctor` warn about a missing spec of a configured API and give `nf config download-spec --api <api>` as the fix. `nf doctor` does not download it.

Every `fetch_spec` call also accepts `--no-verify` to skip TLS certificate validation. After a refresh, `doit convert_specs` and `doit generate_models` rebuild the converted spec and the models.

## ONTAP

Step by step, with the output to expect: [How-to: Add an ONTAP cluster and validate it](../how-to/add-ontap-cluster.md).

- **Inventory:** add each cluster to a data file as `[clusters.NAME]` with an `ip` (see [Config schema: Clusters](../reference/config-schema.md#clusters)). The `NAME` must be the cluster's real name, which Console shows as its cluster name (the working environment name when Console reports none). For AWS Cloud Volumes ONTAP the `ip` may be a node management IP.
- **Credentials:** `nf config set-credential --cluster NAME --user USER` stores them on the cluster entry. A default for every cluster goes under `[clusters]` in `users.toml` (see [Config schema: Credential Resolution Order](../reference/config-schema.md#credential-resolution-order)). The API uses HTTP Basic authentication.
- **Settings:** `<config>/apis/ontap/ontapapi.toml` with a `[general]` section (see [Config schema: ontapapi.toml](../reference/config-schema.md#ontapapitoml)).
- **Spec:** `<config>/apis/ontap/all.json` (see [Spec files](#spec-files)).
- **Check:** `nf config validate`, and `nf doctor --api ontap` to test the connection.

## AIQUM

- **Inventory:** add each instance as `[aiqums.NAME]` with an `ip`.
- **Credentials:** `nf config set-credential --type aiqums --name NAME --user USER`, or a default under `[aiqums]` in `users.toml`.
- **Settings:** `<config>/apis/aiqum/aiqumapi.toml` with a `[general]` section.
- **Spec:** `<config>/apis/aiqum/all.json` (see [Spec files](#spec-files)).
- **Check:** `nf config validate`, `nf doctor --api aiqum`, and `nf config show -s aiqums` to see the loaded entries.

The fields are in [AIQUM API: Setup](../usage/aiqum-api.md#setup).

## DII (Data Infrastructure Insights)

Step by step, with the output to expect: [How-to: Set up the DII API](../how-to/setup-dii.md).

- **Inventory:** add each tenant as `[cloudinsights.NAME]` with an `ip` (see [Config schema: Cloud Insights](../reference/config-schema.md#cloud-insights)).
- **Credentials:** the API token. `nf config set-credential --setting diiapi.api_ro_token` stores one for every tenant in `diiapi.toml`. `nf config set-credential --type cloudinsights --name NAME --user LABEL` stores one per tenant. The client sends it in the `X-CloudInsights-ApiKey` header. Writes need a separate read-write key, `api_rw_token`, set with `nf config set-credential --setting diiapi.api_rw_token`; it is optional and only `DIIAPIClient(config, read_write=True)` uses it. A tenant can have its own read-write key: `nf config set-credential --type cloudinsights --name NAME --read-write` stores it as `rw_enc` on the tenant's entry, and it replaces the `[general]` key for that tenant.
- **Settings:** `<config>/apis/dii/diiapi.toml` with a `[general]` section (see [Config schema: diiapi.toml](../reference/config-schema.md#diiapitoml)).
- **Spec:** `<config>/apis/dii/all.json` (see [Spec files](#spec-files)).
- **Check:** `nf config validate`, `nf doctor --api dii` (it also reports the read-write key: skipped when unset, an error when rejected), and `nf config show -s cloudinsights` to see the loaded entries.

## Digital Advisor

- **Credentials:** one or both of a personal access token and a refresh token (the PAT is used first), stored with `nf config set-credential --setting digitaladvisorapi.personal_access_token` or `--setting digitaladvisorapi.refresh_token`.
- **Settings:** `<config>/apis/digitaladvisor/digitaladvisorapi.toml` with a `[general]` section (see [Config schema: digitaladvisorapi.toml](../reference/config-schema.md#digitaladvisorapitoml)).
- **Schema (optional):** `nf config download-schema` writes `<config>/apis/digitaladvisor/schema.json`.
- **Check:** `nf config validate`, and `nf doctor --api digitaladvisor` to test the token.

The client and the token rotation are in [Digital Advisor API](../usage/digital-advisor-api.md).

## Console and agents (OCCM)

The Console (BlueXP) client and the Console agents (connectors, also called OCCM) share one account setup.

- **Account:** at least one way to authenticate in `<config>/apis/console/consoleapi.toml` `[general]`:
    - a **refresh token** (renews itself): `nf config set-credential --type console --user console`, then paste the token at the prompt. It goes to `users.toml` under `[console]`, never into `consoleapi.toml`;
    - a **service account** (recommended for unattended use): `client_id` in `consoleapi.toml`, and the secret stored with `nf config set-credential --setting consoleapi.client_secret`;
    - a static `user_token` or `service_token`, which is not renewed.

  The full field list, including `org_id`, is in [Config schema: consoleapi.toml](../reference/config-schema.md#consoleapitoml).
- **Connectors:** add each agent as `[connectors.NAME]` with an `ip`. `agent_id` is optional: without it, `DataSource` finds the agent by name in the OCCM cache, so run `nf cache occm refresh` first (see [Config schema: Connectors](../reference/config-schema.md#connectors)).
- **Spec:** `<config>/apis/console/console_openapi.yaml` (see [Spec files](#spec-files)).
- **OCCM needs no files of its own.** Calls to an agent go through `ConsoleAgentClient`, which uses the Console spec and the Console account; nothing under `<config>/apis/occm/` is read. The `docs/example-config/apis/occm/` files only feed code generation. See [Console Agent](../usage/console-agent.md).
- **Scopes:** a scope can have its own Console account; see [Config schema: Scopes](../reference/config-schema.md#scopes).
- **Check:** `nf config validate`, `nf config validate --scope NAME` for a scope, and `nf doctor --api console` to test the token and each agent.

## What `nf config validate` checks

`nf config validate` runs static checks. It reads the loaded TOML and decrypts SOPS values locally. It makes no network call and prints no secret.

| Section | What it checks |
| :--- | :--- |
| Clusters, Users | Each `[clusters]` entry and each `users.toml` table is valid |
| Settings | The ONTAP API, DII API, Digital Advisor API, SMTP, Console and Licensing settings, plus the AIQUM API when you use AIQUM |
| Cluster Credentials | Every cluster resolves a user and password |
| AIQUM, AIQUM Credentials | Each `[aiqums]` entry is valid and has an `ip`, and resolves credentials. An `[aiqums]` inventory without `<config>/apis/aiqum/aiqumapi.toml` `[general]` is an error |
| Connectors | Each `[connectors]` entry is valid |
| Cloud Insights, Cloud Insights Credentials | Each `[cloudinsights]` tenant is valid and resolves an API token and a `base_url` |
| Spec Files | The OpenAPI spec of every configured API is in `<config>/apis/` |

A section other than the first four appears only when it has something to show, so a config that does not use an API shows no line for it.

An error exits 1 and the output ends with a hint for each one, such as `nf config set-credential --cluster NAME --user USER` for a cluster without credentials. A missing spec file is only a warning and the exit code stays 0: the configuration is valid, but the client raises `FileNotFoundError` when it is built. The warning says which file is missing and gives `nf config download-spec --api <api>` as the fix (see [Spec files](#spec-files)).

An API counts as configured when its `*api.toml` has a `[general]` section. DII also counts when `[cloudinsights]` has a tenant, and Console when the root or any scope has a `consoleapi.toml` `[general]`. The OCCM spec is never checked. `nf config validate --scope NAME` checks that scope's inventory and settings and no spec file, because specs live in `<config>/apis/`.

## `nf doctor` or `nf config validate`

`nf config validate` is the offline check, suited to CI. `nf doctor` runs the same static checks, then checks `sops`, the age key, every SOPS value and the caches, then sends one read-only request to each configured API. It prints a fix hint for each problem.

- `nf doctor` also compares your `[clusters]` names with Console's working environments in the OCCM cache, per account, and reports a renamed cluster as an error. If that cache is missing or stale, it says to run `nf cache occm refresh`.
- `nf doctor --offline` skips the requests. `nf doctor --api NAME` limits every check to that API's settings, credentials, SOPS values, cache and live check, plus the shared `sops` and age-key checks (`ontap`, `aiqum`, `dii`, `console`, `digitaladvisor`).
- Every request is a `GET`, with two `POST` cases. The Console OAuth token request goes to the token endpoint and changes no Console resource; a static `user_token` or `service_token` makes none. The Digital Advisor check sends one read-only GraphQL query as a `POST`; with a refresh token it also refreshes and writes the rotated tokens to `digitaladvisorapi.toml`, but only when the stored access token is missing, expired or rejected.
- The first contact with an ONTAP or AIQUM host records its TLS fingerprint in the local trust store, as `nf utils validate` does.
- It exits 1 on any error; warnings do not fail. No output contains a credential.

See [CLI reference: doctor](../reference/cli.md#doctor).

## Next steps

- Read the [Usage Guide](../usage/basics.md).
- Look up every field in the [Config schema](../reference/config-schema.md).
- See the [CLI Reference](../reference/cli.md) for `nf config` and the other commands.
