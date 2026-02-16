"""Fetch the DII (Data Infrastructure Insights) API spec.

Downloads the OpenAPI 3.0.1 spec from the DII REST API documentation
endpoint and removes the servers and security blocks.

Usage:
    uv run python tools/scripts/fetch_dii_spec.py \\
        --host your-tenant.cloudinsights.netapp.com \\
        --api-key YOUR_API_KEY \\
        --output example-config/apis/dii/all.json
"""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def _build_opener(no_verify: bool) -> urllib.request.OpenerDirector:
    """Build a urllib opener with optional TLS bypass."""
    handlers: list[urllib.request.BaseHandler] = []
    if no_verify:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        handlers.append(urllib.request.HTTPSHandler(context=ctx))
    return urllib.request.build_opener(*handlers)


def _sanitize_spec(spec: dict[str, Any]) -> dict[str, Any]:
    """Remove instance-specific blocks and fix spec quirks.

    DII specs include servers (with the tenant URL) and security
    definitions that are instance-specific.  They also contain
    dangling ``$ref`` values pointing to schemas that don't exist
    (e.g. ``CSV file``, ``List``).
    """
    spec.pop("servers", None)
    spec.pop("security", None)

    # Remove from components if present
    components = spec.get("components", {})
    components.pop("securitySchemes", None)

    # Build set of defined schema names for dangling ref detection
    defined_schemas = set(components.get("schemas", {}).keys())

    # Remove per-operation security and fix dangling $refs in responses
    for _path, methods in spec.get("paths", {}).items():
        if not isinstance(methods, dict):
            continue
        for _method, operation in methods.items():
            if not isinstance(operation, dict):
                continue
            operation.pop("security", None)
            _remove_dangling_response_refs(operation, defined_schemas)

    return spec


def _remove_dangling_response_refs(
    operation: dict[str, Any],
    defined_schemas: set[str],
) -> None:
    """Remove response content entries that reference undefined schemas.

    The DII spec contains ``$ref`` values like ``#/components/schemas/CSV file``
    and ``#/components/schemas/List`` that point to schemas not defined in
    the spec.  These cause resolution failures in downstream tools.

    Args:
        operation: A single OpenAPI operation dict.
        defined_schemas: Set of schema names that exist in
            ``components.schemas``.
    """
    responses = operation.get("responses", {})
    for _status, response in responses.items():
        if not isinstance(response, dict):
            continue
        content = response.get("content", {})
        bad_content_types: list[str] = []
        for content_type, content_val in content.items():
            if not isinstance(content_val, dict):
                continue
            schema = content_val.get("schema", {})
            ref = schema.get("$ref", "")
            if ref:
                # Extract schema name from $ref
                schema_name = ref.rsplit("/", 1)[-1]
                if schema_name not in defined_schemas:
                    bad_content_types.append(content_type)
        for ct in bad_content_types:
            del content[ct]


def fetch_spec(
    host: str,
    api_key: str,
    no_verify: bool = False,
) -> dict[str, Any]:
    """Fetch and parse the DII API spec."""
    url = f"https://{host}/rest/documentation/category/all"
    print(f"Fetching spec from {url}...")

    opener = _build_opener(no_verify)
    req = urllib.request.Request(
        url,
        headers={
            "X-CloudInsights-ApiKey": api_key,
            "Accept": "application/json",
        },
    )

    try:
        response = opener.open(req)
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code} - {e.reason}", file=sys.stderr)
        sys.exit(1)

    spec: dict[str, Any] = json.loads(response.read())

    openapi_ver = spec.get("openapi", "unknown")
    info = spec.get("info", {})
    print(f"  OpenAPI: {openapi_ver}")
    print(f"  Title: {info.get('title', 'unknown')}")
    print(f"  Version: {info.get('version', 'unknown')}")

    paths = len(spec.get("paths", {}))
    schemas = len(spec.get("components", {}).get("schemas", {}))
    print(f"  Paths: {paths}, Schemas: {schemas}")

    return spec


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch the DII (Data Infrastructure Insights) API spec.",
    )
    parser.add_argument(
        "--host",
        required=True,
        help="DII tenant hostname (e.g., your-tenant.cloudinsights.netapp.com)",
    )
    parser.add_argument("--api-key", required=True, help="DII API access token")
    parser.add_argument(
        "--output",
        default="example-config/apis/dii/all.json",
        help="Output file path (default: example-config/apis/dii/all.json)",
    )
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip TLS certificate verification",
    )
    args = parser.parse_args()

    spec = fetch_spec(args.host, args.api_key, args.no_verify)
    spec = _sanitize_spec(spec)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(spec, indent=2) + "\n")
    print(f"\nSpec written to {output_path}")


if __name__ == "__main__":
    main()
