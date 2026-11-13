# Console OpenAPI Generator

A build-time tool that converts NetApp's BlueXP / NetApp Console SaaS API
documentation into an OpenAPI 3.0.3 specification.

> [!NOTE]
> The spec is emitted as OpenAPI 3.0.3 even though `tenancy/` and
> `tenancyv4/` evolve independently of any particular OpenAPI version. The
> parsed AsciiDoc uses no OpenAPI 3.1-only constructs (verified against the
> live upstream content), so the lower version maximises tooling
> compatibility — most notably `datamodel-code-generator`, which the
> Pydantic codegen pipeline (`doit console_models`) relies on.

> [!WARNING]
> This generator and its output are **unofficial**. NetApp does not publish a
> machine-readable OpenAPI spec for this API surface. The spec is derived from
> the AsciiDoc sources at
> [`NetAppDocs/console-automation`](https://github.com/NetAppDocs/console-automation)
> and is provided on a best-effort basis. Validate against the live API before
> production use.

## What is generated

`generated/console_openapi.yaml` -- a combined OpenAPI 3.0.3 spec covering the
service folders listed in `info.x-included-source-folders`: `tenancy/`,
`tenancyv4/` and `cvo/` (the Console agent, or OCCM, API). `cm/` is intentionally excluded because its
files are prose tutorials with `curl` examples and need a different parser.

`generated/console_openapi.lock.json` -- reproducibility metadata: source repo
URL, requested git ref, resolved commit SHA, tool version, and the expected
endpoint count. CI verifies that regenerating from this lockfile produces the
same spec.

## Regenerating

```bash
# via doit (preferred)
doit console_openapi_refresh --ref <full-commit-sha>

# direct CLI
uv run python -m tools.console_openapi.cli build [--ref REF] [--service NAME ...] [--lenient]
```

Pass a full commit SHA rather than a branch name, so the lockfile's
`requested_ref` stays pinned. The fetcher uses the system `git` binary and caches a shallow clone under
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
     `content`. A `Status: Default` block becomes the OpenAPI `default`
     response.
   - For `tenancy`, `tenancyv4` and `cvo`, inline request and response bodies
     move into named components (`<service>.<file_stem>.RequestBody`,
     `ResponseBody` for the `default` response, `Response<status>Body`
     otherwise). Only `cvo` operations get a required, synthesized
     `x-agent-id` header parameter.
     The docs over-mark response fields as Required (the live agent returns
     `null` or omits them; `tenancyv4` marks `type`, `version` and `items`
     Required on responses callers omit), so every schema reachable from a
     response of these services has `required` renamed to
     `x-documented-required` and its generated fields are optional;
     request-only schemas keep `required` (#1018, #1027).
   - Path parameters missing from the docs are synthesized in path-template
     order.
4. **Validate** -- a final invariant pass enforces:
   - no unresolved `$ref`s,
   - every path-template variable has a matching `required: true` path
     parameter,
   - every `operationId` is unique,
   - no `Authorization` header parameter survives, and
   - duplicate `verb + full path` combinations either match exactly (deduped)
     or raise.
   `openapi-spec-validator` runs against the final document.

## Server URLs

Every path key in the generated spec is the full path from the host: the
builder adds each service's base path in front of the documented path. The
base paths are recorded once in `info.x-service-base-paths`, and every
operation carries one bare-host server, `https://api.bluexp.netapp.com`.

| Service     | Base path        | Notes                                                |
| :---------- | :--------------- | :--------------------------------------------------- |
| `tenancy`   | (empty)          | v3 paths already include the `/tenancy/...` segment. |
| `tenancyv4` | `/v1/management` | Discovered via `tenancyServiceInformation.urlV4`.    |
| `cvo`       | `/occm/api`      | Console agent API; every call needs `x-agent-id`.    |

These were verified against the live SaaS (`tenancy` and `tenancyv4` with a
user JWT, `cvo` with a service token, #1008). The `build`
command refuses a `--service` with no entry in `_SERVICE_BASE_PATHS`
(`tools/console_openapi/openapi/builder.py`), so a new service must declare its
base path first.

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

## Generated Pydantic models

The committed spec at `generated/console_openapi.yaml` is consumed by a
second build-time pipeline that emits Pydantic v2 models under
`src/pynetappfoundry/models/console/` (subdivided into `tenancy/`,
`tenancyv4/` and `cvo/` packages). The pipeline uses `datamodel-code-generator`
directly — it is intentionally **not** wired into `doit generate_models`,
which is reserved for cache-coupled per-cluster API models. See
[ADR-0008 §"Codegen integration for Console (Issue #699)"](../../docs/decisions/0008-openapi-codegen-for-model-generation.md)
for the rationale.

```bash
# Regenerate the Pydantic tree (after a spec refresh, or when
# tools/doit/console_openapi_tasks.py is updated).
doit console_models

# Determinism guard: regenerate and assert the diff is empty.
doit console_models_check
```

The generated tree is committed in-tree so consumers do not
need `datamodel-code-generator` installed at runtime; only the maintainer
running `doit console_models` does.

## Generated client surface

A third build-time step turns the committed spec and the manifest
`client_ops.toml` into typed operation classes under
`src/pynetappfoundry/clients/console/generated/` (`ConsoleTenancyOps` and
`ConsoleAgentOps`, exposed as `client.ops`). It is a hand-rolled generator,
`client_codegen.py`, with no extra dependency; see ADR-0019, "Generated
operation surface (#735)".

```bash
# Regenerate after editing client_ops.toml, or after regenerating the models.
doit console_client

# Determinism guard: regenerate and assert the diff is empty.
doit console_client_check
```

Each `[[operation]]` in the manifest has:

| Field | Meaning |
|-------|---------|
| `operation_id` | The spec's `operationId` (required). |
| `client` | `"console"` (`ConsoleAPIClient.ops`) or `"agent"` (`ConsoleAgentClient.ops`). |
| `name` | The generated method name, unique per client. |
| `response` | `"object"` (default) or `"list"`. The spec cannot say how many items a response holds, so a list is declared here. |
| `retry` | `true` keeps the wrapper's retry on a non-GET operation. Default: non-GET operations are not retried. |
| `only_query` | Optional list of spec query parameter names to expose. Default: all. |
| `query` | Optional per-parameter overlay. `{ fields = { style = "csv" } }` accepts a string or a sequence and joins it with commas. |

The generator fails, rather than guessing, on: an unknown `operationId`, a
duplicate method name, a query parameter that is not a plain string and has no
overlay, a header parameter other than the synthesized `x-agent-id`, an
`x-token-type` on an agent operation, and a missing model module or class.
Path parameters are always URL-encoded. The operation's `x-token-type` is
written into the call as a literal; an operation with none accepts either token.
A numeric success status maps to the `Response<status>Body` model (for example
`Response200Body`), and `default` maps to `ResponseBody`; every tenancy operation
therefore returns a generated model (#1027).

## Dependencies

Runtime: `pyyaml`, `pydantic`, `click`, system `git`.
Dev only: `openapi-spec-validator`, `datamodel-code-generator` (for
`doit console_models`). `client_ops.toml` is read with `tomllib` (standard
library) by `doit console_client`.

## Adding a new service

1. Confirm the folder follows the auto-generated format (front-matter +
   `[.api-doc-operation]` line + 4/5-column tables). If it uses prose
   tutorials with curl examples (like `cm/`), it needs a different parser.
2. Add its base path to `_SERVICE_BASE_PATHS` in
   `tools/console_openapi/openapi/builder.py`, then add the folder name to
   `DEFAULT_SERVICES` in `tools/console_openapi/cli.py` (or pass it with
   `--service`).
3. Regenerate; update fixtures and tests for any new edge cases.
