---
title: Set Up Digital Advisor
description: Store a Digital Advisor personal access token or refresh token, and check that it works
audience:
  - users
tags:
  - how-to
  - configuration
  - digital-advisor
---

# Set Up Digital Advisor

**Goal:** connect `nf` to Active IQ Digital Advisor with a personal access token, a refresh token or both, and confirm that a read-only query works.

## Before you start

- A config directory, and SOPS set up for encrypted tokens: [Set up a config directory and SOPS secrets](sops-secrets.md).
- A Digital Advisor token from the Digital Advisor portal, one or both of:
    - a **personal access token** (PAT). It is valid for 1 to 90 days and is never refreshed.
    - a **refresh token**. `nf` uses it to get short-lived access tokens itself. Refreshing works for 90 days from your portal login.

With both, `nf` sends the PAT first and falls back to the refresh token only when the PAT is rejected.

## Steps

### 1. Store the token

For a personal access token:

```bash
nf config set-credential --setting digitaladvisorapi.personal_access_token
```

For a refresh token:

```bash
nf config set-credential --setting digitaladvisorapi.refresh_token
```

Each prompts for the token without echoing it, encrypts it, and writes it to `digitaladvisorapi.toml` `[general]`. The first one creates the file:

```
Setting digitaladvisorapi.personal_access_token stored
  File: config/apis/digitaladvisor/digitaladvisorapi.toml
  Table: general
  Key: personal_access_token
  Value: (encrypted)
```

No other key is required. `graphql_url` defaults to `https://gql.aiq.netapp.com/graphql`. See [Config schema: digitaladvisorapi.toml](../reference/config-schema.md#digitaladvisorapitoml).

### 2. Know what a refresh writes

Every refresh returns a new refresh token, so `nf` writes both new tokens back to `digitaladvisorapi.toml`. They are encrypted when the stored refresh token is. This happens on normal use and on `nf doctor`, whenever the stored access token is missing, expired or rejected. Keep the file writable, and don't copy an old version back over it: that restores a refresh token the server no longer accepts. See [Digital Advisor API: Token rotation](../usage/digital-advisor-api.md#token-rotation).

### 3. Download the GraphQL schema (optional)

```bash
nf config download-schema
```

It fetches the schema by introspection, with no credentials, and writes `<config>/apis/digitaladvisor/schema.json`. `nf` never reads the file at run time; it is a reference for writing queries, such as looking up filter enum values. See [Digital Advisor API: Schema](../usage/digital-advisor-api.md#schema).

## Check it worked

```bash
nf config validate
```

Among its lines:

```
│   ├── Digital Advisor API
...
Configuration is valid
```

Then the live check. It sends one read-only GraphQL query:

```bash
nf doctor --api digitaladvisor
```

The output below comes from a working setup with both a PAT and a refresh token, SOPS-encrypted. It exits 0:

```
nf doctor
├── Config: Settings
│   └── Digital Advisor API
├── SOPS
│   ├── sops is installed
│   ├── age key: key file ~/.sops/age/keys.txt
│   ├── settings.digitaladvisorapi.general.personal_access_token: decrypts
│   └── settings.digitaladvisorapi.general.refresh_token: decrypts
└── Digital Advisor
    └── Digital Advisor: token works (personal access token)
```

The PAT worked, so nothing was refreshed and the file was not written. The Digital Advisor row can also read:

| Row | Meaning |
| :--- | :--- |
| `token works (personal access token)` | The PAT works. |
| `token works (stored access token; no refresh)` | Refresh token only: the stored access token still works, so nothing was written. |
| `token works; the access token was missing or expired, so doctor refreshed it and wrote the rotated tokens to digitaladvisorapi.toml` | Refresh token only: doctor refreshed, and stored the new tokens. |
| `token works via the refresh_token fallback ...` (warning) | The PAT was rejected, and the refresh token worked. Store a new PAT before the refresh token's 90 days run out. |

## If it fails

| `nf doctor` shows | Cause | Fix |
| :--- | :--- | :--- |
| `Digital Advisor: token rejected (UNAUTHENTICATED)` | PAT only: the PAT has probably expired | `nf config set-credential --setting digitaladvisorapi.personal_access_token` |
| `Digital Advisor: token rejected (UNAUTHENTICATED)`, with a hint to log in to the portal | Refresh token: the access token was rejected, and so was the refreshed one | Log in to the portal, then `nf config set-credential --setting digitaladvisorapi.refresh_token` |
| `Digital Advisor: token refresh failed` | The refresh request failed, often because the 90-day login window ended | Log in to the portal, then store a fresh refresh token as above. |
| `Digital Advisor: token works, but the rotated tokens could not be written back` (warning) | The refresh worked, but `digitaladvisorapi.toml` could not be written | Make the file writable. The stored refresh token may now be stale: store a fresh one as above. |
| `Digital Advisor: unreachable (ConnectionError)` | The network path or a proxy blocks `gql.aiq.netapp.com` | Check DNS, routing and any proxy. |
| `<field>: SOPS value does not decrypt (SOPSError)` | The key cannot decrypt the stored token | See [SOPS: If it fails](sops-secrets.md#if-it-fails). |

## Next

- [Digital Advisor API](../usage/digital-advisor-api.md): query Digital Advisor from Python
- [Set up AIQUM](setup-aiqum.md)
- [Set up Console and its agents](setup-console.md)
