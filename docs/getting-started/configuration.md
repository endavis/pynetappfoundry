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

`nf config init-sops` creates an age key and wires SOPS so credentials are stored encrypted:

```bash
nf config init-sops
```

It writes `.envrc.local`, `.sops-public-key.txt` and `.gitignore` in the current directory, and the age private key to `~/.sops/age/keys.txt`. Back up that key; encrypted values cannot be read without it. See [CLI Reference: config](../reference/cli.md#config) for its options and [Config schema: SOPS-encrypted values](../reference/config-schema.md#sops-encrypted-values) for which fields accept an encrypted value.

## Spec files

The API clients read an OpenAPI spec from `<config>/apis/<name>/` when they are constructed. A missing spec raises `FileNotFoundError`.

The installed package does not contain any spec. The wheel that `pip` and `uv` install holds only the Python code, and nothing copies a spec into your config directory for you. Copy the committed spec from the repository at the release tag you installed (from a clone, or from GitHub at that tag). The generated models come from the committed spec, so a copy from the same tag matches the installed code.

From a checkout you can also refresh a spec from a live system. `doit fetch_spec` writes `docs/example-config/apis/<api>/all.json` in the repo, sanitizing the spec on the way, and you copy that file into `<config>/apis/<api>/`.

| API | File | Copy from | Refresh from a checkout |
| :--- | :--- | :--- | :--- |
| ONTAP | `<config>/apis/ontap/all.json` | `docs/example-config/apis/ontap/all.json` | `doit fetch_spec --api=ontap --host=<cluster> --username=<user> --password=<password>` |
| AIQUM | `<config>/apis/aiqum/all.json` | `docs/example-config/apis/aiqum/all.json` | `doit fetch_spec --api=aiqum --host=<aiqum> --username=<user> --password=<password>` |
| DII | `<config>/apis/dii/all.json` | `docs/example-config/apis/dii/all.json` | `doit fetch_spec --api=dii --host=<tenant> --api-key=<token>` |
| Console | `<config>/apis/console/console_openapi.yaml` | `tools/console_openapi/generated/console_openapi.yaml` | `doit console_openapi_refresh` |

Every `fetch_spec` call also accepts `--no-verify` to skip TLS certificate validation. After a refresh, `doit convert_specs` and `doit generate_models` rebuild the converted spec and the models.

## ONTAP

- **Inventory:** add each cluster to a data file as `[clusters.NAME]` with an `ip` (see [Config schema: Clusters](../reference/config-schema.md#clusters)).
- **Credentials:** `nf config set-credential --cluster NAME --user USER` stores them on the cluster entry. A default for every cluster goes under `[clusters]` in `users.toml` (see [Config schema: Credential Resolution Order](../reference/config-schema.md#credential-resolution-order)). The API uses HTTP Basic authentication.
- **Settings:** `<config>/apis/ontap/ontapapi.toml` with a `[general]` section (see [Config schema: ontapapi.toml](../reference/config-schema.md#ontapapitoml)).
- **Spec:** `<config>/apis/ontap/all.json` (see [Spec files](#spec-files)).
- **Check:** `nf config validate`.

## AIQUM

- **Inventory:** add each instance as `[aiqums.NAME]` with an `ip`.
- **Credentials:** `nf config set-credential --type aiqums --name NAME --user USER`, or a default under `[aiqums]` in `users.toml`.
- **Settings:** `<config>/apis/aiqum/aiqumapi.toml` with a `[general]` section.
- **Spec:** `<config>/apis/aiqum/all.json` (see [Spec files](#spec-files)).
- **Check:** `nf config show -s aiqums` and `nf config show -s aiqumapi`. `nf config validate` does not check AIQUM yet, so a clean `validate` says nothing about it.

The fields are in [AIQUM API: Setup](../usage/aiqum-api.md#setup).

## DII (Data Infrastructure Insights)

- **Inventory:** add each tenant as `[cloudinsights.NAME]` with an `ip` (see [Config schema: Cloud Insights](../reference/config-schema.md#cloud-insights)).
- **Credentials:** the API token. `nf config set-credential --setting diiapi.api_ro_token` stores one for every tenant in `diiapi.toml`. `nf config set-credential --type cloudinsights --name NAME --user LABEL` stores one per tenant. The client sends it in the `X-CloudInsights-ApiKey` header.
- **Settings:** `<config>/apis/dii/diiapi.toml` with a `[general]` section (see [Config schema: diiapi.toml](../reference/config-schema.md#diiapitoml)).
- **Spec:** `<config>/apis/dii/all.json` (see [Spec files](#spec-files)).
- **Check:** `nf config validate` and `nf config show -s cloudinsights`.

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
- **Check:** `nf config validate`, and `nf config validate --scope NAME` for a scope.

## What `nf config validate` checks

`nf config validate` checks the `[clusters]` entries, `users.toml`, the ONTAP API, DII API, SMTP, Console and Licensing settings, and the cluster credentials. It does not check `aiqumapi.toml`, the `aiqums`, `connectors` and `cloudinsights` inventory with their credentials, or any spec file. Use `nf config show -s <section>` for those. Extending `validate` is tracked in [#1111](https://github.com/endavis/pynetappfoundry/issues/1111).

## Next steps

- Read the [Usage Guide](../usage/basics.md).
- Look up every field in the [Config schema](../reference/config-schema.md).
- See the [CLI Reference](../reference/cli.md) for `nf config` and the other commands.
