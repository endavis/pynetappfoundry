"""Fetch the ONTAP API spec from a cluster.

Downloads the Swagger 2.0 spec from the ONTAP REST API documentation
endpoint, converts from YAML to JSON, and removes the security block.

Usage:
    uv run python tools/scripts/fetch_ontap_spec.py \\
        --host 10.0.0.1 \\
        --username admin \\
        --password secret \\
        --output docs/example-config/apis/ontap/all.json

    # Skip TLS verification (self-signed certs)
    uv run python tools/scripts/fetch_ontap_spec.py \\
        --host 10.0.0.1 \\
        --username admin \\
        --password secret \\
        --no-verify
"""

from __future__ import annotations

import argparse
import base64
import json
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def _build_opener(no_verify: bool) -> urllib.request.OpenerDirector:
    """Build a urllib opener with optional TLS bypass."""
    handlers: list[urllib.request.BaseHandler] = []
    if no_verify:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        handlers.append(urllib.request.HTTPSHandler(context=ctx))
    return urllib.request.build_opener(*handlers)


def _basic_auth_header(username: str, password: str) -> str:
    """Build a Basic auth header value."""
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


def _sanitize_spec(spec: dict[str, Any]) -> dict[str, Any]:
    """Remove security blocks from the spec.

    ONTAP specs include a security definition that references
    basic auth. This is cluster-specific and should not be
    stored in the spec file.
    """
    # Remove top-level security requirement
    spec.pop("security", None)

    # Remove securityDefinitions
    spec.pop("securityDefinitions", None)

    # Remove per-operation security if present
    for _path, methods in spec.get("paths", {}).items():
        if not isinstance(methods, dict):
            continue
        for _method, operation in methods.items():
            if isinstance(operation, dict):
                operation.pop("security", None)

    return spec


def fetch_spec(
    host: str,
    username: str,
    password: str,
    no_verify: bool = False,
) -> dict[str, Any]:
    """Fetch and parse the ONTAP API spec."""
    url = f"https://{host}/docs/api/swagger.yaml"
    print(f"Fetching spec from {url}...")

    opener = _build_opener(no_verify)
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": _basic_auth_header(username, password),
            "Accept": "application/yaml, application/json",
        },
    )

    try:
        response = opener.open(req)
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code} - {e.reason}", file=sys.stderr)
        sys.exit(1)

    content = response.read()
    content_type = response.headers.get("Content-Type", "")

    # Parse based on content type
    if "yaml" in content_type or url.endswith(".yaml"):
        if not HAS_YAML:
            print(
                "ERROR: PyYAML is required to parse YAML specs.\n  Install it with: uv add pyyaml",
                file=sys.stderr,
            )
            sys.exit(1)
        spec: dict[str, Any] = yaml.safe_load(content)
    else:
        spec = json.loads(content)

    swagger_ver = spec.get("swagger", spec.get("openapi", "unknown"))
    info = spec.get("info", {})
    print(f"  Swagger/OpenAPI: {swagger_ver}")
    print(f"  Title: {info.get('title', 'unknown')}")
    print(f"  Version: {info.get('version', 'unknown')}")

    paths = len(spec.get("paths", {}))
    defs = len(spec.get("definitions", spec.get("components", {}).get("schemas", {})))
    print(f"  Paths: {paths}, Definitions: {defs}")

    return spec


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch the ONTAP API spec from a cluster.",
    )
    parser.add_argument("--host", required=True, help="Cluster management IP or hostname")
    parser.add_argument("--username", required=True, help="ONTAP username (e.g., admin)")
    parser.add_argument("--password", required=True, help="ONTAP password")
    parser.add_argument(
        "--output",
        default="docs/example-config/apis/ontap/all.json",
        help="Output file path (default: docs/example-config/apis/ontap/all.json)",
    )
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip TLS certificate verification",
    )
    args = parser.parse_args()

    spec = fetch_spec(args.host, args.username, args.password, args.no_verify)
    spec = _sanitize_spec(spec)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(spec, indent=2) + "\n")
    print(f"\nSpec written to {output_path}")


if __name__ == "__main__":
    main()
