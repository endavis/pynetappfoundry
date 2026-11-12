---
title: "ADR-0025: Pin ONTAP SSH host keys and TLS certificate fingerprints on first use"
description: The ONTAP SSH and REST clients record each host's SSH host key and TLS certificate fingerprint on first use and require it to match afterwards.
date: 2026-11-11
audience:
  - contributors
tags:
  - adr
---

# ADR-0025: Pin ONTAP SSH host keys and TLS certificate fingerprints on first use

## Status

Accepted

## Context

The ONTAP clients connect to clusters that usually present self-signed TLS certificates and SSH host keys that nobody has distributed in advance. Until now `ONTAPCLI` accepted any SSH host key and kept it only in memory, and `ONTAPAPIClient` turned certificate validation off (`verify_ssl=False`). Neither client remembered which identity a cluster had presented, so a cluster whose identity changed looked the same as one seen for the first time. Issue [#980](https://github.com/endavis/pynetappfoundry/issues/980) asks for the identity to be recorded on first use and checked from then on. The behaviour is described in [Host identity](../usage/basics.md#host-identity-ssh-host-keys-and-tls-certificates).

## Decision

1. **Trust on first use.** The first connection to an ONTAP host records its identity. Later connections must present the same identity, otherwise `HostIdentityChangedError` is raised before credentials are sent. DII, AIQUM and OCCM clients are unchanged.
2. **Records live under `<config_dir>/.trust/`.** `known_hosts` holds SSH host keys in OpenSSH format, so `ssh-keygen -R` works on it. `tls_fingerprints.json` holds SHA-256 certificate fingerprints keyed `host:port`. The folder is not `.cache`: [ADR-0018](0018-cache-schema-versioning-and-backward-compatibility-policy.md) treats the cache as deletable and rebuildable, and trust records are not.
3. **One trust store per `Config`, injected.** `Config.get_trust_store()` builds and caches a `HostTrustStore`. `ONTAPCLI` takes an optional keyword `trust_store`; leaving it out keeps the previous in-memory behaviour. `ONTAPAPIClient` resolves the store from its `config`.
4. **SSH uses a custom `paramiko.MissingHostKeyPolicy`.** Paramiko checks the host key after key exchange and before authentication. The policy re-reads the file under a lock, compares, appends and writes atomically. `paramiko.BadHostKeyException` becomes `HostIdentityChangedError`, which names the host, the file and the reset command. Keys in the system `known_hosts` are still honoured.
5. **REST uses `FingerprintPinningAdapter`**, a `requests.HTTPAdapter` that sets urllib3's `assert_fingerprint` per host. Chain validation stays off so self-signed certificates keep working. urllib3 compares the fingerprint at connect time, before the request is written. `HostIdentityChangedError` does not inherit from `requests.ConnectionError`, so it is not retried. `APIWrapper` accepts an optional `https_adapter`. `ONTAPCLI.run_command_python_api` mounts the same adapter on its `HostConnection` session.
6. **First-use capture is one unauthenticated TLS handshake** that reads the peer certificate and saves its SHA-256 fingerprint. That fingerprint is then asserted on the authenticated connection, so a certificate that differs between the two connections is refused before credentials are sent. The capture ignores `HTTPS_PROXY`.
7. **Writes are serialised per file.** A `threading.Lock` per resolved path guards read, merge, temp file, `fsync` and `os.replace`. The directory has mode 0o700 and the files 0o600.
8. **The `requests` floor is raised to `>=2.32.3`**, the first release with `build_connection_pool_key_attributes`.

## Rationale

- Trust on first use needs no distribution step, which fits clusters with self-signed certificates.
- Pinning at connect time keeps credentials from being sent to a host whose identity differs from the recorded one.
- A standard OpenSSH file lets administrators reset one entry with a tool they already know.
- Injecting the store keeps tests free of sockets. An `ONTAPCLI` built without a store uses paramiko's `RejectPolicy`, so it connects only to hosts already in the system `known_hosts`.
- A per-file lock plus atomic replace keeps concurrent first connections from losing entries.

## Consequences

- The first contact with a host is trusted; the usual trust-on-first-use limitation applies to that moment.
- After a legitimate change (a replaced certificate, a rebuilt cluster) the user resets the entry once. The error message gives the command.
- Writers in other processes are not locked; two processes recording the same file at once can lose an entry, which the next connection records again.
- The TLS capture does not go through a proxy, so it needs a direct route to the cluster.
- Code that builds `ONTAPCLI` itself without `trust_store=` now refuses hosts missing from the system `known_hosts`; it passes `trust_store=config.get_trust_store()` to record hosts on first use. Every caller in this package passes a store.
- `.trust/` is ignored by git and is not rebuilt by cache refresh.
- Pinned connections count as verified to urllib3, so the ONTAP client needs no `InsecureRequestWarning` suppression, and netapp_ontap's own process-wide suppression is contained to `HostConnection` construction (#983).
