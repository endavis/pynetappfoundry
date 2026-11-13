---
title: Console Agent
description: Manage on-prem working environments through a Console agent with ConsoleAgentClient
audience:
  - users
tags:
  - console
  - agent
  - occm
  - api
---

# Console Agent

`ConsoleAgentClient` calls a Console agent's `/occm/api` through the Console SaaS host. Use it to list, add and delete on-prem ONTAP working environments. One instance serves one agent: every request carries `x-agent-id: <agent_id>` and a bearer token.

## Configuration

It reads the same settings as `ConsoleAPIClient`, from `consoleapi.toml` (see [Config schema: consoleapi.toml](../reference/config-schema.md#consoleapitoml)).

## Where the agent id comes from

The agent id is the id of the Console agent (connector) you want to reach; it ends in `clients`. The agent itself returns it as `agentId` from `GET /occm/api/occm/system/about`, and `about()` returns the same value, which lets you confirm you reached the intended agent. Listing agents is not wrapped by this project.

## Workspace id for `add`

`add_onprem_working_environment(tenant_id=...)` takes the Console **workspace** id, the `workspacePublicId` from `GET /tenancy/account/{accountId}/workspace`. A working environment reports its `tenantId` in a different, `Tenant-…` form. Passing that value back to `add` fails: the agent answers HTTP 500, and its audit log shows the Tenancy service lookup returned 404. This was measured against a lab agent (#1001).

## Construction

```python
from pynetappfoundry.clients import ConsoleAgentClient

agent = ConsoleAgentClient(config, "your-agent-id")
```

Token source, first match wins:

1. an injected `token_provider`;
2. a refresh token from `users.toml` `[console]` (a user token via the OAuth refresh-token grant; a bad token raises `ConsoleAuthError` at construction);
3. `user_token`;
4. OAuth client credentials (bad credentials raise `ConsoleAuthError` at construction);
5. a static `service_token`.

A refresh token and `user_token` are mutually exclusive in the settings, so 2 and 3 never both apply.

To share one OAuth token cache with `ConsoleAPIClient`, pass its user provider when a refresh token is configured, or its service provider for client credentials:

```python
from pynetappfoundry.clients.console import ConsoleAPIClient, ConsoleAgentClient

console = ConsoleAPIClient(config)
provider = console.user_token_provider or console.service_token_provider
agent = ConsoleAgentClient(config, "your-agent-id", token_provider=provider)
```

`Console.get_connector` and `Console.find_connector` do this for you: they share the user provider when set, otherwise the service provider.

### Token types

| Token | Status |
|-------|--------|
| Service token | Measured working: about, list and get (#1008), and add and delete (#1001). |
| User token | Measured working: about and the on-prem list (#734). Add and delete were not tested with a user token. NetApp's own examples use one (`cm/your_api_call.adoc`). |

## Methods

Responses are generated `cvo` models.

```python
about = agent.about()  # about.agentId

# clusterUuid is only returned when requested through `fields`
envs = agent.list_onprem_working_environments(fields=["ontapClusterProperties"])
env = agent.get_onprem_working_environment("working-environment-id")

created = agent.add_onprem_working_environment(
    tenant_id="your-workspace-public-id",  # not the Tenant-… value a working environment reports
    cluster_address="cluster.example.test",
    cluster_user_name="admin",
    cluster_password="your-cluster-password",  # str or SecretStr
    name="my-cluster",
)

agent.delete_onprem_working_environment(created.publicId)
```

`list_onprem_working_environments` also takes `tenant_id`. `fields` is a string, or a sequence that is comma-joined.

These methods are thin wrappers over `agent.ops`, the generated operations
(`ConsoleAgentOps`, see [ADR-0019](../decisions/0019-console-runtime-client-architecture-org-scoped-access-and-per-token-type-wrapper-isolation.md)).
`agent.ops.create_onprem_working_environment(body)` takes a
`post_onprem_working_environments.RequestBody` directly and, like `add`, is never
retried on 5xx or timeout. `ConsoleAPIClient.ops` holds the tenancy operations.

## Connector for a cluster

`ConsoleInfo.connector` caches the compact `Connector` (`pynetappfoundry.models.console_types.Connector`) of the Console agent that manages a cluster.

```python
connector = agent.get_connector()  # from about(); agent_id, version, system_id, ...

# Match a cluster on this agent (lists with fields=ontapClusterProperties)
env = agent.find_onprem_working_environment("cluster-uuid")  # None when absent

# Search several agents through the org-scoped facade
connector = console.find_connector("cluster-uuid", ["agent-1clients", "agent-2clients"])
connector = console.find_connector("cluster-uuid")  # uses agent_ids from consoleapi.toml
```

- `Console.find_connector(cluster_uuid, agent_ids=None)` queries the agents in order, stops at the first match, and returns `None` when none matches. Errors propagate: an agent ID the Console does not know, or an agent that cannot be reached, raises `requests.HTTPError` instead of being skipped, so keep `agent_ids` current.
- Without an `agent_ids` argument it uses `agent_ids` from `consoleapi.toml` `[general]` (see [Config schema](../reference/config-schema.md#consoleapitoml)). With neither it raises `ValueError`, so a missing configuration is not mistaken for "no connector".
- The agent ids are configured because the tenancy API lists none for a service token.
- `Connector` keeps `agent_id`, `version`, `system_id`, `environment`, `agent_type` and `siteIdentifier.company` / `site`. `privateIp` and `siteIdentifier.host` are network addresses and are not kept, so they never reach the cache.

## Safety

- `add_onprem_working_environment` and `delete_onprem_working_environment` are not retried on a 5xx or timeout, so a transient failure cannot add the same working environment twice. A 401 still triggers one token refresh when a provider is in use.
- Secrets are never logged: the bearer token is redacted, request bodies are not logged, and invalid input raises a `ValueError` that names fields only.
- A response of an unexpected type raises `TypeError` naming only the type.
