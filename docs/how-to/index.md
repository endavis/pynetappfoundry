---
title: How-to Guides
description: Task-oriented guides that take you from a goal to a working, verified setup
audience:
  - users
tags:
  - how-to
---

# How-to Guides

Each guide takes one task from start to finish. They use real commands and show the output to expect. Use the [reference pages](../reference/config-schema.md) to look up a field, and a guide to get something working.

## Guides

| Guide | You end up with |
| :--- | :--- |
| [Set up a config directory and SOPS secrets](sops-secrets.md) | A config directory and an age key, so credentials are stored encrypted |
| [Add an ONTAP cluster and validate it](add-ontap-cluster.md) | A cluster in the inventory with credentials, confirmed by `nf doctor` |
| [Set up the DII API](setup-dii.md) | A DII tenant with a read-only token, and optionally more tenants and a read-write key |

## How each guide is laid out

1. **Goal:** what you will have at the end, in one sentence.
2. **Before you start:** what must already be in place, with a link to the guide that sets it up.
3. **Steps:** numbered commands and config snippets.
4. **Check it worked:** `nf config validate` and `nf doctor`, with the output to expect.
5. **If it fails:** the messages you may see, their cause, and the fix.
6. **Next:** related guides and reference pages.

Example names and addresses use placeholders: `cluster1`, `tenant1`, and the documentation range `192.0.2.0/24`. `<config>` stands for your config directory, which is `./config` by default. Command output shows it as `config/`.
