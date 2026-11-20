---
title: "ADR-0038: nf config download-spec fetches the committed API specs of the installed release"
description: nf config download-spec downloads each API's committed spec from GitHub at the installed release tag or commit instead of a live system.
date: 2026-11-20
audience:
  - contributors
tags:
  - adr
---

# ADR-0038: nf config download-spec fetches the committed API specs of the installed release

## Status

Accepted

## Context

No API spec ships in the installed package. The clients read an OpenAPI spec from `<config>/apis/<api>/` and raise `FileNotFoundError` when it is missing, so a user had to copy the committed spec from the repository by hand. Issue [#1129](https://github.com/endavis/pynetappfoundry/issues/1129) adds a command that does the copy.

## Decision

1. **Command.** `nf config download-spec [--api ontap|aiqum|dii|console] [--force]` downloads the committed spec of the installed release from GitHub into `<config>/apis/<api>/`. Without `--api` it handles every configured API whose spec is missing. An existing file is kept unless `--force` is given. `apis/occm/` is never written.
2. **Source: the committed spec, not a live system.** The generated models come from the committed spec and the runtime spec is the client's path lookup, so a spec taken from one ONTAP or AIQUM instance could drop paths the code calls. The release source needs no device credentials and also covers Console, whose spec is built by `tools/console_openapi` and cannot be fetched live. `doit fetch_spec` stays the way to refresh the committed spec.
3. **Version to git ref** (`src/pynetappfoundry/core/spec_source.py`, `resolve_ref`). A `+g<sha>` segment of the hatch-vcs version gives the commit; a `d<date>` segment as well means local changes, which the command reports as a warning. Without a sha, a `.dev` version or the fallback `0.0.0` is an error, because no commit can be determined. Any other version is a release and the ref is `v<version>`, the `[tool.commitizen] tag_format`. There is no `--ref` override.
4. **Repository from `Project-URL`.** The owner and repository come from the installed distribution's `Repository` project URL, the entry the template's configurator rewrites. Only the raw host `raw.githubusercontent.com` is a constant. A missing entry, a non-GitHub URL or a missing distribution is an error with a hint to copy the file by hand.
5. **Validate, then write.** The text must parse (YAML for `.yaml`, else JSON) to a mapping with a `paths` mapping before it is written, verbatim, with `atomic_write_text`. Each API is attempted; a failed one writes nothing and the run exits 1 listing the failures.
6. **Read-only doctor.** The missing-spec hints of `nf config validate` and `nf doctor` name `nf config download-spec --api <api>` (`spec_download_hint` in `src/pynetappfoundry/core/config_checks.py`). `nf doctor` does not download ([ADR-0035](0035-nf-doctor-runs-static-environment-and-read-only-live-checks-with-fix-hints.md)).

## Rationale

The spec of the release the user installed is the one the code and models were generated from, so it always matches. The tag or commit rule needs no new metadata in the wheel.

Rejected alternatives:

- **Fetch from a live system.** It could produce a spec that no longer matches the models, needs credentials, and cannot cover Console.
- **Ship the specs in the wheel.** The ONTAP spec is about 12 MB; shipping it grows every install, including for users of other APIs.

## Related Issues

- Issue #1129: `nf config download-spec`
- Issue #1111: spec file checks ([ADR-0034](0034-config-checks-are-shared-static-functions-returning-structured-results.md))

## Related Documentation

- [Configuration guide: Spec files](../getting-started/configuration.md#spec-files)
- [CLI reference: config download-spec](../reference/cli.md#config)
