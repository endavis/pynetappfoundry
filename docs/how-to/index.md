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
| [Set up AIQUM](setup-aiqum.md) | AIQUM instances in the inventory with credentials, confirmed by `nf doctor` |
| [Set up Digital Advisor](setup-digital-advisor.md) | A stored personal access token or refresh token that `nf doctor` confirms |
| [Set up Console and its agents](setup-console.md) | A Console account, root or per scope, and its agents, confirmed by `nf doctor` |
| [Fill the cache and query it](fill-and-query-cache.md) | A filled, fresh cache, and fields read from it as text, JSON or CSV |
| [Find expiring licenses and export them to CSV](check-licenses.md) | A license list in a CSV file, and the license check with its email behaviour understood |
| [Check recent events by severity](check-events.md) | EMS events of one or more clusters in a CSV file |
| [Run nf unattended](run-unattended.md) | An `nf` command on a cron or systemd schedule that finds its config and key, and reports failure by exit code |
| [Use scopes to separate environments](use-scopes.md) | A config directory split into scopes, each with its own inventory, credentials and thresholds, checked one at a time |
| [Diagnose a failing setup with nf doctor](diagnose-with-doctor.md) | The failing check found and fixed from its hint, with the exit codes and options of `nf doctor` |
| [Run compliance checks against your fleet](run-compliance-checks.md) | A rules file and `nf cache compliance` run against every cached cluster, with its exit code |
| [Script against the Python API](script-python-api.md) | A Python script that loads the config, finds clusters and reads their cached data |

## How each guide is laid out

1. **Goal:** what you will have at the end, in one sentence.
2. **Before you start:** what must already be in place, with a link to the guide that sets it up.
3. **Steps:** numbered commands and config snippets.
4. **Check it worked:** `nf config validate` and `nf doctor`, with the output to expect.
5. **If it fails:** the messages you may see, their cause, and the fix.
6. **Next:** related guides and reference pages.

Example names and addresses use placeholders: `cluster1`, `tenant1`, `aiqum1`, `bu1`, and the documentation range `192.0.2.0/24`. `<config>` stands for your config directory, which is `./config` by default. Command output shows it as `config/`.
