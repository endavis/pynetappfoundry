# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for this project.

## What is an ADR?

An ADR documents an architectural decision: what was decided and why. The detailed discussion and specification lives in the GitHub Issue; the ADR provides a summary with links.

## ADR Format

ADRs use a simplified format:

```markdown
# ADR-NNNN: Title

## Status
Accepted

## Decision
Brief summary of what was decided.

## Rationale
Why this decision was made.

## Related Issues
- Issue #XX: Description

## Related Documentation
- [Relevant Doc](../path/to/doc.md)
```

See [adr-template.md](adr-template.md) for the template.

## Creating a New ADR

```bash
# Interactive (opens editor)
doit adr --title="Your decision title"

# Non-interactive (for scripts/AI)
doit adr --title="Use Redis" --body="## Status\nAccepted\n..."
doit adr --title="Use Redis" --body-file=adr.md
```

## When to Create an ADR

Create an ADR when:
- Introducing a new tool, framework, or library
- Changing development workflow or processes
- Making decisions that affect project architecture

The Issue contains the full discussion; the ADR summarizes the outcome.

## ADR Statuses

- **Accepted**: Decision is in effect
- **Deprecated**: No longer relevant (kept for history)
- **Superseded**: Replaced by a newer ADR

## Template ADRs

Template-inherited ADRs (9XXX range) are maintained in [docs/template/decisions/](../template/decisions/README.md).

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [0001](0001-use-sqlite-for-cluster-metadata-caching.md) | Use SQLite for cluster metadata caching | Accepted |
| [0002](0002-track-smb-client-impact-azure-maintenance.md) | Track SMB client impact during Azure maintenance | Accepted |
| [0003](0003-use-base-sqlitedb-class-with-version-based-migrations.md) | Use base SQLiteDB class with version-based migrations | Accepted |
| [0004](0004-declarative-field-mapping-framework.md) | Declarative field mapping framework for ONTAP collection | Accepted |
| [0005](0005-uuid-index-for-cache-cross-references.md) | UUID index for cache cross-references | Accepted |
| [0006](0006-generalize-field-mapping-for-multi-api.md) | Generalize field mapping framework for multi-API data collection | Accepted |
