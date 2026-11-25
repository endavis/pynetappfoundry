---
title: Run nf Unattended
description: Run nf commands from cron or a systemd timer, with the config directory, the SOPS age key, logs and exit codes set up for a scheduled job
audience:
  - users
tags:
  - how-to
  - configuration
  - automation
---

# Run nf Unattended

**Goal:** run an `nf` command on a schedule, such as a nightly `nf cache refresh --all`, so that it finds its config and key, writes its files where you expect, and reports failure through its exit code.

## Before you start

- A working config directory, checked by hand with `nf doctor`: [Set up a config directory and SOPS secrets](sops-secrets.md).
- Every credential stored where a job can read it without a prompt. A job cannot answer a password prompt.
- A service account or user that runs the job and can read the config directory and the age key.

## Steps

### 1. Fix the working directory

`nf` resolves two paths against the directory it runs in:

- the config directory: `--config-dir`, or the `NF_CONFIG_DIR` environment variable, defaults to `config`;
- command output, logs and downloaded files go under `data/<command>/` in the working directory, unless `--output-dir` is given.

A scheduler starts the job in a directory you did not choose, so set it. Either `cd` to a fixed directory first, or set `NF_CONFIG_DIR` to an absolute path and give `--output-dir`. The metadata cache always lives in the config directory, at `<config>/.cache/cluster_metadata.db`.

### 2. Make the age key reachable

When the config holds SOPS values, `sops` must be on the job's `PATH` and the age key must be readable. Without `SOPS_AGE_KEY_FILE`, `nf` uses `~/.sops/age/keys.txt` for the user that runs the job. Set `SOPS_AGE_KEY_FILE` when the job runs as a different user or the key is elsewhere. A scheduled job does not read your shell profile or `.envrc.local`, so set these variables in the job itself.

A credential can instead come from an environment variable, which takes precedence over the config files. See [Config schema: Environment Variables](../reference/config-schema.md#environment-variables).

### 3. Schedule the command

With cron, in the crontab of the user that runs the job:

```
PATH=/usr/local/bin:/usr/bin:/bin
NF_CONFIG_DIR=/srv/nf/config
SOPS_AGE_KEY_FILE=/srv/nf/keys.txt
30 2 * * * cd /srv/nf && nf cache refresh --all >> /srv/nf/cache-refresh.out 2>&1
```

With a systemd timer, the service unit sets the same things:

```ini
# /etc/systemd/system/nf-cache-refresh.service
[Service]
Type=oneshot
User=nf
WorkingDirectory=/srv/nf
Environment=NF_CONFIG_DIR=/srv/nf/config
Environment=SOPS_AGE_KEY_FILE=/srv/nf/keys.txt
ExecStart=/usr/local/bin/nf cache refresh --all
```

```ini
# /etc/systemd/system/nf-cache-refresh.timer
[Timer]
OnCalendar=*-*-* 02:30
Persistent=true

[Install]
WantedBy=timers.target
```

Enable it with `systemctl enable --now nf-cache-refresh.timer`. The unit's output goes to the journal: `journalctl -u nf-cache-refresh`.

Use the path that `command -v nf` prints for the account that runs the job. If `nf` is installed in a virtual environment, point at that environment's `bin/nf`.

## Check it worked

Run the job's command once by hand, as the job's user and from its working directory, before you schedule it. Then run the static and environment checks in the same way, which need no network:

```bash
nf doctor --offline
```

It exits 0 when there are no errors. A missing age key or a SOPS value that does not decrypt is an error, and the row says how to fix it.

## Exit codes and logs

| Exit code | Meaning |
| :--- | :--- |
| 0 | Success |
| 1 | An error. `nf cache refresh --all` exits 1 when any cluster failed. For `nf cache check` and `nf cache compliance`, 1 means matches or violations were found |
| 2 | A usage error, such as a bad option. For `nf cache check` and `nf cache compliance`, 2 means an error occurred |

Have the scheduler alert on a non-zero exit. See [CLI Reference: Exit Codes](../reference/cli.md#exit-codes).

Commands that read the inventory write a log file to `data/<command>/logs/` in the working directory, named after the command and the start time, such as `data/cache-refresh/logs/cache-refresh_2026-11-25_02-30-00.log`. Logs accumulate, so prune old ones. Add `--debug` to log more detail and to print a full traceback on an unexpected error.

## If it fails

| Symptom | Cause | Fix |
| :--- | :--- | :--- |
| `Configuration directory not found: <working directory>/config`, exit 1 | The job ran in another directory, and `NF_CONFIG_DIR` is not set | Set `NF_CONFIG_DIR`, or `cd` to the right directory first. |
| `age key missing: key file <path>` in `nf doctor` | The job's user has no key at that path | Set `SOPS_AGE_KEY_FILE` in the job. |
| `sops is not installed` in `nf doctor` | `sops` is not on the job's `PATH` | Set `PATH` in the crontab, or use the full path in the unit. |
| Output or logs land in an unexpected directory | They are relative to the working directory | Set the working directory, or pass `--output-dir`. |

## Next

- [CLI Reference](../reference/cli.md)
- [Cache reference](../reference/cache.md)
- [Set up a config directory and SOPS secrets](sops-secrets.md)
