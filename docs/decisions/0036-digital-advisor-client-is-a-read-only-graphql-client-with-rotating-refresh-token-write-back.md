---
title: "ADR-0036: Digital Advisor client is a read-only GraphQL client with rotating refresh-token write-back"
description: Digital Advisor is read through a small read-only GraphQL client that rotates and writes back its refresh token.
date: 2026-11-19
audience:
  - contributors
tags:
  - adr
---

# ADR-0036: Digital Advisor client is a read-only GraphQL client with rotating refresh-token write-back

## Status

Accepted

## Context

Issue [#1051](https://github.com/endavis/pynetappfoundry/issues/1051) adds a client for Active IQ Digital Advisor. Facts below are marked as measured (a read-only probe on 2026-11-19), *(docs)* (NetApp documentation) or inferred.

Digital Advisor has two APIs. The GraphQL API (`https://gql.aiq.netapp.com/graphql`, `Authorization: Bearer <token>`) is the recommended one *(docs)*; its introspection works without authentication (measured). The REST API (`https://api.activeiq.netapp.com/v1|v2/`) has no public OpenAPI file (measured), is being phased out *(docs)*, and rejects a personal access token with 401 (measured). The backend that feeds `DataSource` is [#1116](https://github.com/endavis/pynetappfoundry/issues/1116).

## Decision

1. **A small GraphQL client, not the OpenAPI layer.** `DigitalAdvisorAPIClient` posts `{"query", "variables"}` with `requests`. It does not sit on `APIWrapper`, because there is no OpenAPI file and REST is being phased out. TLS uses default verification; TOFU pinning is for self-signed ONTAP and AIQUM hosts. REST is used only for the token refresh.
2. **Two credential modes, or both, in `digitaladvisorapi.toml [general]`.** At least one of `personal_access_token` (valid 1-90 days *(docs)*, used as is) or `refresh_token`; `access_token` needs `refresh_token`. With both set the PAT is used first and the refresh pair is the fallback ([#1120](https://github.com/endavis/pynetappfoundry/issues/1120)). With a working PAT there is no token request and no config write until it fails. All three accept `SOPS[...]` and are `set-credential --setting` targets ([ADR-0031](0031-one-command-stores-every-sops-secret-and-encrypt-value-is-removed.md)). The tokens live in this file, not in `users.toml` like the Console refresh token, because they rotate and the write-back needs one unambiguous target. The file is root only. The field is not called `pat`, because `config show` masks keys by substring.
3. **Token handling.** The access token is a JWT valid for one hour (measured). The client reads only `exp`, without verifying the signature, and refreshes 60 seconds early. If `exp` cannot be read, it uses the token until the server answers `UNAUTHENTICATED` (HTTP 200 with `errors[].extensions.code`, measured), then refreshes once and retries once. A PAT that is rejected raises an error saying it has probably expired. With both credentials, a rejected PAT switches the client to the refresh pair for the rest of its life and logs one warning that names the credentials, never a value. The retry is once per credential, so a query sends at most three GraphQL POSTs: PAT, stored access token, refreshed access token. If both fail, the `DigitalAdvisorAuthError` names the renewal step for each credential. Claims and tokens are never logged. The refresh is `POST /v1/tokens/accessToken` with `{"refresh_token"}` and returns both a new `access_token` and a new `refresh_token` on every call (measured). A refresh answered with 400, 401 or 403 is treated as an expired 90-day login window *(docs)*. Those failure statuses were not measured: this is inferred.
4. **Write-back.** After each refresh both new tokens are written to the file in one atomic tomlkit write that keeps comments, SOPS-encrypted when the stored `refresh_token` is. Saving the access token too lets runs within the hour skip the rotation. The write helpers moved from the CLI to `src/pynetappfoundry/core/settings_files.py`, and the write is now atomic (temp file, `fsync`, `os.replace`, mode kept). If the write fails, the client logs an error naming the file and the exception type, never a value, and the call continues with the in-memory tokens, because the data was already fetched. The trade-off: the next run starts from an older stored token. The old token still worked right after an exchange in one test; a longer delay was not measured.
5. **Concurrent refresh is a known limitation.** Two processes refreshing at once are not coordinated; the later write wins. No lock file is added.
6. **Rate limit and retries.** The service allows 300 requests per 5 minutes per IP and answers 429 `USER_API_RATE_LIMIT_EXCEEDED` *(docs)*; no rate-limit headers are sent (measured). The client keeps a sliding window of 300 requests per 300 seconds and retries 429, 502, 503, 504 and connection errors with exponential backoff (5 attempts, 5 s start, 120 s cap), honouring `Retry-After`. The retry loop is hand-written so tests can inject the sleep.
7. **Read only.** `ensure_read_only` scans the document before any request and rejects anything but `query` and `fragment`. The schema has mutations (creating and revoking tokens, measured); they are never sent.
8. **The schema is downloaded, never shipped, and not used at run time.** `nf config download-schema` runs the introspection query without credentials and writes `<config>/apis/digitaladvisor/schema.json`. No NetApp schema is committed or packaged. The client does not validate queries against it: that needs a GraphQL parser (a new dependency), and the server already answers HTTP 400 `GRAPHQL_VALIDATION_FAILED` (measured). The file is reference data for query authors and for #1116.
9. **Typed methods.** `list_systems` and `list_volumes` wrap hand-written documents over `paginate()`. Their default selections are only the scalar fields the probe confirmed; `fields` overrides them, each name checked against `^[A-Za-z_][A-Za-z0-9_]*$` so nothing can be injected. The four required `systems` arguments are required keyword arguments. The filter names are the measured ones; their GraphQL types, and `$pageSize: Int` and `$after: String`, are inferred from the names, and a wrong one surfaces as `GRAPHQL_VALIDATION_FAILED`. There is no `list_clusters`: no `Cluster` fields were measured. The `page_size` default of 100 is not a measured value.
10. **`nf doctor` probes Digital Advisor.** The live check ([#1117](https://github.com/endavis/pynetappfoundry/issues/1117)) refreshes and writes back only when the stored access token is missing, expired or rejected; see [ADR-0035](0035-nf-doctor-runs-static-environment-and-read-only-live-checks-with-fix-hints.md) §10. `nf config validate` has a static "Digital Advisor API" row ([ADR-0034](0034-config-checks-are-shared-static-functions-returning-structured-results.md)).

## Rationale

A hand-written client over GraphQL is the smallest thing that works against the API NetApp recommends, and keeps REST out of new code. Keeping the rotating tokens in one root file makes the write-back unambiguous and reuses the `--setting` machinery. Logging and continuing on a failed write-back protects data already fetched. Not validating against the schema avoids a new dependency for a check the server does.

## Related Issues

- Issue #1051: feat: add an Active IQ Digital Advisor API client
- Issue #1120: feat: let a Digital Advisor refresh token back up the personal access token
- Issue #1116: DataSource backend for Digital Advisor
- Issue #1117: nf doctor live check for Digital Advisor
- Issue #533: DataSource non-ONTAP backends
- [ADR-0019](0019-console-runtime-client-architecture-org-scoped-access-and-per-token-type-wrapper-isolation.md), [ADR-0031](0031-one-command-stores-every-sops-secret-and-encrypt-value-is-removed.md), [ADR-0034](0034-config-checks-are-shared-static-functions-returning-structured-results.md), [ADR-0035](0035-nf-doctor-runs-static-environment-and-read-only-live-checks-with-fix-hints.md)

## Related Documentation

- [Digital Advisor API](../usage/digital-advisor-api.md)
- [Config schema: digitaladvisorapi.toml](../reference/config-schema.md#digitaladvisorapitoml)
- [CLI Reference](../reference/cli.md#config)
