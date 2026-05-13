# ADR-0019: Console runtime client architecture: org-scoped access and per-token-type wrapper isolation

## Status

Proposed. Will be marked Accepted once issue #713 ships the v1 implementation.

## Context

PR #698 added a parser that produces an OpenAPI 3.0.3 spec for NetApp's BlueXP / Console SaaS (`tools/console_openapi/`), and PR #700 (issue #699) generated Pydantic v2 models from that spec (`src/pynetappfoundry/models/console/`). Both are *static artifacts*: no runtime client has been wired up, so the generated models are unreachable from `pynetappfoundry` callers.

Two design questions arise the moment a runtime client is added:

1. **Where does Console live in the access model?** The existing client APIs (DII, ONTAP, AIQUM) are reached via `ClusterEntry.<api>` (ADR-0010) because their data **is** per-cluster. Console is different — Console SaaS is *organization-scoped*. One Console organization typically owns many clusters. A DII/ONTAP-shaped access pattern (`cluster.console`) would force a per-cluster shape onto an org-scoped resource.

2. **How does the client carry two distinct token types?** Console's OpenAPI spec tags every operation with an `x-token-type` extension: either `user` (a logged-in user's JWT) or `service` (a service account's JWT). A single client process can hold both kinds of tokens, but the existing `APIWrapper` (`src/pynetappfoundry/clients/openapi.py`) takes a *static* `auth_header` dict — there is no built-in way to pick one token vs. another per-call without changing the contract that DII, ONTAP, and AIQUM also depend on.

Both questions appear at v1 (issue #713) and persist through any future expansion of Console surface coverage, so it is worth recording the decisions before code lands.

## Decision

Three coupled decisions:

### 1. Console primary access is org-scoped, not cluster-scoped

Instantiate Console via an org-level entry point:

```python
from pynetappfoundry.console import Console

console = Console(settings, org_id="org-123")
org = console.get_organization()
```

`ClusterEntry.console` (the per-cluster namespace pattern from ADR-0010) is **not** the primary access pattern. A `ClusterEntry.console` view *may* be added later as a thin convenience accessor (pre-filtered to the org that owns that cluster), but only when there is a concrete consumer that benefits from the cluster-scoped framing. It is not part of v1.

### 2. The runtime client wraps two `APIWrapper` instances internally, one per `x-token-type`

`ConsoleAPIClient` constructs two `APIWrapper` instances at init time — one carrying the user-token `Authorization` header, one carrying the service-token header — and stores them as private attributes. The `APIWrapper` contract is preserved unchanged.

Per-operation routing is **owned by the calling code** (hand-authored or generated), not by `APIWrapper` introspection. Each operation method picks the correct internal wrapper based on the operation's `x-token-type`:

```python
class ConsoleAPIClient:
    def __init__(self, settings: ConsoleAPISettings) -> None:
        self._user = APIWrapper(..., auth_header={"Authorization": f"Bearer {user_jwt}"})
        self._service = APIWrapper(..., auth_header={"Authorization": f"Bearer {service_jwt}"})

    def get_organization(self, org_id: str) -> Organization:  # x-token-type: user
        return self._user.request(...)

    def post_service_account(self, body: ServiceAccountBody) -> ServiceAccount:  # x-token-type: service
        return self._service.request(...)
```

Callers never touch `self._user` / `self._service` directly. The two-wrapper internals are private surface; reaching for them is a contract violation and a `ConsoleTokenTypeMismatch` exception may be raised at the wrapper boundary as a guard rail.

### 3. v1 hand-authors only the operation methods actually consumed; future expansion generates them

For issue #713's v1 scope (one concrete consumer: `CloudMetadata.organization`), the small number of operation methods is hand-authored. Each method picks its `_user` or `_service` wrapper based on the spec extension.

When Console surface coverage expands meaningfully (rule of thumb: more than ~10 endpoints, or a meaningful subset of the 222), the dispatch layer **must** be generated, not hand-authored. The natural evolution path: extend the Console codegen pipeline (currently models-only via `datamodel-code-generator` per ADR-0008) to also emit a typed client surface with each operation method's `x-token-type` baked in at codegen time. The two-wrapper internal design is preserved; only the source of the dispatch methods changes (human → generator).

## Rationale

Three decisions, each justified separately. The order matters: the org-scoping decision constrains the wrapper-isolation decision (org-level entry point becomes the natural home for the two-wrapper internals), and the wrapper-isolation decision constrains the codegen path (the generator emits dispatch into two named wrappers, not into a single header-swapping wrapper).

### Why org-scoped, not `ClusterEntry.console`

- **Category match.** Console SaaS's natural domain is the organization (subscriptions, folders, projects, service accounts, partnerships). Forcing it into a per-cluster shape would either duplicate org-level data on every cluster's entry, or build awkward "look up the org from the cluster" indirection at every call site.
- **No false promise of cluster scoping.** A `cluster.console.get_subscription()` call would suggest there is a subscription *per cluster*, when in fact there is one subscription *per org* shared across clusters. Org-scoped access removes that confusion.
- **`ClusterEntry.console` view stays optional.** When and if there is a concrete cluster-scoped attribute that benefits from pre-filtering (e.g., "the org that owns *this* cluster"), it can be added without renegotiating the primary access pattern.

### Why two internal `APIWrapper`s, not one with per-call header swap

The plausible alternatives at decision time were:

- **(a) Two internal wrappers, caller picks (chosen).** Each `APIWrapper` carries a static header. The dispatch lives in the operation methods (hand-authored or generated). `APIWrapper` contract is untouched.
- **(b) One wrapper, per-call `auth_header` override.** Requires `APIWrapper` to gain a per-call header override parameter. That change propagates to every existing client (DII, ONTAP, AIQUM) — even if those clients never use the new parameter, the contract surface grows.
- **(c) One wrapper, mutate `auth_header` in place per call.** Concurrency-unsafe and racy; rejected outright.

(a) wins on blast radius: the only file touched is `clients/console/api.py`. The cost of (a) — that operation methods must each know which wrapper to use — is exactly the codegen-time decision that (3) above plans for at scale.

### Why hand-author v1, codegen the rest later

- **Hand-authoring scales poorly past ~10 endpoints.** 222 hand-written wrappers, each repeating the same shape, is a maintenance trap.
- **Codegen preserves the two-wrapper internal design.** The generator emits `self._user.request(...)` vs `self._service.request(...)` based on the spec extension; the runtime contract does not change.
- **v1 doesn't need codegen yet.** The concrete consumer (`CloudMetadata.organization`) needs one or two endpoints. Hand-authored is faster to ship; codegen is the natural next ticket when the second or third consumer arrives.

### Alternatives Considered

- **`ClusterEntry.console` as the only access pattern (DII shape).** Rejected — category mismatch (above).
- **One `APIWrapper` with per-call header swap.** Rejected — propagates contract change to every client. See (b) above.
- **Single token type, push x-token-type concerns to the caller (raw httpx).** Rejected — gives up the `APIWrapper` retry / error handling for Console specifically. Inconsistent with other clients.
- **Auto-attach auxiliary header parameters from spec extensions.** Rejected — couples the client to operation-parameter inspection; out-of-band query/header parameters stay caller-supplied per OpenAPI semantics.

## Consequences

### Positive

- `APIWrapper` contract preserved; no impact on DII, ONTAP, AIQUM.
- Console's org-scoped natural domain is reflected in its access pattern, not hidden behind a per-cluster veneer.
- The v1 → codegen evolution is continuous: hand-authored methods at v1 become generated methods at scale, with no internal redesign.
- The two-wrapper isolation prevents the "wrong token type" footgun by design: callers cannot accidentally reach for the wrong wrapper because the wrappers are not public surface.

### Negative

- Console is the first API in `pynetappfoundry` not reached via `ClusterEntry.<api>`. Developers familiar with the DII / ONTAP / AIQUM shape must learn that Console is different.
- Two `APIWrapper` instances per `Console` client means double the spec-parsing cost at construction time. Mitigation: share the parsed OpenAPI dict between the two wrappers at construction.
- The eventual codegen dispatch layer is *new* codegen (not the existing `tools/codegen/` cache pipeline, not `datamodel-code-generator`'s built-in output). When that ticket is taken on, choose between (a) hand-rolled dispatch codegen on top of the parsed spec + already-generated models, or (b) switching to a tool that emits both models and client (e.g., `openapi-python-client`) and accepting model regeneration churn.

## Related Issues

- Issue #697 / PR #698: feat: add BlueXP / Console SaaS docs to OpenAPI 3.1 parser (then 3.0.3)
- Issue #699 / PR #700: feat: generate Pydantic models from Console OpenAPI spec
- Issue #713: feat: wire Console SaaS auth and runtime client (the v1 implementation this ADR governs)

## Related Documentation

- Console parser: `tools/console_openapi/`
- Generated Console models: `src/pynetappfoundry/models/console/`
- `APIWrapper` contract: `src/pynetappfoundry/clients/openapi.py`
- DII per-cluster precedent (intentionally not followed for primary access): `src/pynetappfoundry/clients/dii/api.py`, `src/pynetappfoundry/core/models.py::DIIAPISettings`
- [ADR-0008: OpenAPI codegen for model generation](0008-openapi-codegen-for-model-generation.md) — covers the Console codegen split; this ADR is its runtime counterpart.
- [ADR-0010: ClusterEntry and namespace access pattern](0010-clusterentry-and-namespace-access-pattern.md) — establishes the per-cluster pattern that Console deliberately diverges from.
- Console runtime client implementation (forthcoming with issue #713): `src/pynetappfoundry/clients/console/api.py`
