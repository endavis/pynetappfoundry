# Console OpenAPI Generator

A build-time tool that converts NetApp's BlueXP / NetApp Console SaaS API
documentation into an OpenAPI 3.1 specification.

> [!WARNING]
> This generator and its output are **unofficial**. NetApp does not publish a
> machine-readable OpenAPI spec for this API surface. The spec is derived from
> the AsciiDoc sources at
> [`NetAppDocs/console-automation`](https://github.com/NetAppDocs/console-automation)
> and is provided on a best-effort basis. Validate against the live API before
> production use.

## What is generated

`generated/console_openapi.yaml` -- a combined OpenAPI 3.1 spec covering the
service folders listed in `info.x-included-source-folders`. v1 covers
`tenancy/` and `tenancyv4/` only; `cm/` is intentionally excluded because its
files are prose tutorials with `curl` examples and need a different parser.

`generated/console_openapi.lock.json` -- reproducibility metadata: source repo
URL, requested git ref, resolved commit SHA, tool version, and the expected
endpoint count. CI verifies that regenerating from this lockfile produces the
same spec.

## Regenerating

```bash
# via doit (preferred)
doit console_openapi_refresh -- --ref main

# direct CLI
uv run python -m tools.console_openapi.cli build [--ref REF] [--service NAME ...] [--lenient]
```

The fetcher uses the system `git` binary and caches a shallow clone under
`$XDG_CACHE_HOME/console-openapi/console-automation`.

## How it works

1. **Fetch** -- shallow-clone (or refresh) `NetAppDocs/console-automation` at
   the requested ref.
2. **Parse** -- walk the included service folders. Each `.adoc` file is parsed
   into an intermediate Pydantic AST (`models.ParsedEndpoint`). Files that
   carry `api: true` in front-matter but contain no `[.api-doc-operation-*]`
   line are recorded as overview pages and skipped.
3. **Build** -- assemble paths, components, and security schemes:
   - `Authorization` header parameters are suppressed and converted to
     `BearerAuth` security on the operation. The `*Token usage:*` callout is
     preserved as `x-token-type: user|service`.
   - Definition anchors become per-file namespaced component schemas
     (`<service>.<file_stem>.<anchor>`). Anchors that have no table fall back
     to either an `additionalProperties` map (for "Hash mapping strings to
     string") or a prose-only `{type: object}` schema -- never a dangling
     `$ref`.
   - 204 responses, and responses without a body table or example, omit
     `content`.
4. **Validate** -- a final invariant pass enforces:
   - no unresolved `$ref`s,
   - every path-template variable has a matching `required: true` path
     parameter,
   - every `operationId` is unique,
   - no `Authorization` header parameter survives, and
   - duplicate `verb + path` combinations either match exactly (deduped) or
     raise.
   `openapi-spec-validator` runs against the final document.

## Server URLs

The generated spec includes per-operation `servers` blocks because the two
services live at different base URLs:

| Service     | Base URL                                          | Notes                                                |
| :---------- | :------------------------------------------------ | :--------------------------------------------------- |
| `tenancy`   | `https://api.bluexp.netapp.com`                   | v3 paths already include the `/tenancy/...` segment. |
| `tenancyv4` | `https://api.bluexp.netapp.com/v1/management`     | Discovered via `tenancyServiceInformation.urlV4`.    |

These were verified against the live SaaS using a user JWT.

### Dynamic discovery

The Console exposes an unauthenticated bootstrap endpoint that returns the
canonical URLs for every BlueXP/Console subservice:

```
GET https://api.bluexp.netapp.com/occm/api/occm/system/support-services
```

Relevant fields:

- `tenancyServiceInformation.url`   → v3 base
- `tenancyServiceInformation.urlV4` → v4 base
- `agentsMgmtUrl`, `licenseServiceInformation.url`, etc. → other services

Consumers that need to follow URL changes over time should hit this endpoint
at startup rather than hard-coding hosts.

## Failure modes

- **Strict (default)**: any malformed endpoint file aborts the build.
- **Lenient (`--lenient`)**: malformed files are skipped with a warning and
  the build continues. Use only when exploring upstream changes; do not
  commit a lenient-mode spec.

## Dependencies

Runtime: `pyyaml`, `pydantic`, `click`, system `git`.
Dev only: `openapi-spec-validator`.

## Adding a new service

1. Confirm the folder follows the auto-generated format (front-matter +
   `[.api-doc-operation]` line + 4/5-column tables). If it uses prose
   tutorials with curl examples (like `cm/`), it needs a different parser.
2. Add the folder name to the `--service` list in
   `tools/doit/console_openapi_tasks.py` or pass it on the CLI.
3. Regenerate; update fixtures and tests for any new edge cases.
