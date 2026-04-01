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
from pathlib import Path

from tools.codegen.adapters import ParsedEndpoint, parse_openapi_spec
from tools.codegen.generators import (
    _path_to_class_name,
    _path_to_module_parts,
    _select_leaf_fields,
    write_endpoint_files,
)


def _deduplicate_endpoints(endpoints: list[ParsedEndpoint]) -> list[ParsedEndpoint]:
    """Deduplicate endpoints that resolve to the same module path.

    When ``/storage/volumes`` and ``/storage/volumes/{uuid}`` both map to
    module path ``["storage", "volumes"]``, keep the endpoint with the
    most leaf fields (the richer schema).

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
            # Pick the endpoint with the most leaf fields
            best = max(candidates, key=lambda e: len(_select_leaf_fields(e.fields)))
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
        endpoint_filter: Optional list of endpoint paths to generate.
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

    if endpoint_filter:
        endpoints = [e for e in endpoints if e.path in endpoint_filter]
        print(f"Filtered to {len(endpoints)} endpoints.")

    # Deduplicate endpoints that resolve to the same module path.
    # e.g. /storage/volumes and /storage/volumes/{uuid} both map to
    # storage/volumes — keep the one with the most leaf fields.
    endpoints = _deduplicate_endpoints(endpoints)

    if not endpoints:
        print("No endpoints to generate.", file=sys.stderr)
        return []

    # Build schema lookup for parent path resolution in mappings
    schema_lookup: dict[str, str] = {ep.path: ep.schema_name for ep in endpoints}

    all_written: list[Path] = []

    for ep in endpoints:
        if dry_run:
            class_name = _path_to_class_name(ep.path, ep.schema_name, api_type)
            print(f"  [dry-run] {ep.path} -> {class_name} ({len(ep.fields)} fields)")
            continue

        written = write_endpoint_files(
            ep,
            output,
            api_type,
            overlay_dir,
            schema_lookup,
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
