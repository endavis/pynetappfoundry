"""CLI entry point for OpenAPI codegen.

Parses an OpenAPI 3.0 spec and generates cache model classes, TypeMapping
definitions, and TOML overlay files.

Usage::

    uv run python tools/codegen/openapi_codegen.py \\
        --spec docs/example-config/apis/ontap/openapi3.json \\
        --output src/pynetappfoundry/cache/ontap/ \\
        --api-type ontap
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Mapping
from pathlib import Path

from tools.codegen.adapters import ParsedEndpoint, detect_shared_schemas, parse_openapi_spec
from tools.codegen.generators import (
    _EXCLUDED_ENDPOINTS,
    _collect_all_leaves,
    _field_to_cache_attr,
    _path_to_class_name,
    _path_to_module_parts,
    is_fetchable_endpoint,
    resolve_class_name_collisions,
    resolve_parent_link,
    write_endpoint_files,
)


def _deduplicate_endpoints(endpoints: list[ParsedEndpoint]) -> list[ParsedEndpoint]:
    """Deduplicate endpoints that resolve to the same module path.

    When ``/storage/volumes`` and ``/storage/volumes/{uuid}`` both map to
    module path ``["storage", "volumes"]``, an envelope endpoint beats a
    singleton one (#925, #934), so a collection URL is never replaced by its
    single-object item endpoint.  Within the same shape the endpoint with the
    most leaf fields (the richer schema) wins.

    Args:
        endpoints: List of parsed endpoints.

    Returns:
        Deduplicated list, preserving original order for the winners.
    """
    groups: dict[tuple[str, ...], list[ParsedEndpoint]] = {}
    for ep in endpoints:
        key = tuple(_path_to_module_parts(ep.path))
        groups.setdefault(key, []).append(ep)

    seen: set[tuple[str, ...]] = set()
    result: list[ParsedEndpoint] = []
    for ep in endpoints:
        key = tuple(_path_to_module_parts(ep.path))
        if key in seen:
            continue
        seen.add(key)
        candidates = groups[key]
        if len(candidates) == 1:
            result.append(candidates[0])
        else:
            # Shape ranks first (envelope beats singleton, #925/#934); the
            # most leaf fields decides within a shape.
            best = max(
                candidates,
                key=lambda e: (e.response_shape != "singleton", len(_collect_all_leaves(e.fields))),
            )
            result.append(best)
    return result


def _build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate cache models and mappings from OpenAPI specs.",
    )
    parser.add_argument(
        "--spec",
        type=Path,
        required=True,
        help="Path to OpenAPI 3.0 JSON spec file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output directory for generated files (e.g. src/pynetappfoundry/cache/ontap/).",
    )
    parser.add_argument(
        "--api-type",
        choices=["ontap", "aiqum", "dii", "occm"],
        default="ontap",
        help="API type (default: ontap).",
    )
    parser.add_argument(
        "--overlay-dir",
        type=Path,
        default=None,
        help="Directory for TOML overlay files (default: alongside model files).",
    )
    parser.add_argument(
        "--endpoints",
        nargs="*",
        default=None,
        help="Only generate for these endpoint paths (e.g. /storage/volumes).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be generated without writing files.",
    )
    return parser


def _drop_unfetchable_endpoints(
    endpoints: list[ParsedEndpoint],
    api_type: str,
    schema_lookup: dict[str, str],
    *,
    shared_schemas: frozenset[str] | set[str],
    class_name_overrides: Mapping[tuple[str, ...], str],
    identifier_map: dict[str, str],
    parent_field_names: dict[str, set[str]],
) -> tuple[list[ParsedEndpoint], dict[str, str]]:
    """Split endpoints into fetchable ones and dropped ones with a reason.

    An endpoint is dropped when the runtime cannot fill every path
    placeholder: a parent fills only the first one, and a parentless mapping
    has all of them stripped (#952).

    Returns:
        ``(kept, dropped)`` where ``dropped`` maps path to reason.
    """
    kept: list[ParsedEndpoint] = []
    dropped: dict[str, str] = {}
    for ep in endpoints:
        link = resolve_parent_link(
            ep,
            api_type,
            schema_lookup,
            shared_schemas=shared_schemas,
            class_name_overrides=class_name_overrides,
            identifier_map=identifier_map,
            parent_field_names=parent_field_names,
        )
        if is_fetchable_endpoint(ep, link):
            kept.append(ep)
        elif link is None:
            dropped[ep.path] = "placeholder with no resolvable parent"
        else:
            dropped[ep.path] = "more than one placeholder; a parent fills only the first"
    return kept, dropped


def run(
    spec: Path,
    output: Path,
    api_type: str = "ontap",
    overlay_dir: Path | None = None,
    endpoint_filter: list[str] | None = None,
    dry_run: bool = False,
) -> list[Path]:
    """Run the codegen pipeline.

    Args:
        spec: Path to OpenAPI 3.0 spec.
        output: Output directory.
        api_type: API type tag.
        overlay_dir: Optional overlay directory.
        endpoint_filter: Optional list of endpoint paths to generate.  Applied
            after parent linkage and the unfetchable-endpoint drop are decided
            from the full spec, so a filtered run matches a full run (#952).
        dry_run: If True, print plan without writing.

    Returns:
        List of all files written.
    """
    if not spec.exists():
        print(f"ERROR: Spec file not found: {spec}", file=sys.stderr)
        sys.exit(1)

    print(f"Parsing {spec} (api_type={api_type})...")
    endpoints = parse_openapi_spec(spec, api_type)
    print(f"Found {len(endpoints)} GET endpoints with response schemas.")

    # Deduplicate endpoints that resolve to the same module path FIRST.
    # e.g. /storage/volumes and /storage/volumes/{uuid} both map to
    # storage/volumes — an envelope beats a singleton (#925, #934); the most
    # leaf fields decides within a shape.  ONTAP
    # collection+item pairs both reference the same schema, but since
    # only one survives dedup the schema isn't actually shared across
    # distinct module paths.  Detecting shared schemas BEFORE dedup
    # would incorrectly flag nearly every ONTAP schema as shared.
    full_spec_endpoints = list(endpoints)  # retain for shared-schema scan
    endpoints = _deduplicate_endpoints(endpoints)

    # Detect schema names still referenced by more than one endpoint
    # *after* deduplication.  For ONTAP this is typically 0 (schemas
    # shared between collection + item are collapsed); for DII this
    # catches schemas like ``Count`` that are genuinely shared across
    # distinct URL paths (7 different ``/foo/count`` endpoints in DII).
    shared_schemas = detect_shared_schemas(endpoints)
    if shared_schemas:
        print(f"Detected {len(shared_schemas)} shared response schema(s) after dedup.")

    # Rename classes whose derived names collide (e.g. DiiAuAcquisitionunit)
    # so the registry never drops a mapping.  Computed on the full deduped
    # list, before any endpoint filter, so names are filter-independent.
    class_name_overrides = resolve_class_name_collisions(
        endpoints, api_type, shared_schemas=shared_schemas
    )
    if class_name_overrides:
        print(f"Resolved {len(class_name_overrides)} class name collision(s).")

    # Build schema lookup from the full (pre-dedup) endpoint list so that
    # child endpoints can always resolve their parent's schema name — even
    # when the parent collection endpoint was collapsed by dedup with its
    # sibling item endpoint.
    schema_lookup: dict[str, str] = {ep.path: ep.schema_name for ep in full_spec_endpoints}

    # Build identifier map from the full endpoint list so that
    # ``generate_mapping`` can look up the parent's actual
    # ``identifier_field`` (e.g. ``"name"`` instead of assuming ``"uuid"``).
    identifier_map: dict[str, str] = {
        ep.path: ep.identifier_field for ep in full_spec_endpoints if ep.identifier_field
    }

    # Build a map of top-level field names per *dedup-winner* endpoint so
    # ``generate_mapping`` can validate that a parent's identifier_field
    # actually exists on the generated parent model before using it as
    # ``parent_id_field``.  Uses the dedup winners (not the full list)
    # because the model that gets generated and registered comes from
    # the winner — the collection endpoint's fields may differ from the
    # item endpoint's fields that actually end up in the model.
    # Keyed by all paths that map to the same module (so child endpoints
    # can look up their parent_path regardless of which sibling won).
    parent_field_names: dict[str, set[str]] = {}
    for ep in endpoints:
        leaves = _collect_all_leaves(ep.fields)
        field_roots = {_field_to_cache_attr(f).split(".")[0] for f in leaves}
        parent_field_names[ep.path] = field_roots
    # Also register under sibling paths that collapsed to the same module
    # path during dedup, so ``parent_path`` lookups work for parents
    # whose collection endpoint was deduped away.
    dedup_module_map = {tuple(_path_to_module_parts(ep.path)): ep.path for ep in endpoints}
    for ep in full_spec_endpoints:
        parts = tuple(_path_to_module_parts(ep.path))
        if parts in dedup_module_map and ep.path != dedup_module_map[parts]:
            parent_field_names[ep.path] = parent_field_names[dedup_module_map[parts]]

    # Drop ONTAP endpoints the runtime cannot fetch (#952).  Decided from the
    # full deduped list so the outcome does not depend on ``endpoint_filter``.
    if api_type == "ontap":
        endpoints, dropped = _drop_unfetchable_endpoints(
            endpoints,
            api_type,
            schema_lookup,
            shared_schemas=shared_schemas,
            class_name_overrides=class_name_overrides,
            identifier_map=identifier_map,
            parent_field_names=parent_field_names,
        )
        for path, reason in dropped.items():
            if not endpoint_filter or path in endpoint_filter:
                print(f"  skipped (unfillable placeholder): {path} ({reason})")

    # Drop paths excluded from codegen (#933); after the #952 drop so no other
    # endpoint's naming or parent linkage changes.
    excluded = _EXCLUDED_ENDPOINTS.get(api_type, frozenset())
    for ep in endpoints:
        if ep.path in excluded and (not endpoint_filter or ep.path in endpoint_filter):
            print(f"  skipped (excluded): {ep.path}")
    endpoints = [e for e in endpoints if e.path not in excluded]

    if endpoint_filter:
        endpoints = [e for e in endpoints if e.path in endpoint_filter]
        print(f"Filtered to {len(endpoints)} endpoints.")

    if not endpoints:
        print("No endpoints to generate.", file=sys.stderr)
        return []

    del full_spec_endpoints

    all_written: list[Path] = []

    for ep in endpoints:
        if dry_run:
            class_name = _path_to_class_name(
                ep.path,
                ep.schema_name,
                api_type,
                shared_schemas=shared_schemas,
                class_name_overrides=class_name_overrides,
            )
            print(f"  [dry-run] {ep.path} -> {class_name} ({len(ep.fields)} fields)")
            continue

        written = write_endpoint_files(
            ep,
            output,
            api_type,
            overlay_dir,
            schema_lookup,
            shared_schemas=shared_schemas,
            class_name_overrides=class_name_overrides,
            identifier_map=identifier_map,
            parent_field_names=parent_field_names,
        )
        all_written.extend(written)
        field_count = len([f for f in ep.fields if not f.is_object or f.is_list])
        print(f"  {ep.path} -> {len(written)} files, {field_count} fields")

    if not dry_run:
        print(f"\nDone: {len(all_written)} files written.")

    return all_written


def main() -> None:
    """CLI entry point."""
    parser = _build_parser()
    args = parser.parse_args()

    run(
        spec=args.spec,
        output=args.output,
        api_type=args.api_type,
        overlay_dir=args.overlay_dir,
        endpoint_filter=args.endpoints,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
