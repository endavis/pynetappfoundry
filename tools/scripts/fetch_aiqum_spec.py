"""Fetch the AIQUM (Active IQ Unified Manager) API spec.

Downloads the Swagger 2.0 spec from the AIQUM REST API documentation
endpoint, converts from YAML to JSON, and removes the security block.

AIQUM 9.18 serves the spec only to a UI login session (Basic auth gets
HTTP 401), so this script logs in with ``POST /login``, keeps the session
cookies, fetches the spec with the CSRF token, then logs out.

Usage:
    uv run python tools/scripts/fetch_aiqum_spec.py \\
        --host aiqum.example.com \\
        --username admin \\
        --password secret \\
        --output docs/example-config/apis/aiqum/all.json

    # Skip TLS verification (self-signed certs)
    uv run python tools/scripts/fetch_aiqum_spec.py \\
        --host aiqum.example.com \\
        --username admin \\
        --password secret \\
        --no-verify
"""

from __future__ import annotations

import argparse
import contextlib
import http.cookiejar
import json
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

try:
    import yaml

    HAS_YAML = True

    class _NoTimestampLoader(yaml.SafeLoader):
        """SafeLoader that keeps timestamps as the strings written in the YAML.

        Spec example/default values such as ``2021-01-01T00:00:00Z`` would
        otherwise load as ``datetime`` and break ``json.dumps``.
        """

    # Copy the resolver table so the global SafeLoader is not mutated.
    _NoTimestampLoader.yaml_implicit_resolvers = {
        first_char: [
            (tag, regexp) for tag, regexp in resolvers if tag != "tag:yaml.org,2002:timestamp"
        ]
        for first_char, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }
except ImportError:
    HAS_YAML = False


def _build_opener(no_verify: bool) -> urllib.request.OpenerDirector:
    """Build a urllib opener with a cookie jar and optional TLS bypass."""
    handlers: list[urllib.request.BaseHandler] = [
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
    ]
    if no_verify:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        handlers.append(urllib.request.HTTPSHandler(context=ctx))
    return urllib.request.build_opener(*handlers)


def _login(
    opener: urllib.request.OpenerDirector,
    base_url: str,
    username: str,
    password: str,
) -> None:
    """Open a UI login session; exit with an error (no password) on failure."""
    body = urllib.parse.urlencode({"username": username, "password": password}).encode()
    req = urllib.request.Request(
        f"{base_url}/login",
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "UM-REQUEST-CSRF-TOKEN": "true",
        },
    )
    try:
        response = opener.open(req)
    except urllib.error.HTTPError as e:
        print(f"ERROR: login failed: HTTP {e.code} - {e.reason}", file=sys.stderr)
        sys.exit(1)
    status = getattr(response, "status", 200)
    if status != 200:
        print(f"ERROR: login failed: HTTP {status}", file=sys.stderr)
        sys.exit(1)


def _csrf_token(opener: urllib.request.OpenerDirector) -> str | None:
    """Return the ``UM-CSRF`` cookie value from the opener's cookie jar, if any."""
    handlers: list[urllib.request.BaseHandler] = getattr(opener, "handlers", [])
    for handler in handlers:
        if isinstance(handler, urllib.request.HTTPCookieProcessor):
            for cookie in handler.cookiejar:
                if cookie.name == "UM-CSRF":
                    return cookie.value
    return None


def _logout(opener: urllib.request.OpenerDirector, base_url: str) -> None:
    """Best-effort logout; errors are ignored."""
    # Best-effort cleanup; never mask the real result.
    with contextlib.suppress(Exception):
        opener.open(urllib.request.Request(f"{base_url}/logout"))


def _sanitize_spec(spec: dict[str, Any]) -> dict[str, Any]:
    """Remove security blocks and non-path documentation entries from the spec.

    AIQUM specs include a security definition that references
    basic auth. This is instance-specific and should not be
    stored in the spec file.

    They also include fake path entries that are actually documentation
    (e.g. ``HTTP status codes``, ``Query And Path Parameters``) which
    have spaces in their names and no HTTP methods.
    """
    spec.pop("security", None)
    spec.pop("securityDefinitions", None)

    # Remove fake documentation entries from paths (keys with spaces
    # or keys that don't start with /)
    paths = spec.get("paths", {})
    bad_paths = [p for p in paths if " " in p or not p.startswith("/")]
    for p in bad_paths:
        del paths[p]

    for _path, methods in paths.items():
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
    """Fetch and parse the AIQUM API spec."""
    base_url = f"https://{host}"
    url = f"{base_url}/docs/api/v2.yaml"
    print(f"Fetching spec from {url}...")

    opener = _build_opener(no_verify)
    _login(opener, base_url, username, password)

    try:
        headers = {"Accept": "application/yaml, application/json"}
        token = _csrf_token(opener)
        if token is not None:
            headers["UM-CSRF-Token"] = token
        req = urllib.request.Request(url, headers=headers)
        try:
            response = opener.open(req)
        except urllib.error.HTTPError as e:
            print(f"ERROR: HTTP {e.code} - {e.reason}", file=sys.stderr)
            sys.exit(1)

        content = response.read()
        content_type = response.headers.get("Content-Type", "")
    finally:
        _logout(opener, base_url)

    if "yaml" in content_type or url.endswith(".yaml"):
        if not HAS_YAML:
            print(
                "ERROR: PyYAML is required to parse YAML specs.\n  Install it with: uv add pyyaml",
                file=sys.stderr,
            )
            sys.exit(1)
        spec: dict[str, Any] = yaml.load(content, Loader=_NoTimestampLoader)  # nosec B506  # SafeLoader subclass, no unsafe tags
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
        description="Fetch the AIQUM API spec.",
    )
    parser.add_argument("--host", required=True, help="AIQUM hostname or IP")
    parser.add_argument("--username", required=True, help="AIQUM username")
    parser.add_argument("--password", required=True, help="AIQUM password")
    parser.add_argument(
        "--output",
        default="docs/example-config/apis/aiqum/all.json",
        help="Output file path (default: docs/example-config/apis/aiqum/all.json)",
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
    output_path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    print(f"\nSpec written to {output_path}")


if __name__ == "__main__":
    main()
